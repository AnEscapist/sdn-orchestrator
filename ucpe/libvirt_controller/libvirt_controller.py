import os
import xml.etree.cElementTree as ET
from inspect import signature, Parameter

import libvirt
import lxml.etree as LET
from libvirt import virConnect
from libvirt import virDomain

from ucpe.libvirt_controller.utils import VMState, get_domain, open_connection, state, get_caller_function_name
from ucpe.libvirt_controller.errors import format_exception, OperationFailedError
from ucpe.libvirt_controller.testing_constants import *
from ucpe.ucpe import UCPE

import traceback as tb

import grpc
import ucpe.libvirt_controller.grpc.libvirt_pb2 as libvirt_pb2
import ucpe.libvirt_controller.grpc.libvirt_pb2_grpc as libvirt_pb2_grpc

import hurry.filesize as filesize
from hurry.filesize import alternative
import datetime


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
    def libvirt_controller_start_vms(**kwargs):
        func = start_vms
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_start_or_resume_vms(**kwargs):
        func = start_or_resume_vms
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
    def libvirt_controller_destroy_vms(**kwargs):
        func = destroy_vms
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_suspend_vm(**kwargs):
        func = suspend_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_suspend_vms(**kwargs):
        func = suspend_vms
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_resume_vm(**kwargs):
        func = resume_vm
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_resume_vms(**kwargs):
        func = resume_vms
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
    func = _state_str_from_domain
    return _libvirt_domain_observer(func, ucpe, vm_name)

def get_all_vm_states(ucpe):
    func = _state_str_from_domain
    return _libvirt_all_domains_observer(func, ucpe)

def _state_str_from_domain(domain):
    return state(domain).name

def get_vm_xml(ucpe, vm_name):
    func = lambda domain: virDomain.XMLDesc(domain, 0)
    return _libvirt_domain_observer(func, ucpe, vm_name)



def get_vm_info(ucpe, vm_name):
    func = _construct_info_dict
    return _libvirt_domain_observer(func, ucpe, vm_name)


def get_all_vm_info(ucpe):
    func = _construct_info_dict
    return _libvirt_all_domains_observer(func, ucpe)


def _construct_info_dict(domain):
    state, maxmem, mem, cpus, cpu_time = domain.info()

    def kilobytes_to_bytes(bytes):
        BYTES_IN_KILOBYTE = 1024
        return bytes * BYTES_IN_KILOBYTE

    info_dict = {"name": domain.name(), "state": VMState(state).name.capitalize(),
                 "memory allocated": filesize.size(kilobytes_to_bytes(maxmem), system=alternative), "memory": mem,
                 "cpus": cpus,
                 "cpu time": cpu_time}  # by default it seems mem == maxmem, cpu time reported in nanoseconds
    if VMState(state) == VMState.RUNNING:
        memory_stats = domain.memoryStats()  # this line only works for running domains
        info_dict['memory'] = memory_stats[
            'rss']  # todo: beware of magic string 'rss' (resident state memory - basically RAM usage)
    else:
        info_dict['memory'] = 0
    info_dict['memory usage'] = "{:.2%}".format(info_dict['memory'] / maxmem)
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
    return _libvirt_connection_call(func, ucpe, success_message, fail_message, verbose=verbose)


def define_vm_from_params(ucpe, vm_name, image_path, vm_memory=4, vm_vcpu_count=1, verbose=True):
    xml = _get_xml_from_params(ucpe, vm_name, image_path, vm_memory=4, vm_vcpu_count=1, verbose=True)
    return define_vm_from_xml(ucpe, xml, verbose=verbose)


def _get_xml_from_params(ucpe, vm_name, image_path, vm_memory=4, vm_vcpu_count=1, verbose=True):
    xsl = _get_modified_xsl(vm_name, image_path, vm_memory, vm_vcpu_count)
    BLANK_XML = "<blank></blank>"  # xsl contains the entire xml text
    dom = LET.fromstring(BLANK_XML)
    xslt = LET.fromstring(xsl)
    transform = LET.XSLT(xslt)
    newdom = transform(dom)
    xml = LET.tostring(newdom, pretty_print=True).decode("utf-8")
    return xml


def _get_modified_xsl(vm_name, image_path, vm_memory, vm_vcpu_count):
    dirname = os.path.dirname(__file__)
    xsl_path = os.path.join(dirname, "template.xsl")  # todo: possibly stick this in a constant
    namespaces = _register_all_namespaces(xsl_path)
    basepath = "xsl:template/domain/"
    tree = ET.parse(xsl_path)  # todo: consider storing the template in text
    root = tree.getroot()

    hugepages = root.find('xsl:variable[@name="hugepages_memory"]', namespaces)
    hugepages.text = str(vm_memory) + "G"  # todo: hardcoding the unit might be bad

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
    success_message = f"Undefined virtual machine \"{vm_name}\""
    fail_message = f"Failed to undefine virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def start_vm(ucpe, vm_name, verbose=True):
    func = virDomain.create
    success_message = f"Started virtual machine \"{vm_name}\""
    fail_message = f"Failed to start virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)

def start_vms(ucpe, vm_names, verbose=True):
    func = virDomain.create
    success_message = f"Sent start signal to vms {vm_names}"
    fail_message = f"Failed to send start signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)

def start_or_resume_vms(ucpe, vm_names, verbose=True):
    func = _start_or_resume_domain
    success_message = f"Sent start/resume signal to vms {vm_names}"
    fail_message = f"Failed to send start signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)

def get_vm_autostart(ucpe, vm_name):
    func = virDomain.autostart
    return _libvirt_domain_observer(func, ucpe, vm_name)

def set_vm_autostart(ucpe, vm_name, autostart, verbose=True):
    func = lambda domain: virDomain.setAutostart(domain, int(autostart))
    success_message = f"Set autostart of {vm_name} to str(autostart)."
    fail_message = f"Failed to set autostart of {vm_name} to {str(autostart)}"
    operation_name = virDomain.setAutostart.__name__
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose,
                                   operation_name=operation_name)

def shutdown_vm(ucpe, vm_name, verbose=True):
    func = virDomain.shutdown
    success_message = f"Sent shutdown signal to virtual machine \"{vm_name}\". \nWarning: This does not guarantee shutdown."
    fail_message = f"Failed to shutdown virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)

def shutdowm_vms(ucpe, vm_names, verbose=True):
    func = virDomain.shutdown
    success_message = f"Sent shutdown signal to vms {vm_names}"
    fail_message = f"Failed to send shutdown signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)

def destroy_vm(ucpe, vm_name, verbose=True):
    func = virDomain.destroy
    success_message = f"Destroyed virtual machine \"{vm_name}\""
    fail_message = f"Failed to destroy virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)

def destroy_vms(ucpe, vm_names, verbose=True):
    func = virDomain.destroy
    success_message = f"Sent destroy signal to vms {vm_names}"
    fail_message = f"Failed to send destroy signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)

def suspend_vm(ucpe, vm_name, verbose=True):
    func = virDomain.suspend
    success_message = f"Suspended virtual machine \"{vm_name}\""
    fail_message = f"Failed to suspend virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)

def suspend_vms(ucpe, vm_names, verbose=True):
    func = virDomain.suspend
    success_message = f"Sent suspend signal to vms {vm_names}"
    fail_message = f"Failed to send suspend signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)

def resume_vm(ucpe, vm_name, verbose=True):
    func = virDomain.resume
    success_message = f"Resumed virtual machine \"{vm_name}\""
    fail_message = f"Failed to resume virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)

def resume_vms(ucpe, vm_names, verbose=True):
    func = virDomain.resume
    success_message = f"Sent suspend signal to vms {vm_names}"
    fail_message = f"Failed to send suspend signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)

def save_vm(ucpe, vm_name, save_path, verbose=True):
    func = lambda domain: virDomain.save(domain, save_path)
    success_message = f"Saved virtual machine \"{vm_name}\" from path \"{save_path}\""
    fail_message = f"Failed to restore virtual machine \"{vm_name}\" from path \"{save_path}\""
    operation_name = virDomain.save.__name__
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose,
                                   operation_name=operation_name)


def restore_vm(ucpe, save_path, verbose=True):
    func = lambda conn: virConnect.restore(conn, save_path)
    success_message = f"Restored virtual machine from path \"{save_path}\""
    fail_message = f"Failed to restore virtual machine from path \"{save_path}\""
    operation_name = virConnect.restore.__name__
    return _libvirt_connection_call(func, ucpe, success_message, fail_message, verbose=verbose,
                                    operation_name=operation_name)


def snap_vm_from_xml(ucpe, vm_name, xml):
    pass

def _start_or_resume_domain(domain):
    function_map = {
        VMState.RUNNING: lambda domain: 0, # empty function returning statuscode 0 (working)
        VMState.PAUSED: virDomain.resume,
        VMState.SHUTOFF: virDomain.create
    }
    return function_map[state(domain)](domain)

def _blockpull(ucpe, vm_name, save_path, base_path):
    channel = grpc.insecure_channel(ucpe.hostname)
    stub = libvirt_pb2_grpc.LibvirtStub(channel)
    request = libvirt_pb2.BlockPullRequest(domain=vm_name, path=save_path,
                                           base=base_path)
    response = stub.BlockPull(request)
    if response.error:
        raise OperationFailedError(name="blockpull")
    return response.out


def _libvirt_domain_mutator(libvirt_domain_func, ucpe, vm_name, success_message, fail_message, verbose=True,
                            operation_name=None):
    # todo: factor out the outer try/catch
    operation_name = libvirt_domain_func.__name__ if operation_name is None else operation_name
    return_dict = {}
    try:
        with get_domain(ucpe, vm_name) as domain:
            try:
                status = libvirt_domain_func(domain)
                if status < 0:
                    print(fail_message)
                    raise OperationFailedError(name=operation_name)
            except Exception:
                return_dict["fail_message"] = fail_message
                return_dict["traceback"] = tb.format_exc()
            else:
                return_dict["success_message"] = success_message
                if verbose:
                    print(success_message)
    except ConnectionRefusedError:
        return_dict["fail_message"] = fail_message
        return_dict["traceback"] = tb.format_exc()
    return return_dict

def _libvirt_multiple_domain_mutator(libvirt_domain_func, ucpe, vm_names, success_message, fail_message, verbose=True, operation_name=None):
    # todo: factor out the outer try/catch
    operation_name = libvirt_domain_func.__name__ if operation_name is None else operation_name
    return_dict = {}
    failed_list = []
    try:
        with open_connection(ucpe) as conn:
            for vm_name in vm_names:
                try:
                    domain = conn.lookupByName(vm_name)
                    status = libvirt_domain_func(domain)
                    if status < 0:
                        raise OperationFailedError(name=operation_name)
                except Exception:
                    success = False
                    failed_list.append(vm_name)
                    return_dict["traceback"] = tb.format_exc() # todo: find a way to get all tracebacks, not just last one
    except ConnectionRefusedError:
        failed_list = vm_names
        return_dict["traceback"] = tb.format_exc()
    if not failed_list:
        return_dict["success_message"] = success_message
        if verbose:
            print(success_message)
    else:
        return_dict["fail_message"] = f"{fail_message}\nFailed for VMs {failed_list}"
        return_dict["warning"] = "Traceback is only available for the last VM for which the operation fails"
    return return_dict


def _libvirt_domain_observer(libvirt_domain_func, ucpe, vm_name):
    # todo: factor out the outer try/catch
    return_dict = {}
    try:
        with get_domain(ucpe, vm_name) as domain:
            try:
                value = libvirt_domain_func(domain)
                return_dict["return"] = value
            except Exception as e:
                return_dict["fail_message"] = format_exception(e)
                return_dict["traceback"] = tb.format_exc()
            else:
                return_dict["success_message"] = f"Retrieved information for virtual machine \"{vm_name}\""
    except ConnectionRefusedError as e:
        return_dict["fail_message"] = format_exception(e)
        return_dict["traceback"] = tb.format_exc()
    return return_dict


def _libvirt_all_domains_observer(libvirt_domain_func, ucpe):
    # todo: factor out the outer try/catch
    return_dict = {}
    try:
        with open_connection(ucpe) as conn:
            try:
                value = {domain.name(): libvirt_domain_func(domain) for domain in
                         conn.listAllDomains()}  # oom unlikely here
                return_dict["return"] = value
            except Exception as e:
                return_dict["fail_message"] = format_exception(e)
                return_dict["traceback"] = tb.format_exc()
            else:
                return_dict[
                    "success_message"] = f"{libvirt_domain_func.__name__} called successfully for all virtual machines."
    except ConnectionRefusedError as e:
        return_dict["fail_message"] = format_exception(e)
        return_dict["traceback"] = tb.format_exc()
    return return_dict


def _libvirt_connection_call(libvirt_conn_func, ucpe, success_message, fail_message, verbose=True,
                             operation_name=None):
    # connfunc: connection --> domain
    # todo: factor out the outer try/catch
    operation_name = libvirt_conn_func.__name__ if operation_name is None else operation_name
    return_dict = {}
    try:
        with open_connection(ucpe) as conn:
            try:
                result = libvirt_conn_func(conn)
                if result is None:
                    print(fail_message)
                    raise OperationFailedError(name=operation_name)
            except:
                return_dict["fail_message"] = fail_message
                return_dict["traceback"] = tb.format_exc()
            else:
                if isinstance(result, virDomain):
                    success_message_extended = success_message + "\n" + f"Virtual Machine Name: \"{result.name()}\""
                    return_dict["success_message"] = success_message_extended
                    if verbose:
                        print(success_message)
    except ConnectionRefusedError:
        return_dict["fail_message"] = fail_message
        return_dict["traceback"] = tb.format_exc()
    return return_dict


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
    return_dict = func(**relevant_kwargs)
    caller_name = get_caller_function_name()
    return_dict["function"] = caller_name
    return return_dict


if __name__ == '__main__':
    # test:
    UBUNTU_IMAGE_PATH = "/var/third-party/ubuntu_16_1_test.qcow2"
    # define_vm_from_params(DEFAULT_UCPE,"test", UBUNTU_IMAGE_PATH)
    # define_vm_from_xml(DEFAULT_UCPE,DEFAULT_XML)
    # start_vm(DEFAULT_UCPE, "test")
    # print(start_vms(DEFAULT_UCPE, ["test", "cloud"]))
    # print(start_or_resume_vms(DEFAULT_UCPE, ["test", "cloud2"]))
    # shutdown_vm(DEFAULT_UCPE, "test")
    # destroy_vm(DEFAULT_UCPE, "test")
    # suspend_vm(DEFAULT_UCPE, "test")
    # suspend_vms(DEFAULT_UCPE, ["test", "cloud2"])
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

    # print(LibvirtController.libvirt_controller_define_vm_from_params(**DEFAULT_KWARGS))
    # print(LibvirtController.libvirt_controller_start_vm(**DEFAULT_KWARGS))
    # print(LibvirtController.libvirt_controller_shutdown_vm(**DEFAULT_KWARGS))
    # print(LibvirtController.libvirt_controller_get_vm_state(**DEFAULT_KWARGS))
    # print(LibvirtController.libvirt_controller_get_vm_xml(**DEFAULT_KWARGS))
    # print(LibvirtController.libvirt_controller_get_vm_autostart(**DEFAULT_KWARGS))
    # LibvirtController.libvirt_controller_set_vm_autostart(**DEFAULT_KWARGS)
    # LibvirtController.libvirt_controller_suspend_vm(**DEFAULT_KWARGS)
    # LibvirtController.libvirt_controller_resume_vm(**DEFAULT_KWARGS)
    # LibvirtController.libvirt_controller_save_vm(**DEFAULT_KWARGS)
    # LibvirtController.libvirt_controller_restore_vm(**DEFAULT_KWARGS)
    # print(LibvirtController.libvirt_controller_get_vm_info(**DEFAULT_KWARGS))
    # print(LibvirtController.libvirt_controller_get_all_vm_info(**DEFAULT_KWARGS))
    # print(LibvirtController.libvirt_controller_destroy_vm(**DEFAULT_KWARGS))
    # LibvirtController.libvirt_controller_undefine_vm(**DEFAULT_KWARGS)
