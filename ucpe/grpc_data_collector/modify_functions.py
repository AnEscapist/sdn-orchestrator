from concurrent import futures

import os
import sys
import subprocess

import netifaces

import psutil

import ucpe.grpc_data_collector.dpdk as dpdk
import get_functions
from distutils import spawn


brctlexe = spawn.find_executable("brctl")
ipexe = spawn.find_executable("ip")


def dpdk_bind(device, driver, force=True):
    return dpdk.bind_one(device, driver, force)


def dpdk_unbind(device, force=True):
    return dpdk.unbind_one(device, force)


def dpdk_enable(driver):
    proc = subprocess.Popen(['sudo', '/sbin/modprobe', driver])
    return proc


def dpdk_add_port(bridge, port_name, port):
    proc = subprocess.run(['sudo', 'ovs-vsctl', 'add-port', bridge, port_name, '--', 'set', 'Interface', port_name,
                           'type=dpdk', f'options:dpdk-devargs={port}'])
    return proc

