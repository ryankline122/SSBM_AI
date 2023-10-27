from .base_agent import BaseAgent
from dolphin import controller

class SampleAgent(BaseAgent):
    def __init__(self, player_index):
        super().__init__(player_index)
        
    def attack(self):
        buttons = controller.get_gc_buttons(self.controller_index)
        buttons["A"] = True
        controller.set_gc_buttons(self.controller_index, buttons)
    
    def go_to(self, coords):
        diff_x, diff_y = super().get_distance_to_opponent(coords)
        
        print(f"diff = ({diff_x}, {diff_y})")
         
        if diff_x < -20:
            super().action("right")
        elif diff_x > 20:
            super().action("left")
            
        if -20 < diff_x < 20:
            super().set_buttons("StickX", 0.0)
            controller.set_gc_buttons(self.controller_index, self.buttons)
        
            if diff_y < -10:
                super().action("jump")
            else:
                super().set_buttons("X", False)
                controller.set_gc_buttons(self.controller_index, self.buttons)
        
            
