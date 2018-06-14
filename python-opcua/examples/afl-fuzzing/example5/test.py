import afl
import sys
from opcua import Client
import os
sys.path.insert(0, "..")

def setting_value(value, var):
    var.set_value(value)
    var.set_data_value(value)
    var.set_writable(value)

def set_array_dimensions(value, var):
    var.set_array_dimensions

def get_attribute(value , var):
    var.get_attribute(value)

def get_child(value):
    client.nodes.objects.get_child("2:MyObject").get_child(value)

if __name__ == "__main__":
    afl.init()
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    buffer = []
    test_array = ["2:MyStringVariable" , "2:MyVariable" , "2:myarrayvar" , "2:MyDateTimeVar"]
    value = sys.stdin.readline().rstrip('\n')
    while value != '':
            buffer.append(value)
            value = sys.stdin.readline().rstrip('\n')
    try:
        client.connect()
        for i in test_array:
            var.append(client.nodes.objects.get_child("2:MyObject").get_child(i))
        while afl.loop(10000):
            get_child(buffer[7])
            for i in var:
                setting_value(buffer[i], i)
                set_array_dimensions(buffer[4], i)
                get_attribute(buffer[5], i)
                get_child(buffer[6],i)
                
        #print(value)
    finally:
        os._exit(0)
        client.disconnect()


#"opc.tcp://0.0.0.0:4840/freeopcua/server/")
#"FreeOpcUa Example Server"
#["None","Basic128Rsa15_Sign","Basic128Rsa15_SignAndEncrypt","Basic256_Sign","Basic256_SignAndEncrypt"]
#"http://examples.freeopcua.github.io" 
#"MyDevice"
#0
#"sensor1"
#0
#1.0
#0
#"device_id"
#0340
#0
#"Controller"
#0
#"state"
#"Idle"
#"MyFolder"
#"Device0001"
#"0:controller"
#"0:state"
#"MyObject"
#"MyVariable"
#9.2
#"MySin"
#0
#"MyStringVariable"
#"Really nice String
#"MyDateTimeVar"
#"myarrayvar"
#[6.9,7.9]
#"myStronglyTypdVariable"
#"myProp"
#"myprop_string"
#"mymethod"
#"multiply"
#300
#500
#9.3
#"Running"
#"This is BaseEvent"


