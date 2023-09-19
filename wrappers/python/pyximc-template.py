from ctypes import *
from typing import Tuple
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

# ------------- API v1 -------------
# @@GENERATED_CODE@@


# ------------------ API v2 ------------------
# --- Public API м2 data types starts here ---
DeviceT = int

# --- Internal utility functions ---


def _check_device_id(device_id: DeviceT) -> None:
    try:
        id_int = int(device_id)
    except ValueError:
        raise ValueError("device_id should be integer, got device_id={} of type {}".format(device_id, type(device_id)))

    if id_int < 0:
        raise ValueError("Got negative device_id ({}). It seems the device was not opened correctly".format(device_id))


def _check_result(result: int) -> None:
    if result == Result.Ok:
        return
    if result == Result.Error:
        raise RuntimeError("General Error")

    if result == Result.NotImplemented:
        raise NotImplementedError(
            "This function is not implemented in the device."
            "Firmware update may be required: https://doc.xisupport.com/en/8smc5-usb/8SMCn-USB/XILab_application_Users_guide/Controller_Settings/About_controller.html"
        )

    if result == Result.ValueError:
        raise ValueError(
            "The input was rejected by device. Some parameters may have incorrect values." 
            "Check documentation: https://libximc.xisupport.com/doc-en/ximc_8h.html"
        )

    if result == Result.NoDevice:
        raise ConnectionError(
            "Cannot send command to the device. Check connection and power. The device_id is invalid. To resume operation you should reopen the device."
        )


# --- Public API v2 functions ---
def open_device(uri: str) -> DeviceT:
    """
    Open a device with OS uri uri and return identifier of the device which can be used in calls.

    :param str uri: a device uri. Device uri has form "xi-com:port" or "xi-net://host/serial" or "xi-emu:///file". In case of USB-COM port the "port" is the OS device uri. For example "xi-com:\\.\COM3" in Windows or "xi-com:/dev/tty.s123" in Linux/Mac. In case of network device the "host" is an IPv4 address or fully qualified domain uri (FQDN), "serial" is the device serial number in hexadecimal system. For example "xi-net://192.168.0.1/00001234" or "xi-net://hostname.com/89ABCDEF". In case of UDP protocol, use "xi-udp://<ip/host>:<port>. For example, "xi-udp://192.168.0.1:1818". Note: to open network device you must call set_bindy_key first. In case of virtual device the "file" is the full filename with device memory state, if it doesn't exist then it is initialized with default values. For example "xi-emu:///C:/dir/file.bin" in Windows or "xi-emu:///home/user/file.bin" in Linux/Mac.
    """
    device_id = DeviceT(lib.open_device(uri.encode()))
    _check_device_id(device_id)
    return device_id


def get_position(device_id: DeviceT) -> Tuple[int, int, int]:
    """
    Reads the value position in steps and micro for stepper motor and encoder steps all engines.

    :param DeviceT device_id: an identifier of device
    """
    position = get_position_t()
    _check_result(lib.get_position(device_id, byref(position)))
    return position.Position, position.uPosition, position.EncPosition


def set_engine_settings(device_id: DeviceT,
                        nom_voltage: int = 1200,
                        nom_current: int = 500,
                        nom_speed: int = 5000,
                        unom_speed: int = 64,
                        engine_flags: int = EngineFlags.ENGINE_ACCEL_ON + EngineFlags.ENGINE_LIMIT_RPM,
                        antiplay: int = 50,
                        microstep_mode: int = MicrostepMode.MICROSTEP_MODE_FRAC_256,
                        steps_per_rev: int = 200) -> None:
    """
    Set engine settings.

    This function send structure with set of engine settings to controller's memory. These settings specify motor shaft movement algorithm, list of limitations and rated characteristics. Use it when you change motor, encoder, positioner etc. Please note that wrong engine settings lead to device malfunction, can lead to irreversible damage of board.

    :param DeviceT device_id: an identifier of device
    :param int nom_voltage: Rated voltage in tens of mV.
    :param int nom_current: Rated current (in mA).
    :param int nom_speed: Nominal (maximum) speed (in whole steps/s or rpm for DC and stepper motor as a master encoder).
    :param int unom_speed: The fractional part of a nominal speed in microsteps (is only used with stepper motor).
    :param int engine_flags: Flags of engine settings.
    :param int antiplay: Number of pulses or steps for backlash (play) compensation procedure.
    :param int microstep_mode: Flags of microstep mode.
    :param int steps_per_rev: Number of full steps per revolution(Used with stepper motor only).
    """
    engine_settings = engine_settings_t(nom_voltage, nom_current, nom_speed, unom_speed, engine_flags, antiplay, microstep_mode, steps_per_rev)
    _check_result(lib.set_engine_settings(device_id, byref(engine_settings)))


def set_move_settings(device_id: DeviceT,
                      speed: int = 1000,
                      uspeed: int = 0,
                      accel: int = 1000,
                      decel: int = 1000,
                      antiplay_speed: int = 50,
                      uantiplay_speed: int = 0,
                      move_flags: int = 0) -> None:
    """
    Set command setup movement (speed, acceleration, threshold and etc).

    :param DeviceT device_id: an identifier of device
    :param int speed: Target speed (for stepper motor: steps/s, for DC: rpm).
    :param int uspeed: Target speed in microstep fractions/s.
    :param int accel: Motor shaft acceleration, steps/s^2(stepper motor) or RPM/s(DC).
    :param int decel: Motor shaft deceleration, steps/s^2(stepper motor) or RPM/s(DC).
    :param int antiplay_speed: Speed in antiplay mode, full steps/s(stepper motor) or RPM(DC).
    :param int uantiplay_speed: Speed in antiplay mode, microsteps/s.
    :param int move_flags: Flags of the motion parameters.
    """
    move_settings = move_settings_t(speed, uspeed, accel, decel, antiplay_speed, uantiplay_speed, move_flags)
    _check_result(lib.set_move_settings(device_id, move_settings))


def command_move(device_id: DeviceT,
                 position: int,
                 uposition: int = 0) -> None:
    """
    Upon receiving the command "move" the engine starts to move with pre-set parameters (speed, acceleration, retention), to the point specified to the Position, uPosition.

    For stepper motor uPosition sets the microstep, for DC motor this field is not used.

    :param DeviceT device_id: an identifier of device
    :param int position: position to move.
    :param int uposition: part of the position to move, microsteps. Microstep size and the range of valid values for this field depend on selected step division mode (see MicrostepMode field in engine_settings)."""
    _check_result(lib.command_move(device_id, position, uposition))


def command_stop(device_id: DeviceT) -> None:
    """
    Immediately stop the engine, the transition to the STOP, mode key BREAK (winding short-circuited), the regime "retention" is deactivated for DC motors, keeping current in the windings for stepper motors (with Power management settings).

    When this command is called, the ALARM flag is reset.

    :param DeviceT device_id: an identifier of device
    """
    _check_result(lib.command_stop(device_id))


def command_power_off(device_id: DeviceT):
    """
    Immediately power off motor regardless its state.

    Shouldn't be used during motion as the motor could be power on again automatically to continue movement. The command is designed for manual motor power off. When automatic power off after stop is required, use power management system.

    :param DeviceT device_id: an identifier of device
    """
    _check_result(lib.command_power_off)


# vim: set ft=python
