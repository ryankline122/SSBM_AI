from .base_agent import BaseAgent
from dolphin import controller, event
import random
import itertools

class DKAgent(BaseAgent):
    """
    An agent specifically designed to play as Donkey Kong
    """
    def __init__(self, player_index):
        super().__init__(player_index)
        self.jumped_at_frame = 0
        self.can_jump = True
        self.jump_count = 0
        self.down_active = 0
        self.down_frame = 0
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
            
            diff_x, diff_y = super().get_distance_to_opponent(opponent_pos)
            attack_direction = "left" if diff_x > 0 else "right"
            
            # Make sure agent is facing opponent
            if diff_x > 0 and agent_direction == "right":
                super().action("left")
            elif diff_x < 0 and agent_direction == "left":
                super().action("right")
            
            # Determines what state the agent should be in based on its location on the stage
            if (-stage_width < agent_pos[0] < stage_width) and agent_pos[1] >= 0:
                if (-stage_width < opponent_pos[0] < stage_width) and opponent_pos[1] >= 0:
                    if abs(diff_x) < 25 and abs(diff_y) < 10:
                        self.attack(attack_direction)
                    
                    else:
                        self.go_to(opponent_pos)
            else:
                self.recover()
                
    def attack(self, direction, smash=False):
        print("Attack")
        opponent_state = self.gamestate.get_current_state()[1] if self.player_index == 'P3' else current_state[2]
        opponent_pos = opponent_state["Position"]
        opponent_percentage = opponent_state["Percentage"]
        
        diff_x, diff_y = super().get_distance_to_opponent(opponent_pos)
        
        attacks = {
            "neutral_attack": 0.1,
            "special_left": 0.2,
            "special_right": 0.2,
            "tilt_up": 0.4,
            "tilt_down": 0.4,
            "tilt_left": 0.4,
            "tilt_right": 0.4,
            "smash_up": 0.0,
            "smash_down": 0.2,
            "smash_left": 0.2,
            "smash_right": 0.2,
            "grab": 0.3,
            "block": 0.6,
        }
        
        weights = self.prepare_weights(attacks, direction, diff_y)
        choice = self.weighted_random(weights)
        
        super().action(choice)
        
    def prepare_weights(self, attacks, direction, diff_y):
        weights = attacks.copy()
        if direction == "left":
            weights["special_right"] = 0
            weights["tilt_right"] = 0
            weights["smash_right"] = 0
        elif direction == "right":
            weights["special_left"] = 0
            weights["tilt_left"] = 0
            weights["smash_left"] = 0
        if diff_y < 0:
            weights['tilt_up'] = 0.6
            weights['smash_up'] = 0.4
        elif diff_y > 0:
            weights['tilt_down'] = 0.5
        return weights

    def weighted_random(self, weights):
        running_totals = list(itertools.accumulate(weights.values()))
        target_distance = random.random() * running_totals[-1]
        for i, weight in enumerate(running_totals):
            if weight >= target_distance:
                return list(weights.keys())[i]
    
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
        elif frames_since_last_jump > 4 and self.can_jump == False and self.jump_count < 2:
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
        print("Go to")
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
        frames_since_first_down = self.gamestate.frame - self.down_frame
        if diff_y > 10:
            if super().get_buttons()["StickY"] != -1:
                # self.down_frame = self.gamestate.frame
                # self.down_active = True
                super().action("down")
            else:
                # Prevents it from getting stuck if unable to drop from platform initially
                super().action("none")
