from flask import Blueprint, render_template, abort,jsonify, request
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function
import os
import webbrowser
import socket

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

@docker_routes.route('/docker/containers_id')
def containers_id():
    messagedata = {"method": "docker_controller_containers_id", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/containers_status')
def containers_status():
    messagedata = {"method": "docker_controller_containers_status", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "all": "True", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/create_container')
def create_container():
    image_name = request.args.get('create_image')
    name = request.args.get('create_name')
    port = request.args.get('create_port')
    messagedata = {"method": "docker_controller_create_container", "params": {
        "body": {'image_name': image_name, 'name': name, 'ports': port, "username": "potato", "hostname": "10.10.81.100", "all": "True", "autostart": 1,
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

@docker_routes.route('/docker/kill_container')
def kill_container():
    id_name = request.args.get('id_name')
    messagedata = {"method": "docker_controller_kill_container", "params": {
        "body": {'id_name': id_name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/container_stats')
def container_stats():
    id_name = request.args.get('id_name')
    messagedata = {"method": "docker_controller_container_stats", "params": {
        "body": {'id_name': id_name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))


@docker_routes.route('/docker/remove_container')
def remove_container():
    id_name = request.args.get('id_name')
    messagedata = {"method": "docker_controller_remove_container", "params": {
        "body": {'id_name': id_name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))


# @docker_routes.route('/docker/rename_container')
# def rename_container():
#     newName = request.args.get('newName')
#     id_name = request.args.get('id_name')
#     messagedata = {"method": "docker_controller_rename_container", "params": {
#         "body": {"newName": newName, 'id_name': id_name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
#                  "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
#     return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/rename_container')
def rename_container():
    newName = request.args.get('newName')
    id_name = request.args.get('id_name')
    messagedata = {'method': 'docker_controller_rename_container', "params": {
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
    # registry = request.args.get('pull_registry')
    # timeout = request.args.get('timeout')
    messagedata = {"method": "docker_controller_pull_image", "params": {
        "body": {"repo": name, "tag": tag, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/images_info')
def image_info():
    name = request.args.get('name')
    messagedata = {"method": "docker_controller_images_info", "params": {
        "body": {"name": name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/inspect_image')
def inspect_image():
    name = request.args.get('name')
    messagedata = {"method": "docker_controller_inspect_image", "params": {
        "body": {"name": name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/remove_image')
def remove_image():
    name = request.args.get('name')
    messagedata = {"method": "docker_controller_remove_image", "params": {
        "body": {"name": name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

#===================docker volumes=================

@docker_routes.route('/docker/list_volumes')
def list_volumes():
    messagedata = {"method": "docker_controller_list_volumes", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/inspect_volume')
def inspect_volume():
    name = request.args.get('name')
    messagedata = {"method": "docker_controller_inspect_volume", "params": {
        "body": {"name": name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/remove_volume')
def remove_volume():
    name = request.args.get('name')
    messagedata = {"method": "docker_controller_remove_volume", "params": {
        "body": {"name": name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/create_volume')
def create_volume():
    name = request.args.get('name')
    messagedata = {"method": "docker_controller_create_volume", "params": {
        "body": {"name": name, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/console_container')
def console_container():
    container_id = request.args.get('container_id')

    # path = 'file:///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-consol/index.html'
    path = 'http://10.10.81.4:8080/console.html' #ip address of the server
    # webbrowser.open(path, new=1)
    # stop_port = 'sudo kill -9 $(sudo lsof -t -i:10000)'
    # code = os.system(stop_port)
    # print(code)
    webbrowser.open(path, new=1)
    cmd = 'sudo node ../docker-browser-console/server.js ' + container_id
    os.system(cmd)
    return f'{cmd}.'

@docker_routes.route('/docker/kill_port')
def kill_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',10000))
    # return str(result)
    if str(result) == '0':
        # return 'listening'
        # stop_port = 'sudo kill -9 $(sudo lsof -t -i:10000)'
        stop_port = 'sudo fuser -k 10000/tcp'
        os.system(stop_port)
        return 'port 10000 stopped!'
    else:
        # return 'not listening'

        return 'port 1000 not listening'
        # return '111' + str(result)
    # sock.close()
    # return 'port clear'


@docker_routes.route('/docker/check_port')
def check_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',10000))
    # return str(result)
    if str(result) == '0':
        return 'yes'
    else:
        return 'no'


#====================docker networks===================

@docker_routes.route('/docker/list_networks')
def list_networks():
    messagedata = {"method": "docker_controller_list_networks", "params": {
        "body": {"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}

    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/inspect_network')
def inspect_network():
    network_id = request.args.get('network_id')

    messagedata = {"method": "docker_controller_inspect_network", "params": {
        "body": {"network_id": network_id, "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    # return network_id
    return jsonify(call_ucpe_function(messagedata))

@docker_routes.route('/docker/create_network')
def create_network():
    network_name = request.args.get('create_name')
    driver = request.args.get('create_driver')
    scope = request.args.get('create_scope')
    subnet = request.args.get('create_subnet')
    gateway = request.args.get('create_gateway')
    enable_ipv6 = request.args.get('create_ipv6')
    messagedata = {"method": "docker_controller_create_network", "params": {
        "body": {"network_name": network_name, 'driver': driver, 'scope': scope,
                'subnet': subnet, 'gateway': gateway, 'enable_ipv6': enable_ipv6,
                "username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1,
                 "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
    return jsonify(call_ucpe_function(messagedata))
