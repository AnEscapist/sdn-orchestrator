import zmq
import random
import sys
import time
import threading
import json
from flask import Flask, render_template 
from flask_socketio import SocketIO, emit

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL);

def start_flask():
    app = Flask(__name__)
    port_socketio = "5000"
    host = '10.10.81.200'

    socketio_socket = SocketIO(app, engineio_logger=True)
    socketio_socket.on_event('get_data', get_data)
    socketio_socket.run(app, host=host, port=port_socketio)

def get_data(messagedata):
    print('here')
    messagedata = json.dumps(messagedata)
    topic = "test-id"
    #messagedata = {"method": "docker_controller_create_client", "params": {"body":{'ip':'10$
    #messagedata = json.dumps(messagedata)
    print("%s %s" % (topic, messagedata))
    socket_pub.send_string(topic, zmq.SNDMORE)
    socket_pub.send_string(messagedata)

def sub_response():
    # Socket to subscribe to responses
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    print("Collecting updates from server...")
    socket_sub.connect("tcp://localhost:%s" % port_sub)
    topicfilter = "test-sn"
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    while True:
        topic = socket_sub.recv().decode('ASCII')
        if socket_sub.get(zmq.RCVMORE) and topic == topicfilter:
            messagedata = socket_sub.recv()
            print(messagedata)
            socketio.emit('vm_state', {'vm_state': messagedata})

port_pub = "5559"
port_sub = "5570"

# Socket to publish requests
context_pub = zmq.Context()
socket_pub = context_pub.socket(zmq.PUB)
socket_pub.connect("tcp://localhost:%s" % port_pub)

t1 = threading.Thread(target=sub_response)

# starting thread 1 
t1.start()

start_flask()

time.sleep(1)

"""
print("%s %s" % (topic, messagedata))
socket_pub.send_string(topic, zmq.SNDMORE)
socket_pub.send_string(messagedata)
print("%s %s" % (topic, messagedata))
socket_pub.send_string(topic, zmq.SNDMORE)
socket_pub.send_string(messagedata)
print("%s %s" % (topic, messagedata))
socket_pub.send_string(topic, zmq.SNDMORE)
socket_pub.send_string(messagedata)
print("%s %s" % (topic, messagedata))
socket_pub.send_string(topic, zmq.SNDMORE)
socket_pub.send_string(messagedata)
print("%s %s" % (topic, messagedata))
socket_pub.send_string(topic, zmq.SNDMORE)
socket_pub.send_string(messagedata)
"""

# wait until thread 1 is completely executed 
#t1.join()
#t2.join()
