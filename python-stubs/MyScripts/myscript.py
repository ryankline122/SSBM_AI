from dolphin import event, gui, memory, controller

class SmashAgent():
    """
    A class representing an AI agent in Super Smash Bros Melee
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
            return char_map[char_val]
        else:
            return "Unknown" 


"""

Script Entry Point

"""

red = 0xffff0000
player1 = SmashAgent(player_index=1)


while True:
    await event.frameadvance()
    buttons = controller.get_gc_buttons(1)
    buttons["A"] = True
    controller.set_gc_buttons(1, buttons)
    await event.frameadvance()
    
    # # draw on screen
    gui.draw_text((10, 10), red, f"P1: {player1.get_character()}")
    # gui.draw_text((10, 10), red, f"C1: {controller.get_gc_buttons(0)}")

