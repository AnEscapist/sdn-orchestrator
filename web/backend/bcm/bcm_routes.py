from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

bcm_routes = Blueprint('bcm', __name__, template_folder='templates')


@bcm_routes.route('/show_vlans')
def show_vlans():
    messagedata = {"method": "bcm_controller_show_vlans", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))

