from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys
import afl

sys.path.insert(0, "..")

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()


from opcua import ua, uamethod, Server


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


# method to be exposed through server

def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y


class VarUpdater(Thread):
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            v = sin(time.time() / 10)
            self.var.set_value(v)
            time.sleep(0.1)



if __name__ == "__main__":
    afl.init()
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)
    logger = logging.getLogger("opcua.address_space")
     logger.setLevel(logging.DEBUG)
    logger = logging.getLogger("opcua.internal_server")
     logger.setLevel(logging.DEBUG)
    logger = logging.getLogger("opcua.binary_server_asyncio")
     logger.setLevel(logging.DEBUG)
    logger = logging.getLogger("opcua.uaprocessor")
     logger.setLevel(logging.DEBUG)

    # now setup our server
    server = Server()
    #server.disable_clock()
    #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    endpoint = sys.stdin.readline().rstrip("\n")
    server.set_endpoint(endpoint)
    server_name = sys.stdin.readline().rstrip("\n") 
    server.set_server_name(server_name)
    # set possible endpoint policies for clients to connect through
    security_policy = sys.stdin.readline().rstrip("\n")
    server.set_security_policy(security_policy)

    # setup our own namespace
    uri_namespace = sys.stdin.readline().rstrip("\n")
    uri = uri_namespace
    idx = server.register_namespace(uri)

    # create a new node type we can instantiate in our address space

    device_object = sys.stdin.readline().rstrip("\n")
    device_node_id = sys.stdin.readline().rstrip("\n")
    dev = server.nodes.base_object_type.add_object_type(int(device_node_id),device_object)

    sensor_name = sys.stdin.readline().rstrip("\n")
    sensor_id = sys.stdin.readline().rstrip("\n")
    sensor_var = sys.stdin.readline().rstrip("\n") 
    dev.add_variable(int(sensor_id), sensor_name, float(sensor_var)).set_modelling_rule(True)

    device_id = sys.stdin.readline().rstrip("\n")
    device_name = sys.stdin.readline().rstrip("\n")
    device_var = sys.stdin.readline().rstrip("\n")
    dev.add_property(int(device_id), device_name, device_var).set_modelling_rule(True)


    ctrl_id = sys.stdin.readline().rstrip("\n")
    ctrl_name = sys.stdin.readline().rstrip("\n")

    ctrl = dev.add_object(int(ctrl_id), ctrl_name)
    ctrl.set_modelling_rule(True)

    ctrl_prop_id = sys.stdin.readline().rstrip("\n")
    ctrl_prop_state = sys.stdin.readline().rstrip("\n")
    ctrl_prop_idle = sys.stdin.readline().rstrip("\n")
    ctrl.add_property(int(ctrl_prop_id), ctrl_prop_state, ctrl_prop_idle).set_modelling_rule(True)

    # populating our address space

    # First a folder to organise our nodes
    folder_name = sys.stdin.readline().rstrip("\n")
    myfolder = server.nodes.objects.add_folder(idx, folder_name)
    # instanciate one instance of our device
    device_name_id = sys.stdin.readline().rstrip("\n")
    mydevice = server.nodes.objects.add_object(idx, device_name_id, dev)

    device_controller = ctrl_id+":"+ ctrl_name.lower() 
    device_state = ctrl_prop_id+":"+ ctrl_prop_state.lower() 
    mydevice_var = mydevice.get_child([device_controller, device_state])  # get proxy to our device state variable 
    # create directly some objects and variables

    object_add_name = sys.stdin.readline().rstrip("\n")
    myobj = server.nodes.objects.add_object(idx, object_add_name)

    var_add_name = sys.stdin.readline().rstrip("\n")
    var_add_value = sys.stdin.readline().rstrip("\n")
    myvar = myobj.add_variable(idx, var_add_name, float(var_add_value))

    mysin_name = sys.stdin.readline().rstrip("\n")
    mysin_var = sys.stdin.readline().rstrip("\n")
    mysin = myobj.add_variable(idx, mysin_name, float(mysin_var), ua.VariantType.Float)

    myvar.set_writable()    # Set MyVariable to be writable by clients

    mysstring_name = sys.stdin.readline().rstrip("\n")
    mysstring_var_string = sys.stdin.readline().rstrip("\n")
    mystringvar = myobj.add_variable(idx, mysstring_name, mysstring_var_string)

    mystringvar.set_writable()    # Set MyVariable to be writable by clients

    mysdate_time_var = sys.stdin.readline().rstrip("\n")
    mydtvar = myobj.add_variable(idx, mysdate_time_var, datetime.utcnow())
    mydtvar.set_writable()    # Set MyVariable to be writable by clients

    myarrayvar_name = sys.stdin.readline().rstrip("\n")
    myarrayvar_var_array = sys.stdin.readline().rstrip("\n")
    myarrayvar = myobj.add_variable(idx, myarrayvar_name, myarrayvar_var_array)

    myarrayvar_strong_var = sys.stdin.readline().rstrip("\n")
    myarrayvar = myobj.add_variable(idx, myarrayvar_strong_var, ua.Variant([], ua.VariantType.UInt32))

    myprop_name = sys.stdin.readline().rstrip("\n")
    myprop_string = sys.stdin.readline().rstrip("\n")
    myprop = myobj.add_property(idx, myprop_name, myprop_string)

    mymethod_name = sys.stdin.readline().rstrip("\n")
    mymethod = myobj.add_method(idx, mymethod_name, func, [ua.VariantType.Int64], [ua.VariantType.Boolean])

    mutiply_name = sys.stdin.readline().rstrip("\n")
    multiply_node = myobj.add_method(idx, mutiply_name, multiply, [ua.VariantType.Int64, ua.VariantType.Int64], [ua.VariantType.Int64])

    # import some nodes from xml
    server.import_xml("custom_nodes.xml")

    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = server.get_event_generator()

    myevgen_severity_lvl = sys.stdin.readline().rstrip("\n")
    myevgen.event.Severity = int(myevgen_severity_lvl)

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    vup = VarUpdater(mysin)  # just  a stupide class update a variable
    vup.start()
    try:
        # enable following if you want to subscribe to nodes on server side
        handler = SubHandler()
        subscription_lvl = sys.stdin.readline().rstrip("\n")
        sub = server.create_subscription(int(subscription_lvl), handler)
        handle = sub.subscribe_data_change(myvar)
        # trigger event, all subscribed clients wil receive it
        var = myarrayvar.get_value()  # return a ref to value in db server side! not a copy!
        var = copy.copy(var)  # WARNING: we need to copy before writting again otherwise no data change event will be generated
        var_arrary_id = sys.stdin.readline().rstrip("\n")
        var.append(float(var_arrary_id))
        myarrayvar.set_value(var)

        mydevice_var_value_set = sys.stdin.readline().rstrip("\n")
        mydevice_var.set_value(mydevice_var_value_set)

        myevgent_trigger_message = sys.stdin.readline().rstrip("\n")
        myevgen.trigger(message= myevgent_trigger_message)

        #embed()
    finally:
        vup.stop()
        server.stop()
