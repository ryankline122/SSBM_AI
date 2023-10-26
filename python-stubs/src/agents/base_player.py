"""
This module contains a class representing a player in SSBM
"""
from dolphin import event, gui, memory, controller
from common import utils
import configparser
import sys

class BasePlayer():
    """
    A class representing a player in Super Smash Bros Melee.
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
        
    def get_position(self):
        """
        Returns the (x,y) position of the agent. 
        """   
        x_pos = memory.read_f32(utils.get_value_at(self.player_index, 'X'))
        y_pos = memory.read_f32(utils.get_value_at(self.player_index, 'Y'))
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
    
    def action(self, action_type):
        """
        Performs the specified action. Available actions are:
        
        Movement:
        ========================
        - jump (X or Y button)
        - left (StickX == -1.0)
        - right (StickX == 1)

        """
        # Define actions here
        if action_type == "jump":
           self.buttons["X"] = True 
        elif action_type == "left":
            self.buttons["StickX"] = -1
        elif action_type == "right":
            self.buttons["StickX"] = 1
        
        
        controller.set_gc_buttons(self.controller_index, self.buttons)
        