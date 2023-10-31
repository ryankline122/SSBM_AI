from .base_agent import BaseAgent
from dolphin import controller, event

class DKAgent(BaseAgent):
    """
    An agent specifically designed to play as Donkey Kong
    """
    def __init__(self, player_index):
        super().__init__(player_index)
        self.jumped_at_frame = 0
        self.can_jump = True
        self.jump_count = 0
        self.gamestate = None
        self.get_distance_to_opponent = (0,0)
    
    def set_gamestate(self, gamestate):
        self.gamestate = gamestate
    
    def act(self):
        """
        Determines what state the agent should be in given the current game state.
        """
        if self.gamestate != None:
            # Get current state of the game to access opponent info
            current_state = self.gamestate.get_current_state()

            agent_state = current_state[1] if self.player_index == 'P1' else current_state[2]
            agent_pos = agent_state["Position"]
            agent_direction = agent_state["Direction"]
            agent_percentage = agent_state["Percentage"]
            agent_stocks = agent_state["Stocks"]
            agent_action_state = agent_state["Action State"]
            agent_knockouts = agent_state["Knockouts"]

            opponent_state = current_state[1] if self.player_index == 'P3' else current_state[2]
            opponent_pos = opponent_state["Position"]
            opponent_direction = opponent_state["Direction"]
            opponent_percentage = opponent_state["Percentage"]
            opponent_stocks = opponent_state["Stocks"]
            opponent_action_state = opponent_state["Action State"]
            opponent_knockouts = opponent_state["Knockouts"]
            
            stage_width = self.gamestate.get_stage_width()
            
            if (-stage_width < agent_pos[0] < stage_width):
                if (-stage_width < opponent_pos[0] < stage_width) and opponent_pos[1] >= 0:
                    # If opponent is on the stage, go after them
                    self.go_to(opponent_pos)
            else:
                self.recover()
    
    def recover(self):
        """
        Takes actions to get itself back on stage
        """
        curr_x, curr_y = super().get_position()
        
        if curr_x < -self.gamestate.get_stage_width():
            super().action("right")
        else:
            super().action("left")
            
        if curr_y < 0:
            self.handle_jumping_for_recovery() 
            
    def handle_jumping_for_recovery(self):
        """
        Handles conflicts with double jumps and Up-"B" while in recovery state
        """
        frames_since_last_jump = self.gamestate.frame - self.jumped_at_frame
        
        # Reset can_jump after 20 frames to allow for double jump
        if self.can_jump == False and frames_since_last_jump > 20:
            self.can_jump = True
            self.jump_count = 0
            
        if self.can_jump:
            super().action("jump")
            self.jump_count += 1
            self.can_jump = False
            self.jumped_at_frame = self.gamestate.frame
        elif frames_since_last_jump > 5 and self.can_jump == False and self.jump_count < 2:
            super().action("jump")
            self.jump_count += 1
            self.can_jump = False
            self.jumped_at_frame = self.gamestate.frame
            
        elif self.jump_count == 2:
            super().action("up_special")
            self.jump_count = 0
    
    def go_to(self, coords):
        """
        This method determines the distance between the agent and a pair of (x,y) coordinates
        and performs actions to close the distance such that the agent is within (+/-target_x, 0)
        with respect to the goal.
        """
        diff_x, diff_y = super().get_distance_to_opponent(coords)
        frames_since_last_jump = self.gamestate.frame - self.jumped_at_frame

        if not self.can_jump and frames_since_last_jump > 20:
            self.can_jump = True
        
        # Keeps agent from getting stuck when oppoent is on end of platform
        target_x = 10 if diff_y >= 0 else 5

        # Adjust X position
        if diff_x < -target_x:
            super().action("right")
        elif diff_x > target_x:
            super().action("left")

        # Handle jumping
        if diff_y < -10 and self.can_jump:
            super().action("jump")
            self.can_jump = False 
            self.jumped_at_frame = self.gamestate.frame
        elif diff_y < -5 and frames_since_last_jump > 5 and not self.can_jump:
            super().action("jump")

        # Adjust Y position
        # TODO: Still seems to be an issue here sometimes
        if diff_y > 10:
            if super().get_buttons()["StickY"] != -1:
                super().action("down")
            else:
                # Prevents it from getting stuck if unable to drop from platform initially
                super().action("none")
