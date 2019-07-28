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
    def grpc_get_hugepages_freemem_b(**kwargs):
        return get_execute(func_name(), "hugepages free_b", **kwargs)

    @staticmethod
    def grpc_get_totalmem(**kwargs):
        return get_execute(func_name(), "memory total", **kwargs)

    @staticmethod
    def grpc_get_availmem(**kwargs):
        return get_execute(func_name(), "memory available", **kwargs)

    @staticmethod
    def grpc_get_availmem_b(**kwargs):
        return get_execute(func_name(), "memory available_b", **kwargs)

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

    # bridge port type dev-address
    @staticmethod
    def grpc_modify_ovs_add_port(**kwargs):
        # print('hello2')
        return modify_execute(func_name(), f"ovs add_port {kwargs['body']['str_param1']} {kwargs['body']['str_param2']} "
                              f"{kwargs['body']['str_param3']} {kwargs['body']['str_param4']}", **kwargs)

    @staticmethod
    def grpc_modify_ovs_del_port(**kwargs):
        return modify_execute(func_name(), f"ovs del_port {kwargs['body']['str_param1']} "
                                           f"{kwargs['body']['str_param2']}", **kwargs)

    @staticmethod
    def grpc_modify_ovs_docker_add_port(**kwargs):
        if 'str_param5' not in kwargs['body']:
            kwargs['body']['str_param5'] = ''
        return modify_execute(func_name(), f"ovs_docker add_port {kwargs['body']['str_param1']} "
                                           f"{kwargs['body']['str_param2']} {kwargs['body']['str_param3']} "
                                           f"{kwargs['body']['str_param4']} {kwargs['body']['str_param5']}", **kwargs)

    @staticmethod
    def grpc_modify_ovs_docker_del_port(**kwargs):
        return modify_execute(func_name(), f"ovs_docker del_port {kwargs['body']['str_param1']} "
                                           f"{kwargs['body']['str_param2']}", **kwargs)


# ==================== private functions ===============================

def func_name():
    return sys._getframe().f_back.f_code.co_name


def interpret_params(input_string, **kwargs):
    # print(**kwargs)
    tmp = input_string.split(" ")
    count = len(tmp)
    # print(tmp)
    # kwargs['body'] = dict()
    kwargs['body']['command'] = tmp[0]
    kwargs['body']['str_request'] = tmp[1]
    if count > 2:
        kwargs['body']['str_param1'] = tmp[2]
        if count > 3:
            kwargs['body']['str_param2'] = tmp[3]
            if count > 4:
                kwargs['body']['str_param3'] = tmp[4]
                if count > 5:
                    kwargs['body']['str_param4'] = tmp[5]
                    if count > 6:
                        kwargs['body']['str_param5'] = tmp[6]
    # print(str(kwargs))
    return kwargs


def get_execute(name, input_string, **kwargs):
    controller = interpret_params(input_string, **kwargs)
    response = data_client.run('get', **controller)
    message = {
        'function': f'{name}',
        'status': f'{response.header}',
        'return': f'{response.str_response}'
    }
    return message


def modify_execute(name, input_string, **kwargs):
    controller = interpret_params(input_string, **kwargs)
    response = data_client.run('modify', **controller)
    message = {
        'function': f'{name}',
        'status': f'{response.status}',
        'return': f'{response.str_response}'
    }
    return message


def main():
    kwargs = {'body': {'str_param1': 'br0', 'str_param2': 'abcd', 'str_param3': 'dpdkvhostuser', 'str_param4': '6',
                       'str_param5': '10.10.81.155/24'}}
    tmp = gRPCDataCollector()
    # print(tmp.grpc_get_linux_bridge_details(**kwargs))
    print(tmp.grpc_modify_ovs_add_port(**kwargs))


if __name__ == '__main__':
    main()
