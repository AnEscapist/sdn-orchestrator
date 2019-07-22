from flask import Blueprint, render_template, abort,jsonify, request
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

@docker_routes.route('/docker/list_containers')
def list_containers():
    messagedata = {"method": "docker_controller_list_containers", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/containers_status')
def containers_status():
    messagedata = {"method": "docker_controller_containers_status", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "all": "True", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/containers_images')
def containers_images():
    messagedata = {"method": "docker_controller_containers_images", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "all": "True", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/change_status')
def change_status():
    change_to = request.args.get('change_to')
    id_name = request.args.get('id_name')
    messagedata = {"method": "docker_controller_change_status", "params": {
        "body": {"change_to": change_to, 'id_name': id_name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/rename_container')
def rename_container():
    newName = request.args.get('newName')
    id_name = request.args.get('id_name')
    messagedata = {"method": "docker_controller_list_containers", "params": {
        "body": {"newName": newName, 'id_name': id_name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/list_images')
def list_images():
    messagedata = {"method": "docker_controller_list_images", "params": {
        "body": {}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/client_info')
def client_info():
    messagedata = {"method": "docker_controller_client_info", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/inspect_container')
def inspect_container():
    id_name = request.args.get('id_name')
    messagedata = {"method": "docker_controller_inspect_container", "params": {
        "body": {"id_name": id_name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/pull_image')
def pull_image():
    name = request.args.get('name')
    tag = request.args.get('tag')
    timeout = request.args.get('timeout')
    messagedata = {"method": "docker_controller_pull_image", "params": {
        "body": {"repo": name, "tag": tag, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata, TIMEOUT=timeout))
