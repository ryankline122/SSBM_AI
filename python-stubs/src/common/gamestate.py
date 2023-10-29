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
        - Player action state
        - Opponent KOs
        - Self destructs
        
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
        stocks = player.get_stocks()
        action_state = player.get_action_state()
        knockouts = player.get_knockouts()
        self_destructs = player.get_self_destructs()
        
        return [pos, direction, percentage, stocks, action_state, knockouts, self_destructs]
    
    def get_current_state(self):
        p1_state = self.get_player_info(0)
        p3_state = self.get_player_info(1)
        time = self.get_time_remaining()
        
        return [time, p1_state, p3_state]

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
        
    def is_terminal_state(self):        
        if self.is_game_active():
            if (int(self.get_time_remaining()) > 0 
                and int(self.players[0].get_stocks()) > 0
                and int(self.players[1].get_stocks()) > 0):
                return False
            else:
                return True
        else:
            return False
    
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