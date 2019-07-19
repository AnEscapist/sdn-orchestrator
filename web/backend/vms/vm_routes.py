from flask import Blueprint, render_template, abort,jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

vm_routes = Blueprint('vms', __name__)

METHOD_PREFIX = 'libvirt_controller_'
HOST_IP = '10.10.81.100' #todo: ask tyler for the bridge ip
HOST_USERNAME = 'potato' #todo: remove the need for this (ask if one account per ucpe)
JSON_RPC_VERSION = '2.0'
JSON_RPC_ID = 0 #todo: ask tyler what id to put

def get_method(method_suffix):
    return METHOD_PREFIX + method_suffix

def get_message_data(method_suffix, body):
    return {"method": get_method(method_suffix), "params" : {"body": body}, 'jsonrpc': JSON_RPC_VERSION, 'id': JSON_RPC_ID}

@vm_routes.route('/all_vm_info/<controller_id>/<ucpe_sn>')
def vm_info(controller_id, ucpe_sn):
    method = 'get_all_vm_info'
    body = {"username": HOST_USERNAME, "hostname": HOST_IP, "vm_name": "test"}
    message_data = get_message_data(method, body)
    return jsonify(call_ucpe_function(message_data, controller_id, ucpe_sn))
