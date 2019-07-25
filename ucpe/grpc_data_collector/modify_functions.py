from concurrent import futures

import os
import sys
import subprocess

import netifaces

import psutil

import ucpe.grpc_data_collector.dpdk as dpdk
from ucpe.grpc_data_collector.bridge import Bridge
import ucpe.grpc_data_collector.get_functions as get_functions
from distutils import spawn


brctlexe = spawn.find_executable("brctl")
ipexe = spawn.find_executable("ip")

devices = dpdk.devices
dpdk.get_device_details(dpdk.network_devices)


def dpdk_bind(device, driver, force=True):
    dev_id = dpdk.dev_id_from_dev_name(device)
    dpdk.bind_one(dev_id, driver, force)
    return True


def dpdk_unbind(device, force=True):
    dev_id = dpdk.dev_id_from_dev_name(device)
    dpdk.unbind_one(dev_id, force)
    return True


def dpdk_enable(driver):
    subprocess.run(['sudo', '/sbin/modprobe', driver])
    return True


def ovs_add_dpdk_port(bridge, port_name, port):
    subprocess.run(['sudo', 'ovs-vsctl', 'add-port', bridge, port_name, '--', 'set', 'Interface', port_name,
                    'type=dpdk', f'options:dpdk-devargs={port}'])
    return True


def ovs_docker_add_port(bridge, interface, container, port, ipaddress):
    # bridge1 = 'br0'
    bridge1 = bridge
    tmp_name = f'{container}-{interface}'
    tmp_var = get_functions.ovs_list_ports_number(bridge1)
    tmp_int = int(port)
    print(tmp_int)
    while port in tmp_var:
        tmp_int = tmp_int + 1
    tmp_num = str(tmp_int)
    print(tmp_num)
    ovsdocker_list = ['sudo', '/usr/local/bin/ovs-docker', 'add-port', bridge1, tmp_name, container, tmp_num]
    if ipaddress != '':
        ovsdocker_list.append(f"--ipaddress={ipaddress}")
    subprocess.run(ovsdocker_list)
    return [True, tmp_int]
