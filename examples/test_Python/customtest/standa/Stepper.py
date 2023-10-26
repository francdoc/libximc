'''
 Stepper class for controlling the stepper motor actuator.
    
 Development resources:
    - http://files.xisupport.com/8SMC4-USB_Programming_manual_Eng.pdf
    - https://doc.xisupport.com/en/8smc5-usb/8SMC5-USB.pdf
    - https://www.standa.lt/products/catalog/motorised_positioners?item=525
 
 '''

from time import sleep
from standa.pyximc import *
import math
import time
from collections import deque

# Set bindy (network) keyfile. Must be called before any call to "enumerate_devices" or "open_device" if you
# wish to use network-attached controllers. Accepts both absolute and relative paths, relative paths are resolved
# relative to the process working directory. If you do not need network devices then "set_bindy_key" is optional.
# In Python make sure to pass byte-array object to this function (b"string literal").
result = lib.set_bindy_key(os.path.join("keyfile.sqlite").encode("utf-8"))
if result != Result.Ok:
    lib.set_bindy_key("keyfile.sqlite".encode("utf-8")) # Search for the key file in the current directory.

########################################################################
#                               CONSTANTS
########################################################################
MAX_ACCEL = 65535 # <Max accel in steps per second squared
MAX_DECEL = 65535 # <Max decel in steps per second squared
MAX_SPEED = 35000 # <Max speed in steps per second
MAX_BACKLASH_SPEED = 5000 # <Max backlash speed in steps per second
NOMINAL_SPEED = 5000 # <Nominal speed in steps per second
DEFAULT_SPEED = 5000 # <Default speed in steps per second
DEFAULT_ACCEL = 5000 # <Default acceleration in steps per second squared
DEFAULT_DECEL = 5000 # <Default deceleration in steps per second squared
WAIT_REFRESH_INTERVAL = 100

STANDA_ERROR_SHIFT = 1 # steps error margin for the actuator
STANDA_REFRESH_SHIFT = 0.25 # seconds to wait for the actuator to refresh its position
STANDA_OSCILATION_TOLERANCE = 1 # steps error margin for the actuator
STANDA_TIMEOUT = 2 # seconds to wait for the actuator to refresh its position

class Stepper():
    """
    Class that represents arbitrary stepper actuator.

    # NOTE: this class adapts depending on the motor encoder type. It can be single_ended_encoder_flag True or False.
    
    """
    def  __init__(self, name, bklash, speed=DEFAULT_SPEED, accel=DEFAULT_ACCEL, decel=DEFAULT_DECEL):
        # Hardware check
        print("Hardware check for actuator (Stepper class): ",name)
        # /////////////////////// SAVING ACTUATOR DEVICE NAME ////////////////////
        print(f"Hardware check for actuator (Stepper class): {str(name)}.")
        # ////////////////////////////////////////////////////////////////////////
        self._id = lib.open_device(name)
        print(f"Device ID: {str(self._id)}")
        if self._id == -1:
            print(f"Error opening actuator, invalid name: {repr(name)}")
            return
        if not self.test_info():
            print(f"Error in printing device n {str(self._id)} information\n")
            return
        if not self.test_status():
            print(f"Error in printing device n {str(self._id)} status\n")
            return

        self.single_ended_encoder_flag = None # we start with a None value for the single_ended encoder flag

        # Get encoder settings, this will be used to check if the actuator has an single_ended encoder and update the flag accordingly
        self.get_encoder_settings() # this function will update the self.single_ended_encoder_flag, affecting the FSM behaviour and the whole code in general

        time.sleep(1) # wait 1 second to let the actuator to be ready for the next command

        print("single_ended encoder flag: ",self.single_ended_encoder_flag)

        time.sleep(1)
        print("Setting initial microstep mode for actuator: ",name)
        self.set_microstep_mode(MicrostepMode.MICROSTEP_MODE_FRAC_256)
        print("Successfully set microstep mode for actuator: ",name)
        time.sleep(1)

        # Initial trajectory settings
        print("Setting initial trajectory settings for actuator: ",name)
        self.set_max_speed(NOMINAL_SPEED)
        print("Successfully set max speed for actuator: ",name)
        time.sleep(1)
                
        # Generating first state of the actuator direction FSM
        self.bklash = abs(bklash)

        if self.single_ended_encoder_flag == True:
            print("Making first movement, FSM positive direction first status for axis: ",str(self._id))
            pos = self.get_pos()
            time.sleep(1) # wait 1 second to let the actuator to be ready for the next command
            self.set_speed(50) # steps/s
            time.sleep(1)
            self.set_accel(50,50) # steps/s2
            self.move_to_pos(bklash+pos+50) # initial movement for setting a positive direction
            self.state = 'positive' # initial state of direction 'positive'
            print("Initial state of FSM for axis: ",str(self._id)," is: ",self.state)
        
        return

    def __del__(self):
        """
        Destructor for the Stepper class.
        """
        id = c_int(self._id)
        result = lib.command_stop(self._id)
        if result != Result.Ok:
            print('\nError sending immediate stop to act n'+repr(self._id))
        result = lib.close_device(byref(id))
        if result != Result.Ok:
            print("\nError trying to close communication with act n"+repr(self._id))

    def set_bklash(self, bklash:int):
        """
        Set the backlash value for the stepper actuator.
        """
        self.bklash = abs(bklash)
        print(f"Set backlash to {repr(self.bklash)} steps for act n {repr(self._id)} axis.")
    
    def get_bklash(self):
        """
        Get the backlash value for the stepper actuator.
        """
        return self.bklash

    def move(self,steps:float,destiny_position:float):
        """
        Move the stepper actuator a given number of steps. The direction is determined by the sign of the steps parameter. 
        If the actuator has an single_ended encoder, the backlash is taken into account.
        """
        if self.single_ended_encoder_flag == True:
            if self.state == 'positive':
                if steps > 0:
                    self.state = 'positive'
                    print("FSM positive direction status for axis: ",str(self._id))
                    print(f"Actual direction state is positive.")
                    print(f"Going to move {steps} steps into positive direction to position {str(destiny_position)}.")
                    res = self.move_to_pos(destiny_position)
                    print("FSM result: ",res)
                    return res
                elif steps < 0:
                    self.state = 'negative'
                    print("FSM negative direction status for axis: ",str(self._id))
                    print(f"Actual direction state is positive.")
                    print(f"Going to move {steps} steps plus {self.bklash} steps taking into account configured backlash because of change to negative direction.")
                    print(f"Resulting shift is then of {str(float(steps-self.bklash))} for axis {str(self._id)} into negative direction.")
                    print(f"Going to move to position {str(float(destiny_position-self.bklash))}.")
                    time.sleep(0.5)
                    res = self.move_to_pos(destiny_position-abs(self.bklash)) # if it is going to negative direction (steps < 0), substracting bklash will make it even go further to negative values.
                    print("FSM result: ",res)
                    return res
            elif self.state == 'negative':
                if steps < 0:
                    self.state = 'negative'
                    print("FSM negative direction status for axis: ",str(self._id))
                    print(f"Actual direction state is negative.")
                    print(f"Going to move {steps} steps into negative direction to position {str(destiny_position)}.")
                    res = self.move_to_pos(destiny_position)
                    print("FSM result: ",res)
                    return res
                elif steps > 0:
                    self.state = 'positive'
                    print("FSM positive direction status for axis: ",str(self._id))
                    print(f"Actual direction state is negative.")
                    print(f"Going to move {steps} steps plus {self.bklash} steps taking into account configured backlash because of change to positive direction.")
                    print(f"Resulting shift is then of {str(float(steps+self.bklash))} for axis {str(self._id)} into positive direction.")
                    print(f"Going to move to position {str(float(destiny_position+self.bklash))}.")
                    time.sleep(0.5)
                    res = self.move_to_pos(destiny_position+abs(self.bklash)) # if it is going to positive direction (steps > 0), adding bklash will make it even go further to positive values.
                    print("FSM result: ",res)
                    return res
        else:
            print(f"Going to move {steps} steps into direction {str(destiny_position)}.")
            res = self.move_to_pos(destiny_position)
            return res # if everything went OK, it will return True. USB error will bring a -4 from move_to_pos function or get_pos function.
            
    def move_to_pos(self, pos:float):
        """
        Moves actuator to recieved position.

        :arguments:
        pos -- The desired trajectory endpoint expressed in steps from home.

        :return:
        True if move is succesful, False otherwise.
        """
        positions_deque = deque() # deque is a list-like container with fast appends and pops on either end
        print(f"Got the next absolute position to go to: {str(pos)}")

        if pos > 0: # if the position is positive, it means that the actuator is going to positive direction
            full_steps= math.floor(pos)
            microsteps = (pos-full_steps)*self._microsteps 
        else: # if the position is negative, it means that the actuator is going to negative direction
            full_steps= math.ceil(pos) 
            microsteps = (pos-full_steps)*self._microsteps
            
        shift_accuracy = float(2.5/self._microsteps) # this is the accuracy of the shift of 1 microstep in microns (um)
        print("Shift accuracy in microns (um): ",shift_accuracy)

        print(f"Absolute position to move taking into account full_steps and microsteps: {str(full_steps)} and {str(microsteps)}")
        print(f"Rounded up data compatible with Standa controller (Standa can't process float numbers): {str(int(full_steps))} and {str(int(microsteps))}")

        result = lib.command_move(self._id, int(full_steps), int(microsteps)) # this is one is for absolute positions
        
        if result != Result.Ok:
            print(f"Error: Unsuccesful command move of actuator n {repr(self._id)}")
            result = None
            ####################################### KILL SECTION #######################################
            print("Aborting printing process. Standa failed.")
            ############################################################################################
            exit()
            # return result # None means the there is no hardware connected to the computer
        
        frozen_t0 = time.time()  # get the current time at the start of the loop
        last_pos = self.get_pos()

        while True:
            """
            Loop for being able to print the current position of the actuator while it is moving. 
            Guarenteeing a sequential logic in the code. Representing the "shifting" state of the actuator.
            This loop will break if the current position is within the error shift of the desired position.
            A timeout condition is implemented if the current position does not change for more than t seconds.
            """
            current_pos = self.get_pos()
            desired_pos = float(pos)
            error_shift = STANDA_ERROR_SHIFT

            # if target position is reached, break the loop (evPOSITIONREACHED)
            if current_pos <= (desired_pos + error_shift) and current_pos >= (desired_pos - error_shift):
                print(f"reach desired position: {repr(current_pos)}")
                break
            
            # if the current position is None, it means that the actuator feedback is corrupted (evNODEVICE).
            if current_pos == None:
                print(f"Error in get_pos call for act n {repr(self._id)}")
                return False
            
            if abs(last_pos - current_pos) <= STANDA_ERROR_SHIFT:
                # if the current position is not changing, it means that the actuator feedback is corrupted (evSHIFTTIMEOUT)
                if (time.time() - frozen_t0) >= STANDA_TIMEOUT:
                    print(f"Timeout ocurred for act n {repr(self._id)}")
                    print("Actuator feedback is not changing.")
                    return False
            else:
                # if the current position is changing, it means that the actuator feedback is working properly.
                frozen_t0 = time.time()
                last_pos = current_pos

            # print(f"current_pos: {repr(current_pos)}") # for debugging
            positions_deque.append(current_pos)
            # print(f"moving to {str(pos)} position... \n") # for debugging

            time.sleep(STANDA_REFRESH_SHIFT)
        
        current_pos = self.get_pos() # this is to get the last position after the loop
        positions_deque.append(current_pos)
    
        print(f"reached desired position, pos= {repr(self.get_pos())}")

        microsteps_lost = abs(microsteps-int(microsteps))   
        print("////////////////////////////////////////////////////////////////////////////////////////////")
        print("Microsteps lost in the shift: ",microsteps_lost)
        print("Accuracy lost of the shift in microns (um) going to specified absolute position: ",microsteps_lost*shift_accuracy)        
        print(f"Accuracy lost in last Standa shift {str(microsteps_lost*shift_accuracy)} microns for device {str(self._id)}.")
        print("////////////////////////////////////////////////////////////////////////////////////////////")

        print("positions deque: ",positions_deque)
        
        return True, positions_deque

    def stop_movement(self):
        """
        Stops any currently trajectory move taking place with deceleration speed.

        :return: True if succesful, false otherwise
        """
        result = lib.command_sstp(self._id)
        if result != Result.Ok:
            print("\nError: failed to send soft stop command of act n"+repr(self._id))
            return False
        return True
    
    def reset_zero(self):
        """
        Commands actuator to move to home and set zero there.

        This function call is blocking and changes the zero reference for future move calls.
        """
        print("\nStarting zero position reset.")

        # Print useful information
        e_set = edges_settings_t()
        enc_set = encoder_settings_t()
        lib.get_encoder_settings(self._id, byref(enc_set))
        lib.get_edges_settings(self._id, byref(e_set))
        print("\nEncoder settings flags: "+repr(enc_set.EncoderSettings))
        print("\nEdges settings flags: "+repr(e_set.EnderFlags))

        h_set = home_settings_t()
        result = lib.get_home_settings(self._id, byref(h_set))
        if result != Result.Ok:
            print("\nResult is "+repr(result))
            print("\nError: Unsuccesful get home settings of actuator n"+repr(self._id))
            return False
        h_set.HomeFlags = 0x100+ 0x70 + 0x2 # Defines movement direction, limit switch and fast algorithm.
        result = lib.set_home_settings(self._id, byref(h_set))
        self._print_home_settings()
        if result != Result.Ok:
            print("\nResult is "+repr(result))
            print("\nError: Unsuccesful set home settings of actuator n"+repr(self._id))
            return False
        result = lib.command_homezero(self._id)
        if result != Result.Ok:
            print("\nResult is "+repr(result))
            print("\nError: Unsuccesful command home zero of actuator n"+repr(self._id))
            return False
        print("\nFinished zero position reset.")
        return True
    
    #############################
    #           SETTERS         #
    #############################

    def set_max_speed(self, speed):
        """
        Sets actuators maximum speed

        :arguments:
        speed -- Maximum speed in steps per second.

        :return:
        True if succesful, False otherwise.
        """
        print("\nSet max speed to "+repr(speed)+"step/s")
        if (speed > MAX_SPEED) or (speed<0):
            print("\nError: invalid speed parameter for actuator n"+repr(self._id))
            return False
        # Create engine settings structure
        eng = engine_settings_t()
        # Get current engine settings from controller
        result = lib.get_engine_settings(self._id, byref(eng))
        if result != Result.Ok:
            print("\nResult="+repr(result))
            print("\nFailed to read engine settings from actuator n"+str(self._id))
            return False
        # Change current speed
        full_steps_per_sec = math.floor(speed)
        microsteps_per_sec = (speed-full_steps_per_sec)*self._microsteps
        eng.NomSpeed = int(full_steps_per_sec)
        eng.uNomSpeed = int(microsteps_per_sec)
        # Write new engine settings to controller
        result = lib.set_engine_settings(self._id, byref(eng))
        if result != 0:
            print("\nFailed to set engine settings from actuator n"+str(self._id))
            return False
        self._max_speed = speed
        return True
    
    def set_speed(self, speed):
        """
        Sets actuator's working speed.

        :arguments:
        speed -- Workking speed in steps per second.
        
        :returns:
        True if susccesful, False otherwise.
        """
        if speed > self._max_speed:
            print(f"Error in set_speed call for act n {repr(self._id)}")
            print("Recieved speed exceeds max speed.")
            print(f"recieved = {repr(speed)}; max_speed = {repr(self._max_speed)}")
        print(f"Set speed to {repr(speed)} step/s")
        # Create move settings structure
        mvst = move_settings_t()
        # Get current move settings from controller
        result = lib.get_move_settings(self._id, byref(mvst))
        if result != Result.Ok:
            print(f"Result = {repr(result)}")
            print(f"Error failed to get move settings for actuator n {repr(self._id)}")
            return False
        # Change current speed
        full_steps_per_sec = math.floor(speed)
        microsteps_per_sec = (speed-full_steps_per_sec)*self._microsteps
        mvst.Speed = int(full_steps_per_sec)
        mvst.uSpeed = int(microsteps_per_sec)
        # Write new move settings to controller
        result = lib.set_move_settings(self._id, byref(mvst))
        if result != Result.Ok:
            print(f"Result = {repr(result)}")
            print(f"Error failed to set move settings for actuator n {repr(self._id)}, quitting program.")
        return True

    def set_microstep_mode(self, microsteps):
        """
        Sets number of microsteps per step available.

        More microsteps per step means better resolution but less torque. Valid inputs are:
        - MICROSTEP_MODE_FULL        = 0x01,
        - MICROSTEP_MODE_FRAC_2      = 0x02,
        - MICROSTEP_MODE_FRAC_4      = 0x03,
        - MICROSTEP_MODE_FRAC_8      = 0x04,
        - MICROSTEP_MODE_FRAC_16     = 0x05,
        - MICROSTEP_MODE_FRAC_32     = 0x06,
        - MICROSTEP_MODE_FRAC_64     = 0x07,
        - MICROSTEP_MODE_FRAC_128    = 0x08,
        - MICROSTEP_MODE_FRAC_256    = 0x09
        """
        if (microsteps>MicrostepMode.MICROSTEP_MODE_FRAC_256)or(microsteps<MicrostepMode.MICROSTEP_MODE_FULL):
            print(f"Recieved invalid parameter in set_microstep_mode: {repr(microsteps)}")
            return False # Recieved invalid input
        self._microsteps = 2**(microsteps-1)
        print(f"Set microstep mode to {repr(microsteps)}")
        # Create engine settings structure
        eng = engine_settings_t() # for HSI XY
        # Get current engine settings from controller
        result = lib.get_engine_settings(self._id, byref(eng))
        if result != Result.Ok: # It will be 0 if all is OK
            print(f"Couldn't read engine settings from actuator n {str(self._id)}")
            return False
        eng.MicrostepMode = microsteps
        # Write new engine settings to controller
        result = lib.set_engine_settings(self._id, byref(eng))
        if result != Result.Ok: # It will be 0 if all is OK
            print(f"Couldn't set engine settings from actuator n {str(self._id)}")
            return False
        return True  

    def set_backlash_mode(self, backlash_steps, backlash_speed):
        """
        Sets number of steps for backlash play.

        EngineFlags needs to be set into ENGINE_ANTIPLAY (engine_settings_t)
        """
        print("\nSet backlash_speed to "+repr(backlash_speed)+" qsteps/s")
        if (backlash_speed>MAX_BACKLASH_SPEED)or(MAX_BACKLASH_SPEED<0):
            print("Error: Invalid backlash speed parameter for actuator n"+repr(self._id))
            return False
        
        # Create engine settings structure
        eng = engine_settings_t()
        # Get current engine settings from controller
        result = lib.get_engine_settings(self._id, byref(eng))
        if result != Result.Ok:
            print("\nResult="+repr(result))
            print("\nFailed to read engine settings from actuator n"+str(self._id))
            return False
        
        # 1) Activate backlash flag
        eng.EngineFlags = EngineFlags.ENGINE_ANTIPLAY
        # Write new engine settings to controller
        result = lib.set_engine_settings(self._id, byref(eng))
        if result != 0:
            print("\nFailed to set engine settings from actuator n"+str(self._id))
            return False

        # 2) Specify backlash steps
        full_backlash_steps= math.floor(backlash_steps)
        eng.Antiplay = int(full_backlash_steps)
        # Write new engine settings to controller
        result = lib.set_engine_settings(self._id, byref(eng))
        if result != 0:
            print("\nFailed to set engine settings from actuator n"+str(self._id))
            return False
        self._antiplay = full_backlash_steps

        # Create move settings structure
        mvst = move_settings_t()
        # Get current move settings from controller
        result = lib.get_move_settings(self._id, byref(mvst))
        if result != Result.Ok:
            print("\nResult="+repr(result))
            print("\nFailed to read move settings from actuator n"+str(self._id))
            return False
        full_backlash_steps_per_sec = math.floor(backlash_speed)
        backlash_microsteps_per_sec = (backlash_speed-full_backlash_steps_per_sec)*self._microsteps
        mvst.AntiplaySpeed = int(full_backlash_steps_per_sec)
        mvst.uAntiplaySpeed = int(backlash_microsteps_per_sec)
        print("\nSet backlash steps to "+repr(backlash_steps)+" steps") # Number of pulses or steps for backlash (play) compensation procedure
        
        # 3) Specify backlash speed
        result = lib.set_move_settings(self._id, byref(mvst))
        if result != 0:
            print("\nResult="+repr(result))
            print("\nFailed to set move settings from actuator n"+str(self._id))
            return False
        self._backlashspeed = full_backlash_steps_per_sec
        self._ubacklashspeed = backlash_microsteps_per_sec

        return True

    def set_accel(self, accel:int, decel:int):
        """
        Sets actuator's maximum acceleration

        :arguments:
        accel -- Maximum acceleration in steps per second.

        :return: Does not return value
        """
        print(f"Set accel to {repr(accel)} steps/s2")
        if (accel>MAX_ACCEL)or(accel<0):
            print(f"Error: Invalid accel parameter for actuator n {repr(self._id)}")
            return False
        if (decel>MAX_DECEL)or(decel<0):
            print(f"Error: Invalid accel parameter for actuator n {repr(self._id)}")
            return False
        # Create move settings structure
        mvst = move_settings_t()
        # Get current move settings from controller
        result = lib.get_move_settings(self._id, byref(mvst))
        if result != Result.Ok:
            print(f"Result = {repr(result)}")
            print(f"Failed to read move settings from actuator n = {str(self._id)}")
            return False
        # Change current accel
        mvst.Accel = int(accel)
        mvst.Decel = int(decel)
        # Write new move settings to controller
        result = lib.set_move_settings(self._id, byref(mvst))
        if result != 0:
            print(f"Result = {repr(result)}")
            print(f"Failed to set move settings from actuator n {str(self._id)}")
            return False
        self._accel = accel
        return True

    def set_pid(self,KpU:int,KiU:int,KdU:int,Kpf:float,Kif:float,Kdf:float): # https://docs.python.org/3/library/ctypes.html
        """
        Sets pid's parameters

        :arguments:
        - Kup -- Proportional gain for voltage PID routine.
        - KiU -- Integral gain for voltage PID routine.
        - KdU -- Differential gain for voltage PID routine.
        - Kpf -- Proportional gain for BLDC position PID routine.
        - Kif -- Integral gain for BLDC position PID routine.
        - Kdf -- Differential gain for BLDC position PID routine.

        :returns:
        True if susccesful, False otherwise.
        """
        pidst = pid_settings_t() # data structure 
        result = lib.get_pid_settings(self._id, byref(pidst)) # get pid_settings_t -> get_pid_settings
        print("Result (previous changing pid values): " + repr(result))
        if result == Result.Ok:
            print("KpU: " + repr(pidst.KpU))
            print("KiU: " + repr(pidst.KiU))
            print("KdU: " + repr(pidst.KdU))
            print("Kpf: " + repr(pidst.Kpf))
            print("Kif: " + repr(pidst.Kif))
            print("Kdf: " + repr(pidst.Kdf))
        
        # Change current PID parameters
        pidst.KpU = int(KpU)
        pidst.KiU = int(KiU)
        pidst.KdU = int(KdU)
        pidst.Kpf = float(Kpf)
        pidst.Kif = float(Kif)
        pidst.Kdf = float(Kdf)
        
        # Write new move settings to controller
        result = lib.set_pid_settings(self._id, byref(pidst)) # http://files.xisupport.com/8SMC4-USB_Programming_manual_Eng.pdf -> 7.1.4.134
        if result != Result.Ok:
            print("\nResult="+repr(result))
            print("\nError failed to set move settings for actuator n"+repr(self._id))
        
        # Printing updated values
        pidst = pid_settings_t() # data structure 
        result = lib.get_pid_settings(self._id, byref(pidst)) # get pid_settings_t -> get_pid_settings
        print("Result (after changing pid values): " + repr(result))
        if result == Result.Ok:
            print("KpU: " + repr(pidst.KpU))
            print("KiU: " + repr(pidst.KiU))
            print("KdU: " + repr(pidst.KdU))
            print("Kpf: " + repr(pidst.Kpf))
            print("Kif: " + repr(pidst.Kif))
            print("Kdf: " + repr(pidst.Kdf))
        return True

    def set_encoder_settings(self,enc_flag:int):
        """ 
        Sets encoder configuration

        enc_flag dictionary:
        - 1 = ENCSET_DIFFERENTIAL_OUTPUT = 0x001
        - 2 = ENCSET_PUSHPULL_OUTPUT = 0x004 # THIS IS KEY
        - 3 = ENCSET_INDEXCHANNEL_PRESENT = 0x010
        - 4 = ENCSET_REVOLUTIONSENSOR_PRESENT = 0x040
        - 5 = ENCSET_REVOLUTIONSENSOR_ACTIVE_HIGH = 0x100
        """

        print("Get previous encoder settings")
        enc = encoder_settings_t() # encoder_settings_t
        result = lib.get_encoder_settings(self._id, byref(enc))
        print(f"Result: {repr(result)}")
        print(f"Result (previous changing encoder settings): {repr(result)}")
        if result == Result.Ok:
            print(f"MaxOperatingFrequency: {repr(enc.MaxOperatingFrequency)}")
            print(f"SupplyVoltageMin: {repr(enc.SupplyVoltageMin)}")
            print(f"SupplyVoltageMax: {repr(enc.SupplyVoltageMax)}")
            print(f"MaxCurrentConsumption: {repr(enc.MaxCurrentConsumption)}")
            print(f"PPR: {repr(enc.PPR)}")
            print(f"EncoderSettings: {repr(enc.EncoderSettings)}")     
        else:
            return False

        # Activate encoder flag depending on enc_flag value
        if enc_flag == 1:
            enc.EncoderSettings = EncoderSettingsFlags.ENCSET_DIFFERENTIAL_OUTPUT
        if enc_flag == 2:
            enc.EncoderSettings = EncoderSettingsFlags.ENCSET_PUSHPULL_OUTPUT # THIS IS KEY
        if enc_flag == 3:
            enc.EncoderSettings = EncoderSettingsFlags.ENCSET_INDEXCHANNEL_PRESENT
        if enc_flag == 4:
            enc.EncoderSettings = EncoderSettingsFlags.ENCSET_REVOLUTIONSENSOR_PRESENT
        if enc_flag == 5:
            enc.EncoderSettings = EncoderSettingsFlags.ENCSET_REVOLUTIONSENSOR_ACTIVE_HIGH

        # Write new engine settings to controller
        result = lib.set_encoder_settings(self._id, byref(enc))
        if result != 0:
            print(f"Failed to set encoder settings from actuator n {str(self._id)})")
            return False
        
        print(f"Getting encoder setting after configuring them for axis {repr(result)}")
        self.get_encoder_settings() # to show update

        return True

    def set_engine_flag(self,eng_flag:int):
        """
        eng_flag dictionary:
        - 1 = ENGINE_REVERSE        = 0x01 # THIS IS KEY
        - 2 = ENGINE_CURRENT_AS_RMS = 0x02
        - 3 = ENGINE_MAX_SPEED      = 0x04
        - 4 = ENGINE_ANTIPLAY       = 0x08
        - 5 = ENGINE_ACCEL_ON       = 0x10
        - 6 = ENGINE_LIMIT_VOLT     = 0x20
        - 7 = ENGINE_LIMIT_CURR     = 0x40
        - 8 = ENGINE_LIMIT_RPM      = 0x80
        """
        eng = engine_settings_t()
        result = lib.get_engine_settings(self._id, byref(eng)) # in pyximc.py -> engine_settings_t -> EngineFlags
        print("Result: " + repr(result))

        # Activate encoder flag depending on eng_flag value
        if eng_flag == 1:
            eng.EngineFlags = EngineFlags.ENGINE_REVERSE # THIS IS KEY
        if eng_flag == 2:
            eng.EngineFlags = EngineFlags.ENGINE_CURRENT_AS_RMS 
        if eng_flag == 3:
            eng.EngineFlags = EngineFlags.ENGINE_MAX_SPEED
        if eng_flag == 4:
            eng.EngineFlags = EngineFlags.ENGINE_ANTIPLAY
        if eng_flag == 5:
            eng.EngineFlags = EngineFlags.ENGINE_ACCEL_ON
        if eng_flag == 6:
            eng.EngineFlags = EngineFlags.ENGINE_LIMIT_VOLT
        if eng_flag == 7:
            eng.EngineFlags = EngineFlags.ENGINE_LIMIT_CURR
        if eng_flag == 8:
            eng.EngineFlags = EngineFlags.ENGINE_LIMIT_RPM

        result = lib.set_engine_settings(self._id, byref(eng))
        if result != 0:
            print(f"Failed to set engine flags from actuator n {str(self._id)}")
            return False
        
        print(f"Checking engine flag settings after configuring them for axis {str(self._id)}")
        self.test_engine() # to show update

    def set_feedback_type(self,IPS:int,feedbk_type:int,feedbk_flags:int,counts_per_turn:int):
        """
        feedbk_type dictionary:
	    - 1 = FEEDBACK_ENCODER                 = 0x01 # THIS IS KEY
	    - 2 = FEEDBACK_EMF                     = 0x04
	    - 3 = FEEDBACK_NONE                    = 0x05
	    - 4 = FEEDBACK_ENCODER_MEDIATED        = 0x06

        feedbk_flags dictionary:
        - 1 = FEEDBACK_ENC_REVERSE             = 0x01
        - 2 = FEEDBACK_ENC_TYPE_BITS           = 0xC0
        - 3 = FEEDBACK_ENC_TYPE_AUTO           = 0x00
        - 4 = FEEDBACK_ENC_TYPE_SINGLE_ENDED   = 0x40 # THIS IS KEY. 0x40 (original) -> 0x41 seems to be the correct hex for this flag
        - 5 = FEEDBACK_ENC_TYPE_DIFFERENTIAL   = 0x80
        """
        print(f"Get feedback config before changing parameters in Standa axis {str(self._id)}")
        feedbk = feedback_settings_t() # structure that contains a class with fields. If you modify a field, you modify the hardware behaviour.
        result = lib.get_feedback_settings(self._id, byref(feedbk)) # feedback_settings_t() -> data structure inside -> get_feedback_settings -> https://doc.xisupport.com/en/8smc5-usb/8SMC5-USB.pdf 
        print(f"Result: {repr(result)}")
        if result == Result.Ok:
            print(f"IPS: {repr(feedbk.IPS)}")
            print(f"FeedbackType: {repr(feedbk.FeedbackType)}")
            print(f"FeedbackFlags: {repr(feedbk.FeedbackFlags)}")
            print(f"CountsPerTurn: {repr(feedbk.CountsPerTurn)}")
        else:
            return False
         
        feedbk.IPS = int(IPS)

        if feedbk_type == 1:
            feedbk.FeedbackType = FeedbackType.FEEDBACK_ENCODER
        if feedbk_type == 2:
            feedbk.FeedbackType = FeedbackType.FEEDBACK_EMF
        if feedbk_type == 3:
            feedbk.FeedbackType = FeedbackType.FEEDBACK_NONE
        if feedbk_type == 4:
            feedbk.FeedbackType = FeedbackType.FEEDBACK_ENCODER_MEDIATED

        if feedbk_flags == 1:
            feedbk.FeedbackFlags = FeedbackFlags.FEEDBACK_ENC_REVERSE
        if feedbk_flags == 2:
            feedbk.FeedbackFlags = FeedbackFlags.FEEDBACK_ENC_TYPE_BITS
        if feedbk_flags == 3:
            feedbk.FeedbackFlags = FeedbackFlags.FEEDBACK_ENC_TYPE_AUTO
        if feedbk_flags == 4:
            feedbk.FeedbackFlags = FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED
        if feedbk_flags == 5:
            feedbk.FeedbackFlags = FeedbackFlags.FEEDBACK_ENC_TYPE_DIFFERENTIAL

        feedbk.CountsPerTurn = int(counts_per_turn)

        result = lib.set_feedback_settings(self._id, byref(feedbk))
        if result != 0:
            print(f"Failed to set feedback settings from actuator n {str(self._id)}")
            return False

        print(f"Get feedback config after changing parameters in Standa axis {str(self._id)}")
        self.get_feedback_settings() # to show update

        return True

    #############################
    #           GETTERS         #
    #############################

    def get_pid(self): # https://docs.python.org/3/library/ctypes.html
        """
        Gets pid's parameters

        :return:
        KpU -- Proportional gain for voltage PID routine.
        KiU -- Integral gain for voltage PID routine.
        KdU -- Differential gain for voltage PID routine.
        Kpf -- Proportional gain for BLDC position PID routine.
        Kif -- Integral gain for BLDC position PID routine.
        Kdf -- Differential gain for BLDC position PID routine.
        """
        pidst = pid_settings_t() # data structure 
        result = lib.get_pid_settings(self._id, byref(pidst)) # get pid_settings_t -> get_pid_settings
        print("Result: " + repr(result))
        if result == Result.Ok:
            print("KpU: " + repr(pidst.KpU))
            print("KiU: " + repr(pidst.KiU))
            print("KdU: " + repr(pidst.KdU))
            print("Kpf: " + repr(pidst.Kpf))
            print("Kif: " + repr(pidst.Kif))
            print("Kdf: " + repr(pidst.Kdf))
            return True
        else:
            return False
    
    def get_pos(self):
        """
        Returns actuator's current position.

        :return:
        position of the actuator in steps with respect to home.
        """

        if self.single_ended_encoder_flag == True:
            x_pos = get_position_t()
            result = lib.get_position(self._id, byref(x_pos))
            print(x_pos.EncPosition)
            if result is not Result.Ok:
                print("Result="+repr(result))
                print("Error retrieving position of actuator n"+repr(self._id))
                result = None
                ####################################### KILL SECTION #######################################
                print("Aborting printing process. Standa failed.")
                ############################################################################################
                exit()
                # return result # None means the there is no hardware connected to the computer
            
            pos = (x_pos.EncPosition)
            return pos
        
        else:
            x_pos = get_position_t()
            result = lib.get_position(self._id, byref(x_pos))
            print(x_pos.Position)
            print(x_pos.uPosition)
            if result is not Result.Ok:
                print("Result="+repr(result))
                print("Error retrieving position of actuator n"+repr(self._id))
                result = None
                ####################################### KILL SECTION #######################################
                print("Aborting printing process. Standa failed.")
                ############################################################################################
                exit()
                # return result # None means the there is no hardware connected to the computer
            
            pos = (x_pos.Position + (x_pos.uPosition/self._microsteps))
            return pos

    def get_speed(self):
        """
        Returns actuator's current speed

        :return:
        speed at which actuator is travelling in micrometres per second
        """
        x_status = status_t()
        result = lib.get_status(self._id, byref(x_status))
        if result == Result.Ok:
            speed = (x_status.CurSpeed+(x_status.uCurSpeed/self._microsteps))
            return speed
        else:
            return -1

    def get_accel(self):
        """
        Returns actuator's maximum acceleration setting

        :return:
        maximum allowed acceleration of actuator
        """
        return self._accel

    def get_name(self):
        """
        Returns actuator's human name identifier

        :return:
        string with actuator's human name
        """
        return repr(self._id)

    def get_movement_settings(self):
        """
        Get movement settings data from actuators
        """
        print("Get movements settings\n")
        mov = move_settings_t() # move_settings_calb_t
        result = lib.get_move_settings(self._id, byref(mov))
        print("Result: " + repr(result))

        if result == Result.Ok:
            print("Speed: " + repr(mov.Speed))
            print("Accel: " + repr(mov.Accel))
            print("Decel: " + repr(mov.Decel))
            print("AntiplaySpeed: " + repr(mov.AntiplaySpeed))
            print("MoveFlags: " + repr(mov.MoveFlags))
            return True
        else:
            return False

    def get_gear_settings(self):
        """
        Get gear settings data from actuators
        """
        print("\nGet gear settings\n")
        gear = gear_settings_t() # gear_settings_calb_t
        result = lib.get_gear_settings(self._id, byref(gear))
        print("Result: " + repr(result))

        if result == Result.Ok:
            print("ReductionIn: " + repr(gear.ReductionIn))
            print("ReductionOut: " + repr(gear.ReductionOut))
            print("RatedInputTorque: " + repr(gear.RatedInputTorque))
            print("RatedInputSpeed: " + repr(gear.RatedInputSpeed))
            print("MaxOutputBacklash: " + repr(gear.MaxOutputBacklash))
            print("InputInertia: " + repr(gear.InputInertia))     
            print("Efficiency: " + repr(gear.Efficiency))
            return True
        else:
            return False
    
    def get_encoder_settings(self):
        """
        Get encoder settings data from actuators.
        
        From 8SMC5-USB User Manual, Release 2.18.0 (pag. 80 from technical documentation). 
        """
        print("Get encoder settings")
        enc = encoder_settings_t() # encoder_settings_t
        result = lib.get_encoder_settings(self._id, byref(enc))
        print(f"Result: {repr(result)}")

        if result == Result.Ok:
            print(f"MaxOperatingFrequency: {repr(enc.MaxOperatingFrequency)}")
            print(f"SupplyVoltageMin: {repr(enc.SupplyVoltageMin)}")
            print(f"SupplyVoltageMax: {repr(enc.SupplyVoltageMax)}")
            print(f"MaxCurrentConsumption: {repr(enc.MaxCurrentConsumption)}")
            print(f"PPR: {repr(enc.PPR)}")
            print(f"EncoderSettings: {repr(enc.EncoderSettings)}")
            if repr(enc.EncoderSettings) == '4':
                print("EncoderSettings: single-ended encoder code = ", repr(enc.EncoderSettings))
                self.single_ended_encoder_flag = True
            if repr(enc.EncoderSettings) == '5':
                print("EncoderSettings: differential encoder code = ", repr(enc.EncoderSettings))
                self.single_ended_encoder_flag = False
            print(f"single_ended encoder flag: {repr(self.single_ended_encoder_flag)}")
            return True 
        else:
            return False

    def get_feedback_settings(self):
        """
        Prints counts per turn of encoder. 
        Controller 8SMC5 supports differential encoders and simple (single-ended) encoders.
        """
        print("Get feedback")
        feedbk = feedback_settings_t() # structure that contains a class with fields. If you modify a field, you modify the hardware behaviour.
        result = lib.get_feedback_settings(self._id, byref(feedbk)) # feedback_settings_t() -> data structure inside -> get_feedback_settings -> https://doc.xisupport.com/en/8smc5-usb/8SMC5-USB.pdf 
        print(f"Result: {repr(result)}")
        if result == Result.Ok:
            print(f"IPS: {repr(feedbk.IPS)}")
            print(f"FeedbackType: {repr(feedbk.FeedbackType)}")
            print(f"FeedbackFlags: {repr(feedbk.FeedbackFlags)}")
            print(f"CountsPerTurn: {repr(feedbk.CountsPerTurn)}")
            return True
        else:
            return False
        
    #####################################
    #           HARDWARE CHECKS         #
    #####################################

    def test_info(self):
        """
        Prints Manufacturer and product related information
        """
        print("Get device info")
        x_device_information = device_information_t()
        result = lib.get_device_information(self._id, byref(x_device_information))
        print("Result: " + repr(result))
        if result == Result.Ok:
            print("Device information:")
            print("Manufacturer: " +
                    repr(string_at(x_device_information.Manufacturer).decode()))
            print("ManufacturerId: " +
                    repr(string_at(x_device_information.ManufacturerId).decode()))
            print("ProductDescription: " +
                    repr(string_at(x_device_information.ProductDescription).decode()))
            print("Major: " + repr(x_device_information.Major))
            print("Minor: " + repr(x_device_information.Minor))
            print("Release: " + repr(x_device_information.Release))
            return True
        else:
            return False

    def test_status(self):
        """
        Prints measured power levels and actuator status flags
        """
        print("Get status")
        x_status = status_t()
        result = lib.get_status(self._id, byref(x_status))
        if result == Result.Ok:
            print("Engine current, mA: " + repr(x_status.Ipwr))
            print("Power supply voltage, tens of mV: " + repr(x_status.Upwr))
            print("USB current, mA: " + repr(x_status.Iusb))
            print("Status.Flags: " + repr(hex(x_status.Flags)))
            return True
        else:
            return False

    def test_engine(self):
        """
        Get test engine data.
        """
        print("Get engine settings")
        eng = engine_settings_t()
        result = lib.get_engine_settings(self._id, byref(eng)) # engine_settings_calb_t
        print("Result: " + repr(result))
        if result == Result.Ok:
            print(f"StespsPerRev: {repr(eng.StepsPerRev)}")
            print(f"Result: {repr(eng)}")
            print(f"NomVoltage: {repr(eng.NomVoltage)}")
            print(f"NomCurrent: {repr(eng.NomCurrent)}")
            print(f"NomSpeed: {repr(eng.NomSpeed)}")
            print(f"EngineFlags: {repr(eng.EngineFlags)}")     
            print(f"Antiplay: {repr(eng.Antiplay)}")
            print(f"MicrostepMode: {repr(eng.MicrostepMode)}")
            print(f"StepsPerRev: {repr(eng.StepsPerRev)}")
            return True
        else:
            return False

    ######################################
    #           LOCAL FUNCTIONS
    ######################################
    def _print_home_settings(self):
        """
        Prints home settings.
        """
        h_settings = home_settings_t()
        result = lib.get_home_settings(self._id, byref(h_settings))
        if result != Result.Ok:
            print("\nError couldn't get home settings.")
            return False
        print("\nFastHome speed, full steps: " + repr(h_settings.FastHome))
        print("\nSlowHome speed, full steps: " + repr(h_settings.SlowHome))
        print("\nDistance from breakpoint, full steps: " + repr(h_settings.HomeDelta))
        print("\nHome Flags: " + repr(hex(h_settings.HomeFlags)))
        return True