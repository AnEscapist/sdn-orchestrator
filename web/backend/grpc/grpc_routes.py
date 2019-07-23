from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

grpc_routes = Blueprint('grpc', __name__, template_folder='templates')


@grpc_routes.route('/grpc/total_mem')
def total_mem():
    messagedata = {"method": "grpc_get_totalmem", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/avail_mem')
def avail_mem():
    messagedata = {"method": "grpc_get_availmem", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/hugepage_total_mem')
def hugepage_total_mem:
    messagedata = {"method": "grpc_get_hugepages_totalmem", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/hugepage_free_mem')
def hugepage_free_mem:
    messagedata = {"method": "grpc_get_hugepages_freemem", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/get_net_devices')
def get_net_devices():
    messagedata = {"method": "grpc_get_dpdk_devices", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/dpdk_bind')
def dpdk_bind():
    slot = request.args.get('slot')
    current_driver = request.args.get('current_driver')
    messagedata = {"method": "grpc_modify_dpdk_bind", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051", "str_param1": f'{slot}', "str_param2": f'{current_driver}'}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))
