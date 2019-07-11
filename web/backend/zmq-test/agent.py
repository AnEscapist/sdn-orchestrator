import zmq
import time
import threading
import json
import sys
from jsonrpc import JSONRPCResponseManager, dispatcher, Dispatcher

sys.path.append('/home/attadmin/projects/sdn-orchestrator/')
from ucpe.libvirt_controller.libvirt_controller import *

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL);


def pub_response(d, mess):
    message = mess.decode('ASCII')
    topic, request = message.split(" ", 1)
    print(topic, request)
    response = JSONRPCResponseManager.handle(request, d)
    print("resp", response)
    socket_pub.send_string("%s %s" % ('test-sn', json.dumps(response.data)))


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

    print("Collecting updates from server...")
    socket_sub.connect("tcp://localhost:%s" % port_sub)
    topicfilter = "test-id"
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    while True:
        received = socket_sub.recv()
        print(received)
        pub_response(d, received)


def main():
    server_routine()
    # Never reached?  Not unless we define a termination condition for
    context_pub.term()
    context_sub.term()


if __name__ == "__main__":
    main()
