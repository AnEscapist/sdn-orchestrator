from inspect import signature, Parameter
import libvirt
from contextlib import contextmanager
from ucpe.libvirt_controller.utils import VMState
from ucpe.libvirt_controller.testing_constants import *
from libvirt import virDomain
from libvirt import virConnect
from ucpe.libvirt_controller.errors import *
from ucpe.ucpe import UCPE
from ucpe.libvirt_controller.utils import get_domain, open_connection, state
import xml.etree.cElementTree as ET
import lxml.etree as LET
import os

class LibvirtController():

    @staticmethod
    def libvirt_controller_define_vm_from_xml(**kwargs):
        func = define_vm_from_xml
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_define_vm_from_params(**kwargs):
        func = define_vm_from_params
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_undefine_vm(**kwargs):
        func = undefine_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_get_vm_state(**kwargs):
        func = get_vm_state
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_get_all_vm_states(**kwargs):
        func = get_all_vm_states
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_get_vm_info(**kwargs):
        func = get_vm_info
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_get_all_vm_info(**kwargs):
        func = get_all_vm_info
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_start_vm(**kwargs):
        func = start_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_shutdown_vm(**kwargs):
        func = shutdown_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_destroy_vm(**kwargs):
        func = destroy_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_suspend_vm(**kwargs):
        func = suspend_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_resume_vm(**kwargs):
        func = resume_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_save_vm(**kwargs):
        func = save_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_restore_vm(**kwargs):
        func = restore_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_get_vm_autostart(**kwargs):
        func = get_vm_autostart
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_set_vm_autostart(**kwargs):
        func = set_vm_autostart
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_get_vm_xml(**kwargs):
        func = get_vm_xml
        return _call_function(func, **kwargs)


def get_vm_state(ucpe, vm_name):
    func = state
    return _libvirt_domain_observer(func, ucpe, vm_name)


def get_vm_xml(ucpe, vm_name):
    func = lambda domain: virDomain.XMLDesc(domain, 0)
    return _libvirt_domain_observer(func, ucpe, vm_name)


def get_all_vm_states(ucpe):
    func = state
    return _libvirt_all_domains_observer(func, ucpe)


def get_vm_info(ucpe, vm_name):
    func = _construct_info_dict
    return _libvirt_domain_observer(func, ucpe, vm_name)


def get_all_vm_info(ucpe):
    func = _construct_info_dict
    return _libvirt_domain_observer(func, ucpe)


def _construct_info_dict(domain):
    state, maxmem, mem, cpus, cpu_time = domain.info()
    memory_stats = domain.memoryStats()
    info_dict = {"state": VMState(state).name, "max_memory": maxmem, "memory": mem, "cpu_count": cpus,
                 "cpu_time": cpu_time}
    info_dict.update(memory_stats)
    return info_dict


def get_vm_vnc_port(ucpe, vm_name):
    func = _vnc_port_from_domain
    return _libvirt_domain_observer(func, ucpe, vm_name)


def _vnc_port_from_domain(domain):
    # TODO: 2019-06-04 today, libvirt-python has no function to directly get the port, so it must be parsed from XML.  Check back in a couple of years
    # copied from: https://stackoverflow.com/questions/13173184/how-to-get-vnc-port-number-using-libvirt
    # todo: generic function to parse info from xml given path from root tag to desired subelement?
    xml = domain.XMLDesc(0)
    root = ET.fromstring(xml)
    # get the VNC port
    graphics = root.find('./devices/graphics[@type="vnc"]')
    port = graphics.get('port')
    return port

def get_vm_interfaces(ucpe, vm_name):
    with get_domain(ucpe, vm_name) as domain:
        interfaces = domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
    return interfaces




def define_vm_from_xml(ucpe, xml, verbose=True):
    func = lambda conn: virConnect.defineXML(conn, xml)
    success_message = "Defined new virtual machine"
    fail_message = "Failed to define new virtual machine"
    _libvirt_connection_call(func, ucpe, success_message, fail_message, verbose=verbose)

def define_vm_from_params(ucpe, vm_name, image_path, vm_memory=4, vm_vcpu_count=1, verbose=True):
    xml = _get_xml_from_params(ucpe, vm_name, image_path, vm_memory=4, vm_vcpu_count=1, verbose=True)
    define_vm_from_xml(ucpe, xml, verbose=verbose)

def _get_xml_from_params(ucpe, vm_name, image_path, vm_memory=4, vm_vcpu_count=1, verbose=True):
    xsl = _get_modified_xsl(vm_name, image_path, vm_memory, vm_vcpu_count)
    BLANK_XML = "<blank></blank>" #xsl contains the entire xml text
    dom = LET.fromstring(BLANK_XML)
    xslt = LET.fromstring(xsl)
    transform = LET.XSLT(xslt)
    newdom = transform(dom)
    xml = LET.tostring(newdom, pretty_print=True).decode("utf-8")
    return xml

def _get_modified_xsl(vm_name, image_path, vm_memory, vm_vcpu_count):
    dirname = os.path.dirname(__file__)
    xsl_path = os.path.join(dirname, "template.xsl") #todo: possibly stick this in a constant
    namespaces = _register_all_namespaces(xsl_path)
    basepath = "xsl:template/domain/"
    tree = ET.parse(xsl_path)  # todo: consider storing the template in text
    root = tree.getroot()

    hugepages = root.find('xsl:variable[@name="hugepages_memory"]', namespaces)
    hugepages.text = str(vm_memory) + "G" #todo: hardcoding the unit might be bad

    name = root.find(basepath + 'name', namespaces)
    name.text = vm_name

    memory = root.find(basepath + 'memory', namespaces)
    memory.text = str(vm_memory)

    vcpu = root.find(basepath + "vcpu", namespaces)
    vcpu.text = str(vm_vcpu_count)

    source = root.find(basepath + 'devices/disk/source', namespaces)
    source.set('file', image_path)

    xsl = ET.tostring(root).decode("utf-8")
    return xsl

def _register_all_namespaces(filename):
    # https://stackoverflow.com/questions/54439309/how-to-preserve-namespaces-when-parsing-xml-via-elementtree-in-python
    # this is so the outputted xml preserves the qemu:blah labels at the bottom of the XML.
    # without registering the namespace qemu, qemu is replaced by ns0 (for namespace 0) in the written xml
    # todo: inefficient - requires an extra pass through the xml, so perhaps consider just registering namespace "qemu"
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])
    return namespaces


def undefine_vm(ucpe, vm_name, verbose=True):
    func = virDomain.undefine
    success_message = "Undefined virtual machine " + vm_name
    fail_message = "Failed to undefine virtual machine " + vm_name
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def start_vm(ucpe, vm_name, verbose=True):
    func = virDomain.create
    success_message = "Started virtual machine " + vm_name
    fail_message = "Failed to start virtual machine " + vm_name
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def get_vm_autostart(ucpe, vm_name):
    func = virDomain.autostart
    return _libvirt_domain_observer(func, ucpe, vm_name)


def set_vm_autostart(ucpe, vm_name, autostart, verbose=True):
    func = lambda domain: virDomain.setAutostart(domain, int(autostart))
    success_message = "Set autostart of " + vm_name + " to " + str(autostart)
    fail_message = "Failed to set autostart of " + vm_name + " to " + str(autostart)
    operation_name = virDomain.setAutostart.__name__
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose,
                            operation_name=operation_name)


def shutdown_vm(ucpe, vm_name, verbose=True):
    func = virDomain.shutdown
    success_message = "Shutdown virtual machine " + vm_name
    fail_message = "Failed to shutdown virtual machine " + vm_name
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def destroy_vm(ucpe, vm_name, verbose=True):
    func = virDomain.destroy
    success_message = "Destroyed virtual machine " + vm_name
    fail_message = "Failed to destroy virtual machine " + vm_name
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def suspend_vm(ucpe, vm_name, verbose=True):
    func = virDomain.suspend
    success_message = "Suspended virtual machine " + vm_name
    fail_message = "Failed to suspend virtual machine " + vm_name
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def resume_vm(ucpe, vm_name, verbose=True):
    func = virDomain.resume
    success_message = "Resumed virtual machine " + vm_name
    fail_message = "Failed to resume virtual machine " + vm_name
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def save_vm(ucpe, vm_name, save_path, verbose=True):
    func = lambda domain: virDomain.save(domain, save_path)
    success_message = "Saved virtual machine " + vm_name + " from path " + save_path
    fail_message = "Failed to restore virtual machine " + vm_name + " from path " + save_path
    operation_name = virDomain.save.__name__
    _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose,
                            operation_name=operation_name)


def restore_vm(ucpe, save_path, verbose=True):
    func = lambda conn: virConnect.restore(conn, save_path)
    success_message = "Restored virtual machine from path " + save_path
    fail_message = "Failed to restore virtual machine from path " + save_path
    operation_name = virConnect.restore.__name__
    _libvirt_connection_call(func, ucpe, success_message, fail_message, verbose=verbose,
                             operation_name=operation_name)


def _libvirt_domain_mutator(libvirt_domain_func, ucpe, vm_name, success_message, fail_message, verbose=True,
                            operation_name=None):
    operation_name = libvirt_domain_func.__name__ if operation_name is None else operation_name
    with get_domain(ucpe, vm_name) as domain:
        status = libvirt_domain_func(domain)
        if status < 0:
            print(fail_message)
            raise OperationFailedError(name=operation_name)
        elif verbose:
            print(success_message)


def _libvirt_domain_observer(libvirt_domain_func, ucpe, vm_name):
    with get_domain(ucpe, vm_name) as domain:
        return libvirt_domain_func(domain)


def _libvirt_all_domains_observer(libvirt_domain_func, ucpe):
    with open_connection(ucpe) as conn:
        return {domain.name(): libvirt_domain_func(domain) for domain in conn.listAllDomains()}  # oom unlikely here


def _libvirt_connection_call(libvirt_conn_func, ucpe, success_message, fail_message, verbose=True,
                             operation_name=None):
    # connfunc: connection --> domain
    operation_name = libvirt_conn_func.__name__ if operation_name is None else operation_name
    with open_connection(ucpe) as conn:
        result = libvirt_conn_func(conn)
        if result is None:
            print(fail_message)
            raise OperationFailedError(name=operation_name)
        elif isinstance(result, virDomain) and verbose:
            print(success_message + "\n" + "Virtual Machine Name: " + result.name())
        elif verbose:
            print(success_message)


def _call_function(func, **kwargs):
    body = kwargs["body"]  # todo: bad
    ucpe = UCPE.from_kwargs(**body)
    params = signature(func).parameters  # get the function arguments
    relevant_kwargs = {"ucpe": ucpe}  # todo: this is REALLY bad
    for param in params:
        if param == "ucpe":
            continue
        if params[param].default == Parameter.empty:
            try:
                relevant_kwargs[param] = body[param]
            except KeyError:
                raise KeyError("missing argument " + param + " in call to " + func.__name__)
        else:  # todo: this is REALLY bad - depends on the arg name, but so does the request/response
            relevant_kwargs[param] = body.get(param, params[param].default)
    return func(**relevant_kwargs)

# test:
UBUNTU_IMAGE_PATH = "/var/third-party/ubuntu_16_1_test.qcow2"
# define_vm_from_params(DEFAULT_UCPE,"test", UBUNTU_IMAGE_PATH)
define_vm_from_xml(DEFAULT_UCPE,DEFAULT_XML)
# start_vm(DEFAULT_UCPE, "test")
# shutdown_vm(DEFAULT_UCPE, "test")
# destroy_vm(DEFAULT_UCPE, "test")
# suspend_vm(DEFAULT_UCPE, "test")
# resume_vm(DEFAULT_UCPE, "test")
# save_vm(DEFAULT_UCPE, "test", "/home/potato/test_savepath.img")
# restore_vm(DEFAULT_UCPE, "test", "/home/potato/test_savepath.img")
# set_vm_autostart(DEFAULT_UCPE, "test", True)
# print(get_vm_autostart(DEFAULT_UCPE, "test"))
# print(get_vm_state(DEFAULT_UCPE, "test"))
# print(get_vm_info(DEFAULT_UCPE, "test"))
# print(get_all_vm_states(DEFAULT_UCPE))
# print(get_vm_vnc_port(DEFAULT_UCPE, "test"))
# print(get_vm_interfaces(DEFAULT_UCPE, "test"))

# LibvirtController.libvirt_controller_define_vm(**DEFAULT_KWARGS)
# LibvirtController.libvirt_controller_start_vm(**DEFAULT_KWARGS)
# LibvirtController.libvirt_controller_shutdown_vm(**DEFAULT_KWARGS)
# print(LibvirtController.libvirt_controller_get_vm_state(**DEFAULT_KWARGS))
# print(LibvirtController.libvirt_controller_get_vm_xml(**DEFAULT_KWARGS))
# print(LibvirtController.libvirt_controller_get_vm_autostart(**DEFAULT_KWARGS))
# LibvirtController.libvirt_controller_set_vm_autostart(**DEFAULT_KWARGS)
# LibvirtController.libvirt_controller_suspend_vm(**DEFAULT_KWARGS)
# LibvirtController.libvirt_controller_resume_vm(**DEFAULT_KWARGS)
# LibvirtController.libvirt_controller_save_vm(**DEFAULT_KWARGS)
# LibvirtController.libvirt_controller_restore_vm(**DEFAULT_KWARGS)
# print(LibvirtController.libvirt_controller_get_vm_info(**DEFAULT_KWARGS))
# LibvirtController.libvirt_controller_destroy_vm(**DEFAULT_KWARGS)
# LibvirtController.libvirt_controller_undefine_vm(**DEFAULT_KWARGS)
