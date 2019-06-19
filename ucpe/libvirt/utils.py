import libvirt
import ucpe.libvirt.VirtualMachine as VM

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
    """Connect to the libvirt daemon on the host (uCPE) specified by the inputted URI parameters.
     Description of Parameters: https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections-Remote_URIs.html
     driver is the only required parameter

     :return: output of libvirt.open(uri)
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
    return conn

def state(domain):
    return VM.VMState(domain.state[0])

def all_vm_states(ucpe):
    conn = connect(ucpe=ucpe)
    domain_states = {domain.name(): state(domain) for domain in conn.listAllDomains()}
    conn.close()
    return domain_states

def vm_state(ucpe, vm_name):
    conn = connect(ucpe=ucpe)
    domain = conn.lookupByName(vm_name)
    return state(domain)

def read(path):
    """return contents of file as a string"""
    with open(path) as f:
        contents = f.read()
    return contents
