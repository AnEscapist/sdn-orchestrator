import sys


def get_caller_function_name():
    return sys._getframe().f_back.f_back.f_code.co_name
