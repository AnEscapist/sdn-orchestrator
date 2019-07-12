from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

grpc_routes = Blueprint('grpc', __name__, template_folder='templates')

@grpc_routes.route('/data-collect', defaults={'page': 'home'})
@grpc_routes.route('/data-collect/dashboard')
def get_cpucount():
    # messagedata = {"body": {"id": 5}}
    messagedata = {"method": "grpc_get_totalcpus",
                   "params": {"body": {"hostname": "10.10.81.100", "port": "50051", "command": "cpu",
                                       "str_request": "total"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(call_ucpe_function(messagedata))


def hello():
    return jsonify(name='zhengqi')
