#! /usr/bin/env ruby
#
#   outlyer-metrics
#
# DESCRIPTION:
#   Pushes metrics from Sensu Nagios Checks and Sensu Graphite Metric Checks
#   to Outlyer. Will also send the check status as an additional `service.status`
#   metric with label `check: sensu.<check_name>` so you can create status alerts and
#   dashboard widgets for the check in Outlyer.
#
# OUTPUT:
#   metric data
#
# PLATFORMS:
#   Linux
#
# DEPENDENCIES:
#   gem: sensu-handler
#
# USAGE:
#   Takes the following optional parameters:
#   
#     -f: set the Handler's check output format to parse. Can either be `graphite` (default) or `nagios`.
#     -t: Set the timeout in seconds for the Outlyer API requests
#   
# NOTES:
#
# LICENSE:
#   Copyright 2018 Dataloop Software, INC. trading as Outlyer (https://www.outlyer.com)
#   Released under the same terms as Sensu (the MIT license); see LICENSE for details.
#

require 'sensu-handler'
require 'net/https'
require 'uri'
require 'json'

#
# Outlyer Metrics
#
class OutlyerMetrics < Sensu::Handler
  
  option :output_format,
         description: 'Output format of checks to process: graphite (default) or nagios',
         short: '-f FORMAT',
         long: '--format FORMAT',
         default: 'graphite'
  
  option :api_timeout,
         description: 'The timeout in seconds for Outlyer API Requests',
         short: '-t TIMEOUT',
         long: '--timeout TIMEOUT',
         default: '5'
  
  # Override filters from Sensu::Handler.
  # They are not appropriate for metric handlers
  #
  def filter
  end
    
  # Create a handle and event set
  #
  def handle
    
    output = @event['check']['output']
    check_status = @event['check']['status'].to_f
    @check_name = @event['check']['name']
    @host = @event['client']['name']
    @environment = @event['client']['environment']
    timestamp = @event['check']['executed'].to_i * 1000
    
    # Uncomment this line for local testing outside Sensu
    #@settings = { "outlyer" => {"account" => "", "api_key" => ""}}

    # Parse output for metric data
    metrics = if config[:output_format] == 'nagios' then
             parse_nagios_output(output, timestamp)
          else
             parse_graphite_output(output)
          end 
    
    # Add a service status metric
    metrics.push(create_datapoint('service.status', check_status, timestamp, {service: "sensu.#{@check_name}"}))
    puts metrics
    # Post metrics to Outlyer
    push_metrics(metrics)
  end
  
  # Create a single data point
  #
  # @param name     [String] metric name
  # @param value    [Float] metric value
  # @param time     [Integer] epoch timestamp of metric in milliseconds
  # @param labels   [HashMap] (Optional) Additional labels to append to data point
  #
  def create_datapoint(name, value, time, labels = nil)
    datapoint = {
                  host: @host,
                  labels: {
                            environment: @environment,
                          },
                  name: name,
                  timestamp: time,
                  type: 'gauge',
                  value: value
                }
    datapoint[:labels].merge!(labels) unless labels.nil?
    datapoint
  end

  # Parse the Nagios output format:
  #   <message> | <metric path 1>=<metric value 1>, <metric path 2>=<metric value 2>...
  #
  # @param output   [String] The full check output
  # @param timestamp[Integer] The epoch timestamp in milliseconds the check was executed
  #
  def parse_nagios_output(output, timestamp)
    data = []
    parts = output.strip.split('|')
    
    if parts.length < 2
      # No performance data
      return data
    end
    
    parts[1].strip.split.each do |metric|
      metric_parts = metric.strip.split('=')
      begin
        name = metric_parts[0]
        value = metric_parts[1].split(";")[0].to_f
        data.push(create_datapoint(@check_name + '.' + name, value, timestamp))
      rescue => error
        # Raised when any metrics could not be parsed
        puts "[OutlyerHandler] The Nagios metric '#{metric}' could not be parsed: #{error.message}"
      end 
    end
    data
  end
  
  # Parse the graphite output format:
  #   <metric path> <metric value> <metric timestamp>\n
  #
  # Each metric is separated by a newline character in the body
  #
  # @param output   [String] The full check output
  #
  def parse_graphite_output(output)
    data = []
    output.split("\n").each do |metric|
      m = metric.split
      next unless m.count == 3
      name = m[0].split('.', 2)[1]
      value = m[1].to_f
      time = m[2].to_i * 1000
      point = create_datapoint(@check_name + '.' + name, value, time)
      data.push(point)
    end
    data
  end

  # Post check metrics to Outlyer's Series API:
  #   
  #   POST https://api2.outlyer.com/v2/accounts/{account}/series
  #
  # @param datapoints     [Object] Array of data points
  #
  def push_metrics(datapoints)
    Timeout.timeout(config[:api_timeout].to_i) do
      uri = URI.parse("https://api2.outlyer.com/v2/accounts/#{settings['outlyer']['account']}/series")

      # Create the HTTP objects
      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = true
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE
      request = Net::HTTP::Post.new(uri.request_uri)
      request.add_field("Authorization", "Bearer #{settings['outlyer']['api_key']}")
      request.add_field("accept", "application/json") 
      request.add_field("Content-Type", "application/json")
      request.body = {samples: datapoints}.to_json

      # Send the request
      response = http.request(request)
      if response.code.to_i != 200
        puts "[OutlyerHandler] Outlyer API Error -- API responded with status code " + response.code
        puts response.body
      end
    end
  # Raised when any metrics could not be sent
  #
  rescue Timeout::Error
    puts '[OutlyerHandler] Outlyer API Error -- timed out while sending metrics'
  rescue => error
    puts "[OutlyerHandler] Outlyer API Error -- failed to send metrics: #{error.message}"
    puts " #{error.backtrace.join("\n\t")}"
  end
end