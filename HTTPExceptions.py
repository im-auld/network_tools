class HTTP400Error(Exception):
    """ Pyhton exception for HTTP 400: Bad Request """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)
        
class HTTP404Error(Exception):
    """ Pyhton exception for HTTP 404: Resource Not Found """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)
        
class HTTP405Error(Exception):
    """ Pyhton exception for HTTP 405: MEthod Not Allowed """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)