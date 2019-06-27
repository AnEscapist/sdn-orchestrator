import docker
import json
import os
import paramiko
import requests
from utilities.Error import testError


class DockerController(object):
    def __init__(self, ip='10.10.81.100', username='potato', password='potato'):
        self.ip = ip
        self.username=username
        self.password = password
        #self.sftp = DockerController.docker_controller_open_sftp(self.ip, self.username, self.password)

    def docker_controller_client(self, ip, port):
        return docker.DockerClient(base_url=ip + ':' + port)

    def docker_controller_open_sftp(self, ip, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)
            return ssh.open_sftp()
        except paramiko.ssh_exception.NoValidConnectionsError as para_no_valid_error:
            print('Connection Error:' + str(para_no_valid_error).split(']')[1])
        except paramiko.ssh_exception.SSHException as para_ssh_exception:
            print('SSH Exception: ' + str(para_ssh_exception))

    def docker_controller_containers(self, dcli, all=True):
        try:
            if all == True:
                return dcli.containers.list(all=all)
            else:
                return dcli.containers.list()
        except OSError as ose:
            print('Connection Error: ' + str(ose).split('(')[1].split(')')[0] + '.' + str(ose).split(':')[-2] + ':' +
                  str(ose).split(']')[-1][:-4])

    def docker_controller_images(self, dcli, name=None, all=True):
        try:
            return dcli.images.list(name=name, all=all)
        except OSError as ose:
            print('Connection Error: ' + str(ose).split('(')[1].split(')')[0] + '.' + str(ose).split(':')[-2] + ':' +
                  str(ose).split(']')[-1][:-4])

    def docker_controller_get_container_status(self, dcli, all=False, id_name=None):
        status = {}
        allContainers = self.docker_controller_containers(dcli, all=True)
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

    def docker_controller_gather_containers(self, dcli, all=True, path='ContainerInfo.json'):

        containerInfo = {}
        containerInfo['Containers'] = []

        allContainers = self.docker_controller_containers(dcli, all=all)
        if os.path.exists(path):
            os.remove(path)
        for i in range(len(allContainers)):
            containerInfo['Containers'].append(allContainers[i].attrs)

        json_str = json.dumps(containerInfo, indent=4)

        with open(path, 'a') as json_file:
            json_file.write(json_str)

    def docker_controller_gather_images(self, dcli, name=None, all=True, path='ImageInfo.json'):
        imageInfo = {}
        imageInfo['Images'] = []

        allImages = self.docker_controller_images(dcli, name=name, all=all)
        if os.path.exists(path):
            os.remove(path)
        for i in range(len(allImages)):
            imageInfo['Images'].append(allImages[i].attrs)

        json_str = json.dumps(imageInfo, indent=4)

        with open(path, 'a') as json_file:
            json_file.write(json_str)

    def docker_controller_commit(self, container, repo=None, tag=None, message=None, author=None, changes=None):
        container.commit(repository=repo, tag=tag, message=message, author=author, changes=changes)

    def docker_controller_save_image(self, image, localPath, remotePath, sftp, chunk_size=2097152, localSave=False):
        remote_file = sftp.open(remotePath, 'wb')
        generator = image.save(chunk_size=chunk_size, named=image.tags)
        for chunk in generator:
            remote_file.write(chunk)
        remote_file.close()
        if localSave:
            #pass
            #sftp.get(remotePath, localPath)
            os.system(f'rsync {self.username}@{self.ip}:{remotePath} {localPath}')
            #os.system('rsync potato@10.10.81.100:/tmp/remote-image.tar /tmp/local-image.tar')

    def docker_controller_export_container(self, container, localPath, remotePath, sftp, localSave=False):
        remote_file = sftp.open(remotePath, 'wb')  # ============== IOError, no such file.
        generator = container.export()
        for chunck in generator:
            remote_file.write(chunck)
        remote_file.close()
        if localSave:
            os.system(f'rsync {self.username}@{self.ip}:{remotePath} {localPath}')
            #sftp.get(remotePath, localPath)  # =============== IOError, no such file.
        # sftp.put('/tmp/test-container.tar', '/tmp/test-container.tar')

    def docker_controller_create_image(self, dcli, remotePath, sftp):
        with sftp.open(remotePath, 'rb') as f:
            dcli.images.load(data=f)

    def docker_controller_pull_image(self, dcli, repo, tag=None):
        try:
            dcli.images.pull(repository=repo, tag=tag)

        except requests.exceptions.HTTPError as re:
            if 'repo' in str(re):
                print('Reqeust Error (repo): ' + str(re).split('(')[-1][:-1])
            elif 'tag' in str(re):
                print('Request Error (tag):' + str(re).split(':')[-1])

    def docker_controller_create_container(self, dcli, image, command=None):
        try:
            dcli.containers.create(image=image.id, stdin_open=True, tty=True)
        except AttributeError as ae:
            print('Invalid image input.')

    def docker_controller_change_status(self, container, changeTo):

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

    def docker_container_console(self, container, command):
        if container.status != 'running':
            print(f'Conflict ("Container {container.id} is not running")')
        else:
            print(container.exec_run(command))