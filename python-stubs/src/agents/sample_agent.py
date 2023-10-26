from .base_player import BasePlayer
from dolphin import controller

class SampleAgent(BasePlayer):
    def __init__(self, player_index):
        super().__init__(player_index)
        
    def attack(self):
        buttons = controller.get_gc_buttons(self.controller_index)
        buttons["A"] = True
        controller.set_gc_buttons(self.controller_index, buttons)
    
    def go_to(self, coords):
        diff = super().get_distance_to_opponent(coords)
        
        if diff[0] < -1:
            super().action("right")
        elif diff[0] > 1:
            super().action("left")
