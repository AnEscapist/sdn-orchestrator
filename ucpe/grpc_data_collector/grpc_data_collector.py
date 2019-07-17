import ucpe.grpc_data_collector.data_client as data_client

import json
import os
import sys

HOSTNAME = '10.10.81.100'
PORT = '50051'


class gRPCDataCollector(object):

    @staticmethod
    def grpc_get_hugepages_totalmem(**kwargs):
        return get_execute(func_name(), "hugepages total", **kwargs)

    @staticmethod
    def grpc_get_hugepages_freemem(**kwargs):
        return get_execute(func_name(), "hugepages free", **kwargs)

    @staticmethod
    def grpc_get_totalmem(**kwargs):
        return get_execute(func_name(), "memory total", **kwargs)

    @staticmethod
    def grpc_get_availmem(**kwargs):
        return get_execute(func_name(), "memory available", **kwargs)

    @staticmethod
    def grpc_get_totalcpus(**kwargs):
        return get_execute(func_name(), "cpu total", **kwargs)

    @staticmethod
    def grpc_get_network_interfaces(**kwargs):
        return get_execute(func_name(), "netifaces list", **kwargs)

    @staticmethod
    def grpc_get_linux_bridges_list(**kwargs):
        return get_execute(func_name(), "bridge list", **kwargs)

    @staticmethod
    def grpc_get_linux_bridges_all(**kwargs):
        return get_execute(func_name(), "bridge all", **kwargs)

    @staticmethod
    def grpc_get_linux_bridge_details(**kwargs):
        return get_execute(func_name(), f"bridge details {kwargs['body']['str_param1']}", **kwargs)

    @staticmethod
    def grpc_get_dpdk_devices(**kwargs):
        return get_execute(func_name(), "dpdk devices", **kwargs)

    @staticmethod
    def grpc_get_sriov_totalvfs(**kwargs):
        return get_execute(func_name(), f"sriov total_vfs {kwargs['body']['str_param1']}", **kwargs)

    @staticmethod
    def grpc_get_sriov_numvfs(**kwargs):
        return get_execute(func_name(), f"sriov num_vfs {kwargs['body']['str_param1']}", **kwargs)

    # device driver
    @staticmethod
    def grpc_modify_dpdk_bind(**kwargs):
        return modify_execute(func_name(), f"dpdk bind {kwargs['body']['str_param1']} {kwargs['body']['str_param2']}", **kwargs)

    @staticmethod
    def grpc_modify_dpdk_unbind(**kwargs):
        return modify_execute(func_name(), f"dpdk unbind {kwargs['body']['str_param1']}", **kwargs)

    @staticmethod
    def grpc_modify_dpdk_enable(**kwargs):
        return modify_execute(func_name(), f"dpdk enable {kwargs['body']['str_param1']}", **kwargs)

    # bridge port br
    @staticmethod
    def grpc_modify_ovs_add_dpdk_port(**kwargs):
        return modify_execute(func_name(), f"ovs add_dpdk_port {kwargs['body']['str_param1']} {kwargs['body']['str_param2']}"
                              f"{kwargs['body']['str_param3']}")


# ==================== private functions ===============================

def func_name():
    return sys._getframe().f_back.f_code.co_name


def json_str(message):
    return json.dumps(message, indent=4)


def get_message(func, info):
    message = {
        'status': f'Get request for {func.__name__} finished',
        'return': f'{info}'
    }
    return json_str(message)


def modify_message(func, status, info, var=True):
    message = {
        'function': f'<{func.__name__}>',
        'status': f'{status}'
    }
    if var:
        message['return'] = f'{info}'

    return json_str(message)

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


def get_execute(name, input_string, **kwargs):
    controller = interpret_params(input_string, **kwargs)
    response = data_client.run('get', **controller)


def modify_execute(name, input_string, **kwargs):
    controller = interpret_params(input_string, **kwargs)
    response = data_client.run('modify', **controller)
    message = {
        'function': f'{name}',
        'status': f'{response.status}',
        'info':
    }


def main():
    kwargs = {'body': {'str_param1': 'b7:00.3', 'str_param2': 'i40e'}}
    tmp = gRPCDataCollector()
    # print(tmp.grpc_get_linux_bridge_details(**kwargs))
    print(tmp.grpc_get_linux_bridges_all(**kwargs))


if __name__ == '__main__':
    main()
