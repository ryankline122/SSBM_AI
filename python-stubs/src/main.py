"""
This script is what Dolphin will run 
"""
import sys
sys.path.append("SSBM_AI\python-stubs\src") # Need this in order to import other files in src

from agents import base_player, sample_agent
from dolphin import event, gui, memory, controller

player1 = base_player.BasePlayer(player_index=1)
player3 = sample_agent.SampleAgent(player_index=3) # P2 points to the same memory address as P1 for some reason, so CPU will be P3
while True:
    await event.frameadvance()
    
    print(f"Player 1:")
    print(f"{player1.get_character()}")
    print(f"{player1.get_percentage()}")
    print(f"{player1.get_position()}")
 
    print(f"Player 3:")
    print(f"{player3.get_character()}")
    print(f"{player3.get_percentage()}")
    print(f"{player3.get_position()}")
    
    print(f"Player 1 --> 3: {player1.get_distance_to_opponent(player3.get_position())}")

    player3.go_to(player1.get_position())