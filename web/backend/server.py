import zmq
import random
import sys
import time
import threading
import json
import queue

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

port_pub = "5559"
port_sub = "5570"
TIMEOUT = 1000 #todo: decide
#todo: set topic to something reasonable, like request id or timestampidk

def call_ucpe_function(messagedata, topic):
    send_request(messagedata, topic)
    q = queue.Queue()
    request_thread = threading.Thread(target=sub_response)
    request_thread.start() #todo: figure out how to configure timeout
    response = q.get(timeout=TIMEOUT)
    return response

def send_request(messagedata, topic):
    # Socket to publish requests
    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.connect("tcp://localhost:%s" % port_pub)
    messagedata = json.dumps(messagedata)
    #messagedata = {"method": "docker_controller_create_client", "params": {"body":{'ip':'10$
    #messagedata = json.dumps(messagedata)
#    print("%s %s" % (topic, messagedata))
    socket_pub.send_string(topic, zmq.SNDMORE)
    socket_pub.send_string(messagedata)

def sub_response(topic, queue):
    # Socket to subscribe to responses
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    print("Collecting updates from server...")
    socket_sub.connect("tcp://localhost:%s" % port_sub)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic)
    while True: #does this block?
        received_topic = socket_sub.recv().decode('ASCII')
        if socket_sub.get(zmq.RCVMORE) and received_topic == topic: #todo: ask tyler why this and is necessary
            response = socket_sub.recv()
            return response

# creating thread
# t1 = threading.Thread(target=sub_response)

# starting thread 1
# t1.start()
#
# time.sleep(1)
topic = "test-id"
messagedata = {"method": "libvirt_controller_get_vm_state", "params": {
    "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
             "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
call_ucpe_function(messagedata, topic)
# messagedata = json.dumps(messagedata)
# print("%s %s" % (topic, messagedata))
# socket_pub.send_string(topic, zmq.SNDMORE)
# socket_pub.send_string(messagedata)
# print("%s %s" % (topic, messagedata))
# socket_pub.send_string(topic, zmq.SNDMORE)
# socket_pub.send_string(messagedata)
# print("%s %s" % (topic, messagedata))
# socket_pub.send_string(topic, zmq.SNDMORE)
# socket_pub.send_string(messagedata)
# print("%s %s" % (topic, messagedata))
# socket_pub.send_string(topic, zmq.SNDMORE)
# socket_pub.send_string(messagedata)
# print("%s %s" % (topic, messagedata))
# socket_pub.send_string(topic, zmq.SNDMORE)
# socket_pub.send_string(messagedata)
# print("%s %s" % (topic, messagedata))
# socket_pub.send_string(topic, zmq.SNDMORE)
# socket_pub.send_string(messagedata)

# wait until thread 1 is completely executed
# t1.join()