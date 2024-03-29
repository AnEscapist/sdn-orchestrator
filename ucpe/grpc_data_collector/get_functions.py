from concurrent import futures

import os
import sys
import time
import datetime
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

total_cpus = psutil.cpu_count()
devices1 = dpdk.devices
drivers = dpdk.dpdk_drivers


def get_hugepages_totalmem():
    global meminfo
    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    hugepagesize_in_b = meminfo['Hugepagesize'] * 1000
    hugepages_total = meminfo['HugePages_Total']
    return fsize(hugepagesize_in_b * hugepages_total, system=alternative)


def get_hugepages_freemem():
    global meminfo
    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    hugepagesize_in_b = meminfo['Hugepagesize'] * 1000
    hugepages_free = meminfo['HugePages_Free']
    return fsize(hugepagesize_in_b * hugepages_free, system=alternative)


def get_hugepages_freemem_b():
    global meminfo
    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    hugepagesize_in_b = meminfo['Hugepagesize'] * 1000
    hugepages_free = meminfo['HugePages_Free']
    return str(hugepagesize_in_b * hugepages_free)


def get_total_mem():
    global meminfo
    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    total_memory_in_b = meminfo['MemTotal'] * 1000
    return fsize(total_memory_in_b, system=alternative)


def get_avail_mem():
    global meminfo
    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    available_memory_in_b = meminfo['MemAvailable'] * 1000
    return fsize(available_memory_in_b, system=alternative)


def get_avail_mem_b():
    global meminfo
    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    available_memory_in_b = meminfo['MemAvailable'] * 1000
    return str(available_memory_in_b)


def get_total_cpus():
    return total_cpus


def get_network_interfaces():
    return netifaces.interfaces()


def dpdk_get_devices():
    with open(os.devnull, 'w') as devnull:
        ret = subprocess.call(['which', 'lspci'],
                              stdout=devnull, stderr=devnull)
        if ret != 0:
            print("'lspci' not found - please install 'pciutils'")
            sys.exit(1)

    # devices1 = dpdk.devices

    dpdk.check_modules()
    dpdk.clear_data()
    dpdk.get_device_details(dpdk.network_devices)

    devices1 = dpdk.devices
    # tmp = devices

    device_list = dict()
    for d in devices1.keys():

        device_dict = dict()
        dd = devices1[d]

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

    return device_list


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


def ovs_list_ports(br):
    proc = subprocess.Popen(['ovs-vsctl', 'list-ports', br], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    var = proc.stdout.read().decode('utf-8').split()
    # print(var)
    return var


def ovs_list_ports_number(br):
    list1 = ovs_list_ports(br)
    tmp = list()
    for i in list1:
        proc = subprocess.Popen(['ovs-vsctl', 'get', 'Interface', i, 'ofport'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        tmp.append(proc.stdout.read().decode('utf-8').strip())
    # print(tmp)
    return tmp


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


def lshw_get_businfo():
    proc = subprocess.Popen(['sudo', 'lshw', '-c', 'network', '-businfo'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # time.sleep(2)
    list1 = list()
    i = 0
    for line in proc.stdout:
        if i < 2:
            i = i + 1
        else:
            tmp_dict = dict()
            val = line.decode('utf-8').split(None, 3)
            ident = val[0].strip().rsplit('@')[1]
            check1 = val[1].strip()
            check2 = val[2].strip()
            if ident not in dpdk_get_devices():
                val = line.decode('utf-8').split(None, 2)
                tmp_dict['bus_info'] = ''
                tmp_dict['device'] = val[0].strip()
                tmp_dict['class'] = val[1].strip()
                tmp_dict['description'] = val[2].strip()

            else:
                tmp_dict['bus_info'] = val[0].strip()
                if check1 == 'network' and (check2 == 'Ethernet' or check2 == 'I350'):
                    val = line.decode('utf-8').split(None, 2)
                    tmp_dict['device'] = ''
                    tmp_dict['class'] = val[1].strip()
                    tmp_dict['description'] = val[2].strip()
                else:
                    tmp_dict['device'] = val[1].strip()
                    tmp_dict['class'] = val[2].strip()
                    tmp_dict['description'] = val[3].strip()
            list1.append(tmp_dict)
    return str(list1)


def cpu_percent():
    return psutil.cpu_percent()


def mem_percent():
    p = dict(psutil.virtual_memory()._asdict())
    return_val = p['percent']
    return return_val


def collect_data(time_length):
    script_dir = os.path.dirname(__file__)
    fp = os.path.join(script_dir, 'json/host_collect.json')
    with open(fp, 'r') as json_file:
        data = json.load(json_file)
        for x in range(0, time_length):
            data['body'].append({
                'date': datetime.date.today(),
                'time': datetime.datetime.utcnow(),
                'cpu_usage': cpu_percent(),
                'mem_percent': mem_percent()
            })
            time.sleep(1)
    with open(fp, 'w') as outfile:
        json.dump(data, outfile)


def main():
    print(cpu_percent())
    print(mem_percent())


if __name__ == "__main__":
    main()
