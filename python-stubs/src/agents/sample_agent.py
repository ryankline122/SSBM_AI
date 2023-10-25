from .base_player import BasePlayer
from dolphin import controller

class SampleAgent(BasePlayer):
    def __init__(self, player_index):
        super().__init__(player_index)
        self.controller_index = player_index - 1
        
    def attack(self):
        buttons = controller.get_gc_buttons(self.controller_index)
        buttons["A"] = True
        controller.set_gc_buttons(self.controller_index, buttons)