from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

bcm_routes = Blueprint('bcm', __name__, template_folder='templates')


@bcm_routes.route('/show_pvlans/')
def show_pvlans():
    messagedata = {"method": "bcm_controller_show_pvlans", "params": {
        "body": {"hostname": "10.10.81.250", "port": "50051"}},
                   "jsonrpc": "2.0", "id": 0
                   }
    return jsonify(call_ucpe_function(messagedata))


@bcm_routes.route('/create_vlan/<vlanid>')
def create_vlan(vlanid):
    messagedata = {"method": "bcm_controller_create_vlan", "params": {
        "body": {"hostname": "10.10.81.250", "port": "50051",
                 "vlanid": int(vlanid)}},
                   "jsonrpc": "2.0", "id": 0
                   }
    return jsonify(call_ucpe_function(messagedata))


@bcm_routes.route('/show_active_ports/')
def show_active_ports():
    messagedata = {"method": "bcm_controller_show_active_ports", "params": {
        "body": {"hostname": "10.10.81.250", "port": "50051"}},
                   "jsonrpc": "2.0", "id": 0
                   }
    return jsonify(call_ucpe_function(messagedata))


@bcm_routes.route('/show_vlans/')
def show_vlans():
    messagedata = {"method": "bcm_controller_show_vlans", "params": {
        "body": {"hostname": "10.10.81.250", "port": "50051"}},
                   "jsonrpc": "2.0", "id": 0
                   }
    return jsonify(call_ucpe_function(messagedata))
