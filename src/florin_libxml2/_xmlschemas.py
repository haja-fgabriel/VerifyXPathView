from ctypes import cdll, c_char_p, c_int, CFUNCTYPE, byref
from . import florin_libxml2

libxml_error = None


def load_schema(path):
    path = c_char_p(path.encode())
    encoding = c_char_p("UTF-8".encode())
    default_options = c_int(0)
    
    # Initialize the libxml2 parser
    florin_libxml2.xmlInitParser()
    #florin_libxml2.xmlSetGenericErrorFunc(None, byref(handle_libxml_error))
    doc = florin_libxml2.xmlReadFile(path, encoding, default_options)
    if not doc:
        raise Exception("Unknown error in the xmlReadFile function call!")
