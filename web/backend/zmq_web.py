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
#TIMEOUT = 15  # todo: decide  #MOVED IT AS A PARAMETER OF CALL_UCPE_FUNCTION
CONTROLLER_ID = "test-id"
BROKER_IP = "10.10.81.200"  # todo: make this not global
UCPE_LIST = ["test-sn"]  # serial numbers of ucpes this controller controls
# todo: set topic to something reasonable, like request id or timestampidk
REQUEST_ID_DELIMITER = "___"
TIMEOUT = 120
RANDOMIZED_IDS = True
# NOTE: TOPICS CANNOT CONTAIN SPACES

request_ids = queue.Queue()
request_queue = queue.Queue()
response_queues = dict()  # request_id -> responseQueue
response_queues_lock = threading.Lock()
max_id = 0
max_id_lock = threading.Lock()

'''
OVERALL STRUCTURE:
request_queue is a threadsafe queue of requests.  
response_queues is a dictionary mapping request_ids to response queues.

A request is a tuple of (messagedata, request_id).
A response is a tuple of (responsedata, request_id)

To make a request with messagedata M, a request_id R is generated.  Request (M,R) is placed in request_queue.
A response queue for request R is created and inserted into response_queues under key R.
call_ucpe_function blocks (via a Queue.get call) until either timeout or a response appears in the response queue.

The request handler pops request (M,R) from request_queue and publishes its messagedata under the topic controller_id___R

A response (P,R) will come back with topic ucpe_sn___R.  We put P into the response queue response_queues[R]. 
immediately, call_ucpe_function's Queue.get call is successful so call_ucpe_function stops blocking and returns P.
'''


def call_ucpe_function(messagedata, controller_id='test-id', ucpe_sn='test-sn', timeout=TIMEOUT):
    '''
    send a request directed to uCPE with serial number ucpe_sn containing messagedata to the message bus,
    block until either timeout or response is received from uCPE
    :param messagedata: payload for json-rpc server
    :param controller_id: controller id
    :param ucpe_sn: ucpe serial number
    :param timeout: time to wait for response before throwing an error
    :return: result of function specified by messagedata
    '''
    print(messagedata,'\n', controller_id,'\n', ucpe_sn)
    request_id = get_request_id()
    response_queue = queue.Queue() # construct response queue
    with response_queues_lock:
        response_queues[request_id] = response_queue # add response queue to response_queues under key request_id
    send_request(messagedata, controller_id, request_id) # adds request to request_queue
    response = response_queue.get(timeout=timeout) # await response (this line blocks until queue is not empty or timeout, whichever is first)
    # todo: if using deterministic system, guarantee that thread handling request is terminated before recycling the request_id
    if not RANDOMIZED_IDS: # after receiving response or giving up on it, put request id back in queue
        request_ids.put(request_id) #todo: remember to put this back when we're done
    return response


def get_topic(id, request_id):
    return f'{id}___{request_id}'


def request_id_from_topic(topic):
    '''
    :param topic: string of the form '<ucpe_sn/controller_id>___<request_id>
    :return: request_id
    '''
    return int(topic.rsplit(REQUEST_ID_DELIMITER)[1])


def get_request_id():
    '''
    get request id- currently randomized for testing so that multiple computers can send requests to the same uCPE using the same controller_id
    use get_request_id_deterministic instead to guarantee that request ids are unique (this does not allow two computers to use the same controller_id, which shouldn't happen in real life anyway)
    '''
    if RANDOMIZED_IDS:
        return get_request_id_randomized()
    else:
        return get_request_id_deterministic()

def get_request_id_randomized():
    return random.randrange(0, 10**12)

def get_request_id_deterministic():
    '''
    :return: an int from 1 - N, where N is the max number of requests that have been handled at once thus far
    '''
    global max_id
    with max_id_lock:
        if request_ids.empty():
            max_id += 1
            return max_id
        return request_ids.get()


def send_request(messagedata, controller_id, request_id):
    '''
    place request in request_queue
    :param messagedata: json-rpc messagedata
    :param controller_id: controller id
    :param request_id: request id
    '''
    # Socket to publish requests
    topic = get_topic(controller_id, request_id)
    message = json.dumps(messagedata)
    # socket_pub.send_string('%s %s' % (topic, dump))
    request = namedtuple('Request', ['message', 'topic'])
    request.message = message
    request.topic = topic
    request_queue.put(request)


def sub_response(queue, ucpe_sn, request_id):
    '''
    not used
    '''
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
    '''
    take requests off the request queue and publish their messagedata under their respective topics
    '''
    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.connect("tcp://%s:%s" % (BROKER_IP, port_pub))
    while True:
        request = request_queue.get()  # blocks
        socket_pub.send_string('%s %s' % (request.topic, request.message))
        print('sent', request.topic, request.message)


def startRequestHandler():
    requestHandler = threading.Thread(target=handleRequests)
    requestHandler.start()
    time.sleep(1)


def handleResponses():
    '''
    listen for incoming responses and put them in their appropriate response queues
    '''
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


def startResponseHandler():
    responseHandler = threading.Thread(target=handleResponses)
    responseHandler.start()
    time.sleep(1)  # todo: why do we need this?

def start():
    startResponseHandler()
    startRequestHandler()


# tests
def handleFiniteRequests(iterations):
    context_pub = zmq.Context()
    socket_pub = context_pub.socket(zmq.PUB)
    socket_pub.connect("tcp://%s:%s" % (BROKER_IP, port_pub))
    for i in range(iterations):
        request = request_queue.get()  # blocks
        socket_pub.send_string('%s %s' % (request.topic, request.message))
        print('sent', request.topic, request.message)

def startFiniteRequestHandler(iterations):
    finiteRequestHandler = threading.Thread(target=handleFiniteRequests, args=[iterations])
    finiteRequestHandler.start()
    time.sleep(0.5)  # todo: why do we need this?

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


def startFiniteResponseHandler(iterations):
    finiteResponseHandler = threading.Thread(target=handleFiniteResponses, args=[iterations])
    finiteResponseHandler.start()
    time.sleep(0.5)  # todo: why do we need this?

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
    messagedata = {'method': 'grpc_get_totalcpus', 'params': {
        'body': {'hostname': '10.10.81.100', 'port': '50051'}},
                   'jsonrpc': '2.0', 'id': 0
                   }
    print(call_ucpe_function(messagedata))

