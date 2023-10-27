class GameState():
    """
    A class to hold global game state 
    """
    def __init__(self):
        self.frame = 0
    
    def update_frame(self):
        self.frame += 1