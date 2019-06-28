#=========================Error================================#
def ose_error(ose, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'No route to host: ' + str(ose).split('(')[1].split(')')[0]
    }
    return err

def fnf_erro(path, func):
    err = {
        'function': f'<{func.__name__}>',
        'fail message': f'No such file or directory: {path}'
    }
    return err


#=========================Message================================#
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



