import docker
import os
import requests
from ucpe.docker_controller.docker_global import dcli, api_cli, sftp, ip, username
from ucpe.docker_controller.docker_controller_message import *

#=======================docker network===============================

def list_networks():
    func = list_networks
    name_list = []
    id_list = []
    try:
        network_list = dcli.networks.list()
    except docker.errors.APIError as ae:
        return api_error(ae, func)
    except OSError as ose:
        return ose_error(ose,func)

    for network in network_list:
        id_list.append(network.id)
        name_list.append(network.name)
    return network_list_message(list=name_list, id_list=id_list, func=func)


def create_network(network_name, driver='bridge', subnet=None, gateway=None, enable_ipv6=False):
    func = create_network
    try:
        if subnet and gateway:
            ipam_pool = docker.types.IPAMPool(
                subnet=subnet,
                gateway=gateway
            )
            ipam_config = docker.types.IPAMConfig(
                pool_configs=[ipam_pool]
            )
            network = dcli.networks.create(name=network_name, driver=driver,
                                           ipam=ipam_config, enable_ipv6=enable_ipv6)
        else:
            network = dcli.networks.create(name=network_name, driver=driver)
    except docker.errors.APIError as ae:
        return api_error(ae, func)
    return create_network_message(network.id, func)

def connect_container(id_name, network_id):
    func = connect_container
    try:
        container = dcli.containers.get(id_name)
        network = dcli.networks.get(network_id)
    except docker.errors.NotFound as nf:
        return nf_error(nf, func)
    except docker.errors.NullResource as nr:
    	return nr_error(nr, func)
    try:
        network.connect(container)
    except docker.errors.APIError as ae:
        return api_error(ae, func)
    return connect_container_message(id_name, network_id, func)

def disconnect_container(id_name, network_id, force=False):
    func = disconnect_container
    try:
        container = dcli.containers.get(id_name)
        network = dcli.networks.get(network_id)
    except docker.errors.NotFound as nf:
        return nf_error(nf, func)
    try:
        network.disconnect(container, force=force)
    except docker.errors.APIError as ae:
        return api_error(ae, func)
    return disconnect_container_message(id_name, network_id, func)


def remove_network(network_id):
    func = remove_network
    try:
        dcli.networks.get(network_id).remove()
    except docker.errors.NotFound as nf:
        return nf_error(nf, func)
    except docker.errors.APIError as ae:
        return api_error(ae, func)
    return remove_network_message(network_id, func)

#============================docker network end==========================
