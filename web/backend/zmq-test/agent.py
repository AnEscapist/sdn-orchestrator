import zmq
import time
import threading
import json
import sys
from jsonrpc import JSONRPCResponseManager, dispatcher, Dispatcher

sys.path.append('/home/attadmin/projects/sdn-orchestrator/')
sys.path.append('/home/att-pc-7/Zhengi/Project/sdn-orchestrator/')
sys.path.append('/home/att/projects/sdn-orchestrator/')

from ucpe.libvirt_controller.libvirt_controller import *
from ucpe.docker_controller.docker_controller import *
from ucpe.grpc_data_collector.grpc_data_collector import *
from ucpe.bcm_controller.bcm_controller import *

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

CONTROLLER_ID = 'test-id'
UCPE_SN = 'test-sn' #todo: get the ucpe serial number

def pub_response(d, mess):
    message = mess.decode('ASCII')
    topic, request = message.split(" ", 1)
    new_topic = get_new_topic(topic)
    response = JSONRPCResponseManager.handle(request, d)
    print(topic, new_topic)
    socket_pub.send_string("%s %s" % (new_topic, json.dumps(response.data)))

def get_new_topic(old_topic):
    request_id = old_topic.rsplit("___")[1]
    return f'{UCPE_SN}___{request_id}' #todo: factor out the ___ into a constant

port_sub = "5560"
port_pub = "5569"
# Socket to subscribe to requests
context_sub = zmq.Context()
socket_sub = context_sub.socket(zmq.SUB)

# Socket to publish responses
context_pub = zmq.Context()
socket_pub = context_pub.socket(zmq.PUB)
socket_pub.connect("tcp://localhost:%s" % port_pub)

"""
class test1:

    @staticmethod
    def test1_1(*args, **kwargs):
        return "test1_1"

    @staticmethod
    def test1_2(*args, **kwargs):
        return "test1_2"

class test2:

    @staticmethod
    def test2_1(*args, **kwargs):
        return "test2_1"

    @staticmethod
    def test2_2(*args, **kwargs):
        return "test2_2"

    @staticmethod
    def test2_3(*args, **kwargs):
        return "test2_3"
"""

def server_routine():
    d = Dispatcher()
    d.build_method_map(LibvirtController)
    d.build_method_map(gRPCDataCollector)
    d.build_method_map(DockerController)
    d.build_method_map(BCMController)

    print("Collecting updates from server...")
    socket_sub.connect("tcp://localhost:%s" % port_sub)
    topicfilter = CONTROLLER_ID
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    while True:
        received = socket_sub.recv()
        pub_response(d, received)


def main():
    server_routine()
    # Never reached?  Not unless we define a termination condition for
    context_pub.term()
    context_sub.term()


if __name__ == "__main__":
    main()
