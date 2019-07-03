from concurrent import futures

import os
import sys
import subprocess

import netifaces

import psutil

import dpdk
import get_functions
from distutils import spawn


brctlexe = spawn.find_executable("brctl")
ipexe = spawn.find_executable("ip")


def dpdk_bind(device, driver, force=True):
    dev_id = dpdk.dev_id_from_dev_name(device)
    return dpdk.bind_one(dev_id, driver, force)


def dpdk_unbind(device, force=True):
    dev_id = dpdk.dev_id_from_dev_name(device)
    return dpdk.unbind_one(dev_id, force)


def dpdk_enable(driver):
    proc = subprocess.Popen(['sudo', '/sbin/modprobe', driver])
    return proc


def dpdk_add_port(bridge, port_name, port):
    proc = subprocess.Popen(['sudo', 'ovs-vsctl', 'add-port', bridge, port_name, '--', 'set', 'Interface', port_name,
                             'type=dpdk', f'options:dpdk-devargs={port}'])
    return proc

