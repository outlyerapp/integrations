# (C) 2018 Dataloop Software, INC. Trading as Outlyer
# Unit tests for the Sensu Outlyer Handler
#
# Make sure you set your environment variable for SENSU_CONFIG_FILES
# so your API configuration and settings are correctly setup when running the tests

require 'test/unit'
require 'json'

class TestOutlyerHandler < Test::Unit::TestCase
 
  def setup
    @script = File.expand_path('../bin/outlyer-metrics.rb', File.dirname(__FILE__))
  end
  
  def test_nagios_output_1
    
    host = "ip-10-127-222-123.us-east-2.compute.internal"
    output = "HTTP OK: HTTP/1.1 301 Moved Permanently - 388 bytes in 0.188 second response time |time=0.187882s;;;0.000000 size=388B;;;0"
    event = create_new_event('nagios-check', output, host)
    
    # Initialize class with command line args piped in
    run_script_with_input(event.to_json, ['-f', 'nagios', '-d'])
  end
  
  def test_graphite_output_1
    
    metrics_host = "ip-10-127-222-123.us-east-2.compute.internal"
    client_name = "client-12"
    scheme = "CLOUDTRUST.DEV.OPS_TEAM.APPSERVER.asg-sensu-server.DLCLOUDTRUST.00:00:23:59:1-7.#{metrics_host}"
    output = %Q{#{scheme}.cpu-pcnt-usage.user 4.57 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.nice 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.system 1.52 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.idle 93.91 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.iowait 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.irq 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.softirq 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.steal 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.guest 0.00 #{Time.now.to_i}}
    event = create_new_event('graphite-check', output, client_name)
    
    # Initialize class with command line args piped in
    run_script_with_input(event.to_json, ['-d'])
  end
  
  def test_graphite_output_no_schema
    
    metrics_host = "ip-10-127-222-123.us-east-2.compute.internal"
    client_name = "client-12"
    scheme = "CLOUDTRUST.DEV.OPS_TEAM.APPSERVER.#{metrics_host}"
    output = %Q{#{scheme}.cpu-pcnt-usage.user 4.57 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.nice 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.system 1.52 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.idle 93.91 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.iowait 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.irq 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.softirq 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.steal 0.00 #{Time.now.to_i}
#{scheme}.cpu-pcnt-usage.guest 0.00 #{Time.now.to_i}}
    event = create_new_event('graphite-check', output, client_name)
    
    # Initialize class with command line args piped in
    run_script_with_input(event.to_json, ['-d'])
  end
    
  # Run the handler script with arguments and input event JSON
  # 
  # @param input  [Object]  Event object with event data
  # @param args   [Array]   (Optional) String array of command line options for script
  #
  def run_script_with_input(input, args=[])
    puts "\n========================================================"
    puts "Running script #{@script} #{args.join(" ")}:\n\n"
     IO.popen(([@script] + args).join(" "), "r+") do |child|
       child.write(input)
       child.close_write
       puts child.read
     end
  end
  
  # Create a new event object with current timestamp and given output and check 
  # name
  #
  # @param check_name  [String]  The name of the check being run
  # @param output      [String]  The output of the check
  # @param hostname    [String]  Hostname of client running check
  #
  def create_new_event(check_name, output, hostname)
    event = {
      id: "ef6b87d2-1f89-439f-8bea-33881436ab90",
      action: "create",
      timestamp: Time.now.to_i,
      occurrences: 2,
      check: {
        type: "metric",
        total_state_change: 11,
        history: ["0", "0", "1", "1", "2", "2"],
        status: 0,
        output: output,
        executed: Time.now.to_i,
        issued: Time.now.to_i,
        name: check_name,
        thresholds: {
          critical: 180,
          warning: 120
        }
      },
      client: {
        timestamp: Time.now.to_i,
        version: "1.0.0",
        socket: {
          port: 3030,
          bind: "127.0.0.1"
        },
        subscriptions: ["all"],
        environment: ["dev", "application", "webserver"],
        address: "10.127.252.186",
        name: hostname
      }
    }
    event
  end
end
