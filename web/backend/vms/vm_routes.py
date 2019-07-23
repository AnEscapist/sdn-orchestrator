from flask import Blueprint, request, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function
import os

vm_routes = Blueprint('vms', __name__)

METHOD_PREFIX = 'libvirt_controller_'
HOST_IP = '10.10.81.100'  # todo: ask tyler for the bridge ip
HOST_USERNAME = 'potato'  # todo: remove the need for this (ask if one account per ucpe)
JSON_RPC_VERSION = '2.0'
JSON_RPC_ID = 0  # todo: ask tyler what id to put

IMAGE_BASE_PATH = '/var/third-party/base'
# todo: put these in a database
IMAGE_FILES = {
    'Vyatta Router': 'vyatta.qcow2',
    'Ubuntu 16.04': 'ubuntu_16.qcow2',
    'AT&T Storage': 'blah1',
    'AT&T Monitor': 'blah2'
}

def get_method(method_suffix):
    return METHOD_PREFIX + method_suffix


def get_message_data(method_suffix, body):
    return {"method": get_method(method_suffix), "params": {"body": body}, 'jsonrpc': JSON_RPC_VERSION,
            'id': JSON_RPC_ID}


@vm_routes.route('/all_vm_info/<controller_id>/<ucpe_sn>')
def vm_info(controller_id, ucpe_sn):
    method = 'get_all_vm_info'
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, "vm_name": "test"}
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    print(type(response['result']['return']))
    return jsonify(response)


@vm_routes.route('/post', methods=['POST'])
def test_post():
    print(request.is_json)
    data = request.get_json()
    print("received post", data['vm_names'])
    return "good job\n"


# TODO: DRY up the below

@vm_routes.route('/start_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def start_selected_vms(controller_id, ucpe_sn):
    method = 'start_vms'
    data = request.get_json()
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, "vm_names": data["vm_names"]}
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)


@vm_routes.route('/start_or_resume_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def start_or_resume_selected_vms(controller_id, ucpe_sn):
    method = 'start_or_resume_vms'
    data = request.get_json()
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, "vm_names": data["vm_names"]}
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)


@vm_routes.route('/pause_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def pause_selected_vms(controller_id, ucpe_sn):
    method = 'suspend_vms'
    data = request.get_json()
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, "vm_names": data["vm_names"]}
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)


@vm_routes.route('/kill_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def kill_selected_vms(controller_id, ucpe_sn):
    method = 'destroy_vms'
    data = request.get_json()
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, "vm_names": data["vm_names"]}
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)


@vm_routes.route('/delete_selected_vms/<controller_id>/<ucpe_sn>', methods=['POST'])
def delete_selected_vms(controller_id, ucpe_sn):
    method = 'delete_vms'
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
    image_path = os.path.join(IMAGE_BASE_PATH, image_file)
    body = {
        "username": HOST_USERNAME,
        "hostname": HOST_IP,
        "vm_name": form['vmName'],
        "image_path": image_path,
        "vm_memory": form['vmMemory'],
        "vm_vcpu_count": form['vmCPUs'],
        "use_hugepages": form['hugepagesEnabled']
    }
    message_data = get_message_data(method, body)
    response = call_ucpe_function(message_data, controller_id, ucpe_sn)
    return jsonify(response)
