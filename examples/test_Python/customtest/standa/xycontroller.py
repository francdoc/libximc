import time
import csv
import standa.pystanda as pystanda

SET_PAUSE = 1.5 # pause between movements in seconds

###################################################### USER CONFIG ######################################################

struct_mechanical_resolution = {
    "ratio": 0.8         # 1 step /1.25 microns = 0.8 steps/micron
}

##########################################################################################################################

class Standa:
    def __init__(self):
        """Initialize Standa controller"""
        self.shift_counter = 0 # counter for relative map
        self.move_counter = 0 # counter for absolute map
        self.buffer_abs = 0 # number of jumps in the absolute map
        self.buffer_rel = 0 # number of jumps in the relative map
        self.offset_x = 0 # offset for absolute map
        self.offset_y = 0 # offset for absolute map
        self.x_axis_num = 0 # calls STANDA_X_ID inside pystanda hardware library
        self.y_axis_num = 1 # calls STANDA_Y_ID inside pystanda hardware library
        self.mechres = float(struct_mechanical_resolution["ratio"])
        
        pystanda.detecthw() 
        res_x = pystanda.grab(self.x_axis_num)
        res_y = pystanda.grab(self.y_axis_num)
        print("res_x: ",res_x)
        print("res_y: ",res_y)
    
    def shift(self,x:float,y:float):
        """Move relative to current position"""
        shift_x = float(x) # relative shift x in mm
        shift_y = float(y) # relative shift y in mm
                    
        distance_x = float(shift_x * 1000)  # convert to um
        steps_x = distance_x * self.mechres    # um * steps / um = steps
        velocity_x = float(1 * 1000)     # convert to um/s
        accel_x = float(1 * 1000)        # convert to um/s^2
        steps_per_second_x = velocity_x * self.mechres
        steps_per_second_squared_x = accel_x * self.mechres
        pystanda.speedacc(self.x_axis_num, steps_per_second_x, steps_per_second_squared_x, steps_per_second_squared_x)
        pystanda.shift(self.x_axis_num, steps_x)
 
        distance_y = float(shift_y * 1000)  # convert to um
        steps_y = distance_y * self.mechres    # um * steps / um = steps
        velocity_y = float(1 * 1000)     # convert to um/s
        accel_y = float(1 * 1000)        # convert to um/s^2
        steps_per_second_y = velocity_y * self.mechres
        steps_per_second_squared_y = accel_y * self.mechres
        pystanda.speedacc(self.y_axis_num, steps_per_second_y, steps_per_second_squared_y, steps_per_second_squared_y)
        pystanda.shift(self.y_axis_num, steps_y)

    def getpos(self):
        """Get current position"""
        res = pystanda.getpos(self.x_axis_num) # steps
        x_abs_position_um = float(res) / self.mechres # steps / (steps/um) = um
        x_abs_position_mm = x_abs_position_um / 1000
        x = x_abs_position_mm

        res = pystanda.getpos(self.y_axis_num) # steps
        y_abs_position_um = float(res) / self.mechres # steps / (steps/um) = um
        y_abs_position_mm = y_abs_position_um / 1000
        y = y_abs_position_mm

        return x,y

    def setoffset(self,x:float,y:float):
        """Set offset for absolute map"""
        self.offset_x = float(x)
        self.offset_y = float(y)
        print("Offset for absolute map set to:",self.offset_x,self.offset_y)
        return self.offset_x,self.offset_y
    
    def load_rel_map(self,map_file:str):
        """Get relative 2D movement path from a CSV file. First row is x, second row is y"""
        map_file = str(map_file)
        self.shift_x_values = []
        self.shift_y_values = []
        with open(map_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.shift_x_values.append(float(row[0]))
                self.shift_y_values.append(float(row[1]))
        print("shift x_values:", self.shift_x_values)
        print("shift y_values:", self.shift_y_values)
        self.buffer_rel = len(self.shift_x_values) # number of jumps in the map
        return self.shift_x_values, self.shift_y_values
    
    def run_rel_map(self,mov_pause_ms:float):
        """Run relative 2D movement map"""
        for i in range(len(self.shift_x_values)):
            print("Position before shift:",self.pidevice.qPOS())
            self.shift(self.shift_x_values[i],self.shift_y_values[i])
            time.sleep(mov_pause_ms/1000)
            self.getpos()
        print("Done")
    
    def jump_rel_map(self,index:int):
        """Execute 1 indexed jump in the relative coordinates map."""
        self.shift(self.shift_x_values[index],self.shift_y_values[index])
        time.sleep(SET_PAUSE)
        self.getpos()

    def nextshift(self):
        """Execute 1 jump in the relative coordinates map (it has to be loaded first with load_rel_map function). Useful for synchronizing with other devices"""
        self.shift(self.shift_x_values[self.shift_counter],self.shift_y_values[self.shift_counter])
        time.sleep(SET_PAUSE)
        self.getpos()
        self.shift_counter += 1
        if self.buffer_rel == self.shift_counter:
            self.shift_counter = 0
            print("Restarting map")
    
    def run_rel_path(self,shift_x_values:list,shift_y_values:list,mov_pause_ms:float):
        """Run relative 2D movement path based on input lists"""
        for i in range(len(shift_x_values)):
            print("Position before shift:",self.pidevice.qPOS())
            self.shift(shift_x_values[i],shift_y_values[i])
            time.sleep(mov_pause_ms/1000)
            self.getpos()
        print("Done")

    def geterror(self):
        """Get current error"""
        res = self.pidevice.qERR()
        return res