import docker
import os
import requests
from ucpe.docker_controller.docker_global import dcli, api_cli, sftp, ip, username
from ucpe.docker_controller.docker_controller_message import *

def create_volume(name):
	dcli.volumes.create(name)
	return create_volume_message(name, create_volume)
