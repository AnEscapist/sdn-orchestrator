import docker
import json
import os
import paramiko
import requests
from inspect import signature, Parameter
from ucpe.docker_controller.docker_controller_message import *
from utilities.error import testError


class DockerController(object):
    def __init__(self, ip='10.10.81.100', port='2375', username='potato', password='potato'):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        # self.docker_client = docker.DockerClient(base_url=ip + ':' + port)
        # self.sftp = _open_sftp(ip=ip, username=username, password=password)
        # self.sftp = DockerController.docker_controller_open_sftp(self.ip, self.username, self.password)

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


# =====================================private functions======================#
def _create_client(low_level = False):
    ip = DockerController().ip
    port = DockerController().port
    if not low_level:
        return docker.DockerClient(base_url=ip + ':' + port)
    return docker.APIClient(base_url=ip + ':' + port)

def _open_sftp():
    ip = DockerController().ip
    username = DockerController().username
    password = DockerController().password
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        return ssh.open_sftp()
    except paramiko.ssh_exception.NoValidConnectionsError as para_no_valid_error:
        print('Connection Error:' + str(para_no_valid_error).split(']')[1])
    except paramiko.ssh_exception.SSHException as para_ssh_exception:
        print('SSH Exception: ' + str(para_ssh_exception))


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


# ===============================private functions end=======================================

#========================docker client===========================

dcli = _create_client(low_level=False)
api_cli = _create_client(low_level=True)
sftp = _open_sftp()


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



#===========================docker containers========================


def list_containers(all=True):
    func = DockerController.docker_controller_list_containers
    try:
        if all == True:
            container_list = dcli.containers.list(all=all)
        else:
            container_list = dcli.containers.list()
        return container_list_message(list=container_list, all=all, func=func)
    except OSError as ose:
        return ose_error(ose, func)


def list_images(name=None, all=True):
    func = DockerController.docker_controller_list_images
    try:
        image_list = dcli.images.list(name=name, all=all)
        return image_list_message(list=image_list, name=name, all=all, func=func)
    except OSError as ose:
        return ose_error(ose, func)


def containers_status(path='ContainerStatus.json', all=False, id_name=None):
    func = DockerController.docker_controller_containers_status
    status = {}
    try:
        container_list = dcli.containers.list(all=all)
    except OSError as ose:
        return ose_error(ose, func)

    if all:
        for container in container_list:
            status['container:' + container.name + '(id: ' + container.short_id + ')'] = container.status
    else:
        try:
            container = dcli.containers.get(id_name)
            status['container:' + container.name + '(id: ' + container.short_id + ')'] = container.status
        except docker.errors.NotFound:
            return cnf_error(id_name, func)
        # except docker.errors.NullResource as nre:
        #     print('Invalid input: ' + str(nre))
    json_str = json.dumps(status, indent=4)
    try:
        with open(path, 'w') as json_file:
            json_file.write(json_str)
    except FileNotFoundError:
        return fnf_error(path, func)

    return json_file_message(path, func)


def containers_info(path='ContainerInfo.json', all=True):
    func = DockerController.docker_controller_containers_info
    containerInfo = {}
    containerInfo['Containers'] = []

    try:
        if all == True:
            container_list = dcli.containers.list(all=all)
        else:
            container_list = dcli.containers.list()
    except OSError as ose:
        return ose_error(ose, func)
    if os.path.exists(path):
        os.remove(path)
    for i in range(len(container_list)):
        containerInfo['Containers'].append(container_list[i].attrs)

    json_str = json.dumps(containerInfo, indent=4)
    try:
        with open(path, 'a') as json_file:
            json_file.write(json_str)
    except FileNotFoundError:
        return fnf_error(path, func)
    return json_file_message(path, func)

def commit(id_name, repo=None, tag=None, message=None, author=None, changes=None):
    func = DockerController.docker_controller_commit
    try:
        container = dcli.containers.get(id_name)
    except docker.errors.NotFound:
        return cnf_error(id_name, func)
    container.commit(repository=repo, tag=tag, message=message, author=author, changes=changes)
    return commit_message(id_name, repo, tag, author, func)

def export_container(id_name, local_path, remote_path, local_save=False):
    func = DockerController.docker_controller_export_container
    try:
        remote_file = sftp.open(remote_path, 'wb')  # ============== IOError, no such file.
    except FileNotFoundError:
        remote_path = f'{DockerController().username}@{DockerController().ip}:{remote_path}'
        return fnf_error(remote_path, func)
    container = dcli.containers.get(id_name)
    generator = container.export()
    for chunck in generator:
        remote_file.write(chunck)
    remote_file.close()
    if local_save:
        os.system(f'rsync {DockerController().username}@{DockerController().ip}:{remote_path} {local_path}')
        return export_container_message(id_name, local_path, DockerController().username,
                                   DockerController().ip, remote_path, local_save, func)
        #sftp.get(remotePath, localPath)  # =============== IOError, no such file.
    # sftp.put('/tmp/test-container.tar', '/tmp/test-container.tar')

def create_container(image_name, detach=True):
    func = DockerController.docker_controller_create_container
    try:
        image = dcli.images.get(image_name)
        container = dcli.containers.run(image=image.id, detach=detach, stdin_open=True, tty=True)
    except requests.exceptions.HTTPError:
        return inf_erro(image_name, func)
    return create_container_message(container.id, image_name, func)

def change_status(id_name, change_to):
    func = DockerController.docker_controller_change_status

    # possible state: created, restarting, runing, paused, exited
    try:
        container = dcli.containers.get(id_name)
    except requests.exceptions.HTTPError:
        return cnf_error(id_name, func)
    curStatus = container.status
    if curStatus == change_to:
        return change_status_warning(id_name, curStatus, func)
    else:
        if change_to == 'running':
            container.start()
        elif change_to == 'exited':
            container.stop()
        elif change_to == 'paused':
                container.pause()
        elif change_to == 'restart':
            container.restart()
        else:
            return invalid_input_warning(input=change_to, func=func)
    return change_status_message(id_name, change_to, func)

def inspect_container(id_name):
    func = DockerController.docker_controller_inspect_container
    try:
        inspection = api_cli.inspect_container(id_name)
        '''
        for key in inspection['NetworkSettings'].keys():
            print(key)
        print(inspection['NetworkSettings']['IPAddress'])
        '''
        return inspect_container_message(id_name, inspection, func)
    except requests.exceptions.HTTPError:
        return cnf_error(id_name, func)
#======================docker container end============================


#======================docker images==========================

def list_images(name=None, all=True):
    func = DockerController.docker_controller_list_images
    try:
        image_list = dcli.images.list(name=name, all=all)
        return image_list_message(list=image_list, name=name, all=all, func=func)
    except OSError as ose:
        return ose_error(ose, func)


def images_info(path='ImagesInfo.json', name=None, all=True):
    func = DockerController.docker_controller_images_info
    imageInfo = {}
    imageInfo['Images'] = []

    try:
        image_list = dcli.images.list(name=name, all=all)
    except OSError as ose:
        return ose_error(ose, func)

    if os.path.exists(path):
        os.remove(path)
    for i in range(len(image_list)):
        imageInfo['Images'].append(image_list[i].attrs)

    json_str = json.dumps(imageInfo, indent=4)
    try:
        with open(path, 'a') as json_file:
            json_file.write(json_str)
    except FileNotFoundError:
        return fnf_error(path, func)
    return json_file_message(path, func)


def save_image(image_name, local_path, remote_path, local_save=False, chunk_size=2097152):
    func = DockerController.docker_controller_save_image
    try:
        remote_file = sftp.open(remote_path, 'wb')
    except FileNotFoundError:
        remote_path = f'{DockerController().username}@{DockerController().ip}:{remote_path}'
        return fnf_error(remote_path, func)
    image = dcli.images.get(image_name)
    generator = image.save(chunk_size=chunk_size, named=image.tags)
    for chunk in generator:
        remote_file.write(chunk)
    remote_file.close()
    if local_save:
        # sftp.get(remotePath, localPath)
        os.system(f'rsync {DockerController().username}@{DockerController().ip}:{remote_path} {local_path}')
        return save_image_message(image_name, local_path, DockerController().username,
                                  DockerController().ip, remote_path, local_save, func)

        # os.system('rsync potato@10.10.81.100:/tmp/remote-image.tar /tmp/local-image.tar')


def export_container(id_name, local_path, remote_path, local_save=False):
    func = DockerController.docker_controller_export_container
    try:
        remote_file = sftp.open(remote_path, 'wb')  # ============== IOError, no such file.
    except FileNotFoundError:
        remote_path = f'{DockerController().username}@{DockerController().ip}:{remote_path}'
        return fnf_error(remote_path, func)
    container = dcli.containers.get(id_name)
    generator = container.export()
    for chunck in generator:
        remote_file.write(chunck)
    remote_file.close()
    if local_save:
        os.system(f'rsync {DockerController().username}@{DockerController().ip}:{remote_path} {local_path}')
        return export_container_message(id_name, local_path, DockerController().username,
                                        DockerController().ip, remote_path, local_save, func)
        # sftp.get(remotePath, localPath)  # =============== IOError, no such file.
    # sftp.put('/tmp/test-container.tar', '/tmp/test-container.tar')


def create_image(remote_path):
    func = DockerController.docker_controller_create_image
    try:
        with sftp.open(remote_path, 'rb') as f:
            image = dcli.images.load(data=f)
            print(image)
            remote_path = f'{DockerController().username}@{DockerController().ip}:{remote_path}'
            return create_image_message(image[0].id, remote_path, func)
    except docker.errors.ImageLoadError:
        remote_path = f'{DockerController().username}@{DockerController().ip}:{remote_path}'
        return il_error(remote_path, func)
    except FileNotFoundError:
        return fnf_error(remote_path, func)


def pull_image(repo, tag=None):
    func = DockerController.docker_controller_pull_image
    try:
        dcli.images.pull(repository=repo, tag=tag)
        return pull_image_message(repo, tag, func)
    except requests.exceptions.HTTPError as re:
        return pull_error(re, func)


#=======================docker images end======================================