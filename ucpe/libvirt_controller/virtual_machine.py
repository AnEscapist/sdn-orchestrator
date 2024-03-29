from contextlib import contextmanager
import ucpe.libvirt_controller.utils as utils
from libvirt import virDomain
from ucpe.libvirt_controller.errors import *


class VirtualMachine():
    # todo: lazy parameter access for immutable values
    def __init__(self, ucpe, def_xml, name):
        # todo: docstring
        self.ucpe = ucpe
        self.def_xml = def_xml  # xml used to define vm
        # todo: parse name (and other data) from xml
        self.name = name
        self.save_path = None
        # todo: deal with outside mutations of these

    def start(self, verbose=True):
        with self._get_domain() as domain:
            created_status = virDomain.create(domain)
            if created_status < 0:
                print("Failed to start virtual machine", self.name)
                raise OperationFailedError(name="start")
            elif verbose:
                print("Started virtual machine", self.name)

    @property
    def autostart(self):
        with self._get_domain() as domain:
            if domain.autostart() == 1:
                return True
            return False

    @autostart.setter
    def autostart(self, autostart):
        with self._get_domain() as domain:
            if autostart:
                domain.setAutostart(1)
            else:
                domain.setAutostart(0)

    @property
    def xml(self):
        # todo: use this as a cache - determine if xml is current
        # todo: this might be bad if it's slow
        with self._get_domain() as domain:
            return domain.XMLDesc(0)

    def saveXML(self, path):
        # todo: think about whether to allow overwriting or not, possibly have some overwrite flag
        # path is a path on the remote (not the uCPE)
        with open(path, 'w') as out:
            out.write(self.xml)

    @property
    def state(self):
        with self._get_domain() as domain:
            return utils.state(domain)

    @state.setter
    def state(self, state):
        raise ReadOnlyError()

    def suspend(self, verbose=True):
        # todo: return value
        with self._get_domain() as domain:
            status = domain.suspend()
            if status < 0:
                print("Failed to suspend virtual machine", self.name)
                raise OperationFailedError(name="suspend")
            elif verbose:
                print("Suspended virtual machine", self.name)

    def resume(self, verbose=True):
        with self._get_domain() as domain:
            status = domain.resume()
            if status < 0:
                print("Failed to resume virtual machine", self.name)
                raise OperationFailedError(name="resume")
            elif verbose:
                print("Resumed virtual machine", self.name)

    def save(self, path, verbose=True):
        """
        saves a persistent image of the vm to a specified path
        :param path: path on the uCPE to the desired save location
        todo: somehow enforce that a restore can happen only once from a given file
        """
        with self._get_domain() as domain:
            status = domain.save(path)
            if status < 0:
                print("Failed to save virtual machine", self.name, "to path", path)
                raise OperationFailedError(name="save")
            elif verbose:
                print("Saved virtual machine", self.name, "to path", path)
                print("Warning: you can only restore once from your save file.")
            self.save_path = path

    def restore(self, save_path=None, verbose=True):
        if save_path:
            self.save_path = save_path
        if self.save_path is None:
            # todo: raise error
            print("Cannot restore without first saving.")
        conn = utils.connect(self.ucpe, verbose=False)
        status = conn.restore(self.save_path)
        if status < 0:
            print("Failed to restore virtual machine from path", self.save_path)
            raise OperationFailedError(name="restore")
        elif verbose:
            print("Restored virtual machine", self.name, "from path", self.save_path)
        self.save_path = None
        conn.close()

    def shutdown(self, verbose=True):
        # todo: bug - have to wait ~20 seconds after starting before stopping
        with self._get_domain() as domain:
            status = domain.shutdown()
            if status < 0:
                print("Failed to shut down virtual machine", self.name)
                raise OperationFailedError(name="shutdown")
            elif verbose:
                print("Shutting down virtual machine", self.name)

    def destroy(self, verbose=True):
        with self._get_domain() as domain:
            status = domain.destroy()
            if status < 0:
                print("Failed to destroy virtual machine", self.name)
                raise OperationFailedError(name="destroy")
            elif verbose:
                print("Destroyed virtual machine", self.name)

    def undefine(self, verbose=True):
        # todo: lock all activity after undefining
        with self._get_domain() as domain:
            if domain.isActive():
                print("Virtual machine is running.  Stop it first before undefining.")
                # todo: ask tyler if should be able to undefine while running
            status = domain.undefine()
            if status < 0:
                print("Failed to undefine virtual machine", self.name)
                raise OperationFailedError(name="undefine")
            elif verbose:
                print("Undefined", self.name)

    @contextmanager
    def _get_domain(self, verbose=False):
        conn = None
        try:
            conn = utils.connect(ucpe=self.ucpe, verbose=verbose)
            domain = conn.lookupByName(self.name)
            yield domain
        finally:
            conn.close()

    @classmethod
    def define(cls, ucpe, xml_path, verbose=True, autostart=False):
        # todo: set a default value for the xml
        # todo: allow an xml string input
        """
        define and start a persistent virtual machine based on an xml configuration
        :param ucpe: UCPE object
        :param xml_path: path to xml
        :return: VirtualMachine instance representing created domain
        """
        xml_contents = utils.read(xml_path)
        conn = utils.connect(ucpe)
        domain = conn.defineXML(xml_contents)  # todo: make persistent
        if domain is None:
            print("Failed to define a virtual machine from XML", xml_path)
            # todo: define an error for this scenario
        print("Defined new virtual machine", domain.name())
        if (autostart):
            domain.autostart(1)
            print("Set virtual machine", domain.name(), "to autostart")
        conn.close()
        return cls(ucpe, xml_contents, domain.name())
