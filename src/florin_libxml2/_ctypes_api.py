from ctypes import cdll, CFUNCTYPE, c_void_p, c_char_p
from pathlib import Path
import platform

CURRENT_ARCH = platform.architecture()
BITNESS, CURRENT_OS = CURRENT_ARCH

def _get_libxml2_path():
    if CURRENT_OS == "WindowsPE":
        libxml2_path = Path("libxml2.dll")
    else:
        raise NotImplementedError(f"For non-Windows users: please specify the " + \
                                f"path to the libxml2 library in '{__file__}'.")
    return libxml2_path.resolve()

florin_libxml2 = cdll.LoadLibrary(str(_get_libxml2_path()))

"""
The original C declaration:

typedef void (*xmlGenericErrorFunc) (void *ctx,
				 const char *msg,
				 ...) LIBXML_ATTR_FORMAT(2,3);
"""
xmlGenericErrorFunc = CFUNCTYPE(c_void_p, c_char_p, )