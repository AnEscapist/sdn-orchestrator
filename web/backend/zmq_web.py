import sys

sys.path.append('/home/attadmin/projects/sdn-orchestrator/')
sys.path.append('/home/att-pc-7/Zhengqi/Project/sdn-orchestrator/')
sys.path.append('/home/att/projects/sdn-orchestrator/')
import zmq
import time
import threading
import json
import queue
import signal
import math
import random
from collections import namedtuple

signal.signal(signal.SIGINT, signal.SIG_DFL)

port_pub = "5559"
port_sub = "5570"
TIMEOUT = 15  # todo: decide
CONTROLLER_ID = "test-id"
BROKER_IP = "10.10.81.200"  # todo: make this not global
UCPE_LIST = ["test-sn"]  # serial numbers of ucpes this controller controls
# todo: set topic to something reasonable, like request id or timestampidk
REQUEST_ID_DELIMITER = "___"
# NOTE: TOPICS CANNOT CONTAIN SPACES

request_ids = queue.Queue()
request_queue = queue.Queue()
response_queues = dict()  # request_id -> responseQueue
response_queues_lock = threading.Lock()
max_id = 0
max_id_lock = threading.Lock()


def call_ucpe_function(messagedata, controller_id='test-id', ucpe_sn='test-sn'):
    print(messagedata,'\n', controller_id,'\n', ucpe_sn)
    if not request_ids.empty():
        print('ids', request_ids.queue)
    request_id = get_request_id()
    response_queue = queue.Queue()
    with response_queues_lock:
        response_queues[request_id] = response_queue
    # response_thread = threading.Thread(target=sub_response, args=(response_queue, ucpe_sn, request_id))
    # response_thread.start() #todo: figure out how to configure timeout
    # time.sleep(1) #todo: BAD
    send_request(messagedata, controller_id, request_id)
    response = response_queue.get(timeout=TIMEOUT)
    # request_ids.put(request_id) #todo: remember to put this back when we're done
    return response


def get_topic(id, request_id):
    return f'{id}___{request_id}'


def request_id_from_topic(topic):
    return int(topic.rsplit(REQUEST_ID_DELIMITER)[1])


def get_request_id():
    # global max_id
    # with max_id_lock:
    #     if request_ids.empty():
    #         max_id += 1
    #         return max_id
    #     return request_ids.get()
    return random.randrange(0, 10**12)


def send_request(messagedata, controller_id, request_id):
    # Socket to publish requests
    topic = get_topic(controller_id, request_id)
    message = json.dumps(messagedata)
    # socket_pub.send_string('%s %s' % (topic, dump))
    request = namedtuple('Request', ['message', 'topic'])
    request.message = message
    request.topic = topic
    request_queue.put(request)


def sub_response(queue, ucpe_sn, request_id):
    # Socket to subscribe to responses
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    # print("Collecting updates from server...")
    socket_sub.connect("tcp://%s:%s" % (BROKER_IP, port_sub))
    topic = get_topic(ucpe_sn, request_id)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, topic)
    # print("subscribed to", topic)
    received = socket_sub.recv().decode('ASCII')
    # print("received")
    topic, message = received.split(" ", 1)
    # print(topic, message)
    response = json.loads(message)
    queue.put(response)
    return response


def handleRequests():
    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.connect("tcp://%s:%s" % (BROKER_IP, port_pub))
    while True:
        request = request_queue.get()  # blocks
        socket_pub.send_string('%s %s' % (request.topic, request.message))
        print('sent', request.topic, request.message)


def handleFiniteRequests(iterations):
    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.connect("tcp://%s:%s" % (BROKER_IP, port_pub))
    for i in range(iterations):
        request = request_queue.get()  # blocks
        socket_pub.send_string('%s %s' % (request.topic, request.message))
        print('sent', request.topic, request.message)


def startRequestHandler():
    requestHandler = threading.Thread(target=handleRequests)
    requestHandler.start()


def startFiniteRequestHandler(iterations):
    finiteRequestHandler = threading.Thread(target=handleFiniteRequests, args=[iterations])
    finiteRequestHandler.start()
    time.sleep(0.5)  # todo: why do we need this?


def handleResponses():
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    # print("Collecting updates from server...")
    socket_sub.connect("tcp://%s:%s" % (BROKER_IP, port_sub))
    for ucpe_sn in UCPE_LIST:
        socket_sub.setsockopt_string(zmq.SUBSCRIBE, ucpe_sn)
    print("Listening for Responses")
    while True:
        received = socket_sub.recv().decode('ASCII')
        topic, message = received.split(" ", 1)
        print('received', topic, message)
        response = json.loads(message)
        request_id = request_id_from_topic(topic)
        with response_queues_lock:
            if request_id in response_queues:
                response_queue = response_queues[request_id]
                response_queue.put(response)


def handleFiniteResponses(iterations):
    context_sub = zmq.Context()
    socket_sub = context_sub.socket(zmq.SUB)
    # print("Collecting updates from server...")
    socket_sub.connect("tcp://%s:%s" % (BROKER_IP, port_sub))
    for ucpe_sn in UCPE_LIST:
        socket_sub.setsockopt_string(zmq.SUBSCRIBE, ucpe_sn)
    print("Listening for Responses")
    for i in range(iterations):
        received = socket_sub.recv().decode('ASCII')
        topic, message = received.split(" ", 1)
        # print('received', topic, message)
        response = json.loads(message)
        request_id = request_id_from_topic(topic)
        with response_queues_lock:
            if request_id in response_queue:
                response_queue = response_queues[request_id]
                response_queue.put(response)


def startResponseHandler():
    responseHandler = threading.Thread(target=handleResponses)
    responseHandler.start()
    time.sleep(0.5)  # todo: why do we need this?


def startFiniteResponseHandler(iterations):
    finiteResponseHandler = threading.Thread(target=handleFiniteResponses, args=[iterations])
    finiteResponseHandler.start()
    time.sleep(0.5)  # todo: why do we need this?


def start():
    startResponseHandler()
    startRequestHandler()
    time.sleep(2)


# tests
def checkForDeadlock():
    controller_id = "test-id"
    ucpe_sn = "test-sn"
    messagedata = {"method": "libvirt_controller_get_vm_state", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    # print(call_ucpe_function(messagedata, controller_id, ucpe_sn))
    # docker_md = {"method": "docker_controller_list_images", "params": {
    #     "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
    #              "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    # docker_md = {"method": "docker_controller_list_containers", "params": {
    #     "body": {}}, "jsonrpc": "2.0", "id": 0}
    # print(call_ucpe_function(docker_md, controller_id, ucpe_sn))
    # grpc_md = {"method": "grpc_get_totalcpus", "params": {
    #     "body": {"hostname": "10.10.81.100", "port": "50051"}}, "jsonrpc": "2.0", "id": 0}
    # print(call_ucpe_function(grpc_md, controller_id, ucpe_sn))

    number_of_threads = 1000
    sleep_time = 0
    threads = []

    print("testing with", number_of_threads, "threads")
    start()

    for i in range(number_of_threads):
        thread = threading.Thread(target=call_ucpe_function, args=(messagedata, controller_id, ucpe_sn))
        threads.append(thread)

    for thread in threads:
        thread.start()
        time.sleep(sleep_time)

    for thread in threads:
        assert len(set(request_ids.queue)) == len(list(request_ids.queue))
        thread.join()

    assert len(set(request_ids.queue)) == len(list(request_ids.queue))
    print("Success!")


def checkForMemoryLeakage():
    minutes = 15
    messagedata = {"method": "libvirt_controller_get_vm_state", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    for i in range(minutes * 60):
        call_ucpe_function(messagedata)
        time.sleep(1)
    time.sleep(math.inf)  # wait


# creating thread
# t1 = threading.Thread(target=sub_response)

# starting thread 1
# t1.start()
#
# time.sleep(1)

if __name__ == "__main__":
    # checkForMemoryLeakage()
    # checkForDeadlock()
    start()
    time.sleep(2)
    # messagedata = {"method": "libvirt_controller_get_vm_state",
    #  "params": {"body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test"}}, "jsonrpc": "2.0",
    #  "id": 0}
    # call_ucpe_function(messagedata)
