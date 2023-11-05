"""
This module contains a class representing a agent in SSBM
"""
from dolphin import event, gui, memory, controller
from common import utils
import configparser
import sys

class BaseAgent():
    """
    A class representing an agent in Super Smash Bros Melee.
    """
    def __init__(self, player_index):
        # Maps player number to string to access proper configuration
        player_index_map = {
            1: "P1",
            2: "P2",
            3: "P3",
            4: "P4"
        }
        self.player_index = player_index_map[player_index]
        self.controller_index = player_index - 1
        self.buttons = controller.get_gc_buttons(self.controller_index)

    def get_character(self):
        """
        Returns the character name of the agent.
        """
        char_map = {
            0: 'Dr. Mario',
            1: 'Mario',
            2: 'Luigi',
            3: 'Bowser',
            4: 'Peach',
            5: 'Yoshi',
            6: 'DK',
            7: 'Captain Falcon',
            8: 'Ganondorf',
            9: 'Falco',
            10: 'Fox',
            11: 'Ness',
            12: 'Ice Climbers',
            13: 'Kirby',
            14: 'Samus',
            15: 'Zelda',
            16: 'Link',
            17: 'Young Link',
            18: 'Pichu',
            19: 'Pikachu',
            20: 'Jigglypuff',
            21: 'Mewtwo',
            22: 'Mr Game and Watch',
            23: 'Marth',
            24: 'Roy',
        }
        char_val = hex(memory.read_u32(utils.get_value_at(self.player_index, 'Character')))
        char_val = (int(char_val[2:], 16) & 0xFFFF) / 257
        
        if char_val in char_map:
            return char_map[char_val]
        else:
            return "Unknown" 
    
    def get_facing_direction(self):
        """
        Returns a string indicating the direction the agent is facing
        """
        val = memory.read_f32(utils.get_value_at(self.player_index, 'Direction'))
        
        if val == 1:
            return "right"
        elif val == -1:
            return "left"
        
    def get_stocks(self):
        val = hex(memory.read_u32(utils.get_value_at(self.player_index, 'stocks')))
        return val[2]
    
    def get_action_state(self):
        return memory.read_u32(utils.get_value_at(self.player_index, 'action_state'))
    
    def get_position(self, isDelta=False):
        """
        Returns the (x,y) position of the agent. 
        """
        if not isDelta: 
            x_pos = memory.read_f32(utils.get_value_at(self.player_index, 'X'))
            y_pos = memory.read_f32(utils.get_value_at(self.player_index, 'Y'))
        else:
            x_pos = memory.read_f32(utils.get_value_at(self.player_index, 'X_delta'))
            y_pos = memory.read_f32(utils.get_value_at(self.player_index, 'Y_delta'))
        
        is_grounded = memory.read_u32(utils.get_value_at(self.player_index, 'isGrounded'))
        if is_grounded == 0 and y_pos < 1:
            y_pos = 0.0
        
        return (x_pos, y_pos)
    
    def get_percentage(self):
        """
        Returns the current percentage of the agent as a float.
        """
        return memory.read_f32(utils.get_value_at(self.player_index, 'Percentage'))

    def get_distance_to_opponent(self, opponent_pos):
        """
        Returns the difference between the two player positions.
        
        Positive x = to the left
        Positive y = under
        Negative x = to the right
        Positive y = above 
        """
        curr_x, curr_y = self.get_position()
        opp_x, opp_y = opponent_pos

        return ((curr_x - opp_x), (curr_y - opp_y))
    
    def get_knockouts(self):
        return memory.read_u32(utils.get_value_at(self.player_index, 'knockouts'))

    def get_self_destructs(self):
        sd_map = {
            0: 0,
            768: 0,
            66048: 1,
            131328: 2,
            196608: 3
        }
        val = memory.read_u32(utils.get_value_at(self.player_index, 'self_destructs'))
        
        if val in sd_map:
            return sd_map[val]
    
    def action(self, action_type, reset_buttons=True):
        """
        Performs the specified action. Available actions are:
        
        Movement:
        ========================
        - jump
        - left
        - right
        - down

        Attack:
        ========================
        - neutral_attack
        - tilt_up
        - tilt_down
        - tilt_left
        - tilt_right
        - smash_up
        - smash_down
        - smash_left
        - smash_right

        Specials:
        ========================
        - neutral_special
        - up_special
        - down_special
        - left_special
        - right_special

        Other:
        ========================
        - shield
        - grab
        """
        if reset_buttons and action_type != "block":
            self.reset_buttons()
        
        # Movement
        if action_type == "jump":
           self.buttons["X"] = True 
        elif action_type == "left":
            self.buttons["StickX"] = -1
        elif action_type == "right":
            self.buttons["StickX"] = 1
        elif action_type == "down":
            self.buttons["StickY"] = -1
            
        # Neutral Attacks
        elif action_type == "neutral_attack":
            self.buttons["A"] = True
        
        # Special Moves
        elif action_type == "neutral_special":
            self.buttons["B"] = True
        elif action_type == "up_special":
            self.buttons["StickY"] = 1
            self.buttons["B"] = True
        elif action_type == "down_special":
            self.buttons["StickY"] = -1
            self.buttons["B"] = True
        elif action_type == "left_special":
            self.buttons["StickX"] = -1
            self.buttons["B"] = True
        elif action_type == "right_special":
            self.buttons["StickX"] = 1
            self.buttons["B"] = True
            
        # Tilt Attacks - for left and right check facing direction
        elif action_type == "tilt_left":
            self.buttons["StickX"] = -0.4
            self.buttons["A"] = True
        elif action_type == "tilt_right":
            self.buttons["StickX"] = 0.4
            self.buttons["A"] = True
        elif action_type == "tilt_up":
            self.buttons["StickY"] = 0.4
            self.buttons["A"] = True
        elif action_type == "tilt_down":
            self.buttons["StickY"] = -0.4
            self.buttons["A"] = True

        # Smash Attacks
        elif action_type == "smash_left":
            self.buttons["StickX"] = -1
            self.buttons["A"] = True
        elif action_type == "smash_right":
            self.buttons["StickX"] = 1
            self.buttons["A"] = True
        elif action_type == "smash_up":
            self.buttons["StickY"] = 1
            self.buttons["A"] = True
        elif action_type == "smash_down":
            self.buttons["StickY"] = -1
            self.buttons["A"] = True

        # Other
        elif action_type == "block":
            self.buttons["TriggerLeft"] = 1
        elif action_type == "grab":
            self.buttons["Z"] = True
        elif action_type == "none":
            pass
            
        controller.set_gc_buttons(self.controller_index, self.buttons)
        
    def set_buttons(self, button, value):
        self.buttons[button] = value
    
    def get_buttons(self):
        return self.buttons

    def reset_buttons(self):
        self.buttons = {
            'A': False,
            'B': False,
            'X': False,
            'Y': False,
            'Z': False,
            'Start': False,
            'Up': False,
            'Down': False,
            'Left': False,
            'Right': False,
            'L': False,
            'R': False,
            'StickX': 0.0,
            'StickY': 0.0,
            'CStickX': 0.0,
            'CStickY': 0.0,
            'TriggerLeft': 0.0,
            'TriggerRight': 0.0,
        }
        
        controller.set_gc_buttons(self.controller_index, self.buttons)