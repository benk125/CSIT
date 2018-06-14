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
    var.get_attribute(int(value))

def get_child(value, var):
    test = var.get_child(value)

def add_variable_folder(value,value2, value3 , value4 ,var):
    folder = var.add_folder(value , value2)
    variable = var.add_variable(value3 , value2, value4)
    client.delete_nodes([folder, variable])



if __name__ == "__main__":
    afl.init()
    client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/")
    buffer = []
    test_array = ["2:MyStringVariable" , "2:MyVariable" , "2:myarrayvar" , "2:MyDateTimeVar"]
    value = sys.stdin.readline().rstrip('\n')
    var_array = []
    while value != '':
        buffer.append(value)
        value = sys.stdin.readline().rstrip('\n')
    #print(buffer)
    try:
        client.connect()
        var2 = client.nodes.objects.get_child("2:MyObject")
        for i in test_array:
            var_array.append(var2.get_child(i))
       # while afl.loop(10000):
        ben = True
        if ben == True:
            get_child(buffer[6], var2)
            add_variable_folder(buffer[7] , buffer[8], buffer[9], buffer[10], var2)
            print("here2")
            for i in range(0, len(var_array)):
                setting_value(buffer[i], var_array[i])
                print("here3")
                set_array_dimensions(buffer[4], var_array[i])
                print("here4")
                get_attribute(buffer[5], var_array[i])
                print("here5")
    except Exception as e:
        print(e)
        
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


