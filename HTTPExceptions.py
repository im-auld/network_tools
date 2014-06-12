class HTTPException(Exception):
    pass
    
class HTTP400Error(HTTPException):
    """ Pyhton exception for HTTP 400: Bad Request """
    def __init__(self, message):
        self.message = message
        self.code = '400'
    
    def __str__(self):
        return repr(self.message)
        
class HTTP404Error(HTTPException):
    """ Pyhton exception for HTTP 404: Resource Not Found """
    def __init__(self, message):
        self.message = message
        self.code = '404'
    
    def __str__(self):
        return repr(self.message)
        
class HTTP405Error(HTTPException):
    """ Pyhton exception for HTTP 405: Method Not Allowed """
    def __init__(self, message):
        self.message = message
        self.code = '405'
    
    def __str__(self):
        return repr(self.message)