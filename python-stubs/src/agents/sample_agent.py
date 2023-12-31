from .base_agent import BaseAgent
from dolphin import controller, event

class SampleAgent(BaseAgent):
    """
    A Sample Agent class to help get you started creating your own agents.
    """
    def __init__(self, player_index):
        super().__init__(player_index)
        self.jumped_at_frame = 0
        self.jumped = False
        self.gamestate = None 
    
    def set_gamestate(self, gamestate):
        self.gamestate = gamestate
    
    def go_to(self, coords):
        """
        This method determines the distance between the agent and a pair of (x,y) coordinates
        and performs actions to close the distance such that the agent is within (+/-target_x, 0)
        with respect to the goal.
        """
        diff_x, diff_y = super().get_distance_to_opponent(coords)
        frames_since_last_jump = self.gamestate.frame - self.jumped_at_frame

        if self.jumped and frames_since_last_jump > 20:
            self.jumped = False
        
        # Keeps agent from getting stuck when oppoent is on end of platform
        target_x = 10 if diff_y >= 0 else 5

        # Adjust X position
        if diff_x < -target_x:
            super().action("right")
        elif diff_x > target_x:
            super().action("left")

        # Handle jumping
        if diff_y < -10 and not self.jumped:
            super().action("jump")
            self.jumped = True
            self.jumped_at_frame = self.gamestate.frame
        elif diff_y < -5 and frames_since_last_jump > 5 and self.jumped:
            super().action("jump")

        # Adjust Y position
        if diff_y > 10:
            if super().get_buttons()["StickY"] != -1:
                super().action("down")
            else:
                # Prevents it from getting stuck if unable to drop from platform initially
                super().action("none")
