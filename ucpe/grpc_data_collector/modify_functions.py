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


def dpdk_bind(device, driver, force=False):
    dev_id = dpdk.dev_id_from_dev_name(device)
    dpdk.bind_one(dev_id, driver, force)
    return True


def dpdk_unbind(device, force=False):
    dev_id = dpdk.dev_id_from_dev_name(device)
    dpdk.unbind_one(dev_id, force)
    return True


def dpdk_enable(driver):
    subprocess.run(['sudo', '/sbin/modprobe', driver])
    return True


def ovs_add_port(bridge, if_port, type, vlan):
    subprocess.run(['sudo', 'ovs-vsctl', 'add-port', bridge, if_port, f'tag={vlan}', '--', 'set', 'Interface', if_port,
                    f'type={type}'])
    ovs_socket = f'/usr/local/var/run/openvswitch/{if_port}'
    subprocess.run(['sudo', 'chmod', '777', ovs_socket])
    return True


def ovs_del_port(bridge, vm):
    vm1 = f'vm_{vm}'
    for i in get_functions.ovs_list_ports(bridge):
        if i.rsplit('_', 1)[0] == vm1:
            subprocess.run(['sudo', 'ovs-vsctl', 'del-port', bridge, i])
    return True


def ovs_docker_add_port(bridge, interface, container, port, ipaddress):
    # bridge1 = 'br0'
    bridge1 = bridge

    tmp_var = get_functions.ovs_list_ports_number(bridge1)
    tmp_int = int(port)
    # print(tmp_int)
    while port in tmp_var:
        tmp_int = tmp_int + 1
    tmp_num = str(tmp_int)
    # print(tmp_num)
    ovsdocker_list = ['sudo', '/usr/local/bin/ovs-docker', 'add-port', bridge1, interface, container, tmp_num]
    if ipaddress != '':
        ovsdocker_list.append(f"--ipaddress={ipaddress}")
    subprocess.run(ovsdocker_list)
    return [True, tmp_int]


def ovs_docker_del_port(bridge, container):
    for i in get_functions.ovs_list_ports(bridge):
        if i.rsplit('_', 1)[0] == container:
            subprocess.run(['sudo', 'ovs-docker', 'del-ports', bridge, i])
            subprocess.run(['sudo', 'ovs-vsctl', 'del-port', bridge, i])
    return True


def sriov_createvfs(device, number_str):
    number = int(number_str)
    total = int(get_functions.sriov_totalvfs(device))
    current = int(get_functions.sriov_numvfs(device))
    value = str(number+current)
    if number + current >= total:
        value = get_functions.sriov_totalvfs(device)
    subprocess.run(['echo', f'\"{value}\"', '>', f'/sys/bus/pci/devices/{device}/sriov_numvfs'])


def sriov_vf_vlan():
    return None