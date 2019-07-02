from utilities.Error import Error


class ReadOnlyError(Error):
    def __init__(self):
        message = "Attribute is read-only."
        Error.__init__(self, message)


class DomainNotFoundError(Error):
    def __init__(self, name="UNKNOWN_NAME"):
        message = "Domain with name " + name + " could not be found"
        Error.__init__(self, message)


class OperationFailedError(Error):
    def __init__(self, name="UNKNOWN_NAME"):
        message = "Operation " + name + " failed"
        Error.__init__(self, message)
