from utilities.Error import Error

class ReadOnlyError(Error):
    def __init__(self):
        message = "Attribute is read-only."
        Error.__init__(self, message)

class DomainNotFoundError(Error):
    def __init__(self, domain_name):
        message = "Domain with name " + domain_name + " could not be found."
        Error.__init__(self, message)

class OperationFailedError(Error):
    def __init__(self):
        message = "Operation failed."
        Error.__init__(self, message)

raise DomainNotFoundError("mydomain")





