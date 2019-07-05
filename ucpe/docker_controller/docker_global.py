import docker
import paramiko

ip = '10.10.81.100'
port = '2375'
username='potato'
password='potato'

#========================docker client===========================

def _create_client(low_level = False):
    if not low_level:
        return docker.DockerClient(base_url=ip + ':' + port)
    return docker.APIClient(base_url=ip + ':' + port)

def _open_sftp():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        return ssh.open_sftp()
    except paramiko.ssh_exception.NoValidConnectionsError as para_no_valid_error:
        print('Connection Error:' + str(para_no_valid_error).split(']')[1])
    except paramiko.ssh_exception.SSHException as para_ssh_exception:
        print('SSH Exception: ' + str(para_ssh_exception))


    
dcli = _create_client(low_level=False)
api_cli = _create_client(low_level=True)
sftp = _open_sftp()

#===========================docker client end=========================