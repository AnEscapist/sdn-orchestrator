import ucpe.libvirt.utils as utils

class VirtualMachine():
    def __init__(self, xml, ucpe):
        self.xml = xml
        self.ucpe = ucpe




    @classmethod
    def create(cls, xml, ucpe):
        """
        create a persistent domain based on an xml configuration
        :param xml: path to xml
        :return: VirtualMachine instance representing created domain
        """
        xml_contents = utils.read(xml)
        return VirtualMachine(xml)



