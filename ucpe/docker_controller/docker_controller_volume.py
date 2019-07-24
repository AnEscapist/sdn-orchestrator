import docker
import os
import requests
from ucpe.docker_controller.docker_global import dcli, api_cli, sftp, ip, username
from ucpe.docker_controller.docker_controller_message import *

def create_volume(name):
	func = create_volume
	try:
		dcli.volumes.create(name)
	except docker.errors.APIError as ae:
		return api_error(ae, func)
	return create_volume_message(name, create_volume)

def list_volumes():
	func = list_volumes
	try:
		volumes_list = dcli.volumes.list()
	except docker.errors.APIError as ae:
		return api_error(ae, func)
	return list_volumes_message(volumes_list, func)

def inspect_volume(name):
	func = inspect_volume
	try:
		inspection = api_cli.inspect_volume(name)
		return inspect_volume_message(name, inspection, func)
	except docker.errors.APIError as ae:
		return api_error(ae, func)
