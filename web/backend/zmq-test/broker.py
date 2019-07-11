import zmq

import threading
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL);


def request():
    try:
        context = zmq.Context(1)

        ##### Request device

        # Socket facing client
        frontend_req = context.socket(zmq.SUB)
        frontend_req.bind("tcp://*:5559")
        frontend_req.setsockopt_string(zmq.SUBSCRIBE, "") #TODO: don't sub to everything - just the controllers the broker is responsible for

        # Socket facing services
        backend_req = context.socket(zmq.PUB)
        backend_req.bind("tcp://*:5560")

        zmq.device(zmq.FORWARDER, frontend_req, backend_req)

    except Exception as e:
        print(e)
        print("bringing down zmq device")
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


def response():
    try:
        context = zmq.Context(1)

        ##### Response device

        # Socket facing client
        backend_resp = context.socket(zmq.PUB)
        backend_resp.bind("tcp://*:5570")

        # Socket facing services
        frontend_resp = context.socket(zmq.SUB)
        frontend_resp.bind("tcp://*:5569")
        frontend_resp.setsockopt_string(zmq.SUBSCRIBE, "")

        zmq.device(zmq.FORWARDER, frontend_resp, backend_resp)

    except Exception as e:
        print(e)
        print("bringing down zmq device")
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=request)
    t2 = threading.Thread(target=response)

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
