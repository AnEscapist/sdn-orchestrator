import json
def json_str(message):
    return json.dumps(message, indent=4)

#=========================Error================================#
def type_error(te, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail_message': str(te)
    }
    return json_str(err)

def nr_error(nre, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail_message': str(nre)
    }
    return json_str(err)

def api_error(ae, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': str(ae).split(':', 1)[1].lstrip()
    }
    return json_str(err)

def nf_error(nfe, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': str(nfe).split(':', 1)[1].lstrip()
    }
    return json_str(err)

def ose_error(ose, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'No route to host: ' + str(ose).split('(')[1].split(')')[0]
    }
    return json_str(err)

def fnf_error(path, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'No such file or directory: {path}'
    }
    return json_str(err)

def cnf_error(id, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'Container: {id} not found!'
    }
    return json_str(err)

def inf_error(image_name, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'Image: {image_name} not found!'
    }
    return json_str(err)

def il_error(path, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'Cannot load image from {path}!'
    }
    return json_str(err)

def pull_error(re, func):
    if 'repo' in str(re):
        fail_message = f'Reqeust Error (repo): ' + str(re).split('(')[-1][:-1]
    elif 'tag' in str(re):
        fail_message = 'Request Error (tag):' + str(re).split(':')[-1]
    else:
        fail_message = str(re).split(':', 1)[1]
    err = {
        'function': f'<{func.__name__}>',
        'fail message': fail_message
    }
    return json_str(err)


#=========================Warning===============================#
def change_status_warning(id_name, curStatus, func):
    warning = {
        'function': f'<{func.__name__}>',
        'waring message': f'Container {id_name} is already {curStatus}!',
        'return': f'Current status - [{curStatus}].'
    }
    return json_str(warning)
def invalid_input_warning(input, func):
    warning = {
        'function': f'<{func.__name__}>',
        'waring message': f'Invalid input: {input}!'
    }
    return json_str(warning)

#=========================Message================================#
def json_file_message(path, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': 'Information retrieved successfully!',
        'return': f'JSON FILE: {path} created and saved.'
    }
    return json_str(message)

def client_info_message(info, path,func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Information retrieved successfully and json file {path} created!',
        'return': f'{info}'
    }
    return json_str(message)

def containers_status_message(status, path, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'JSON FILE: {path} created and saved.',
        'return': f'{status}'
    }
    return json_str(message)

def containers_images_message(images, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': 'Got all the images for the existing containers.',
        'return': f'{images}'
    }
    return json_str(message)

def container_list_message(list, all, func):
    if all:
        message = {
            'function': f'<{func.__name__}>',
            'success message': 'All containers are listed!',
            'return': f'LIST: {list}'
        }
    else:
        message = {
            'function': f'<{func.__name__}>',
            'success message': 'All running containers are listed!',
            'return': f'LIST: {list}'
        }
    return json_str(message)

def containers_id_message(list, all, func):
    if all:
        message = {
            'function': f'<{func.__name__}>',
            'success message': 'All containers id are listed!',
            'return': f'LIST: {list}'
        }
    else:
        message = {
            'function': f'<{func.__name__}>',
            'success message': 'All running containers id are listed!',
            'return': f'LIST: {list}'
        }
    return json_str(message)

def rename_container_message(id_name, newName, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Name of container {id_name} changed to {newName}.',
        'return': f'{newName}'
    }
    return json_str(message)

def image_list_message(list, name, all, func):
    if name:
        message = {
            'function': f'<{func.__name__}>',
            'success message': f'All {name} images are listed!',
            'return': f'LIST: {list}'
        }
    else:
        message = {
            'function': f'<{func.__name__}>',
            'success message': f'All images are listed!',
            'return': f'LIST: {list}'
        }
    return json_str(message)

def commit_message(id_name, repo, tag, author, func):
    if not author:
        author = 'Unknown'
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Container: {id_name} committed to image: {repo}:{tag}',
        'return': f'IMAGE: {repo}:{tag}'
    }
    return json_str(message)

def save_image_message(image_name, local_path, username, ip, remote_path, local_save, func):
    if local_save:
        message = {
            'function': f'<{func.__name__}>',
            'success message': f'Image: {image_name} saved locally {local_path} and remotely {username}@{ip}{remote_path}',
            'return': f'FILES: {local_path} and {username}@{ip}{remote_path} created and saved!'
        }
    else:
        message = {
            'function': f'<{func.__name__}>',
            'success message': f'Image: {image_name} saved remotely {username}@{ip}{remote_path}',
            'return': f'FILES: {username}@{ip}{remote_path} created and saved!'
        }
    return json_str(message)

def export_container_message(id_name, local_path, username, ip, remote_path, local_save, func):
    if local_save:
        message = {
            'function': f'<{func.__name__}>',
            'success message': f'Container: {id_name} saved locally {local_path} and remotely {username}@{ip}{remote_path}',
            'return': f'FILES: {local_path} and {username}@{ip}{remote_path} created and saved!'
        }
    else:
        message = {
            'function': f'<{func.__name__}>',
            'success message': f'Container: {id_name} saved remotely {username}@{ip}{remote_path}',
            'return': f'FILES: {username}@{ip}{remote_path} created and saved!'
        }
    return json_str(message)

def create_container_message(container_id, image_name, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Container {container_id} created by using image {image_name}!',
        'return': f'CONTAINER: {container_id}'
    }
    return json_str(message)

def create_image_message(image_id, remote_path, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Image: {image_id} created by using {remote_path}',
        'return': f'IMAGE: {image_id} ceated!'
    }
    return json_str(message)

def pull_image_message(repo, tag, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Image: {repo}:{tag} pulled successfully!',
        'return': f'IMAGE: {repo}:{tag}'
    }
    return json_str(message)


def change_status_message(id_name, curStatus, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Status of container {id_name} changed to {curStatus}!',
        'return': f'Current status - [{curStatus}].'
    }
    return json_str(message)

def inspect_container_message(id_name, inspection, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Container {id_name} inspected.',
        'return': inspection
    }
    return json_str(message)

def create_network_message(net_id, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'A new network created!',
        'return': f'NETWORK: {net_id}'
    }
    return json_str(message)

def connect_container_message(id_name, net_id, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Container {id_name} connected to network {net_id}!',
    }
    return json_str(message)

def disconnect_container_message(id_name, net_id, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Container {id_name} disconnected to network {net_id}!',
    }
    return json_str(message)


def remove_network_message(net_id, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Network {net_id} removed!',
    }
    return json_str(message)


#===========================docker volume===================
def create_volume_message(name, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Volume {name} created!',
    }
    return json_str(message)
