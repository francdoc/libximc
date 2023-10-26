"""
import zaxis
z = zaxis.axis()
z.update()
z.move(self, speed: float, accel: float, decel: float, distance: float) # speed in mm/s, distance in mm, accel in mm/s^2, decel in mm/s^2
"""

import standa.pystanda as pystanda

###################################################### USER CONFIG ######################################################

struct_mechanical_resolution = {
    "ratio": 0.8         # 1 step /1.25 microns = 0.8 steps/micron
}

##########################################################################################################################

class axis:
    """Class to control a z Standa controller."""
    def __init__(self):
        self.mechres = float(struct_mechanical_resolution["ratio"])
        res = pystanda.detecthw() 
        self.device_num = 2 # calls STANDA_Z_ID inside pystanda hardware library
        
        pystanda.grab(self.device_num)

    def move(self, speed: float, accel: float, decel: float, distance: float): # speed in mm/s, distance in mm, accel in mm/s^2, decel in mm/s^2
        if speed < 0:
            raise ValueError("Speed value must be positive")
        if accel < 0:
            raise ValueError("Acceleration value must be positive")
        if decel < 0:
            raise ValueError("Deceleration value must be positive")
        if speed >= 2.4:
            raise ValueError("Speed value must be less than 2.4 mm/s")
        if accel >= 2.4:
            raise ValueError("Acceleration value must be less than 2.4 mm/s^2")
        if decel >= 2.4:
            raise ValueError("Deceleration value must be less than 2.4 mm/s^2")
        
        distance = float(distance * 1000)  # convert to um
        steps = distance * self.mechres    # um * steps / um = steps
        velocity = float(speed * 1000)     # convert to um/s
        accel = float(accel * 1000)        # convert to um/s^2
        steps_per_second = velocity * self.mechres
        steps_per_second_squared = accel * self.mechres
        pystanda.speedacc(self.device_num, steps_per_second, steps_per_second_squared, steps_per_second_squared)
        
        pystanda.shift(self.device_num, steps)
        
    def update(self):
        """Returns the absolute position of the axis in mm"""
        res = pystanda.getpos(self.device_num) # steps
        abs_position_um = float(res) / self.mechres # steps / (steps/um) = um
        abs_position_mm = abs_position_um / 1000
        return abs_position_mm # mm
    
if __name__ == "__main__":
    """Test code for the API"""
    z = axis()
    z.move(speed=0.1, accel=0.1, decel=0.1, distance=0.1)
    print(z.update())
    z.move(speed=0.1, accel=0.1, decel=0.1, distance=-0.1)
    print(z.update())    