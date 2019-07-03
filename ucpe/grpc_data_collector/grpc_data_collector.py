import data_client

import json
import os

HOSTNAME = '10.10.81.100'
PORT = '50051'


class gRPCDataCollector(object):

    @staticmethod
    def grpc_get_hugepages_totalmem(**kwargs):
        return get_execute("hugepages total", **kwargs)

    @staticmethod
    def grpc_get_hugepages_freemem(**kwargs):
        return get_execute("hugepages free", **kwargs)

    @staticmethod
    def grpc_get_totalmem(**kwargs):
        return get_execute("memory total", **kwargs)

    @staticmethod
    def grpc_get_availmem(**kwargs):
        return get_execute("memory available", **kwargs)

    @staticmethod
    def grpc_get_totalcpus(**kwargs):
        return get_execute("cpu total", **kwargs)

    @staticmethod
    def grpc_get_network_interfaces(**kwargs):
        return get_execute("netifaces list", **kwargs)

    @staticmethod
    def grpc_get_linux_bridges_list(**kwargs):
        return get_execute("bridge list", **kwargs)

    @staticmethod
    def grpc_get_linux_bridges_all(**kwargs):
        return get_execute("bridge all", **kwargs)

    @staticmethod
    def grpc_get_linux_bridge_details(**kwargs):
        return get_execute(f"bridge details {kwargs['body']['str_param1']}", **kwargs)

    @staticmethod
    def grpc_get_dpdk_devices(**kwargs):
        return get_execute("dpdk devices", **kwargs)

    @staticmethod
    def grpc_modify_dpdk_bind(**kwargs):
        return get_execute(f"dpdk bind {kwargs['body']['str_param1']} {kwargs['body']['str_param2']}", **kwargs)

    @staticmethod
    def grpc_modify_dpdk_unbind(**kwargs):
        return get_execute(f"dpdk unbind {kwargs['body']['str_param1']}", **kwargs)

    @staticmethod
    def grpc_modify_dpdk_enable(**kwargs):
        return get_execute(f"dpdk enable {kwargs['body']['str_param1']}", **kwargs)


# ==================== private functions ===============================
def interpret_params(input_string, **kwargs):
    tmp = input_string.split(" ")
    count = len(tmp)
    # print(tmp[0])
    # print(tmp[1])
    kwargs['body']['command'] = tmp[0]
    kwargs['body']['str_request'] = tmp[1]
    if count > 2:
        kwargs['body']['str_param1'] = tmp[2]
        if count > 3:
            kwargs['body']['str_param2'] = tmp[3]
            if count > 4:
                kwargs['body']['str_param3'] = tmp[4]
    # print(str(**kwargs))
    return kwargs


def get_execute(input_string, **kwargs):
    controller = interpret_params(input_string, **kwargs)
    return data_client.run('get', **controller)


def modify_execute(input_string, **kwargs):
    controller = interpret_params(input_string, **kwargs)
    return data_client.run('modify', **controller)


def main():
    kwargs = {'body': {'hostname': '10.10.81.100' , 'port': '50051'}}
    tmp = gRPCDataCollector()
    tmp.grpc_get_dpdk_devices(**kwargs)


if __name__ == '__main__':
    main()
