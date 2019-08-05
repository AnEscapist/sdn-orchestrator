import os
import xml.etree.cElementTree as ET
# from inspect import signature, Parameter
import inspect

import libvirt
import lxml.etree as LET
from libvirt import virConnect
from libvirt import virDomain

from ucpe.libvirt_controller.utils import VMState, get_domain, open_connection, state, get_caller_function_name, \
    get_file_basename_no_extension, ovs_interface_names_from_vm_name
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

import subprocess

import sys

sys.path.append('/home/attadmin/projects/sdn-orchestrator/')

from multiprocessing import Process, Queue

'''
Formatting: 
return_dict: {
    success_message: appears in return dict iff operation succeeds
    fail_message: appears in return dict iff operation fails
    return: return value of operation (optional)
    traceback: error trace (if traceback is present, fail message must also be present)
    warning: warning message
}
'''

global vnc_process
vnc_process = None


class LibvirtController():
    '''
    maintainers:
    Roger Jin: 6/4/19 - 8/9/19
        - rogerjin@mit.edu
    '''

    '''
    for each of the static methods below, see definition of func for documentation
    see bottom of this file for example usage, testing_constants.py for example of kwargs
    '''

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
    def libvirt_controller_delete_vms(**kwargs):
        func = delete_vms
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

    @staticmethod
    def libvirt_controller_prepare_vm_console(**kwargs):
        func = prepare_vm_console
        return _call_function(func, **kwargs)

    @staticmethod
    def libvirt_controller_get_vm_vnc_port(**kwargs):
        func = get_vm_vnc_port
        return _call_function(func, **kwargs)


def get_vm_state(ucpe, vm_name):
    '''
    get state of one domain
    :param ucpe: ucpe object
    :param vm_name: name of domain to get state of
    :return: 'RUNNING', 'PAUSED', 'SHUTOFF', depending on domain state
    '''
    func = _state_str_from_domain
    return _libvirt_domain_observer(func, ucpe, vm_name)


def get_all_vm_states(ucpe):
    '''
    retrieve dictionary mapping domain name to domain state
    :param ucpe: ucpe object
    :return: dictionary mapping domain name to domain state
    '''
    func = _state_str_from_domain
    return _libvirt_all_domains_observer(func, ucpe)


def _state_str_from_domain(domain):
    '''
    retrieve a string representing domain's state (RUNNING, PAUSED, SHUTOFF) from virDomain object
    :param domain: virDomain object to retrieve state from
    :return: 'RUNNING', 'PAUSED', or 'SHUTOFF' depending on domain state
    '''
    return state(domain).name


def _image_name_from_xml(xml):
    '''
    retrieve domain image name (name of image file without extension) from xml
    :param xml: domain xml definition
    :return: name of domain image
    '''
    basepath = ""
    root = ET.fromstring(xml)  # todo: consider storing the template in text
    # root = tree.getroot()

    source = root.find(basepath + 'devices/disk/source')
    image = source.get('file')
    return get_file_basename_no_extension(image)


def get_vm_xml(ucpe, vm_name):
    '''
    get xml definition of domain with name vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to get xml of
    :return: xml string of domain with name vm_name on uCPE ucpe
    '''
    func = lambda domain: virDomain.XMLDesc(domain, 0)
    return _libvirt_domain_observer(func, ucpe, vm_name)


def get_vm_info(ucpe, vm_name):
    '''
    get info dict for domain on uCPE ucpe with name vm_name
    :param ucpe: ucpe object
    :param vm_name: name of domain to get info of
    :return: info dict for domain with name vm_name
    '''
    func = _construct_info_dict
    return _libvirt_domain_observer(func, ucpe, vm_name)


def get_all_vm_info(ucpe):
    '''
    get info dict for all domains on uCPE ucpe
    :param ucpe: ucpe object
    :return: dictionary mapping domain name to _construct_info_dict(domain)
    '''
    func = _construct_info_dict
    return _libvirt_all_domains_observer(func, ucpe)


def _construct_info_dict(domain):
    '''
    construct a dictionary of information about a domain, consisting of name, state, allocated memory, memory currently using, cpu count, cpu time
    :param domain: domain to construct info dict for
    :return: info dict
    '''
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

    info_dict['image'] = _image_name_from_xml(domain.XMLDesc(0))
    return info_dict


def prepare_vm_console(ucpe, vm_name):
    '''
    open a console session to the domain with name vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: domain name
    :return: return dict (see top of file for formatting)
    '''
    global vnc_process
    if vnc_process is not None:
        vnc_process.terminate()
    with get_domain(ucpe, vm_name) as domain:
        vnc_port = _vnc_port_from_domain(domain)
    queue = Queue()
    # todo: error handling
    vnc_process = Process(target=prepare_vm_console_helper, args=(ucpe.hostname, vnc_port))
    vnc_process.start()
    # out, err = queue.get()
    # return_dict = {"return": out}
    # if not err:
    #     return_dict["success_message"] = f"Successfully prepared VNC for {vm_name}"
    # else:
    #     return_dict["fail_message"] = f"Failed to prepare VNC for {vm_name}"
    #     return_dict["error"] = err
    #     return_dict["traceback"] = tb.format_exc()
    return {"warning": "no error handling"}


def prepare_vm_console_helper(hostname, port):
    '''
    run noVNC's launch.sh script with the hostname and port as arguments
    :param hostname: ip address of the uCPE
    :param port: vnc port
    '''
    launch_script_path = '/home/attadmin/projects/sdn-orchestrator/utilities/novnc/utils/launch.sh'
    p = subprocess.Popen([launch_script_path, '--vnc', f'{hostname}:{port}'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    print('in the process', p.args)
    p.communicate()


def get_vm_vnc_port(ucpe, vm_name):
    '''
    get vnc port from domain with name vm_name
    :param ucpe: ucpe object
    :param vm_name: name of domain to retrieve vnc port of
    :return: vnc port of domain with name vm_name
    '''
    func = _vnc_port_from_domain
    return _libvirt_domain_observer(func, ucpe, vm_name)


def _vnc_port_from_domain(domain):
    '''
    get vnc port from domain
    :param domain: virDomain object, must be running
    :return: vnc port
    '''
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
    '''
    get domain interfaces
    :param ucpe: ucpe object
    :param vm_name: name of domain
    :return: list of interfaces on the domain
    '''
    with get_domain(ucpe, vm_name) as domain:
        interfaces = domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
    return interfaces


def define_vm_from_xml(ucpe, xml, verbose=True):
    '''
    define domain given xml file
    :param ucpe: ucpe object
    :param xml: domain xml definition
    :param verbose: if true, print success statements
    :return: return_dict (see top of file for format)
    '''
    func = lambda conn: virConnect.defineXML(conn, xml)
    success_message = "Defined new virtual machine"
    fail_message = "Failed to define new virtual machine"
    return _libvirt_connection_call(func, ucpe, success_message, fail_message, verbose=verbose)


def define_vm_from_params(ucpe, vm_name, vm_image_path, vm_memory=4, vm_hugepage_memory=4, vm_use_hugepages=False,
                          vm_vcpu_count=1, vm_bridge_name=None, vm_ovs_interface_count=0, verbose=True):
    '''
    define domain given parameters
    :param vm_name: name of domain
    :param vm_image_path: path to domain .qcow2 image
    :param vm_memory: amount of memory in gigabytes
    :param vm_use_hugepages: boolean
    :param vm_vcpu_count: int
    :param vm_bridge_name: name of bridge
    :param vm_ovs_interface_count: number of ovs interfaces
    :return: return dict (see top of file for format)
    '''
    if vm_use_hugepages:
        vm_memory = vm_hugepage_memory
    image_file_name = os.path.basename(vm_image_path)
    channel = grpc.insecure_channel('10.10.81.100:50061')
    stub = libvirt_pb2_grpc.LibvirtStub(channel)
    request = libvirt_pb2.CopyRequest(vm_name=vm_name, image_file_name=image_file_name)
    response = stub.CopyImage(request)
    # todo: error handling
    xml = _get_xml_from_params(ucpe, vm_name, vm_image_path, vm_memory=vm_memory, vm_use_hugepages=vm_use_hugepages,
                               vm_vcpu_count=vm_vcpu_count, vm_bridge_name=vm_bridge_name,
                               vm_ovs_interface_count=vm_ovs_interface_count,
                               verbose=True)
    return define_vm_from_xml(ucpe, xml, verbose=verbose)


def _get_xml_from_params(ucpe, vm_name, vm_image_path, vm_memory=4, vm_use_hugepages=False, vm_vcpu_count=1,
                         vm_bridge_name=None, vm_ovs_interface_count=0, verbose=True):
    '''
    get vm xml definition from given parameters
    :param vm_name: name of domain
    :param vm_image_path: path to domain .qcow2 image
    :param vm_memory: amount of memory in gigabytes
    :param vm_use_hugepages: boolean
    :param vm_vcpu_count: int
    :param vm_bridge_name: name of bridge
    :param vm_ovs_interface_count: number of ovs interfaces
    :return: xml string definition of domain
    '''
    xsl = _get_modified_xsl(vm_name, vm_image_path, vm_memory, vm_use_hugepages, vm_vcpu_count,
                            vm_bridge_name=vm_bridge_name, vm_ovs_interface_count=vm_ovs_interface_count)
    BLANK_XML = "<blank></blank>"  # xsl contains the entire xml text
    dom = LET.fromstring(BLANK_XML)
    xslt = LET.fromstring(xsl)
    transform = LET.XSLT(xslt)
    newdom = transform(dom) # perform xsl transformation on blank xml to get domain xml definition
    xml = LET.tostring(newdom, pretty_print=True).decode("utf-8")
    return xml


def _get_modified_xsl(vm_name, vm_image_path, vm_memory, vm_use_hugepages, vm_vcpu_count, vm_bridge_name=None,
                      vm_ovs_interface_count=0):
    '''
    fill in variables in the template XSL file
    :param vm_name: name of domain
    :param vm_image_path: path to domain .qcow2 image
    :param vm_memory: amount of memory in gigabytes
    :param vm_use_hugepages: boolean
    :param vm_vcpu_count: int
    :param vm_bridge_name: name of bridge
    :param vm_ovs_interface_count: number of ovs interfaces
    :return: xsl string with variables filled in
    '''
    dirname = os.path.dirname(__file__) # allows relative path to template.xsl
    xsl_path = os.path.join(dirname, "template.xsl")  # todo: possibly stick this in a constant

    if vm_use_hugepages:  # todo: clean up, right now there is one template for hugepages, one for nonhugepages
        xsl_path = os.path.join(dirname, "template_hugepages.xsl")

    namespaces = _register_all_namespaces(xsl_path) # must do this because qemu args are namespaced
    basepath = "xsl:template/domain/"
    tree = ET.parse(xsl_path)  # todo: consider storing the template in text
    root = tree.getroot()

    if vm_use_hugepages: # set hugepage memory variable
        hugepages = root.find('xsl:variable[@name="hugepages_memory"]', namespaces)
        hugepages.text = str(vm_memory) + "G"  # todo: hardcoding the unit might be bad

    name = root.find(basepath + 'name', namespaces) # set domain name
    name.text = vm_name

    memory = root.find(basepath + 'memory', namespaces) # set domain memory
    memory.text = str(vm_memory)

    vcpu = root.find(basepath + "vcpu", namespaces) # set domain vcpus
    vcpu.text = str(vm_vcpu_count)

    source = root.find(basepath + 'devices/disk/source', namespaces) # set domain image path
    source.set('file', vm_image_path)

    # interface things
    devices = root.find(basepath + 'devices', namespaces)
    bridge_insertion_point = 1

    # bridges
    if vm_bridge_name is not None:
        interfaces = _get_bridge_interface_element(vm_bridge_name)
        devices.insert(bridge_insertion_point, interfaces)

    # ovs interfaces
    ovs_interface_elements = _get_ovs_interface_elements(vm_name, vm_ovs_interface_count)
    ovs_insertion_point = 2
    for interface_element in ovs_interface_elements[::-1]:
        devices.insert(ovs_insertion_point, interface_element)

    xsl = ET.tostring(root).decode("utf-8")
    return xsl


def _get_bridge_interface_element(vm_bridge_name, interface_model_type='virtio', interface_link_state='up'):
    '''
    get an ElementTree Element representing a linux bridge interface element in a domain XML definition
    :param vm_bridge_name: name of bridge
    :param interface_model_type: interface model type
    :param interface_link_state: interface link state
    :return: ElementTree Element representing linux bridge interface element in a domain XML definition

    the returned ElementTree Element represents an XML element of the form

        <interface type="bridge"
            <source bridge="mgmtbr"/>
            <model type="virtio"/>
            <link state="up"/>
        </interface>

    '''
    # devices is an Element in an ElementTree

    interface = ET.Element("interface", {"type": "bridge"})
    source = ET.SubElement(interface, "source", {"bridge": vm_bridge_name})
    model = ET.SubElement(interface, "model", {"type": interface_model_type})
    link = ET.SubElement(interface, "link", {"state": interface_link_state})
    return interface


def _get_ovs_interface_elements(vm_name, vm_ovs_interface_count, interface_model_type='virtio',
                                interface_link_state='up'):
    '''
    get a list of ElementTree Elements representing interface elements of type vhostuser in a domain XML definition
    :param vm_name: name of domain to get ovs interface elements for
    :param vm_ovs_interface_count: desired number of ovs interfaces
    :param interface_model_type: interface model type
    :param interface_link_state: interface link state (doesn't seem to actually work)
    :return: a list of ElementTree elements representing interface elements

    each ElementTree Element represents an XML element of the form:

        <interface type="vhostuser">
            <source mode="client"
                    path="/usr/local/var/run/openvswitch/vm_vyatta_eth0"
                    type="unix"/>
            <model type="virtio"/>
            <link state="up"/>
        </interface>

    '''
    interface_names = ovs_interface_names_from_vm_name(vm_name, vm_ovs_interface_count)
    interface_elements = []
    for interface_name in interface_names:
        interface_type = 'vhostuser'
        ovs_basepath = '/usr/local/var/run/openvswitch/'
        source_mode = 'client'
        source_type = 'unix'
        interface = ET.Element("interface", {"type": interface_type})
        source = ET.SubElement(interface, "source", {
            "mode": source_mode,
            "path": ovs_basepath + interface_name,
            "type": source_type
        })
        model = ET.SubElement(interface, "model", {"type": interface_model_type})
        link = ET.SubElement(interface, "link", {"state": interface_link_state})
        interface_elements.append(interface)
    return interface_elements


def _register_all_namespaces(filename):
    '''
    :param filename: xml file to register namespaces of in ElementTree
    '''
    # https://stackoverflow.com/questions/54439309/how-to-preserve-namespaces-when-parsing-xml-via-elementtree-in-python
    # this is so the outputted xml preserves the qemu:blah labels at the bottom of the XML.
    # without registering the namespace qemu, qemu is replaced by ns0 (for namespace 0) in the written xml
    # todo: inefficient - requires an extra pass through the xml, so perhaps consider just registering namespace "qemu"
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])
    return namespaces


def undefine_vm(ucpe, vm_name, verbose=True):
    '''
    undefine domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to undefine
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.undefine
    success_message = f"Undefined virtual machine \"{vm_name}\""
    fail_message = f"Failed to undefine virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def delete_vms(ucpe, vm_names, verbose=True):
    '''
    destroy and undefine domains with name in vm_names on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_names: list of names of domains to shutdown
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = _delete_domain
    success_message = f"Deleted all vms in {vm_names}"
    fail_message = f"Failed to delete all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)


def start_vm(ucpe, vm_name, verbose=True):
    '''
    start domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to start
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.create
    success_message = f"Started virtual machine \"{vm_name}\""
    fail_message = f"Failed to start virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def start_vms(ucpe, vm_names, verbose=True):
    '''
    start domains with name in vm_names on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to start
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.create
    success_message = f"Sent start signal to vms {vm_names}"
    fail_message = f"Failed to send start signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)


def start_or_resume_vms(ucpe, vm_names, verbose=True):
    '''
    start or resume domains with name in vm_names on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to start or resume
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = _start_or_resume_domain
    success_message = f"Sent start/resume signal to vms {vm_names}"
    fail_message = f"Failed to send start signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)


def get_vm_autostart(ucpe, vm_name):
    '''
    get autostart state of domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to get autostart state of
    :return: true if vm autostarts, false otherwise
    '''
    func = virDomain.autostart
    return _libvirt_domain_observer(func, ucpe, vm_name)


def set_vm_autostart(ucpe, vm_name, autostart, verbose=True):
    '''
    set autostart state of domain vm_nmame on uCPE ucpe to autostart
    :param ucpe: ucpe object
    :param vm_name: name of domain to shutdown
    :param autostart: boolean
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = lambda domain: virDomain.setAutostart(domain, int(autostart))
    success_message = f"Set autostart of {vm_name} to str(autostart)."
    fail_message = f"Failed to set autostart of {vm_name} to {str(autostart)}"
    operation_name = virDomain.setAutostart.__name__
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose,
                                   operation_name=operation_name)


def shutdown_vm(ucpe, vm_name, verbose=True):
    '''
    shutdown domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to shutdown
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.shutdown
    success_message = f"Sent shutdown signal to virtual machine \"{vm_name}\". \nWarning: This does not guarantee shutdown."
    fail_message = f"Failed to shutdown virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def shutdowm_vms(ucpe, vm_names, verbose=True):
    '''
    shutdown domains with name in vm_names on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_names: list of names of domains to shutdown
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.shutdown
    success_message = f"Sent shutdown signal to vms {vm_names}"
    fail_message = f"Failed to send shutdown signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)


def destroy_vm(ucpe, vm_name, verbose=True):
    '''
    destroy domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to destroy
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.destroy
    success_message = f"Destroyed virtual machine \"{vm_name}\""
    fail_message = f"Failed to destroy virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def destroy_vms(ucpe, vm_names, verbose=True):
    '''
    destroy domains with name in vm_names on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_names: list of names of domains to destroy
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.destroy
    success_message = f"Sent destroy signal to vms {vm_names}"
    fail_message = f"Failed to send destroy signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)


def suspend_vm(ucpe, vm_name, verbose=True):
    '''
    suspend domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to suspend
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.suspend
    success_message = f"Suspended virtual machine \"{vm_name}\""
    fail_message = f"Failed to suspend virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def suspend_vms(ucpe, vm_names, verbose=True):
    '''
    suspend domains with name in vm_names on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_names: list of names of domains to suspend
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.suspend
    success_message = f"Sent suspend signal to vms {vm_names}"
    fail_message = f"Failed to send suspend signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)


def resume_vm(ucpe, vm_name, verbose=True):
    '''
    resume domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_name: name of domain to resume
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.resume
    success_message = f"Resumed virtual machine \"{vm_name}\""
    fail_message = f"Failed to resume virtual machine \"{vm_name}\""
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose)


def resume_vms(ucpe, vm_names, verbose=True):
    '''
    resume domains with name in vm_names on uCPE ucpe
    :param ucpe: ucpe object
    :param vm_names: list of names of domains to resume
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = virDomain.resume
    success_message = f"Sent suspend signal to vms {vm_names}"
    fail_message = f"Failed to send suspend signal to all vms in {vm_names}"
    return _libvirt_multiple_domain_mutator(func, ucpe, vm_names, success_message, fail_message, verbose=verbose)


def save_vm(ucpe, vm_name, save_path, verbose=True):
    '''
    save domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param save_path: path where save image is to be stored
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = lambda domain: virDomain.save(domain, save_path)
    success_message = f"Saved virtual machine \"{vm_name}\" from path \"{save_path}\""
    fail_message = f"Failed to restore virtual machine \"{vm_name}\" from path \"{save_path}\""
    operation_name = virDomain.save.__name__
    return _libvirt_domain_mutator(func, ucpe, vm_name, success_message, fail_message, verbose=verbose,
                                   operation_name=operation_name)


def restore_vm(ucpe, save_path, verbose=True):
    '''
    restore domain vm_name on uCPE ucpe
    :param ucpe: ucpe object
    :param save_path: path where image was stored
    :param verbose: if true, print success messages
    :return: see top of file for return_dict format
    '''
    func = lambda conn: virConnect.restore(conn, save_path)
    success_message = f"Restored virtual machine from path \"{save_path}\""
    fail_message = f"Failed to restore virtual machine from path \"{save_path}\""
    operation_name = virConnect.restore.__name__
    return _libvirt_connection_call(func, ucpe, success_message, fail_message, verbose=verbose,
                                    operation_name=operation_name)


def snap_vm_from_xml(ucpe, vm_name, xml):
    pass


def _start_or_resume_domain(domain):
    '''
    start domain if shutoff, resume domain if paused, do nothing if already running
    :param domain: virDomain object
    '''
    function_map = {
        VMState.RUNNING: lambda domain: 0,  # empty function returning statuscode 0 (working)
        VMState.PAUSED: virDomain.resume,
        VMState.SHUTOFF: virDomain.create
    }
    return function_map[state(domain)](domain)


def _delete_domain(domain):
    '''
    destroy and undefine domain
    :param domain: virDomain object
    '''
    # todo: this will fail as soon as we add any snapshots. snapshots must be deleted first.
    if state(domain) != VMState.SHUTOFF:
        virDomain.destroy(domain)
    virDomain.undefine(domain)


def _blockpull(ucpe, vm_name, save_path, base_path):
    '''
    calls the following on uCPE ucpe:
    virsh blockpull --domain vm_name --path save_path --base base_path --wait
                    --verbose
    pulls the backing chain from (base_path, save_path] into save_path
    :param ucpe: ucpe object
    :param vm_name: name of domain to perform blockpull operation on
    :param save_path: path to some image in backing chain
    :param base_path: path to image in backing chain which becomes the new base
    :return: result of above bash call

    example:
        backing chain for vm_test on ucpe U1:
            base <-- snap1 <-- snap2
        _blockpull(U1, vm_test, <snap2_path>, <base path>) would result in the backing chain
        base <-- snap2, where snap2 now also contains the data of snap1
    '''
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
    '''
    call libvirt_domain_func on libvirt domain vm_name on uCPE ucpe
    :param libvirt_domain_func: any function that accepts a virDomain object and performs a mutation on it (e.g. virDomain.destroy)
    :param ucpe: ucpe object
    :param vm_name: name of domain to apply libvirt_domain_func to
    :param success_message: message to include in return_dict on success
    :param fail_message: message to include in return_dict on fail
    :param verbose: if true, print success messages
    :param operation_name: name of operation that appears in error messages (defaults to name of libvirt_domain_func)
    :return: return dict - see top of file for return_dict format
    '''
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


def _libvirt_multiple_domain_mutator(libvirt_domain_func, ucpe, vm_names, success_message, fail_message, verbose=True,
                                     operation_name=None):
    '''
    call libvirt_domain_func on all libvirt domains on uCPE ucpe whose names appear in vm_names
    :param libvirt_domain_func: any function that accepts a virDomain object and performs a mutation on it (e.g. virDomain.destroy)
    :param ucpe: ucpe object
    :param vm_names: list of names of domains to call libvirt_domain_func on
    :param success_message: message to include in return_dict on success
    :param fail_message: message to include in return_dict on fail
    :param verbose: if true, print success messages
    :param operation_name: name of operation that appears in error messages (defaults to name of libvirt_domain_func)
    :return: return dict - see top of file for return_dict format
    '''
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
                    if status is not None and status < 0:
                        raise OperationFailedError(name=operation_name)
                except Exception:
                    success = False
                    failed_list.append(vm_name)
                    return_dict[
                        "traceback"] = tb.format_exc()  # todo: find a way to get all tracebacks, not just last one
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
    '''
   call libvirt_domain_func on domain vm_name on uCPE ucpe
   :param libvirt_domain_func: a function that accepts a virDomain object and performs an observation (e.g. virDomain.state)
   :param ucpe: ucpe object
   :param vm_name: name of domain to call libvirt_domain_func on
   :param success_message: message to include in return_dict on success
   :param fail_message: message to include in return_dict on fail
   :param verbose: if true, print success messages
   :param operation_name: name of operation that appears in error messages (defaults to name of libvirt_domain_func)
   :return: return dict - see top of file for return_dict format
   '''
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
    '''
   call libvirt_domain_func on all domains on uCPE ucpe
   :param libvirt_domain_func: a function that accepts a virDomain object and performs an observation (e.g. virDomain.state)
   :param ucpe: ucpe object
   :param success_message: message to include in return_dict on success
   :param fail_message: message to include in return_dict on fail
   :param verbose: if true, print success messages
   :param operation_name: name of operation that appears in error messages (defaults to name of libvirt_domain_func)
   :return: return dict - see top of file for return_dict format
    '''
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
    '''
   call libvirt_conn_func
   :param libvirt_conn_func: a function that accepts a virConnect object
   :param ucpe: ucpe object
   :param success_message: message to include in return_dict on success
   :param fail_message: message to include in return_dict on fail
   :param verbose: if true, print success messages
   :param operation_name: name of operation that appears in error messages (defaults to name of libvirt_domain_func)
   :return: return dict - see top of file for return_dict format
    '''
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
    '''
    essentially calls func(**kwargs['body']), but allows kwargs['body'] to have additional arguments that don't appear in the signature of func
    :param func: any function
    :param kwargs: a dictionary, where kwargs['body'] is a dictionary mapping argument names to argument values.  Every argument of func must appear in the keyset of kwargs['body'].
    :return: return value of func(**kwargs['body']), where extra arguments in kwargs['body'] are ignored

    example:
        def func(a, b=3):
            return a + b
        kwargs = {'body': {'a': 1, 'b': 2, 'c': 3}}
    _call_function(func, **kwargs) would return 3.
    '''
    body = kwargs["body"]  # todo: bad
    ucpe = UCPE.from_kwargs(**body)
    params = inspect.signature(func).parameters  # get the function arguments
    relevant_kwargs = {"ucpe": ucpe}  # todo: this is REALLY bad
    for param in params:
        if param == "ucpe":
            continue
        if params[param].default == inspect.Parameter.empty:
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
    # print(prepare_vm_console(DEFAULT_UCPE, 'test2'))
    # define_vm_from_params(DEFAULT_UCPE, "test", UBUNTU_IMAGE_PATH, vm_use_hugepages=True, vm_bridge_name="mgmtbr",
    #                       vm_ovs_interface_count=4)
    # define_vm_from_xml(DEFAULT_UCPE,DEFAULT_XML)
    # start_vm(DEFAULT_UCPE, "test")
    # print(start_vms(DEFAULT_UCPE, ["test", "cloud"]))
    # print(start_or_resume_vms(DEFAULT_UCPE, ["test", "cloud2"]))
    # shutdown_vm(DEFAULT_UCPE, "test")
    # destroy_vm(DEFAULT_UCPE, "test")
    # destroy_vms(DEFAULT_UCPE, ["test", "cloud2"])
    # suspend_vm(DEFAULT_UCPE, "test")
    # suspend_vms(DEFAULT_UCPE, ["test", "cloud2"])
    # resume_vm(DEFAULT_UCPE, "test")
    # save_vm(DEFAULT_UCPE, "test", "/home/potato/test_savepath.img")
    # restore_vm(DEFAULT_UCPE, "test", "/home/potato/test_savepath.img")
    # set_vm_autostart(DEFAULT_UCPE, "test", True)
    # print(get_vm_autostart(DEFAULT_UCPE, "test"))
    # print(get_vm_state(DEFAULT_UCPE, "test"))
    # print(get_vm_info(DEFAULT_UCPE, "monitor"))
    # print(get_all_vm_states(DEFAULT_UCPE))
    # print(get_vm_vnc_port(DEFAULT_UCPE, "test"))
    # print(get_vm_interfaces(DEFAULT_UCPE, "test"))

    # calls with kwargs
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
    # from threading import Thread
    # def test():
    #     print(LibvirtController.libvirt_controller_prepare_vm_console(**{'body':{'hostname': '10.10.81.100', 'username': 'potato', 'vm_name': 'test2'}}))
    # test_thread = Thread(target=test)
    # test_thread.start()
    # print("done")
