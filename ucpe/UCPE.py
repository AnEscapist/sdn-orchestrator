import ucpe.libvirt_controller.utils as virtutils


class UCPE():
    def __init__(self, username, hostname, libvirt_driver=virtutils.DRIVER, libvirt_transport=virtutils.TRANSPORT,
                 libvirt_port=virtutils.PORT, libvirt_path=virtutils.PATH,
                 libvirt_extra_params=virtutils.EXTRAPARAMETERS, use_libvirt=True):
        """
        constructor
        :param username: username of account on uCPE
        :param hostname: hostname of uCPE (possibly IP address)

        libvirt_controller URI parameters:
        Description: https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Connections-Remote_URIs.html
        :param libvirt_driver:
        :param libvirt_transport:
        :param libvirt_port:
        :param libvirt_path:
        :param libvirt_extra_params:

        :param use_libvirt: if True, initialize fields for the URI parameters
        """
        # TODO: determine which of these field should be immutable
        # Someday: make a config file for the libvirt_controller stuff
        self.username = username
        self.hostname = hostname
        if libvirt_driver or use_libvirt: self.driver = libvirt_driver; use_libvirt = True
        if libvirt_transport or use_libvirt: self.libvirt_transport = libvirt_transport; use_libvirt = True
        if libvirt_port or use_libvirt: self.libvirt_port = libvirt_port; use_libvirt = True
        if libvirt_path or use_libvirt: self.libvirt_path = libvirt_path; use_libvirt = True
        if libvirt_extra_params or use_libvirt: self.libvirt_extra_params = libvirt_extra_params; use_libvirt = True

    @classmethod
    def from_kwargs(cls, **kwargs):
        #todo: consider if this is necessary
        username = kwargs["username"]
        hostname = kwargs["hostname"]
        libvirt_driver = kwargs.get("libvirt_driver", virtutils.DRIVER)
        libvirt_transport = kwargs.get("libvirt_transport", virtutils.TRANSPORT)
        libvirt_port = kwargs.get("libvirt_port", virtutils.PORT)
        libvirt_path = kwargs.get("libvirt_path", virtutils.PATH)
        libvirt_extra_params = kwargs.get("libvirt_extra_params", virtutils.EXTRAPARAMETERS)
        use_libvirt = kwargs.get("use_libvirt", True)
        return cls(username, hostname, libvirt_driver=libvirt_driver, libvirt_transport=libvirt_transport,
                    libvirt_port=libvirt_port, libvirt_path=libvirt_path, libvirt_extra_params=libvirt_extra_params,
                    use_libvirt=use_libvirt)
