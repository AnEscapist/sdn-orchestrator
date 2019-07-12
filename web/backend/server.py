import zmq
import random
import sys
import time
import threading
import json
import queue
import signal
from flask import Flask, escape, request, jsonify

app = Flask(__name__)

#example route
#/api/containers in frontend
@app.route('/docker/abcde', methods=['POST', 'GET'])
def get_containers():
    # messagedata = {"body": {"id": 5}}
    messagedata = {"method": "libvirt_controller_get_vm_state", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    #return jsonify(name='ucpe', email='alkjdflk@gmail.com')
    print(jsonify(call_ucpe_function(messagedata)))
    return jsonify(call_ucpe_function(messagedata))

signal.signal(signal.SIGINT, signal.SIG_DFL)

port_pub = "5559"
port_sub = "5570"
TIMEOUT = 1000 #todo: decide
CONTROLLER_ID = "test-id"
BROKER_IP = "10.10.81.200" #todo: make this not global
#todo: set topic to something reasonable, like request id or timestampidk
#NOTE: TOPICS CANNOT CONTAIN SPACES

ids = queue.Queue()
max_id = 0
max_id_lock = threading.Lock()

def call_ucpe_function(messagedata, controller_id='test-id', ucpe_sn='test-sn'):
    if not ids.empty():
        print(ids.queue)
    request_id = get_request_id()
    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.connect("tcp://%s:%s" % (BROKER_IP, port_pub))
    q = queue.Queue()
    response_thread = threading.Thread(target=sub_response, args=(q, ucpe_sn, request_id))
    response_thread.start() #todo: figure out how to configure timeout
    time.sleep(1) #todo: BAD
    send_request(messagedata, controller_id, request_id, socket_pub)
    response = q.get(timeout=TIMEOUT)
    ids.put(request_id)
    return response

def get_topic(id, request_id):
    return f'{id}___{request_id}'

def get_request_id():
    global max_id
    with max_id_lock:
        if ids.empty():
            max_id += 1
            return max_id
        return ids.get()

def send_request(messagedata, controller_id, request_id, socket_pub):
    # Socket to publish requests
    topic = get_topic(controller_id, request_id)
    print("send_topic", topic)
    dump = json.dumps(messagedata)
    socket_pub.send_string('%s %s' % (topic, dump))

def sub_response(queue, ucpe_sn, request_id):
    # Socket to subscribe to responses
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    print("Collecting updates from server...")
    socket_sub.connect("tcp://%s:%s" % (BROKER_IP, port_sub))
    topic = get_topic(ucpe_sn, request_id)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic)
    while True: #does this block?
        received = socket_sub.recv().decode('ASCII')
        topic, message = received.split(" ", 1)
        print(topic, message)
        response = json.loads(message)
        queue.put(response)
        return response

# creating thread
# t1 = threading.Thread(target=sub_response)

# starting thread 1
# t1.start()
#
# time.sleep(1)
controller_id = "test-id"
ucpe_sn = "test-sn"

messagedata = {"method": "libvirt_controller_get_vm_state", "params": {
    "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
             "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

if __name__ == "__main__":
    app.run(threaded=True)
    #print(call_ucpe_function(messagedata, controller_id, ucpe_sn))
    # number_of_threads = 1
    # sleep_time = 0.001
    # threads = []
    # for i in range(number_of_threads):
    #     thread = threading.Thread(target=call_ucpe_function, args=(messagedata, controller_id, ucpe_sn))
    #     threads.append(thread)
    #
    # for thread in threads:
    #     thread.start()
    #     time.sleep(sleep_time)
    #
    # for thread in threads:
    #     thread.join()
    #
    # print(list(ids.queue))
    # assert len(set(ids.queue)) == len(list(ids.queue))
