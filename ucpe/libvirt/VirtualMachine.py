from contextlib import contextmanager
import ucpe.libvirt.utils as utils
from enum import Enum, auto
import libvirt
from libvirt import virDomain

class VirtualMachine():
    #todo: lazy parameter access for immutable values
    def __init__(self, ucpe, xml, name):
        #todo: docstring
        self.ucpe = ucpe
        self._xml = xml #xml contents
        #todo: parse name (and other data) from xml
        self.name = name
        self.save_path = None
        #todo: deal with outside mutations of these

    def start(self):
        #todo: error handling
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        created_status = virDomain.create(domain) #bad
        if created_status < 0:
            print("Failed to start domain", self.name)
        else:
            print("Started domain", self.name)
        conn.close()

    @property
    def autostart(self):
        conn = utils.connect(self.ucpe, verbose=False)
        domain = conn.lookupByName(self.name)
        autostart = domain.autostart()
        conn.close()
        return autostart

    @autostart.setter
    def autostart(self, autostart):
        conn = utils.connect(self.ucpe, verbose=False)
        domain = conn.lookupByName(self.name)
        if autostart:
            domain.setAutostart(1)
        else:
            domain.setAutostart(0)
        conn.close()

    @property
    def xml(self):
        #todo: use this as a cache - determine if xml is current
        #todo: this might be bad if it's slow
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        xml = domain.XMLDesc(0)
        conn.close()
        return xml

    def saveXML(self, path):
        #todo: think about whether to allow overwriting or not, possibly have some overwrite flag
        with open(path, 'w') as out:
            out.write(self.xml)

    @property
    def state(self):
        # conn = utils.connect(self.ucpe)
        # domain = conn.lookupByName(self.name)
        # state = utils.state(domain) #this is possibly completely wrong
        # conn.close()
        # return state
        with self._get_domain() as domain:
            return utils.state(domain) #this is possibly completely wrong

    def suspend(self):
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        status = domain.suspend()
        if status < 0:
            print("Failed to suspend domain", self.name)
            #todo: raise error
        else:
            print("Suspended domain", self.name)
        conn.close()

    def resume(self):
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        status = domain.resume()
        if status < 0:
            print("Failed to resume domain", self.name)
            #todo: raise error
        else:
            print("Resumed domain", self.name)
        conn.close()

    def save(self, path):
        """
        saves a persistent image of the vm to a specified path
        :param path: path on the uCPE to the desired save location
        todo: somehow enforce that a restore can happen only once from a given file
        """
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        status = domain.save(path)
        if status < 0:
            print("Failed to save domain", self.name, "to path", path)
            #todo: raise error
        else:
            print("Saved domain", self.name, "to path", path)
        self.save_path = path
        conn.close()

    def restore(self):
        if self.save_path is None:
            #todo: raise error
            print("Cannot restore without first saving.")
        conn = utils.connect(self.ucpe)
        status = conn.restore(self.save_path)
        if status < 0:
            print("Failed to restore domain from path", self.save_path)
        else:
            print("Restored domain", self.name, "from path", self.save_path)
        self.save_path = None
        conn.close()

    def shutdown(self):
        #todo: error handling
        #todo: bug - have to wait ~20 seconds after starting before stopping
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        domain.shutdown()
        print("Shutting down domain", self.name)
        conn.close()

    def destroy(self):
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        domain.destroy()
        print("Destroyed domain", self.name)
        conn.close()

    def undefine(self):
        #todo: lock all activity after undefining
        conn = utils.connect(self.ucpe)
        domain = conn.lookupByName(self.name)
        if domain.isActive():
            print("Domain is running.  Stop it first before undefining.")
            #todo: ask tyler if should be able to undefine while running
        domain.undefine()
        print("Undefined", self.name)
        conn.close()

    @contextmanager
    def _get_domain(self, verbose=False):
        try:
            conn = utils.connect(ucpe=self.ucpe, verbose=verbose)
            domain = conn.lookupByName(self.name)
            yield domain
        finally:
            conn.close()

    @classmethod
    def define(cls, ucpe, xml_path, verbose=True, autostart=False):
        #todo: set a default value for the xml
        #todo: allow an xml string input
        """
        define and start a persistent domain based on an xml configuration
        :param ucpe: UCPE object
        :param xml_path: path to xml
        :return: VirtualMachine instance representing created domain
        """
        xml_contents = utils.read(xml_path)
        conn = utils.connect(ucpe)
        domain = conn.defineXML(xml_contents) #todo: make persistent
        if domain is None:
            print("Failed to define a domain from XML", xml_path)
            #todo: define an error for this scenario
        print("Defined new domain", domain.name())
        if(autostart):
            domain.autostart(1)
            print("Set domain", domain.name(), "to autostart")
        conn.close()
        return cls(ucpe, xml_contents, domain.name())

class VMState(Enum):
    NOSTATE = libvirt.VIR_DOMAIN_NOSTATE
    RUNNING = libvirt.VIR_DOMAIN_RUNNING
    BLOCKED = libvirt.VIR_DOMAIN_BLOCKED
    PAUSED  = libvirt.VIR_DOMAIN_PAUSED
    SHUTDOWN = libvirt.VIR_DOMAIN_SHUTDOWN
    SHUTOFF = libvirt.VIR_DOMAIN_SHUTOFF
    CRASHED = libvirt.VIR_DOMAIN_CRASHED
    PMSUSPENDED = libvirt.VIR_DOMAIN_PMSUSPENDED
