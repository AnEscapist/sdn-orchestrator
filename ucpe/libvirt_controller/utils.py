from enum import Enum
import sys
import libvirt
import paramiko
import socket
from contextlib import contextmanager
import os

# URI Parameters, as documented here:
# https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections-Remote_URIs.html
DRIVER = "qemu"
TRANSPORT = "TCP"
USERNAME = "potato"
HOSTNAME = "10.10.81.100"
PORT = "16509" #assumes TCP
PATH = "system"
EXTRAPARAMETERS = ""
TIMEOUT = 1 #seconds


def connect(ucpe=None, driver=DRIVER, transport=TRANSPORT, username=USERNAME, hostname=HOSTNAME, port=PORT, path=PATH,
            extraparameters=EXTRAPARAMETERS, verbose=True):
    """Connect to the libvirt_controller daemon on the host (uCPE) specified by the inputted URI parameters.
     Description of Parameters: https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections-Remote_URIs.html
     driver is the only required parameter

     :return: output of libvirt_controller.open(uri)
     :raise: ConnectionError if unable to connect
     """
    if ucpe:
        transport = ucpe.libvirt_transport
        username = ucpe.username
        hostname = ucpe.hostname
        port = ucpe.libvirt_port
        path = ucpe.libvirt_path
        extraparameters = ucpe.libvirt_extra_params

    if not valid_remote_socket(hostname, port):
        raise ConnectionRefusedError(f"Could not connect to \"{hostname}:{port}\". Ensure that your hostname and port are correct.")
    uri = get_uri(driver=driver, transport=transport, username=username, hostname=hostname, port=port, path=path,
            extraparameters=extraparameters, verbose=True)
    conn = libvirt.open(uri)
    if conn is None:
        raise ConnectionError(f"Failed to connect to {uri}")
    elif verbose:
        print("Successfully connected to", uri)
        print(
            "Warning: you must close this connection yourself by calling the .close() method of the return value of this function.")
    return conn

def get_uri(driver=DRIVER, transport=TRANSPORT, username=USERNAME, hostname=HOSTNAME, port=PORT, path=PATH,
                extraparameters=EXTRAPARAMETERS, verbose=True):
    transport = "+" + transport if transport else ""
    username = username + "@" if username else ""
    hostname = hostname if hostname else ""
    port = ":" + port if port else ""
    path = path if path else ""
    extraparameters = "?" + extraparameters if extraparameters else ""
    uri = driver + transport + "://" + username + hostname + port + "/" + path + extraparameters
    return uri

def valid_remote_socket(hostname, port):
    if isinstance(port, str):
        port = int(port)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((hostname, port))
        return True
    except socket.timeout:
        return False

@contextmanager
def open_connection(ucpe=None, driver=DRIVER, transport=TRANSPORT, username=USERNAME, hostname=HOSTNAME, port=PORT,
                    path=PATH,
                    extraparameters=EXTRAPARAMETERS, verbose=True):
    conn = None
    try:
        conn = connect(ucpe=ucpe, driver=driver, transport=transport, username=username, hostname=hostname, port=port,
                       path=path,
                       extraparameters=extraparameters, verbose=verbose)
        yield conn
    finally:
        if conn:
            conn.close()


@contextmanager
def get_domain(ucpe, vm_name, verbose=False):
    conn = None
    try:
        conn = connect(ucpe=ucpe, verbose=verbose)
        domain = conn.lookupByName(vm_name)
    except Exception as e:
        raise e
    else:
        yield domain
    finally:
        if conn:
            conn.close()

def get_file_basename_no_extension(filepath):
    basename = os.path.basename(filepath)
    basename_no_ext, ext = os.path.splitext(basename)
    return basename_no_ext

def ovs_interface_names_from_vm_name(vm_name, ovs_interface_count):
    return ['_'.join([vm_name,'vmeth'+str(k)]) for k in range(ovs_interface_count)]

def state(libvirt_domain):
    return VMState(libvirt_domain.state()[0])

def get_caller_function_name():
    return sys._getframe().f_back.f_back.f_code.co_name

def read(path):
    """return contents of file as a string"""
    with open(path) as f:
        contents = f.read()
    return contents


# def copy_image(image_filename):

class VMState(Enum):
    NOSTATE = libvirt.VIR_DOMAIN_NOSTATE
    RUNNING = libvirt.VIR_DOMAIN_RUNNING
    BLOCKED = libvirt.VIR_DOMAIN_BLOCKED
    PAUSED = libvirt.VIR_DOMAIN_PAUSED
    SHUTDOWN = libvirt.VIR_DOMAIN_SHUTDOWN
    SHUTOFF = libvirt.VIR_DOMAIN_SHUTOFF
    CRASHED = libvirt.VIR_DOMAIN_CRASHED
    PMSUSPENDED = libvirt.VIR_DOMAIN_PMSUSPENDED

#test:
# def caller():
#     callee()
#
# def callee():
#     print("i got called by:", get_caller_function_name())
#
# caller()
