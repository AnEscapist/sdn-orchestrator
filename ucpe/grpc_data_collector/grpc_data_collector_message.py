import json


def json_str(message):
    return json.dumps(message, indent=4)


def get_value_message(func, info):
    message = {
        'function': f'<{func.__name__}>',
        'status': f'Function {func.__name__} finished',
        'return': f'{info}'
    }
    return json_str(message)

def get_list_message(func, info):
    message = {
        'function': f'<{func.__name__}>',
        'status': f'Function {func.__name__} finished',
        'return': f'LIST: {info}'
    }
    return json_str(message)