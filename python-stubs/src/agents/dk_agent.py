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
        self.gamestate = None
    
    def set_gamestate(self, gamestate):
        self.gamestate = gamestate
    
    def act(self):
        """
        Determines what state the agent should be in given the current game state.
        """
        if self.gamestate != None:
            current_state = self.gamestate.get_current_state()
            prev_state = self.gamestate.get_prev_state()

            # Current State of players
            curr_agent_state = current_state[1] if self.player_index == 'P1' else current_state[2]
            curr_agent_pos = curr_agent_state["Position"]
            curr_agent_direction = curr_agent_state["Direction"]
            curr_agent_percentage = curr_agent_state["Percentage"]
            curr_agent_stocks = curr_agent_state["Stocks"]
            curr_agent_action_state = curr_agent_state["Action State"]

            curr_opponent_state = current_state[1] if self.player_index == 'P3' else current_state[2]
            curr_opponent_pos = curr_opponent_state["Position"]
            curr_opponent_direction = curr_opponent_state["Direction"]
            curr_opponent_percentage = curr_opponent_state["Percentage"]
            curr_opponent_stocks = curr_opponent_state["Stocks"]

            stage_width = self.gamestate.get_stage_width()
            
            diff_x, diff_y = super().get_distance_to_opponent(curr_opponent_pos)
            attack_direction = "left" if diff_x > 0 else "right"
            
            # Roll away from opponent
            if (curr_agent_action_state == 184 or
                curr_agent_action_state == 183 or
                curr_agent_action_state == 192 or
                curr_agent_action_state == 196 or
                curr_agent_action_state == 197):
                get_up_direction = "left" if diff_x < 0 else "right"
                super().action(get_up_direction)

            # Make sure agent is facing opponent
            if diff_x > 0 and curr_agent_direction == "right":
                super().action("left")
            elif diff_x < 0 and curr_agent_direction == "left":
                super().action("right")
            
            # Determines what state the agent should be in based on its location on the stage
            if (-stage_width < curr_agent_pos[0] < stage_width ):
                if ((-stage_width < curr_opponent_pos[0] < stage_width) and curr_opponent_pos[1] >= 0):
                    if abs(diff_x) < 27 and abs(diff_y) < 20:
                        # Makes sure to do something when holding opponent
                        isHolding = True if curr_agent_action_state == 216 else False
                        self.attack(attack_direction, holding=isHolding)
                    else:
                        self.go_to(curr_opponent_pos)
            else:
                self.recover()
                
    def attack(self, direction, smash=False, holding=False):
        """
        Chooses a weighted random attack based on the current state of the players.
        """
        current_state = self.gamestate.get_current_state()
        opponent_state = current_state()[1] if self.player_index == 'P3' else current_state()[2]
        opponent_pos = opponent_state["Position"]
        opponent_percentage = opponent_state["Percentage"]
        
        diff_x, diff_y = super().get_distance_to_opponent(opponent_pos)
        
        attacks = {
            "neutral_attack": 0.2,
            "special_left": 0.4,
            "special_right": 0.4,
            "tilt_up": 0.2,
            "tilt_down": 0.5,
            "tilt_left": 0.5,
            "tilt_right": 0.5,
            "smash_up": 0.0,
            "smash_down": 0.3,
            "smash_left": 0.3,
            "smash_right": 0.3,
            "grab": 0.3,
            "block": 0.2,
        }
        
        weights = self.prepare_weights(attacks, direction, diff_y, holding)
        choice = self.weighted_random(weights)

        super().action(choice)
        
    def prepare_weights(self, attacks, direction, diff_y, holding):
        """
        Adjusts the attack weights as needed before making a selection.
        """
        weights = attacks.copy()

        current_state = self.gamestate.get_current_state()
        prev_state = self.gamestate.get_prev_state()

        curr_agent_state = current_state[1] if self.player_index == 'P1' else current_state[2]
        curr_agent_percentage = curr_agent_state["Percentage"]

        curr_opponent_state = current_state[1] if self.player_index == 'P3' else current_state[2]
        curr_opponent_percentage = curr_opponent_state["Percentage"]

        if direction == "left":
            weights["special_right"] = 0
            weights["tilt_right"] = 0
            weights["smash_right"] = 0

            if curr_opponent_percentage > 80 and super().get_buttons()['StickX'] != -1:
                weights['smash_left'] = 0.8

        elif direction == "right":
            weights["special_left"] = 0
            weights["tilt_left"] = 0
            weights["smash_left"] = 0

            if curr_opponent_percentage > 80 and super().get_buttons()['StickX'] != 1:
                weights['smash_right'] = 0.8
               
        if diff_y < 0:
            weights['tilt_down'] = 0.0
            weights['smash_down'] = 0.0
            weights['tilt_up'] = 6.0
            if curr_opponent_percentage > 80 and super().get_buttons()['StickY'] != 1:
                weights['smash_up'] = 0.8
        elif diff_y > 0:
            weights['smash_up'] = 0.0
            weights['tilt_up'] = 0.0
            if curr_opponent_percentage > 80 and super().get_buttons()['StickY'] != -1:
                weights['smash_down'] = 0.8
            
        if holding:
            weights['grab'] = 0
            weights['block'] = 0
            weights['neutral'] = 0.4
            
        if prev_state != []:
            prev_agent_state = prev_state[1] if self.player_index == 'P1' else current_state[2]
            prev_agent_percentage = prev_agent_state["Percentage"]

            prev_opponent_state = prev_state[1] if self.player_index == 'P3' else current_state[2]
            prev_opponent_percentage = prev_opponent_state["Percentage"]
            
            if curr_agent_percentage > prev_agent_percentage:
                weights['block'] = 0.6
            
        return weights

    def weighted_random(self, weights):
        """
        Makes a random choice from a list of weighted attacks.
        """
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
            return
        elif frames_since_last_jump > 4 and self.can_jump == False and self.jump_count < 2:
            super().action("jump")
            self.jump_count += 1
            self.can_jump = False
            self.jumped_at_frame = self.gamestate.frame
            return
            
        elif self.jump_count == 2:
            super().action("up_special")
            self.jump_count = 0
            return
    
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
        
        target_x = 10

        # Adjust X position
        if diff_x < -target_x:
            super().action("right")
        elif diff_x > target_x:
            super().action("left")

        # Handle jumping
        if diff_y < -15 and self.can_jump:
            super().action("jump")
            self.can_jump = False 
            self.jumped_at_frame = self.gamestate.frame
        elif diff_y < -10 and frames_since_last_jump > 5 and not self.can_jump:
            super().action("jump")

        # Adjust Y position
        frames_since_first_down = self.gamestate.frame - self.down_frame
        if diff_y > 10:
            # Prevents it from getting stuck if unable to drop from platform initially
            if frames_since_first_down > 3:
                self.down_frame = self.gamestate.frame
                super().action("down")
            else:
                super().action("none")
