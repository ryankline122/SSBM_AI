"""
This script is what Dolphin will run 
"""
import sys
sys.path.append("SSBM_AI\python-stubs\MyScripts") # Need this in order to import other files in MyScripts/

import agent
from dolphin import event, gui, memory, controller

player1 = agent.SmashAgent(player_index=1)
while True:
    await event.frameadvance()
    player1.get_character()
 
