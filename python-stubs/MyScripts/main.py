"""
This script is what Dolphin will run 
"""
import sys
sys.path.append("SSBM_AI\python-stubs\MyScripts") # Need this in order to import other files in MyScripts/

import player
from dolphin import event, gui, memory, controller

player1 = player.BasePlayer(player_index=1)
player3 = player.BasePlayer(player_index=3) # P2 points to the same memory address as P1 for some reason, so CPU will be P3
while True:
    await event.frameadvance()
    print(f"Player 1:")
    print(f"{player1.get_percentage()}")
    print(f"{player1.get_position()}")
    print(f"{player1.get_facing_direction()}")
 
    print(f"Player 3:")
    print(f"{player3.get_percentage()}")
    print(f"{player3.get_position()}")
    print(f"{player3.get_facing_direction()}")