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
        # Get the distance and frames since the last jump
        diff_x, diff_y = super().get_distance_to_opponent(coords)
        frames_since_last_jump = self.gamestate.frame - self.jumped_at_frame

        # Reset the jumped flag if it's been more than 20 frames since the last jump
        if self.jumped and frames_since_last_jump > 20:
            self.jumped = False
        
        # Keeps agent from getting stuck when oppoent is on end of platform
        target_x = 10 if diff_y >= 0 else 5

        # Adjust X position
        if diff_x < -target_x:
            super().action("right")
        elif diff_x > target_x:
            super().action("left")
        else:
            super().set_buttons("StickX", 0.0)
            controller.set_gc_buttons(self.controller_index, self.buttons)

        # Handle jumping
        if diff_y < -10 and not self.jumped:
            super().action("jump")
            self.jumped = True
            self.jumped_at_frame = self.gamestate.frame
        elif frames_since_last_jump > 5 and self.jumped:
            super().set_buttons("X", False)
            controller.set_gc_buttons(self.controller_index, self.buttons)

        # Adjust Y position
        if diff_y > 10 and super().get_buttons()['StickY'] == 0.0:
            super().set_buttons("StickY", -1.0)
        else:
            super().set_buttons("StickY", 0.0)

