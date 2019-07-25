from flask import Blueprint, request, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function
import os
import time
import subprocess
from multiprocessing import Process
from threading import Thread

vm_routes = Blueprint('vms', __name__)

METHOD_PREFIX = 'libvirt_controller_'
HOST_IP = '10.10.81.100'  # todo: ask tyler for the bridge ip
HOST_USERNAME = 'potato'  # todo: remove the need for this (ask if one account per ucpe)
JSON_RPC_VERSION = '2.0'
JSON_RPC_ID = 0  # todo: ask tyler what id to put

IMAGE_ACTIVE_PATH = '/var/third-party/active'
# todo: put these in a database
IMAGE_FILES = {
    'Vyatta Router': 'vyatta.qcow2',
    'Ubuntu 16.04': 'ubuntu_16.qcow2',
    'AT&T Storage': 'storage.qcow2',
    'AT&T Monitor': 'monitor.qcow2'
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
    return jsonify(response)

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
    return _handle_state_change(method, controller_id, ucpe_sn)

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
    image_file = IMAGE_FILES[form['vmImage']]
    image_path = os.path.join(IMAGE_ACTIVE_PATH, form['vmName'], image_file)
    body = {
        "username": HOST_USERNAME,
        "hostname": HOST_IP,
        "vm_name": form['vmName'],
        "vm_image_path": image_path,
        "vm_memory": parseMemoryGB(form['vmMemory']),
        "vm_vcpu_count": form['vmCPUs'],
        "vm_use_hugepages": form['hugepagesEnabled'],
        "vm_hugepage_memory": parseMemoryGB(form['vmHugepageMemory'])
    }
    if form['vmAddBridgeInterface']:
        body['vm_bridge_name'] = form['vmBridge']
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)

@vm_routes.route('/images/<controller_id>/<ucpe_sn>')
def get_vm_images(controller_id, ucpe_sn):
    return jsonify({"images": sorted(IMAGE_FILES.keys())})

global vnc_process
vnc_subprocess = None

@vm_routes.route('/console/<controller_id>/<ucpe_sn>/<vm_name>')
def prepare_vm_console(controller_id, ucpe_sn, vm_name):
    get_vnc_port_method = 'get_vm_vnc_port'
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, 'vm_name': vm_name}
    message_data = get_message_data(get_vnc_port_method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    print(response)
    vnc_port = response['result']['return']

    # if vnc_process is not None:
    #     vnc_process.terminate()
    #     print("terminating")
    #todo: error handling
    # vnc_process = Process(target = prepare_vm_console_helper, args=(HOST_IP, vnc_port))
    # vnc_process.start()
    local_vnc_port = 6080
    subprocess.Popen(f'exec fuser -k {local_vnc_port}/tcp', shell=True)
    print("starting sleep")
    time.sleep(3)
    print("ending sleep")
    # result = prepare_vm_console_helper(HOST_IP, vnc_port)
    console_thread = Thread(target=prepare_vm_console_helper, args=(HOST_IP, vnc_port))
    console_thread.start()
    return jsonify(result="attempted to start vnc console", warning="no error handling") # todo: error handling

def prepare_vm_console_helper(hostname, port):
    # global vnc_subprocess
    # if vnc_subprocess is not None:
    #     print("terminating")
    try:
        launch_script_path = '/home/attadmin/projects/sdn-orchestrator/utilities/novnc/utils/launch.sh'
        vnc_subprocess = subprocess.Popen(f'exec {launch_script_path} --vnc {hostname}:{port}', shell=True)
        print('in the process', vnc_subprocess.args)
        vnc_subprocess.communicate()
        return "success"
    except:
        return "failure"

def parseMemoryGB(memoryStr):
    return int(memoryStr.split(" ")[0])

