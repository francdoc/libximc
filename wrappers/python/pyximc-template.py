from ctypes import *
import os
import platform
import struct
import sys


# Load library
def _load_specific_lib(path, load_method):
    try:
        lib = load_method(path)
        return lib
    except OSError as err:
        raise RuntimeError("Error loading file {} - {}".format(path, str(err)))


def _near_script_path(libname) -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), libname)


def _load_lib():
    os_kind = platform.system().lower()
    if os_kind == "windows":
        if sys.version_info[0] == 3 and sys.version_info[0] >= 8:
            method = lambda path: WinDLL(path, winmode=RTLD_GLOBAL)
        else:
            method = WinDLL
        if 8 * struct.calcsize("P") == 32:
            libs = "bindy.dll", "xiwrapper.dll", "libximc.dll"
            dirs = _near_script_path("win32"), _near_script_path(""), ""
        else:
            libs = "bindy.dll", "xiwrapper.dll", "libximc.dll"
            dirs = _near_script_path("win64"), _near_script_path(""), ""
    elif os_kind == "linux":
        method = CDLL
        cpu_kind = platform.machine().lower()
        libs = "libbindy.so", "libxiwrapper.so", "libximc.so"
        if cpu_kind == "arm":
            cpu_path = "debian-armhf"
        elif cpu_kind == "i386":
            cpu_path = "debian-i386"
        else:
            cpu_path = "debian-amd64"
        print(cpu_kind)
        dirs = _near_script_path(cpu_path), _near_script_path(""), ""
    elif os_kind == "darwin":
        method = CDLL
        libs = ("libjximc.dylib",)
        dirs = _near_script_path("macosx"), _near_script_path(""), ""
    else:
        raise RuntimeError("Unexpected OS: {}".format(os_kind))

    def load_from_directory(libs, dirname):
        paths = [os.path.join(dirname, lib) for lib in libs]
        for path in paths:
            lib = _load_specific_lib(path, method)
        # libximc is loaded last
        return lib

    errors = []
    for dirname in dirs:
        try:
            lib = load_from_directory(libs, dirname)
        except Exception as exc:
            errors.append(str(exc))
        else:
            return lib

    if os_kind == "darwin":
        try:
            lib = CDLL("libximc.framework/libximc")
        except Exception as exc:
            errors.append(str(exc))
        else:
            return lib

    error_msg = "Unable to load library. Paths tried:\n" + "\n".join(errors)
    raise RuntimeError(error_msg)


# use cdecl on unix and stdcall on windows
def ximc_shared_lib():
    """
    if platform.system() == "Linux":
        return CDLL("libximc.so")
    elif platform.system() == "FreeBSD":
        return CDLL("libximc.so")
    elif platform.system() == "Darwin":
        return CDLL("libximc.framework/libximc")
    elif platform.system() == "Windows":
        if sys.version_info[0] == 3 and sys.version_info[0] >= 8:
            return WinDLL("libximc.dll", winmode=RTLD_GLOBAL)
        else:
            return WinDLL("libximc.dll")
    else:
        return None
    """

    return _load_lib()


lib = ximc_shared_lib()


# Common declarations
class Result:
    Ok = 0
    Error = -1
    NotImplemented = -2
    ValueError = -3
    NoDevice = -4


class calibration_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('A', c_double),
        ('MicrostepMode', c_uint)
    ]


class device_enumeration_t(LittleEndianStructure):
    pass


class device_network_information_t(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('ipv4', c_uint32),
        ('nodename', c_char * 16),
        ('axis_state', c_uint),
        ('locker_username', c_char * 16),
        ('locker_nodename', c_char * 16),
        ('locked_time', c_ulonglong),
    ]


# Clarify function types
lib.enumerate_devices.restype = POINTER(device_enumeration_t)
lib.get_device_name.restype = c_char_p


# @@GENERATED_CODE@@



# vim: set ft=python
