"""
This script is what Dolphin will run 
"""
import sys
sys.path.append("SSBM_AI\python-stubs\src") # Need this in order to import other files in src

from agents.base_agent import BaseAgent
from agents.sample_agent import SampleAgent
from common.gamestate import GameState
from dolphin import event, gui, memory, controller

gamestate = GameState()
player1 = BaseAgent(player_index=1, gamestate=gamestate)
player3 = SampleAgent(player_index=3, gamestate=gamestate) # P2 points to the same memory address as P1 for some reason, so CPU will be P3
while True:
    await event.frameadvance()
    gamestate.update_frame()

    # print(f"Player 1:")
    # print(f"{player1.get_character()}")
    # print(f"{player1.get_percentage()}")
    # print(f"{player1.get_position()}")
 
    # print(f"Player 3:")
    # print(f"{player3.get_character()}")
    # print(f"{player3.get_percentage()}")
    # print(f"{player3.get_position()}")
    
    if gamestate.frame % 120 == 0:
        player3.action("grab")
    else:
        player3.reset_buttons()
    
    print(player3.buttons)
    
    # player3.go_to(player1.get_position())
    