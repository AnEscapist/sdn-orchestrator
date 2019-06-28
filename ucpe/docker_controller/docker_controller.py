import docker
import json
import os
import paramiko
import requests
from inspect import signature, Parameter
from ucpe.docker_controller.docker_controller_message import *
from utilities.Error import testError


class DockerController(object):
    def __init__(self, ip='10.10.81.100', port = '2375', username='potato', password='potato'):
        self.ip = ip
        self.port = port
        self.username=username
        self.password = password
        self.docker_client = docker.DockerClient(base_url=ip + ':' + port)
        self.sftp = _open_sftp(ip=ip, username=username, password=password)
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






def client_info(dcli, path='ClientInfo.json'):
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
        return fnf_erro(path, func)





def list_containers(dcli, all=True):
    func = DockerController.docker_controller_list_containers
    try:
        if all == True:
            container_list = dcli.containers.list(all=all)
        else:
            container_list = dcli.containers.list()
        return container_list_message(list=container_list, all=all, func=func)
    except OSError as ose:
        return ose_error(ose,func)

def list_images(dcli, image_name=None, all=True):
    func = DockerController.docker_controller_list_images
    try:
        image_list = dcli.images.list(name=image_name, all=all)
        return image_list_message(list=image_list, name=image_name, all=all, func=func)
    except OSError as ose:
        return ose_error(ose, func)

#=============================================TODO=================

def containers_status(dcli, path='ContainerStatus.json', all=False, id_name=None):
    status = {}
    try:
        container_list = dcli.containers.list(all=all)
    except OSError as ose:
        message = {
            'function': '<docker_controller_list_containers>',
            'fail message': f'No route to host: ' + str(ose).split('(')[1].split(')')[0]
        }
        return message

    if all:
        for container in container_list:
            status['container:' + container.name + '(id: ' + container.short_id + ')'] = container.status
    else:
        try:
            container = dcli.containers.get(id_name)
            status['container:' + container.name + '(id: ' + container.short_id + ')'] = container.status
        except docker.errors.NotFound as nfe:
            print('Container Not Found: ' + str(nfe)[29:-1])
        except docker.errors.NullResource as nre:
            print('Invalid input: ' + str(nre))
    json_str = json.dumps(status, indent=4)
    with open(path, 'w') as json_file:
        json_file.write(json_str)

def containers_info(dcli, path='ContainerInfo.json', all=True):

    containerInfo = {}
    containerInfo['Containers'] = []

    allContainers = list_containers(dcli, all=all)
    if os.path.exists(path):
        os.remove(path)
    for i in range(len(allContainers)):
        containerInfo['Containers'].append(allContainers[i].attrs)

    json_str = json.dumps(containerInfo, indent=4)

    with open(path, 'a') as json_file:
        json_file.write(json_str)

def images_info(dcli, path='ImageInfo.json', name=None, all=True):
    imageInfo = {}
    imageInfo['Images'] = []

    allImages = list_images(dcli, name=name, all=all)
    if os.path.exists(path):
        os.remove(path)
    for i in range(len(allImages)):
        imageInfo['Images'].append(allImages[i].attrs)

    json_str = json.dumps(imageInfo, indent=4)

    with open(path, 'a') as json_file:
        json_file.write(json_str)

def commit(container, repo=None, tag=None, message=None, author=None, changes=None):
    container.commit(repository=repo, tag=tag, message=message, author=author, changes=changes)

def save_image(image, localPath, remotePath, sftp, chunk_size=2097152, localSave=False):
    remote_file = sftp.open(remotePath, 'wb')
    generator = image.save(chunk_size=chunk_size, named=image.tags)
    for chunk in generator:
        remote_file.write(chunk)
    remote_file.close()
    if localSave:
        #pass
        #sftp.get(remotePath, localPath)
        os.system(f'rsync {DockerController.username}@{DockerController.ip}:{remotePath} {localPath}')
        #os.system('rsync potato@10.10.81.100:/tmp/remote-image.tar /tmp/local-image.tar')

def export_container(container, localPath, remotePath, sftp, localSave=False):
    remote_file = sftp.open(remotePath, 'wb')  # ============== IOError, no such file.
    generator = container.export()
    for chunck in generator:
        remote_file.write(chunck)
    remote_file.close()
    if localSave:
        os.system(f'rsync {DockerController.username}@{DockerController.ip}:{remotePath} {localPath}')
        #sftp.get(remotePath, localPath)  # =============== IOError, no such file.
    # sftp.put('/tmp/test-container.tar', '/tmp/test-container.tar')

def create_image(dcli, remotePath, sftp):
    with sftp.open(remotePath, 'rb') as f:
        dcli.images.load(data=f)

def pull_image(dcli, repo, tag=None):
    try:
        dcli.images.pull(repository=repo, tag=tag)

    except requests.exceptions.HTTPError as re:
        if 'repo' in str(re):
            print('Reqeust Error (repo): ' + str(re).split('(')[-1][:-1])
        elif 'tag' in str(re):
            print('Request Error (tag):' + str(re).split(':')[-1])

def create_container(dcli, image, command=None):
    try:
        dcli.containers.create(image=image.id, stdin_open=True, tty=True)
    except AttributeError as ae:
        print('Invalid image input.')

def change_status(container, changeTo):

    # possible state: created, restarting, runing, paused, exited

    curStatus = container.status
    if curStatus == changeTo:
        print('Same status, no need to change.')
    else:
        if changeTo == 'running':
            container.start()
        elif changeTo == 'exited':
            container.stop()
        elif changeTo == 'paused':
            container.pause()
        elif changeTo == 'restart':
            container.restart()
        else:
            print('Status Wrong!')


#=====================================private functions======================#

def _open_sftp(ip, username, password):
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
                raise  KeyError('missing argument' + param + 'in call to ' + func.__name__)
        else:
            relevent_kwargs[param] = body.get(param, params[param].default)
    return func(**relevent_kwargs)

