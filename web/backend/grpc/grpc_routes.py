from flask import Blueprint, render_template, abort, jsonify
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