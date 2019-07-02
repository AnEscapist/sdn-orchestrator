import data_client

import json
import os


class gRPCDataController(object):
    HOSTNAME = '10.10.81.100'
    PORT = '50051'

    params = dict()

    def __init__(self):
        temp = dict()
        temp['hostname'] = self.HOSTNAME
        temp['port'] = self.PORT
        temp['command'] = str()
        temp['str_request'] = str()
        temp['str_param1'] = None
        temp['str_param2'] = None
        self.params['body'] = temp

    @staticmethod
    def grpc_get_hugepages_totalmem(self, hostname=HOSTNAME, port=PORT):
        return get_execute(self, "hugepages total", hostname, port)

    @staticmethod
    def grpc_get_hugepages_freemem(self, hostname=HOSTNAME, port=PORT):
        return get_execute(self, "hugepages free", hostname, port)

    @staticmethod
    def grpc_get_totalmem(self, hostname=HOSTNAME, port=PORT):
        return get_execute(self, "memory total", hostname, port)

    @staticmethod
    def grpc_get_availmem(self, hostname=HOSTNAME, port=PORT):
        return get_execute(self, "memory available", hostname, port)

    @staticmethod
    def grpc_get_totalcpus(self, hostname=HOSTNAME, port=PORT):
        return get_execute(self, "cpu total", hostname, port)


# ==================== private functions ===============================
def interpret_params(controller, input_string):
    tmp = input_string.split(" ")
    count = len(tmp)
    # print(tmp[0])
    # print(tmp[1])
    controller.params['body']['command'] = tmp[0]
    controller.params['body']['str_request'] = tmp[1]
    if count > 2:
        controller.params['body']['str_params1'] = tmp[2]
        if count > 3:
            controller.params['body']['str_params2'] = tmp[3]
    # print(str(controller.params))
    return controller


def get_execute(controller, input_string, hostname, port):
    controller = interpret_params(controller, input_string)
    controller.params['body']['hostname'] = hostname
    controller.params['body']['port'] = port
    body = controller.params['body']
    return data_client.run('get', **body)


def modify_execute(controller, input_string, hostname, port):
    interpret_params(controller, input_string)
    controller.params['body']['hostname'] = hostname
    controller.params['body']['port'] = port
    body = controller.params['body']
    return data_client.run('modify', **body)
