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
    proc = subprocess.Popen(['sudo', '/sbin/modprobe', driver])
    return True


def dpdk_add_port(bridge, port_name, port):
    proc = subprocess.run(['sudo', 'ovs-vsctl', 'add-port', bridge, port_name, '--', 'set', 'Interface', port_name,
                           'type=dpdk', f'options:dpdk-devargs={port}'])
    return True

