from concurrent import futures

import os
import sys
import json
import subprocess

from hurry.filesize import size as fsize
from hurry.filesize import alternative

import netifaces

import psutil

import ucpe.grpc_data_collector.dpdk as dpdk
from ucpe.grpc_data_collector.bridge import Bridge
from distutils import spawn

brctlexe = spawn.find_executable("brctl")
ipexe = spawn.find_executable("ip")

# PCI base class for NETWORK devices
NETWORK_BASE_CLASS = "02"
CRYPTO_BASE_CLASS = "0b"

# Definitions
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())

hugepagesize_in_b = meminfo['Hugepagesize'] * 1000
total_memory_in_b = meminfo['MemTotal'] * 1000
available_memory_in_b = meminfo['MemAvailable'] * 1000
hugepages_total = meminfo['HugePages_Total']
hugepages_free = meminfo['HugePages_Free']

total_cpus = psutil.cpu_count()
devices = dpdk.devices
drivers = dpdk.dpdk_drivers


def get_hugepages_totalmem():
    return fsize(hugepagesize_in_b * hugepages_total, system=alternative)


def get_hugepages_freemem():
    return fsize(hugepagesize_in_b * hugepages_free, system=alternative)


def get_total_mem():
    return fsize(total_memory_in_b, system=alternative)


def get_avail_mem():
    return fsize(available_memory_in_b, system=alternative)


def get_total_cpus():
    return total_cpus


def get_network_interfaces():
    return netifaces.interfaces()


def dpdk_get_devices():
    global devices
    dpdk.status_flag = True
    dpdk.status_dev = "all"
    with open(os.devnull, 'w') as devnull:
        ret = subprocess.call(['which', 'lspci'],
                              stdout=devnull, stderr=devnull)
        if ret != 0:
            print("'lspci' not found - please install 'pciutils'")
            sys.exit(1)

    dpdk.check_modules()
    dpdk.clear_data()
    dpdk.get_device_details(dpdk.network_devices)

    # tmp = devices

    device_list = dict()
    for d in devices.keys():

        device_dict = dict()
        dd = devices[d]

        device_dict['slot'] = dd["Slot"]
        device_dict['device_name'] = dd["Device_str"]
        device_dict['interface'] = dd["Interface"]
        device_dict['current_driver'] = dd["Driver_str"]
        device_dict['drivers'] = list()
        device_dict['drivers'].append(dd["Driver_str"])
        for i in dd["Module_str"].split(','):
            device_dict['drivers'].append(i)
        if dd["Driver_str"] in drivers:
            device_dict['driver_type'] = 'DPDK'
        else:
            device_dict['driver_type'] = 'Kernel'

        device_list[dd["Slot"]] = device_dict

    tmp = device_list

    return tmp


def get_linux_bridges_list():
    """ Return a list of unsorted bridge details. """
    p = subprocess.Popen([brctlexe, 'show'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    wlist = map(str.split, p.stdout.read().decode("utf-8").splitlines()[1:])
    brwlist = filter(lambda x: len(x) != 1, wlist)
    brlist = map(lambda x: x[0], brwlist)
    q = map(Bridge, brlist)
    # for qq in q:
    #     print(qq)
    return q


def print_linux_bridges_list():
    bridge_list = []
    q = get_linux_bridges_list()
    for qq in q:
        # print(qq)
        bridge_list.append(str(qq))
    return bridge_list


def brctl_show(self):
    """ Return a list of unsorted bridge details. """
    p = subprocess.Popen([brctlexe, 'show', self], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout.read().decode('utf-8').split()[7:]


def get_linux_bridge_id(br):
    return brctl_show(br)[1].strip()


def get_interfaces(br):
    list1 = []
    for i in brctl_show(br)[3:]:
        list1.append(i.strip())
    return list1


def get_stp(br):
    return brctl_show(br)[2].strip()


def get_linux_bridges_all():
    names = print_linux_bridges_list()
    bridge_list = []

    for name in names:
        bridge_dict = dict()
        bridge_dict['bridge_name'] = name
        bridge_dict['bridge_id'] = get_linux_bridge_id(name)
        bridge_dict['stp_enabled'] = get_stp(name)
        bridge_dict['interfaces'] = get_interfaces(name)
        bridge_list.append(bridge_dict)

    return bridge_list


def get_linux_bridge_details(br):
    my_list = get_linux_bridges_all()
    # print(my_list)
    for item in my_list:
        print(item['bridge_name'])
        if item['bridge_name'] == br:
            return item


def sriov_totalvfs(device):
    dpdk.get_device_details(dpdk.network_devices)
    dev_id = dpdk.dev_id_from_dev_name(device)
    value = subprocess.Popen(['cat', f'/sys/bus/pci/devices/{dev_id}/sriov_totalvfs'], stdout=subprocess.PIPE)
    # print(value)
    return value.stdout.read().decode('utf-8').strip()


def sriov_numvfs(device):
    dpdk.get_device_details(dpdk.network_devices)
    dev_id = dpdk.dev_id_from_dev_name(device)
    value = subprocess.Popen(['cat', f'/sys/bus/pci/devices/{dev_id}/sriov_numvfs'], stdout=subprocess.PIPE)
    # print(value)
    return value.stdout.read().decode('utf-8').strip()
