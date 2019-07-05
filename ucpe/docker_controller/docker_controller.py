import docker
import json
import os
import paramiko
import requests
from inspect import signature, Parameter
from ucpe.docker_controller.docker_controller_container import *
from ucpe.docker_controller.docker_controller_volume import *
from ucpe.docker_controller.docker_controller_message import *

from ucpe.docker_controller.docker_global import *

class DockerController(object):
    def __init__(self, ip='10.10.81.100', port = '2375', username='potato', password='potato'):
        self.ip = ip
        self.port = port
        self.username=username
        self.password = password
        #self.docker_client = docker.DockerClient(base_url=ip + ':' + port)
        #self.sftp = _open_sftp(ip=ip, username=username, password=password)
        #self.sftp = DockerController.docker_controller_open_sftp(self.ip, self.username, self.password)

        '''
        @staticmethod
        def docker_controller_open_sftp(**kwargs):
            func = open_sftp
            return _call_function(func, **kwargs)
            '''


        @staticmethod
        def docker_controller_client_info(**kwargs):
            func = client_info
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_list_containers(**kwargs):
            func = list_containers
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_list_images(**kwargs):
            func = list_images
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_containers_status(**kwargs):
            func = containers_status
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_containers_info(**kwargs):
            func = containers_info
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_images_info(**kwargs):
            func = images_info
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_commit(**kwargs):
            func = commit
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_save_image(**kwargs):
            func = save_image
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_export_container(**kwargs):
            func = export_container
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_create_image(**kwargs):
            func = create_image
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_pull_image(**kwargs):
            func = pull_image
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_create_container(**kwargs):
            func = create_container
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_change_status(**kwargs):
            func = change_status
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_inspect_container(**kwargs):
            func = inspect_container
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_create_network(**kwargs):
            func = create_network
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_connect_container(**kwargs):
            func = connect_container
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_disconnect_container(**kwargs):
            func = disconnect_container
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_remove_network(**kwargs):
            func = remove_network
            return _call_function(func, **kwargs)

        @staticmethod
        def docker_controller_create_volume(**kwargs):
            func = create_volume
            return _call_function(func, **kwargs)

# =====================================private functions======================#




def _call_function(func, **kwargs):
    body = kwargs['body']
    params = signature(func).parameters
    relevent_kwargs = {}
    for param in params:
        if params[param].default == Parameter.empty:
            try:
                relevent_kwargs[param] = body[param]
            except KeyError:
                raise KeyError('missing argument' + param + 'in call to ' + func.__name__)
        else:
            relevent_kwargs[param] = body.get(param, params[param].default)
    return func(**relevent_kwargs)

#===============================private functions end=======================================

#========================docker client===========================
'''
dcli = _create_client(low_level=False)
api_cli = _create_client(low_level=True)
'''


def client_info(path='ClientInfo.json'):
    func = DockerController.docker_controller_client_info
    try:
        info = dcli.info()
    except OSError as ose:
        return ose_error(ose, func)
    json_str = json.dumps(info, indent=4)
    try:
        with open(path, 'w') as json_file:
            json_file.write(json_str)
            return json_file_message(path, func)
    except FileNotFoundError:
        return fnf_error(path, func)
#===========================docker client end=========================




