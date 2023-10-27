from .base_agent import BaseAgent
from dolphin import controller, event

class SampleAgent(BaseAgent):
    def __init__(self, player_index, gamestate):
        super().__init__(player_index, gamestate)
        self.jumped_at_frame = 0
        self.jumped = False
        self.gamestate = gamestate
        
    def attack(self):
        buttons = controller.get_gc_buttons(self.controller_index)
        buttons["A"] = True
        controller.set_gc_buttons(self.controller_index, buttons)
    
    def go_to(self, coords):
        """
        Takes actions to approach the given
        """
        diff_x, diff_y = super().get_distance_to_opponent(coords)
        delta_x, delta_y = super().get_position(isDelta=True)
        x, y = super().get_position()
        
        frames_since_last_jump = self.gamestate.frame - self.jumped_at_frame
        
        if self.jumped == True and frames_since_last_jump > 20:
            self.jumped = False
        
        if diff_x < -20:
            super().action("right")
        elif diff_x > 20:
            super().action("left")
            
        if -20 < diff_x < 20:
            super().set_buttons("StickX", 0.0)
            controller.set_gc_buttons(self.controller_index, self.buttons)
        
            if diff_y < -10 and not self.jumped:
                super().action("jump")
                self.jumped = True
                self.jumped_at_frame = self.gamestate.frame
                
            elif frames_since_last_jump > 4 and self.jumped:
                super().set_buttons("X", False)
                controller.set_gc_buttons(self.controller_index, self.buttons)

            if diff_y > 10:
                super().set_buttons("StickY", -1.0)
            else:
                super().set_buttons("StickY", 0.0)
