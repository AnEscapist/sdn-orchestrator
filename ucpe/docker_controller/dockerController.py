import docker
import json
import os
import paramiko
import requests
from utilities.Error import testError


def docker_client(ip, port):
    return docker.DockerClient(base_url=ip + ':' + port)

def open_sftp(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        return ssh.open_sftp()
    except paramiko.ssh_exception.NoValidConnectionsError as para_no_valid_error:
        print('Connection Error:' + str(para_no_valid_error).split(']')[1])
    except paramiko.ssh_exception.SSHException as para_ssh_exception:
        print('SSH Exception: ' + str(para_ssh_exception))


def all_containers(dcli, all=True):
    #try:
    if all == True:
        return dcli.containers.list(all=all)
    else:
        return dcli.containers.list()
        #raise testError('testERror')
    #except OSError as oe:


        #raise testError()
        #print('Connection Error: ' + str(ose).split('(')[1].split(')')[0] + '.' + str(ose).split(':')[-2] + ':' + str(ose).split(']')[-1][:-4])


def all_images(dcli, name=None, all=True):
    try:
        return dcli.images.list(name=name, all=all)
    except OSError as ose:
        print('Connection Error: ' + str(ose).split('(')[1].split(')')[0] + '.' + str(ose).split(':')[-2] + ':' + str(ose).split(']')[-1][:-4])



def get_container_status(dcli, all=False, id_name=None):
    status = {}
    allContainers = all_containers(dcli, all=True)
    if all:
        for container in allContainers:
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
    with open('ContainerStatus.json', 'w') as json_file:
        json_file.write(json_str)


def gather_containers(dcli, path='ContainerInfo.json'):

    containerInfo = {}
    containerInfo['Containers'] = []

    allContainers = all_containers(dcli, all=True)
    if os.path.exists(path):
        os.remove(path)
    for i in range(len(allContainers)):
        containerInfo['Containers'].append(allContainers[i].attrs)

    json_str = json.dumps(containerInfo, indent=4)

    with open(path, 'a') as json_file:
        if i ==len(allContainers) - 1:
            json_file.write(json_str)
        else:
            json_file.write(json_str + ',\n')

def gather_images(dcli, name=None, all=True, path='ImageInfo.json'):
    imageInfo = {}
    imageInfo['Images'] = []

    allImages = all_images(dcli, name=name, all=all)
    if os.path.exists(path):
        os.remove(path)
    for i in range(len(allImages)):
        imageInfo['Images'].append(allImages[i].attrs)

    json_str = json.dumps(imageInfo, indent=4)

    with open(path, 'a') as json_file:
        if i == len(allImages) - 1:
            json_file.write(json_str)
        else:
            json_file.write(json_str + ',\n')

def commit_container_to_image(container, repo=None, tag=None, message=None, author=None, changes=None):
    container.commit(repository=repo, tag=tag, message=message, author=author, changes=changes)

def save_image_to_tar(image, localPath, remotePath, sftp, chunk_size=2097152, localSave=False):
    remote_file = sftp.open(remotePath, 'wb')
    generator = image.save(chunk_size=chunk_size, named=image.tags)
    for chunk in generator:
        remote_file.write(chunk)
    remote_file.close()
    if localSave:
        sftp.get(remotePath, localPath)


def export_container_to_tar(container, localPath, remotePath, sftp, localSave=False):
    remote_file = sftp.open(remotePath, 'wb') # ============== IOError, no such file.
    generator = container.export()
    for chunck in generator:
        remote_file.write(chunck)
    remote_file.close()
    if localSave:
        sftp.get(remotePath, localPath)  # =============== IOError, no such file.
    #sftp.put('/tmp/test-container.tar', '/tmp/test-container.tar')

def create_image_from_tar(dcli, remotePath, sftp):
    with sftp.open(remotePath, 'rb') as f:
        dcli.images.load(data=f)


    '''
    if not os.path.exists(localPath):
        sftp.get(remotePath, localPath)    # ================ IOError, no such file.

    with open(localPath, 'rb') as f:
        dcli.images.load(data=f)
        
        '''


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
        dcli.containers.create(image=image.id,stdin_open=True, tty=True)
    except AttributeError as ae:
        print('Invalid image input.')

def change_container_status(container, changeTo):

    #possible state: created, restarting, runing, paused, exited

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


def console_container(container, command):
    if container.status != 'running':
        print(f'Conflict ("Container {container.id} is not running")')
    else:
        print(container.exec_run(command))


if __name__ == '__main__':

    dockerClient = docker_client('10.10.81.100', '2375')
    allContainers = all_containers(dockerClient, all=True)
    allImages = all_images(dockerClient, all=True)
    #print(type(dockerClient.images))
    #print(len(allContainers))

    sftp = open_sftp('10.10.81.100', 'potato', 'potato')


    while True:
        func = input('=====Select the function=====\n'
                    '1: Get container status\n'
                    '2: Get the containers info\n'
                    '3: Get the images info\n'
                    '4: Commit container to image\n'
                    '5: Save image to tar\n'
                    '6: Create image from tar\n'
                    '7: Export container to tar\n'
                    '8: Create container from image\n'
                    '9: Pull image from online repository\n'
                    '10: Change container status\n'
                    '11: Console container\n'
                    '0: Exit\n')

        if func == '1':
            get_container_status(dockerClient, all=True)
        elif func == '2':
            gather_containers(dockerClient)
        elif func == '3':
            gather_images(dockerClient)
        elif func == '4':
            commit_container_to_image(allContainers[0], 'abc', 'abc', 'this is a commit test')
        elif func == '5':
            save_image_to_tar(image=allImages[0], localPath='/tmp/test-image.tar', sftp=sftp, remotePath='/tmp/test-image.tar', localSave=True)
        elif func == '6':
            create_image_from_tar(remotePath='/tmp/test-image.tar', localPath='tmp/test-image.tar', sftp=sftp)
        elif func == '7':
            export_container_to_tar(dockerClient, allContainers[0], sftp=sftp)
        elif func == '8':
            create_container(dockerClient, image=allImages[0])
        elif func == '9':
            pull_image(dockerClient, 'ubuntu', 'eoan')
        elif func == '10':
            changeTo = input('Change the status to (running, exited, paused or restart):')
            change_container_status(allContainers[0], changeTo=changeTo)
        elif func == '11':
            console_container(allContainers[1], 'ls')
        elif func == '0':
            break


#getContainerStatus(all=True)
#getherImages()
#commitContainerToImage(allContainers[0], 'abc', 'abc', 'this is a commit test')
#saveImageToTar(allImages[0])
#createImageFromTar('/tmp/test-image.tar')
#exportToTar(allContainers[0])
#createContainer(allImages[0])

#pullImage('ubuntu', 'eoan')
#createContainer(image=allImages[0])


#getOmeContainerStatus(allContainers[0])
#changeContainerStatus(allContainers[0], 'restart')
#consoleContainer(allContainers[0], 'ls')