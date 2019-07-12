from flask import Blueprint, render_template, abort,jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

docker_routes = Blueprint('docker_page', __name__, template_folder='templates')

#example route
# @app.route('/docker/abcde', methods=['POST', 'GET'])
# def get_containers():
#     # messagedata = {"body": {"id": 5}}
#     messagedata = {"method": "libvirt_controller_get_vm_state", "params": {
#         "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
#                  "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
#
#     #return jsonify(name='ucpe', email='alkjdflk@gmail.com')
#     return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/abcde')
def get_containers():
    # messagedata = {"body": {"id": 5}}
    messagedata = {"method": "docker_controller_list_containers", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(name='ucpe', email='alkjdflk@gmail.com')
    # return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/hello')
def hello():
    return jsonify(name='docker docker')
