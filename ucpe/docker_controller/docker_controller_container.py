import docker
import os
import requests
import ast
from ucpe.docker_controller.docker_global import dcli, api_cli, sftp, ip, username
from ucpe.docker_controller.docker_controller_message import *


#===========================docker containers========================


def list_containers(all=True):
    func = list_containers
    name_list = []
    try:
        if all == True:
            container_list = dcli.containers.list(all=all)
        else:
            container_list = dcli.containers.list()

        for container in container_list:
            name_list.append(container.name)
        return container_list_message(list=name_list, all=all, func=func)
    except OSError as ose:
        return ose_error(ose,func)

def containers_id(all=True):
    func = containers_id
    id_list = []
    try:
        if all == True:
            container_list = dcli.containers.list(all=all)
        else:
            container_list = dcli.containers.list()

        for container in container_list:
            id_list.append(container.short_id)
        return containers_id_message(list=id_list, all=all, func=func)
    except OSError as ose:
        return ose_error(ose,func)


def containers_status(path='ContainerStatus.json', all=False, id_name=None):
    func = containers_status
    status = {}
    try:
        container_list = dcli.containers.list(all=all)
    except OSError as ose:
        return ose_error(ose, func)

    if all:
        for container in container_list:
            status['container:' + container.name + '(id: ' + container.short_id + ')'] = f'[{container.status}]'
    else:
        try:
            container = dcli.containers.get(id_name)
            status['container:' + container.name + '(id: ' + container.short_id + ')'] = f'[{container.status}]'
        except docker.errors.NotFound:
            return cnf_error(id_name, func)
        except docker.errors.NullResource as nre:
             return nr_error(nre, func)
    json_str = json.dumps(status, indent=4)
    try:
        with open(path, 'w') as json_file:
            json_file.write(json_str)
    except FileNotFoundError:
        return fnf_error(path, func)

    return containers_status_message(status, path, func)

def containers_images(all=True):
    #return images of all the containers
    func = containers_images
    images = []
    try:
        container_list = dcli.containers.list(all=all)
    except OSError as ose:
        return ose_error(ose, func)
    for container in container_list:
        images.append(container.image)
    return containers_images_message(images, func)



def containers_info(path='ContainerInfo.json', all=True):
    func = containers_info
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

def inspect_container(id_name):
    func = inspect_container
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

def commit(id_name, repo=None, tag=None, message=None, author=None, changes=None):
    func = commit
    try:
        container = dcli.containers.get(id_name)
    except docker.errors.NotFound:
        return cnf_error(id_name, func)
    container.commit(repository=repo, tag=tag, message=message, author=author, changes=changes)
    return commit_message(id_name, repo, tag, author, func)

def export_container(id_name, local_path, remote_path, local_save=False):
    func = export_container
    try:
        remote_file = sftp.open(remote_path, 'wb')  # ============== IOError, no such file.
    except FileNotFoundError:
        remote_path = f'{username}@{ip}:{remote_path}'
        return fnf_error(remote_path, func)
    container = dcli.containers.get(id_name)
    generator = container.export()
    for chunck in generator:
        remote_file.write(chunck)
    remote_file.close()
    if local_save:
        os.system(f'rsync {username}@{ip}:{remote_path} {local_path}')
    return export_container_message(id_name, local_path, username,
                                   ip, remote_path, local_save, func)
        #sftp.get(remotePath, localPath)  # =============== IOError, no such file.
    # sftp.put('/tmp/test-container.tar', '/tmp/test-container.tar')

def create_container(image_name, name=None, ports=None, volumes=None, detach=True):
    func = create_container
    bind=dict()
    if ports:
        container_port = ports.split(':')[0]
        host_port = ports.split(':')[1]
        if host_port == 'None':
            bind[container_port] = None
        elif host_port[0] == '(' and host_port[-1] == ')':
            bind[container_port] = (host_port.split(',')[0][1:], host_port.split(',')[1].strip()[:-1])
        elif host_port[0] == '[' and host_port[-1] == ']':
            bind[container_port] = [host_port.split(',')[0][1:], host_port.split(',')[1].strip()[:-1]]
        else:
            bind[container_port] = host_port

    mnt = dict()
    if volumes:
        mnt = ast.literal_eval(volumes)
    #return type(mnt)

    try:
        image = dcli.images.get(image_name)
        container = dcli.containers.run(image=image.id, name=name, ports=bind, volumes=mnt,
                                        detach=detach, stdin_open=True, tty=True)
    except docker.errors.APIError as ae:
        return api_error(ae, func)
    except docker.errors.NullResource as nre:
    	return nr_error(nre, func)
    return create_container_message(container.id, image_name, func)

def change_status(id_name, change_to):
    func = change_status
    # possible state: created, restart, runing, paused, exited
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
        try:
            container = dcli.containers.get(id_name)
        except requests.exceptions.HTTPError:
            return cnf_error(id_name, func)
        curStatus = container.status
    return change_status_message(id_name, curStatus, func)


def rename_container(id_name, newName):
    func = rename_container
    try:
        container = dcli.containers.get(id_name)
    except requests.exceptions.HTTPError:
        return cnf_error(id_name, func)
    try:
        container.rename(newName)
        return rename_container_message(id_name, newName, func)
    except docker.errors.APIError as ae:
        return api_error(ae, func)

def kill_container(id_name):
    # kill one or more containers
    # todo: kill multiple contianers
    func = kill_container
    try:
        container = dcli.containers.get(id_name)
    except requests.exceptions.HTTPError:
        return cnf_error(id_name, func)
    try:
        container.kill()
        return kill_container_message(id_name, func)
    except docker.errors.APIError as ae:
        return api_error(ae, func)



def remove_container(id_name):
    func = remove_container
    try:
        container = dcli.containers.get(id_name)
    except requests.exceptions.HTTPError:
        return cnf_error(id_name, func)
    try:
        container.remove()
        return remove_container_message(id_name, func)
    except docker.errors.APIError as ae:
        return api_error(ae, func)

#======================docker container end============================
