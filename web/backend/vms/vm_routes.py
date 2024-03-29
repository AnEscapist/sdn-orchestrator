from flask import Blueprint, request, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function
import os
import math
import time
import subprocess
from multiprocessing import Process
from threading import Thread
import pexpect
from pexpect import popen_spawn
from web.backend.grpc.grpc_routes import ovs_add_port_helper, ovs_del_port_helper
#from ucpe.libvirt_controller.utils import ovs_interface_names_from_vm_name

vm_routes = Blueprint('vms', __name__)

METHOD_PREFIX = 'libvirt_controller_'
HOST_IP = '10.10.81.100'  # todo: ask tyler for the bridge ip
HOST_USERNAME = 'potato'  # todo: remove the need for this (ask if one account per ucpe)
JSON_RPC_VERSION = '2.0'
JSON_RPC_ID = 0  # todo: ask tyler what id to put

IMAGE_ACTIVE_PATH = '/var/third-party/active'
# todo: put these in a database
# IMAGE_FILES = {
#     'Vyatta Router': 'vyatta.qcow2',
#     'Ubuntu 16.04': 'ubuntu_16.qcow2',
#     'Cloud Storage': 'storage.qcow2',
#     'Online Behavior Management': 'monitor.qcow2'
# }

IMAGE_FILE_INFO = {
    'Vyatta Router': {'name': 'Vyatta Router', 'filename': 'vyatta.qcow2', 'filesize': '0.4 GB', 'class': 'Router',
                      'description': 'Vyatta has a competitive set of advanced routing and security features. The major features include: IPv4 IPv6 routing with RIPv2, OSPFv3, and BGP4 dynamic routing protocols; DHCP server/client; 802.1Q VLANs; WAN support with DSL, T1/E1 and T3 cards, LAN connectivity support to 10GbE, WAN link load balancing, VoIP QoS, stateful inspection firewall, site-to-site IPsec VPN, SSL VPN, Intrusion Prevention, Web Filtering, NAT, RADIUS and TACACS+ authentication, VMware and Xen Optimization, VRRP, SNMP, Familiar CLI and web GUI management, Remote Access API for management and configuration, and more. ',
                      'os': 'VyOS'},
    # http://www.zycko.com/download/187.pdf
    'Ubuntu 16.04': {'name': 'Ubuntu 16.04', 'filename': 'ubuntu_16.qcow2', 'filesize': '1.7 GB', 'class': 'Generic',
                     'description': 'A free and open-source Linux distribution based on Debian.',
                     'os': 'Ubuntu 16.04'
                     },
    'Cloud Storage': {'name': 'Cloud Storage', 'filename': 'storage.qcow2', 'filesize': '8.9 GB', 'class': 'Storage',
                     'description': 'An AT&T open-source VNF for deduplicated cloud storage.',
                     'os': 'Ubuntu 18.04'},
    'Online Behavior Management': {'name': 'Online Behavior Management', 'filename': 'monitor.qcow2', 'filesize': '1.4 GB', 'class': 'Monitor',
                     'description': 'An AT&T open-source VNF for traffic monitoring and deep packet inspection (DPI)-based traffic control.',
                     'os': 'Ubuntu 18.04'
                     }
}


def get_method(method_suffix):
    return METHOD_PREFIX + method_suffix


def get_message_data(method_suffix, body):
    return {"method": get_method(method_suffix), "params": {"body": body}, 'jsonrpc': JSON_RPC_VERSION,
            'id': JSON_RPC_ID}


@vm_routes.route('/all_vm_info/<controller_id>/<ucpe_sn>')
def all_vm_info(controller_id, ucpe_sn):
    method = 'get_all_vm_info'
    body = {"username": HOST_USERNAME, "hostname": HOST_IP}
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    rename_images(response)
    return jsonify(response)


def imagefile_dict(image_info_dictionary):
    filename_key = 'filename'
    return {image_info_dictionary[key][filename_key]: key for key in image_info_dictionary}


def rename_images(response):
    reverse_image_dict = imagefile_dict(IMAGE_FILE_INFO)
    info_dict = response['result']['return']
    for vm_name in info_dict:
        image = info_dict[vm_name]['image'] + ".qcow2"
        if image in reverse_image_dict:
            info_dict[vm_name]['image'] = reverse_image_dict[image]


@vm_routes.route('/start_or_resume_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def start_or_resume_selected_vms(controller_id, ucpe_sn):
    method = 'start_or_resume_vms'
    return _handle_state_change(method, controller_id, ucpe_sn)


@vm_routes.route('/pause_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def pause_selected_vms(controller_id, ucpe_sn):
    method = 'suspend_vms'
    return _handle_state_change(method, controller_id, ucpe_sn)


@vm_routes.route('/kill_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def kill_selected_vms(controller_id, ucpe_sn):
    method = 'destroy_vms'
    return _handle_state_change(method, controller_id, ucpe_sn)


@vm_routes.route('/delete_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def delete_selected_vms(controller_id, ucpe_sn):
    method = 'delete_vms'
    ovs_interface_deletion_threads = []
    vms = request.get_json()['vm_names']
    for vm_name in vms:
        ovs_interface_deletion_threads.append(Thread(target=ovs_del_port_helper, args=(vm_name,)))
    for thread in ovs_interface_deletion_threads:
        thread.start()
    out = _handle_state_change(method, controller_id, ucpe_sn)
    for thread in ovs_interface_deletion_threads:
        thread.join()
    return out


def _handle_state_change(method, controller_id, ucpe_sn):
    data = request.get_json()
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, "vm_names": data["vm_names"]}
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)


@vm_routes.route('/create_vm/<controller_id>/<ucpe_sn>', methods=['POST'])
def create_vm(controller_id, ucpe_sn):
    # precondition: it must be possible to create a vm from the given parameters (sufficient memory, hugepage memory, etc)
    method = 'define_vm_from_params'
    data = request.get_json()
    # TODO: database for image paths
    form = data["form"]
    UNTAGGED_VLAN_INDICATOR = '0' #magic string - this is REALLLY bad - fix in grpc api
    vlans = [interface['vlan'] for interface in form['vmOVSInterfaceVLANs']]
    for i in range(len(vlans)):
        if vlans[i] == '':
            vlans[i] = UNTAGGED_VLAN_INDICATOR  # todo: change this to a map
    create_vm_ovs_interfaces(form['vmName'], int(form['vmOVSInterfaceCount']), vlans)
    image_file = IMAGE_FILE_INFO[form['vmImage']]['filename']
    image_path = os.path.join(IMAGE_ACTIVE_PATH, form['vmName'], image_file)
    body = {
        "username": HOST_USERNAME,
        "hostname": HOST_IP,
        "vm_name": form['vmName'],
        "vm_image_path": image_path,
        "vm_memory": parseMemoryGB(form['vmMemory']),
        "vm_vcpu_count": form['vmCPUs'],
        "vm_use_hugepages": form['hugepagesEnabled'],
        "vm_hugepage_memory": parseMemoryGB(form['vmHugepageMemory']),
        "vm_ovs_interface_count": int(form['vmOVSInterfaceCount']),
    }
    if form['vmBridge'] != 'No Bridge':
        body['vm_bridge_name'] = form['vmBridge']
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)


def create_vm_ovs_interfaces(vm_name, number_of_interfaces, vlans):
    interface_names = ovs_interface_names_from_vm_name(vm_name, number_of_interfaces)
    # create them by calling jesse's thing
    interface_type = 'dpdkvhostuser'
    threads = []
    for index, interface in enumerate(interface_names):
        # todo: this is really bad - interface_names must be in order eth0, eth1, ... (interface_names, vlans are 2 parallel arrays- bad pattern)
        # threads.append(Thread(ovs_add_port(interface, interface_type)))
        threads.append(
            Thread(target=ovs_add_port_helper, args=(interface, interface_type, vlans[index])))  # todo: change
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return


@vm_routes.route('/images/<controller_id>/<ucpe_sn>')
def get_vm_images(controller_id, ucpe_sn):
    return jsonify({"images": sorted(IMAGE_FILE_INFO.keys())})


@vm_routes.route('/image_info/<controller_id>/<ucpe_sn>')
def get_vm_image_info(controller_id, ucpe_sn):
    return jsonify(IMAGE_FILE_INFO)


global vnc_process
vnc_subprocess = None


@vm_routes.route('/console/<controller_id>/<ucpe_sn>/<vm_name>')
def prepare_vm_console(controller_id, ucpe_sn, vm_name):
    get_vnc_port_method = 'get_vm_vnc_port'
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, 'vm_name': vm_name}
    message_data = get_message_data(get_vnc_port_method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    print(response)
    ucpe_vnc_port = response['result']['return']

    # if vnc_process is not None:
    #     vnc_process.terminate()
    #     print("terminating")
    # todo: error handling
    # vnc_process = Process(target = prepare_vm_console_helper, args=(HOST_IP, vnc_port))
    # vnc_process.start()
    local_vnc_port = 6080
    kill_subprocess = pexpect.spawn(f'fuser -k {local_vnc_port}/tcp',
                                    timeout=None)  # timeout=None means wait indefinitely
    # kill_subprocess.expect(f'{local_vnc_port}/tcp')
    # kill_subprocess.expect(f'{local_vnc_port}')
    # print('before', kill_subprocess.before)
    # print('after', kill_subprocess.after)
    # print("starting sleep")
    time.sleep(3)  # todo: remove the need for this
    # print("ending sleep")
    # result = prepare_vm_console_helper(HOST_IP, vnc_port)
    prepare_vm_console_helper(HOST_IP, ucpe_vnc_port, local_vnc_port)
    return jsonify(result="attempted to start vnc console", warning="no error handling")  # todo: error handling


def prepare_vm_console_helper(hostname, ucpe_vnc_port, local_vnc_port):
    try:
        def launch_console():
            launch_script_path = '../../utilities/novnc/utils/launch.sh'
            vnc_subprocess = pexpect.spawn(f'{launch_script_path} --vnc {hostname}:{ucpe_vnc_port}',
                                           timeout=None)  # timeout=None means wait indefinitely
            vnc_subprocess.expect(f'{local_vnc_port}/vnc.html') # blocks until 6080/vnc.html appears in terminal todo: find appropriate string to expect
            vnc_subprocess.read() # blocks forever
        Thread(target=launch_console).start()
        return "success"
    except:
        return "failure"


def parseMemoryGB(memoryStr):
    return int(memoryStr.split(" ")[0])


# test
if __name__ == '__main__':
    # print(create_vm_ovs_interfaces('test_run', 1))
    # print(ovs_add_port('test_port_roger', 'dpdkvhostuser' ))
    print()
