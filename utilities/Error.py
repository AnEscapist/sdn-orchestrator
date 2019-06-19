class Error(Exception):
    def __init__(self, message):
        super()
        print(type(self).__name__ + ":", message)



