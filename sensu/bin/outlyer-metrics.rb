#! /usr/bin/env ruby
#
#   outlyer-metrics
#
# DESCRIPTION:
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
#
# NOTES:
#
# LICENSE:
#   Copyright 2018 Dataloop Software, INC. trading as Outlyer (https://www.outlyer.com)
#   Released under the same terms as Sensu (the MIT license); see LICENSE for details.
#

require 'sensu-handler'
require 'net/http'
require 'uri'
require 'json'

#
# Outlyer Metrics
#
class OutlyerMetrics < Sensu::Handler
  # Override filters from Sensu::Handler.
  # They are not appropriate for metric handlers
  #
  def filter
  end

  # Create a handle and event set
  #
  def handle

    @event['check']['output'].split("\n").each do |line|
      name, value, timestamp = line.split(/\s+/)
      emit_metric(name, value, timestamp)
    end
    # Add a service.status metric for check status
    emit_metric('service.status', @event['status'], Time.now.to_i * 1000.0)
  end

  # Push metric point
  #
  # @param name       [String]
  # @param value      [String]
  # @param _timestamp [String]
  def emit_metric(name, value, _timestamp)
    timeout(5) do
      uri = URI.parse("https://api2.outlyer.com/v2/accounts/" + settings['outlyer']['account'] + "/series")
      header = {'Content-Type': 'text/json',
                'Authorization': 'Bearer ' + settings['outlyer']['api_key']}

      # Create datapoint json body
      datapoint = { samples:
                    [{
                      host: 'sensu',
                      labels: {},
                      name: name,
                      timestamp: _timestamp,
                      type: 'gauge',
                      value: value
                    }]
                  }

      # Create the HTTP objects
      http = Net::HTTP.new(uri.host, uri.port)
      request = Net::HTTP::Post.new(uri.request_uri, header)
      request.body = datapoint.to_json

      # Send the request
      response = http.request(request)
    end
  # Raised when any metrics could not be sent
  #
  rescue Timeout::Error
    puts 'Outlyer -- timed out while sending metrics'
  rescue => error
    puts "Outlyer -- failed to send metrics: #{error.message}"
    puts " #{error.backtrace.join("\n\t")}"
  end
end