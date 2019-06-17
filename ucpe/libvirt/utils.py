import libvirt


# URI Parameters, as documented here:
# https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections-Remote_URIs.html
DRIVER = "qemu"
TRANSPORT = "TCP"
USERNAME = "potato"
HOSTNAME = "10.10.81.100"
PORT = None #defaults - ssh:22, tcp:16509, tls:16514 applied if no port specified
PATH = "system"
EXTRAPARAMETERS = ""

def connect(driver=DRIVER, transport=TRANSPORT, username=USERNAME, hostname=HOSTNAME, port=PORT, path=PATH, extraparameters=EXTRAPARAMETERS, verbose=True):
    """Connect to the libvirt daemon on the host (uCPE) specified by the parameters."""
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

def read(path):
    """return contents of file as a string"""
    with open(path) as f:
        contents = f.read()
    return contents
