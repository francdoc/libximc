'''
A python wrapper for Standa actuators using Stepper API. 
'''

from standa.pyximc import *
import tempfile
from standa.Stepper import Stepper
import re
import time
from collections import deque

print("...........................")
print("pystanda imported")
print("...........................")
print("booting system")
print("...........................")

if sys.version_info >= (3,0):
    import urllib.parse

# Data structure to store device parameters
data = {
    "dev_count": 0,
    "open_name": None,
    "flag_virtual": False,
    "open_name_deque": deque(),
    "STANDA_X_ID": None,
    "STANDA_Y_ID": None,
    "STANDA_Z_ID": None,
    "act_deque": deque(),
    "act_x": None,
    "act_y": None,
    "act_z": None
}

# ############################################# FOR PYSTANDA EXTERNAL USE #####################################################

def detecthw():
    """
    Detects the number of Standa devices connected to the computer and returns the number of devices detected.
    """
    # This is device search and enumeration with probing. It gives more information about devices.
    probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
    enum_hints = b"addr="
    # enum_hints = b"addr=" # Use this hint string for broadcast enumerate
    devenum = lib.enumerate_devices(probe_flags, enum_hints)
    print("Device enum handle: " + repr(devenum))
    print("Device enum handle type: " + repr(type(devenum)))

    time.sleep(1)

    dev_count = lib.get_device_count(devenum)
    print("...........................")
    print("Device count: " + repr(dev_count))
    print("...........................")
    print("standa controller numeration goes from 0 to "+str(int(dev_count-1)) +"\n")
    print("...........................")

    controller_name = controller_name_t()
    for dev_ind in range(0, dev_count):
        enum_name = lib.get_device_name(devenum, dev_ind)
        result = lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))
        if result == Result.Ok:
            print("Enumerated device #{} name (port name): ".format(dev_ind) + repr(enum_name) + ". Friendly name: " + repr(controller_name.ControllerName) + ".")
            
    time.sleep(1)

    flag_virtual = 0

    if dev_count == 0: # no physical devices connected to the computer
        if sys.version_info >= (3,0):
            open_name = None
            # use URI for virtual device when there is new urllib python3 API
            tempdir = tempfile.gettempdir() + "/testdevice.bin"
            if os.altsep:
                tempdir = tempdir.replace(os.sep, os.altsep)
            # urlparse build wrong path if scheme is not file
            uri = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme="file", \
                    netloc=None, path=tempdir, params=None, query=None, fragment=None))
            open_name = re.sub(r'^file', 'xi-emu', uri).encode()
            flag_virtual = 1
            print("virtual flag: ",flag_virtual)
            print("The real controller is not found or busy with another app.")
            print("The virtual controller is opened to check the operation of the library.")
            print("If you want to open a real controller, connect it or close the application that uses it.")

            time.sleep(0.10)

            if not open_name:
                exit(1)

            if type(open_name) is str:
                open_name = open_name.encode()
                data["open_name"] = open_name

            print("\nOpen simulated device " + repr(open_name))
            
            time.sleep(0.10)
            
            print("...........................")

    open_name_deque = deque()

    STANDA_X_ID = None
    STANDA_Y_ID = None
    STANDA_Z_ID = None

    if dev_count > 0: # there are physical devices connected to the computer
        
        for i in range(dev_count):
            ##################### STANDA HARDWARE DEVICE DETECTION #######################
            if len(sys.argv) > 1:
                open_name_deque = sys.argv[1]

            elif dev_count > 0:
                standa_device = lib.get_device_name(devenum, i)
                open_name_deque.append(standa_device)
            ##############################################################################

            time.sleep(0.5)

            if not open_name_deque[i]:
                exit(1)

            if type(open_name_deque[i]) is str:
                open_name_deque[i] = open_name_deque[i].encode()

            print("\nOpen real device " + repr(open_name_deque[i]))

            print("...........................")
            print("deque of standa devices: ",open_name_deque)
            print("...........................")

            """
            Standa ID dictionary (for future development):

            Pair X-Y number 1 (Linux OS):
            b'xi-com:///dev/ximc/00007A09'
            b'xi-com:///dev/ximc/000079DF'

            Pair X-Y number 2 (Linux OS):
            b'xi-com:///dev/ximc/00007D41'
            b'xi-com:///dev/ximc/00007D42'

            Pair X-Y: number 3 (Linux OS):
            b'xi-com:///dev/ximc/00007D3C'
            b'xi-com:///dev/ximc/00007D13'
            
            Single Z 1 (Linux OS):
            b'xi-com:///dev/ximc/00007B0B'

            Single Z 2 (Linux OS):
            b'xi-com:///dev/ximc/00007BAE'
            
            Single Z 3 (Linux OS):
            b'xi-com:///dev/ximc/0000779D'

            Individual device (single controller) for Windows OS example:
            b'xi-com:\\\\.\\COM5'
            """

            # TODO: 
            #       * pystanda.py needs in the future to adapt to the controller selected (dual or single).
            #       * And to assign X,Y or Z axes according to the axes (AXIS 1 or AXIS 2) in use.

            if len(open_name_deque) == 2:                 
                # Convert deque objects to tuples for using as keys in the dictionary
                open_name_deque_tuple = tuple(open_name_deque)

                # Define the expected device pairs for different configurations
                EXPECTED_DEVICES = {
                    # Pair X-Y number 1 (Linux OS)
                    tuple([b'xi-com:///dev/ximc/00007A09', b'xi-com:///dev/ximc/000079DF']): (b'xi-com:///dev/ximc/00007A09', b'xi-com:///dev/ximc/000079DF'),

                    # Pair X-Y number 2 (Linux OS)
                    tuple([b'xi-com:///dev/ximc/00007D41', b'xi-com:///dev/ximc/00007D42']): (b'xi-com:///dev/ximc/00007D41', b'xi-com:///dev/ximc/00007D42'),

                    # Pair X-Y: number 3 (Linux OS)
                    tuple([b'xi-com:///dev/ximc/00007D3C', b'xi-com:///dev/ximc/00007D13']): (b'xi-com:///dev/ximc/00007D3C', b'xi-com:///dev/ximc/00007D13')
                }

                # Check if the open_name_deque_tuple is in the EXPECTED_DEVICES dictionary
                if open_name_deque_tuple in EXPECTED_DEVICES:
                    STANDA_X_ID, STANDA_Y_ID = EXPECTED_DEVICES[open_name_deque_tuple]
                    print("STANDA_X_ID:", STANDA_X_ID)
                    print("STANDA_Y_ID:", STANDA_Y_ID)
                else:
                    print("Unexpected device IDs:", open_name_deque_tuple)

            if len(open_name_deque) == 1:
                    STANDA_X_ID = None
                    STANDA_Y_ID = None
                    STANDA_Z_ID = open_name_deque[0] # attaching the identified single controller to STANDA_Z_ID
                    
    print("STANDA_X_ID:", STANDA_X_ID)
    print("STANDA_Y_ID:", STANDA_Y_ID)
    print("STANDA_Z_ID:", STANDA_Z_ID)

    data["dev_count"] = dev_count
    data["flag_virtual"] = flag_virtual
    data["open_name_deque"] = open_name_deque
    data["STANDA_X_ID"] = STANDA_X_ID
    data["STANDA_Y_ID"] = STANDA_Y_ID
    data["STANDA_Z_ID"] = STANDA_Z_ID

    return dev_count,flag_virtual,open_name_deque, STANDA_X_ID, STANDA_Y_ID, STANDA_Z_ID

def showaxis():
    """
    Shows the axis contained in the deque.
    """
    open_name_deque = data["open_name_deque"]
    print(open_name_deque)

def grab(n:int): # device number to grab
    """
    Grabs the device n from the deque.
    """
    STANDA_X_ID = data["STANDA_X_ID"]
    STANDA_Y_ID = data["STANDA_Y_ID"]
    STANDA_Z_ID = data["STANDA_Z_ID"]
    flag_virtual = data["flag_virtual"]
    dev_count = data["dev_count"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]

    print("...........................")
    n = int(n)
    if flag_virtual == 1: # no actual devices
        bklash_simu = 0 # simulated backlash compensation for imaginary actuator
        print(f"open_name: {open_name}")
        act = Stepper(open_name,bklash_simu) # grabbing virtual actuator and instancing Stepper class for it.
        act_deque.append(act)
        print(f"virtual actuator: {act_deque}")
        print("...........................")
        print("<<<<<<<< WARNING >>>>>>>>")
        print("Grabbed a virtual axis, did not grab real device.")
        print("<<<<<<<<< EXIT >>>>>>>>>>")
        print("...........................")
        exit()
    
    if dev_count > 0:
        ########################### HARDCODED BACKLASH COMPENSATION ###########################
        bklash_0 = 0 # initial backlash compensation for axis 0
        bklash_1 = 0 # initial backlash compensation for axis 1
        bklash_2 = 0 # initial backlash compensation for axis 2
        #######################################################################################
        if n == 0:
            try:
                act_x = Stepper(STANDA_X_ID,bklash_0) # grabbing actuator 0 and instancing Stepper class for it.
                act_deque.append(act_x)
                data["act_x"] = act_x
                print("grabbed actuator: ",act_deque)
                return True, act_deque
            except Exception as e:
                print(f"ERROR: could not grab actuator 0")
                print(e)
                return False
        if n == 1:
            try:
                act_y = Stepper(STANDA_Y_ID,bklash_1) # grabbing actuator 1 and instancing Stepper class for it.
                act_deque.append(act_y)
                data["act_y"] = act_y
                print("grabbed actuator: ",act_deque)
                return True, act_deque
            except Exception as e:
                print(f"ERROR: could not grab actuator 1")
                print(e)
                return False
        if n == 2:
            try:
                act_z = Stepper(STANDA_Z_ID,bklash_2)
                act_deque.append(act_z)
                data["act_z"] = act_z
                print("grabbed actuator: ",act_deque)
                return True, act_deque
            except Exception as e:
                print(f"ERROR: could not grab actuator 2")
                print(e)
                return False
    print("............................")
    # update data
    data["act_deque"] = act_deque
    
#####################################################################################################
#### FUNCTIONS FROM STEPPER CLASS (LOCATED in Stepper.py) ACCESSED IN THIS API THROUGH act_deque ####
"""
set_bklash
get_bklash
set_speed
set_accel
stop_movement
get_pos
get_pid
set_pid
move
get_feedback_settings
test_engine
get_movement_settings
get_gear_settings
get_encoder_settings
set_feedback_type
set_backlash_mode
set_encoder_settings
set_engine_flag
"""
#####################################################################################################

def setbklash(n:int,bklash:int):
    """
    Sets backlash compensation for the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]

    print("...........................")
    n = int(n)
    bklash = int(bklash)
    if flag_virtual == 1: # no actual devices
        print(f"open_name: {open_name}")
        act = act_deque[n]
        print(f"virtual actuator act: {act}")
    if dev_count > 0: # several devices detected
        if n == 0:
            act = act_x
        if n == 1:
            act = act_y
        if n == 2:
            act = act_z
        print(f"actuator instance: {act}")
        try:
            act.set_bklash(bklash)
        except Exception as e:
            print(f"ERROR: could not configure new backlash")
            print(e)

def getbklash(n:int):
    """
    Gets backlash compensation for the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    n = int(n)
    if flag_virtual == 1: # no actual devices
        print("open_name: ",open_name)
        act = act_deque[n]
        print("virtual actuator act: ",act)
    if dev_count > 0: # several devices detected
        if n == 0:
            act = act_x
        if n == 1:
            act = act_y
        if n == 2:
            act = act_z
        print("actuator instance: ",act)
        try:
            bklash = act.get_bklash()
            print("backlash for axis: "+str(n))
            print(bklash)
            return bklash
        except Exception as e:
            print("ERROR: could not get backlash")
            print(e)
        print("...........................")

def speedacc(n:int,speed:int,accel:int,decel:int):
    """
    Sets speed, acceleration and deceleration for the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    n = int(n)
    speed = int(speed)
    accel = int(accel)
    decel = int(decel)
    if flag_virtual == 1: # no actual devices
        print("open_name: ",open_name)
        act = act_deque[n]
        print("virtual actuator act: ",act)
    if dev_count > 0: # several devices detected
        if n == 0:
            act = act_x
        if n == 1:
            act = act_y
        if n == 2:
            act = act_z
        print(f"actuator instance: {act}")
    try:
        act.set_speed(speed) # maximum speed in steps per second
        act.set_accel(accel,decel) # maximum acceland decel in steps per second squared
        print("...........................")
        print(f"standa instance {act}")
        print(f"standa instance {act.set_speed}")
        print(f"standa instance {act.set_accel}")
        print("...........................")
        return True
    except Exception as e:
        print(f"ERROR: could not configure speed and acceleration for {act}")
        print(e)
        return False

def stop(n:int):
    """
    Stops the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        print("stopping command sent")
        act.stop_movement()
        print('reached position = '+repr(act.get_pos()))
        print("...........................")
    except Exception as e:
        print("ERROR: could not stop")
        print(e)

def getpos(n:int):
    """
    Gets the position of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    if flag_virtual == 1: # no actual devices
        print("open_name: ",open_name)
        act = act_deque[n]
        print("virtual actuator act: ",act)
    if dev_count > 0: # several devices detected
        if n == 0:
            act = act_x
        if n == 1:
            act = act_y
        if n == 2:
            act = act_z
        print("actuator instance: ",act)
    res = act.get_pos()
    print("actual position: ",res)
    print("...........................")
    return res

def getpid(n:int):
    """
    Gets the PID parameters of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    if flag_virtual == 1: # no actual devices
        print("open_name: ",open_name)
        act = act_deque[n]
        print("virtual actuator act: ",act)
    if dev_count > 0: # several devices detected
        if n == 0:
            act = act_x
        if n == 1:
            act = act_y
        if n == 2:
            act = act_z
        print("actuator instance: ",act)
    act_getpid = act.get_pid()
    print("pid: ",act_getpid)
    print("...........................")
    return act_getpid

def set_pid(n,KpU:int,KiU:int,KdU:int,Kpf:float,Kif:float,Kdf:float):
    """
    Sets the PID parameters of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    try:
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        if (KpU or KiU or KdU or Kpf or Kif or Kdf) > 0: 
            act.set_pid(KpU,KiU,KdU,Kpf,Kif,Kdf)
        else:
            print("negative control values are not accepted")
    except Exception as e:
        print("ERROR: could not set pid configuration")
        print(e)

def shift(n:int,steps:float): # steps -> movement shift -> relative steps movement
    """
    Shifts the device n by steps steps.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    ####### internal conditions for movement call ################
    if steps == 0:
        print("Step of 0 not allowed.")
        return False
    #############################################################
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print(f"actuator instance: {act}")
        steps = float(steps)
        print(f"get_pos(): {act.get_pos()}")
        print(f"moving {str(steps)} steps")
        destiny_position = float(act.get_pos() + steps) # other option is to use int(act.get_pos())
        print(f"destiny position: {destiny_position}")
        ##################### movement call #####################
        res = act.move(steps,destiny_position)
        print("pystanda shift res: ",res)
        #########################################################
        return res # returns True if movement was successful
    
    except Exception as e:
        print("ERROR: could not move")
        print(e)
        return False

def get_feedback_data(n):
    """
    Gets the feedback data of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        act_getfeedbk = act.get_feedback_settings()
        print("Encoder feedback: ",act_getfeedbk)
        print("...........................")
    except Exception as e:
        print("ERROR: could not get feedback data")
        print(e)

def get_engine_data(n):
    """
    Gets the engine data of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        act_testeng= act.test_engine()
        print("Test engine: ",act_testeng)
        print("...........................")
    except Exception as e:
        print("ERROR: could not get test engine data")
        print(e)

def get_move_settings(n):
    """
    Gets the move settings data of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        act_getmovesett = act.get_movement_settings()
        print("Move settings data: ",act_getmovesett)
        print("...........................")
    except Exception as e:
        print("ERROR: could not get nove settings data")
        print(e)

def get_gear_settings(n):
    """
    Gets the gear settings data of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        act_getgearsett = act.get_gear_settings()
        print("Gear settings data: ",act_getgearsett)
        print("...........................")
    except Exception as e:
        print("ERROR: could not get gear settings data")
        print(e)

def get_encoder_settings(n):
    """
    Gets the encoder settings data of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        act_getencsett = act.get_encoder_settings()
        print("Encoder settings data: ",act_getencsett)
        print("...........................")
    except Exception as e:
        print("ERROR: could not get encoder settings data")
        print(e)

def set_feedback_type(n:int,IPS:int,feedbk_type:int,feedbk_flags:int,counts_per_turn:int):
    """
    - Used with 8SMC5-USB-B9-2 Two Axis Controller.
    - 8SMC5-USB-B9-2 Two Axis Controller -> the front panel also contains status LED, left and right limit switch LED, left and right movement buttons for each of the two controller boards of the two-axis system.
    - Additional resources: https://doc.xisupport.com/en/8smc5-usb/8SMC5-USB.pdf -> 4.1.3.1 Enclosure view.
    -----------------------------
    - n = standa_number_device (axis)
    -----------------------------
    - IPS: the number of encoder counts per shaft revolution. Range: 1..65535. The field is obsolete, it is recommended to write 0 to IPS and use the extended 
    CountsPerTurn field.
    -----------------------------
    feedbk_type dictionary:
    - 1 = FEEDBACK_ENCODER                 = 0x01 # THIS IS KEY
    - 2 = FEEDBACK_EMF                     = 0x04
    - 3 = FEEDBACK_NONE                    = 0x05
    - 4 = FEEDBACK_ENCODER_MEDIATED        = 0x06
    -----------------------------
    feedbk_flags dictionary:
    - 1 = FEEDBACK_ENC_REVERSE             = 0x01
    - 2 = FEEDBACK_ENC_TYPE_BITS           = 0xC0
    - 3 = FEEDBACK_ENC_TYPE_AUTO           = 0x00
    - 4 = FEEDBACK_ENC_TYPE_SINGLE_ENDED   = 0x40 # THIS IS KEY
    - 5 = FEEDBACK_ENC_TYPE_DIFFERENTIAL   = 0x80
    -----------------------------
    - CountsPerTurn: the number of encoder counts per shaft revolution. Range: 1..4294967295. To use the CountsPerTurn field, write 0 in the IPS field, otherwise the value from
    the IPS field will be used.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    IPS = int(IPS)
    feedbk_type = int(feedbk_type)
    feedbk_flags = int(feedbk_flags)
    counts_per_turn = int(counts_per_turn)
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print(f"open_name: {open_name}")
            act = act_deque[n]
            print(f"virtual actuator act: {act}")
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print(f"actuator instance: {act}")
        act.set_feedback_type(IPS,feedbk_type,feedbk_flags,counts_per_turn)
    except Exception as e:
        print("ERROR: could not set feedback type")
        print(e)

def set_backlash_type(n,backlash_steps, backlash_speed):
    """
    Sets the backlash type of the device n.
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    backlash_steps = int(backlash_steps)
    backlash_speed = float(backlash_speed)
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print("actuator instance: ",act)
        act.set_backlash_mode(backlash_steps,backlash_speed)
    except Exception as e:
        print("ERROR: could not set backlash mode")
        print(e)

def set_encoder_type(n:int,enc_flag:int):
    """
    - n = standa_number_device (axis)
    -----------------------------
    enc_flag dictionary:
    - 1 = ENCSET_DIFFERENTIAL_OUTPUT = 0x001
    - 2 = ENCSET_PUSHPULL_OUTPUT = 0x004 # THIS IS KEY
    - 3 = ENCSET_INDEXCHANNEL_PRESENT = 0x010
    - 4 = ENCSET_REVOLUTIONSENSOR_PRESENT = 0x040
    - 5 = ENCSET_REVOLUTIONSENSOR_ACTIVE_HIGH = 0x100
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    enc_flag = int(enc_flag)
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print("open_name: ",open_name)
            act = act_deque[n]
            print("virtual actuator act: ",act)
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print(f"actuator instance: {act}")
        act.set_encoder_settings(enc_flag)
    except Exception as e:
        print("ERROR: could not set encoder mode")
        print(e)
        
def set_engine_flag(n:int,eng_flag:int):
    """
     - n = standa_number_device (axis)
    -----------------------------
    eng_flag dictionary:
    - 1 = ENGINE_REVERSE        = 0x01 # THIS IS KEY
    - 2 = ENGINE_CURRENT_AS_RMS = 0x02
    - 3 = ENGINE_MAX_SPEED      = 0x04
    - 4 = ENGINE_ANTIPLAY       = 0x99 
    - 5 = ENGINE_ACCEL_ON       = 0x10
    - 6 = ENGINE_LIMIT_VOLT     = 0x20
    - 7 = ENGINE_LIMIT_CURR     = 0x40
    - 8 = ENGINE_LIMIT_RPM      = 0x80
    """
    flag_virtual = data["flag_virtual"]
    open_name = data["open_name"]
    act_deque = data["act_deque"]
    act_x = data["act_x"]
    act_y = data["act_y"]
    act_z = data["act_z"]
    dev_count = data["dev_count"]
    
    print("...........................")
    eng_flag = int(eng_flag)
    try:
        n = int(n)
        if flag_virtual == 1: # no actual devices
            print(f"open_name: {open_name}")
            act = act_deque[n]
            print(f"virtual actuator act {act}")
        if dev_count > 0: # several devices detected
            if n == 0:
                act = act_x
            if n == 1:
                act = act_y
            if n == 2:
                act = act_z
            print(f"actuator instance {act}")
        act.set_engine_flag(eng_flag)
    except Exception as e:
        print(f"ERROR: could not set engine flag for {act}")
        print(e)

def swapaxis():
    """
    Swaps the 2 axis in the actuator deque.
    """
    act_deque = data["act_deque"]
    print("...........................")
    if len(act_deque)==2:
        print("Original actuator deque structure: ",act_deque)
        print("Swapping the 2 axis.")
        act_deque[0], act_deque[1] = act_deque[1], act_deque[0]
        print("Swapped actuator deque structure: ",act_deque)
    else:
        print("Deque must be of size 2. The 2 axis must be grabbed.")
    print("...........................")

def cleanaxis():
    """
    Clears the actuator deque.
    """
    act_deque = data["act_deque"]    
    print("...........................")
    try:
        act_deque.clear()
        print(f"Actuator deque has been cleared: {act_deque}")
    except Exception as e:
        print(e)
    print("...........................")