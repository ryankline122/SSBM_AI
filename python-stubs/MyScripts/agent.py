from dolphin import event, gui, memory, controller

class SmashAgent():
    """
    A class representing an AI agent in Super Smash Bros Melee.
    
    Assuming agent is Player 1.
    """
    def __init__(self, player_index):
        self.player_index = player_index

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
        char_val = memory.read_u32(0x803F0E08) / 257
        
        if char_val in char_map:
            print(f"Player 1's Selected Character is: {char_map[char_val]}")
            return char_map[char_val]
        else:
            return "Unknown" 
    
    def get_facing_direction(self):
        """
        Returns a string indicating the direction the agent is facing
        """
        val = memory.read_f32(0x80C5CC0C)
        
        if val == 1:
            return "right"
        elif val == -1:
            return "left"
        
    def get_position(self):
        """
        Returns the (x,y) position of the agent. 
        
        NOTE: Memory addresses may not always be consistent.
        """   
        x_pos = memory.read_f32(0x80C5CC90)
        y_pos = memory.read_f32(0x80C5CC94)
        is_grounded = memory.read_u32(0x80C5CCC0)
        
        if is_grounded == 0 and y_pos < 1:
            y_pos = 0.0
        
        return (x_pos, y_pos)
    
    def get_percentage(self):
        """
        Returns the current percentage of the agent as a float.
        """
        return memory.read_f32(0x80C5E410)