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


@grpc_routes.route('/grpc/avail_mem_bytes')
def avail_mem_bytes():
    messagedata = {"method": "grpc_get_availmem_b", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/hugepage_total_mem')
def hugepage_total_mem():
    messagedata = {"method": "grpc_get_hugepages_totalmem", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/hugepage_free_mem')
def hugepage_free_mem():
    messagedata = {"method": "grpc_get_hugepages_freemem", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/hugepage_free_mem_bytes')
def hugepage_free_mem_bytes():
    messagedata = {"method": "grpc_get_hugepages_freemem_b", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/cpu_total')
def cpu_total():
    messagedata = {"method": "grpc_get_totalcpus", "params": {
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


@grpc_routes.route('/grpc/linux_bridge_list')
def linux_bridge_list():
    messagedata = {"method": "grpc_get_linux_bridges_list", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051"}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))

# method for Roger, not same syntax as Zhengqi
@grpc_routes.route('/grpc/ovs_add_port/<if_port>/<type>')
def ovs_add_port(if_port, type):
    bridge = 'br0'
    messagedata = {"method": "grpc_modify_ovs_add_port", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051", "str_param1": bridge, "str_param2": if_port,
                 "str_param3": type}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))

#method for Roger too
@grpc_routes.route('/grpc/ovs_del_port/<vm_name>')
def ovs_del_port(vm_name):
    bridge = 'br0'
    container = request.args.get('container')
    messagedata = {"method": "grpc_modify_ovs_del_port", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051", "str_param1": f'{bridge}', "str_param2": f'{vm_name}'}},
        "jsonrpc": "2.0", "id": 0
    }
    # return jsonify(call_ucpe_function(messagedata))
    p = call_ucpe_function(messagedata)
    return jsonify(p)


@grpc_routes.route('/grpc/ovs_docker_add_port')
def ovs_docker_add_port():
    bridge = 'br0'
    interface = request.args.get('ovs_int')
    # print(interface)
    container = request.args.get('create_name')
    # print(container)
    port = request.args.get('int_port')
    # print(port)
    ipaddress = request.args.get('int_ip')
    # print(ipaddress)
    messagedata = {"method": "grpc_modify_ovs_docker_add_port", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051", "str_param1": f'{bridge}', "str_param2": f'{interface}',
                 "str_param3": f'{container}', "str_param4": f'{port}', "str_param5": f'{ipaddress}'}},
        "jsonrpc": "2.0", "id": 0
    }
    return jsonify(call_ucpe_function(messagedata))


@grpc_routes.route('/grpc/ovs_docker_del_port')
def ovs_docker_del_port():
    bridge = 'br0'
    container = request.args.get('container')
    messagedata = {"method": "grpc_modify_ovs_docker_del_port", "params": {
        "body": {"hostname": "10.10.81.100", "port": "50051", "str_param1": f'{bridge}', "str_param2": f'{container}'}},
        "jsonrpc": "2.0", "id": 0
    }
    # return jsonify(call_ucpe_function(messagedata))
    p = call_ucpe_function(messagedata)
    return jsonify(p)


def main():
    # proc = ovs_add_port("abcd", "dpdkvhostuser")
    proc = cpu_total()
    return str(proc)


if __name__ == "__main__":
    main()
