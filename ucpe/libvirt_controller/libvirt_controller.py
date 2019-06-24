from inspect import signature, Parameter
from contextlib import contextmanager
from ucpe.libvirt_controller.utils import VMState
from ucpe.libvirt_controller.testing_constants import *
from libvirt import virDomain
from libvirt import virConnect
from ucpe.libvirt_controller.errors import *
from ucpe.ucpe import UCPE
from ucpe.libvirt_controller.utils import get_domain, open_connection, state

class LibvirtController():

    @staticmethod
    def libvirt_controller_define_vm(**kwargs):
        func = define_vm
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

def define_vm(ucpe, xml, verbose=True):
    func = lambda conn: virConnect.defineXML(conn, xml)
    success_message = "Defined new virtual machine"
    fail_message = "Failed to define new virtual machine"
    _libvirt_connection_call(func, ucpe, success_message, fail_message, verbose=verbose)

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

def _construct_info_dict(domain):
    state, maxmem, mem, cpus, cpu_time = domain.info()
    return {"state": VMState(state).name, "max_memory": maxmem, "memory": mem, "cpu_count": cpus, "cpu_time": cpu_time}

def _call_function(func, **kwargs):
    body = kwargs["body"] #todo: bad
    ucpe = UCPE.from_kwargs(**body)
    params = signature(func).parameters #get the function arguments
    relevant_kwargs = {"ucpe": ucpe} #todo: this is REALLY bad
    for param in params:
        if param == "ucpe":
            continue
        if params[param].default == Parameter.empty:
            try:
                relevant_kwargs[param] = body[param]
            except KeyError:
                raise KeyError("missing argument " + param + " in call to " + func.__name__)
        else: #todo: this is REALLY bad - depends on the arg name, but so does the request/response
            relevant_kwargs[param] = body.get(param, params[param].default)
    return func(**relevant_kwargs)

# test:
# define_vm(DEFAULT_UCPE, DEFAULT_XML)
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
