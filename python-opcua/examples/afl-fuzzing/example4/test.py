import afl
import sys
from opcua import Client
import os
sys.path.insert(0, "..")

def testing(value, var, value2 , var2):
    print value
    print var
    var.set_value(value)
    var2.set_value(value2)


if __name__ == "__main__":
    afl.init()
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    value = sys.stdin.readline().rstrip("\n")
    value2 = sys.stdin.readline().rstrip("\n")
    try:
        client.connect()
        var = client.nodes.objects.get_child("2:MyObject").get_child("2:MyStringVariable")
        var2 = client.nodes.objects.get_child("2:MyObject").get_child("2:MyVariable")
        while afl.loop(10000):
            testing(str(value), var, float(value2) , var2)
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


