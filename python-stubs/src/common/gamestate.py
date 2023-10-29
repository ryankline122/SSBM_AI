from collections import defaultdict
from dolphin import memory
from . import utils

class GameState():
    """
    A class to hold global game state 
    """
    def __init__(self, players):
        """
        State needed to identify a given frame:
        
        Game info:
        - IsMatchRunning
        - IsPaused
        - Remaining time in match
        - Current frame
        
        Player Info:
        - Player positions 
        - Player percentages
        - Player directions
        - Player stocks
        - Player action state -07
        
        Terminal States:
        - Time remaining == 0.0
        - Agent Stocks == 0
        - Opponent Stocks == 0
        
        Rewards (use negative rewards for non-terminal states):
        - Increasing opponent percentage
        - Increase P1 KO
        
        Punishments:
        - Self Destruct
        - Increase P3 KO
        - Increasing percentage
        
        
        """
        
        
        self.frame = 0
        self.players = players
        self.Q = defaultdict(dict)
        
    def get_player_info(self, player_index):
        player = self.players[player_index]
        pos = player.get_position()
        direction = player.get_facing_direction()
        percentage = player.get_percentage()
        stocks = 0 # TODO
        action_state = 0 # TODO
        
        return [pos, direction, percentage, stocks, action_state]
    
    def get_game_info(self):
        pass
    
    def get_current_state(self):
        pass

    def is_game_active(self):
        if memory.read_u32(utils.get_value_at('Global', 'game_active')) == 0:
            return False
        else:
            return True
    
    def is_game_paused(self):
        if memory.read_u32(utils.get_value_at('Global', 'game_pause')) == 0:
            return False
        else:
            return True
    
    def get_time_remaining(self):
        """
        Returns remaining time in seconds
        """
        if self.is_game_active():
            return memory.read_u32(utils.get_value_at('Global', 'game_time'))
        else:
            return 0.0
    
    def update_frame(self):
        self.frame += 1