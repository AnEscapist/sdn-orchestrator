import ucpe.libvirt_controller.VirtualMachine
import libvirt
import ucpe.libvirt_controller.VirtualMachine as VM
from contextlib import contextmanager

# URI Parameters, as documented here:
# https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections-Remote_URIs.html
DRIVER = "qemu"
TRANSPORT = "TCP"
USERNAME = "potato"
HOSTNAME = "10.10.81.100"
PORT = ""  # defaults - ssh:22, tcp:16509, tls:16514 applied if no port specified
PATH = "system"
EXTRAPARAMETERS = ""

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

    transport = "+" + transport if transport else ""
    username = username + "@" if username else ""
    hostname = hostname if hostname else ""
    port = ":" + port if port else ""
    path = path if path else ""
    extraparameters = "?" + extraparameters if extraparameters else ""

    uri = driver + transport + "://" + username + hostname + port + "/" + path + extraparameters
    conn = libvirt.open(uri)
    if conn is None:
        print("Failed to connect to", uri)
        raise ConnectionError
    elif verbose:
        print("Successfully connected to", uri)
        print(
            "Warning: you must close this connection yourself by calling the .close() method of the return value of this function.")
    return conn

@contextmanager
def open_connection(ucpe=None, driver=DRIVER, transport=TRANSPORT, username=USERNAME, hostname=HOSTNAME, port=PORT, path=PATH,
            extraparameters=EXTRAPARAMETERS, verbose=True):
    conn = None
    try:
        conn = connect(ucpe=ucpe, driver=driver, transport=transport, username=username, hostname=hostname, port=port, path=path,
            extraparameters=extraparameters, verbose=verbose)
        yield conn
    finally:
        conn.close()

@contextmanager
def get_domain(ucpe, vm_name, verbose=False):
    conn = None
    try:
        conn = connect(ucpe=ucpe, verbose=verbose)
        domain = conn.lookupByName(vm_name)
        yield domain
    finally:
        conn.close()

def state(libvirt_domain):
    #rn returns VMState.SHUTOFF.  consider making it return "SHUTOFF"
    return VM.VMState(libvirt_domain.state()[0])


def read(path):
    """return contents of file as a string"""
    with open(path) as f:
        contents = f.read()
    return contents
