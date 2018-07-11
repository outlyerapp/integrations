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
  end

  # Push metric point
  #
  # @param name       [String]
  # @param value      [String]
  # @param _timestamp [String]
  def emit_metric(name, value, _timestamp)
    timeout(3) do
      # TODO
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