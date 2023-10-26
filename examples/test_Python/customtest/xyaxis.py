"""
import xyaxis
xy = xyaxis.xy(offset_x, offset_y, "relative_coor_2d_path.csv",0)
xy.update()
xy.move(i) # 0<=i<N_relative coordinates
"""

import standa.xycontroller as controller

class xy:
    """Class to control an xy Standa controller."""
    def __init__(self, offset_x:int, offset_y:int, coord_path:str, coord_init:int):
        self.c = controller.Standa()
        self.c.setoffset(offset_x, offset_y)
        self.num_movements = self.c.load_rel_map(coord_path)
        self.c.jump_rel_map(coord_init)
        self.c.getpos()

    def move(self,index:int):
        res = self.c.jump_rel_map(index)
        return res
    
    def update(self):
       res = self.c.getpos()
       return res