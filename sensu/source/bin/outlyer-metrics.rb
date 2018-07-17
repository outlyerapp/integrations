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
#     -d: Enable debugging to see additional logging in Output
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
       
  option :debug,
         description: 'Enable debug for more verbose output',
         boolean: true,
         short: '-d',
         long: '--debug', 
         default: false
  
  # Override filters from Sensu::Handler.
  # They are not appropriate for metric handlers
  #
  def filter
  end
    
  # Create a handle and event set
  #
  def handle

    output = @event['check']['output']
    @check_name = @event['check']['name']
    @host = @event['client']['name'].strip.to_s
    @environment = @event['client']['environment']
    
    if config[:debug]
      puts "Handling check #{@check_name} for host #{@host} in environment #{@environment}"
    end
    
    # Parse output for metric data
    metrics = if config[:output_format] == 'nagios' then
             parse_nagios_output(output, timestamp)
          else
             parse_graphite_output(output)
          end 
      
    # Post metrics to Outlyer
    push_metrics(metrics)
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
        labels = {service: "sensu.#{sanitize_value(@check_name)}"}
        data.push(create_datapoint(name, value, timestamp, labels))
      rescue => error
        # Raised when any metrics could not be parsed
        puts "The Nagios metric '#{metric}' could not be parsed: #{error.message}"
      end 
    end
    data.push(create_status_metric(@event['check']['status'].to_f))
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
    
    # Get Schemes to parse Graphite metrics if exists
    schemes = nil
    if settings['outlyer'].key?('schemes') && settings['outlyer']['schemes'] != nil
        schemes = settings['outlyer']['schemes']
    end
    
    # Parse the metric on each line in graphite format
    metric_host = @host
    output.split("\n").each do |metric|
      m = metric.split
      next unless m.count == 3
        labels = {service: "sensu.#{sanitize_value(@check_name)}"}
        
        # Check to see if we have a scheme filter that matches the metric name
        if schemes
          template = nil
          schemes.each do |scheme|
            filter = Regexp.new("^#{Regexp.escape(scheme['filter']).gsub('\*','[^\.]*?')}$")
            if m[0] =~ filter
              template = scheme['template']
              if config[:debug]
                puts "Template Found: '#{template}' with REGEX '#{filter.inspect}'"
              end
              break
            end
          end
          
          # Found a template to parse metric
          if template
            metric_parts = m[0].split('.')
            template_parts = template.split('.')
            
            # Iterate through the template to parse the metric labels
            template_parts.each_with_index do |val,index|
              key = sanitize_value(val, 40)
              value = sanitize_value(metric_parts[index])
              if labels.key?(key)
                # If value is spread over multiple parts re-append the value
                labels[key] += ".#{value}"
              else
                labels.merge!(Hash[key,value])
              end
            end
            
            # Now we have all the labels extracted, need to ensure a
            # name was given and optional host
            if labels.key?('name')
              metric_name = labels['name']
              labels.delete('name')
            end
            if labels.key?('host')
              metric_host = labels['host']
              labels.delete('host')
            end
            
          else
            # If no template found, ignore metric and put warning in handler
            # this avoids un-configured checks sending bad data to Outlyer
            puts "No scheme was found that matches the metric '#{m[0]}.'"
            puts "Please configure a scheme for the check '#{@check_name}' "\
              "on the Sensu client '#{@host}'."
            data.push(create_status_metric(3))
            return data
          end
        else
          metric_name = sanitize_value(m[0])
        end
        
      value = m[1].to_f
      time = m[2].to_i * 1000
      point = create_datapoint(metric_name, value, time, labels, metric_host)
      data.push(point)
    end
    if config[:debug]
      puts "Parsed #{data.length} of #{output.split("\n").length} metrics"
    end 
    data.push(create_status_metric(@event['check']['status'].to_f, metric_host))
    data
  end
  
  # Create the status metric for the check with status:
  #   
  #   0 - OK
  #   1 - WARN
  #   2 - CRITICAL
  #   3 - UNKNOWN
  # 
  # Unknown is used to tell Outlyer there was a parsing error for the check
  # 
  # @param check_status   [Integer] Check status code
  # @param host           [String] (Optional) hostname of host that ran the check
  # @param timestamp      [Integer] (Optional) timestamp of when host ran the check
  #
  def create_status_metric(check_status, host=@host, timestamp=@event['check']['executed'].to_i * 1000)
    return create_datapoint('service.status', check_status, timestamp, {service: "sensu.#{sanitize_value(@check_name)}"}, host)
  end
  
  # Ensures all label values conform to Outlyer's data format requirements:
  #   
  #   * values can only contain the characters `-._A-Za-z0-9`, other characters 
  #     will be replaced by underscore including spaces
  #   * values can only be 80 characters or less
  #
  # @param value      [String] The value to sanitize
  # @param max_length [Integer] The maximum length of string, default 80
  #
  def sanitize_value(value, max_length = 80)
    if !value
      return ''
    end
    value = value.gsub(/[^-._A-Za-z0-9]/i, '_').downcase
    if value.length > max_length
      puts "Warning: value '#{value}' is greater than 80 characters and will be truncated to last 80 characters"
      value = value.split(//).last(max_length).join
    end
    value
  end
  
  # Create a single data point
  #
  # @param name         [String] metric name
  # @param value        [Float] metric value
  # @param time         [Integer] epoch timestamp of metric in milliseconds
  # @param labels       [HashMap] (Optional) Additional labels to append to data point
  # @param metric_host  [String] (Optional) Set a host for the metric
  #
  def create_datapoint(name, value, time, labels = {}, metric_host=@host)
    datapoint = {
                  host: metric_host,
                  labels: labels,
                  name: name,
                  timestamp: time,
                  type: 'gauge',
                  value: value
                }
    datapoint
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
      request.body = JSON.pretty_generate({samples: datapoints})
      
      if config[:debug]
        puts "DEBUG: Outlyer API Payload: #{request.body}"
      end
      
      # Send the request
      response = http.request(request)
      if response.code.to_i != 200
        puts "Outlyer API Error -- API responded with status code #{response.code}"
        puts "Outlyer API Response: #{response.body}"
        puts "Outlyer API Request Body: #{request.body}"
        return
      end
      puts "Successfully pushed #{datapoints.length} metrics to Outlyer"
    end
  # Raised when any metrics could not be sent
  #
  rescue Timeout::Error
    puts 'Outlyer API Error -- timed out while sending metrics'
    exit(2)
  rescue => error
    puts "Outlyer API Error -- failed to send metrics: #{error.message}"
    puts " #{error.backtrace.join("\n\t")}"
    if config[:debug]
      puts "Event Data: \n#{JSON.pretty_generate(@event)}"
    end
    exit(2)
  end
end