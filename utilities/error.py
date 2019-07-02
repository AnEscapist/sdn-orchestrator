class Error(Exception):
    def __init__(self, message):
        super()
        self.message = type(self).__name__ + ": "  + message

    def __str__(self):
        return self.message

    def __rep__(self):
        return self.message

