# =========================Error================================#
def ose_error(ose, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'No route to host: ' + str(ose).split('(')[1].split(')')[0]
    }
    return err


def fnf_error(path, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'No such file or directory: {path}'
    }
    return err


def cnf_error(id, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'Container: {id} not found!'
    }
    return err


def inf_erro(image_name, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'Image: {image_name} not found!'
    }
    return err


def il_error(path, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'Cannot load image from {path}!'
    }
    return err


def pull_error(re, func):
    print(re)
    fail_message = 'fail to pull error '
    if 'repo' in str(re):
        fail_message = f'Reqeust Error (repo): ' + str(re).split('(')[-1][:-1]
    if 'tag' in str(re):
        fail_message = 'Request Error (tag):' + str(re).split(':')[-1]
    err = {
        'function': f'<{func.__name__}>',
        'fail message': fail_message
    }
    return err


# =========================Warning===============================#
def change_status_warning(id_name, status, func):
    warning = {
        'function': f'<{func.__name__}>',
        'waring message': f'Container {id_name} is already {status}!'
    }
    return warning


def invalid_input_warning(input, func):
    warning = {
        'function': f'<{func.__name__}>',
        'waring message': f'Invalid input: {input}!'
    }
    return warning


# =========================Message================================#
def json_file_message(path, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': 'Information retrieved successfully!',
        'return': f'JSON FILE: {path} created and saved.'
    }
    return message


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
    print('type of message:', type(message['return']))
    return message


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
    return message


def commit_message(id_name, repo, tag, author, func):
    if not author:
        author = 'Unknown'
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Container: {id_name} committed to image: {repo}:{tag}',
        'return': f'IMAGE: {repo}:{tag}'
    }
    return message


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
            'return': f'FILES: {local_path} and {username}@{ip}{remote_path} created and saved!'
        }
    return message


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
            'return': f'FILES: {local_path} and {username}@{ip}{remote_path} created and saved!'
        }
    return message


def create_image_message(image_id, remote_path, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Image: {image_id} created by using {remote_path}',
        'reutnr': f'IMAGE: {image_id} ceated!'
    }
    return message


def pull_image_message(repo, tag, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Image: {repo}:{tag} pulled successfully!',
        'reutrn': f'IMAGE: {repo}:{tag}'
    }
    return message


def create_container_message(container_id, image_name, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Container {container_id} created by using image {image_name}!',
        'reutrn': f'CONTAINER: {container_id}'
    }
    return message


def change_status_message(id_name, change_to, func):
    message = {
        'function': f'<{func.__name__}>',
        'success message': f'Status of container {id_name} changed to {change_to}!',
    }
    return message
