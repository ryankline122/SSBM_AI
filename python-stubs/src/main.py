"""
This script is what Dolphin will run 
"""
import sys
sys.path.append("C:\\Users\matth\PycharmProjects\AI_Final_Project\dolphin-scripting-preview3-x64\SSBM_AI\python-stubs\src") # Need this in order to import other files in src

from agents.base_agent import BaseAgent
from agents.sample_agent import SampleAgent
from agents.pikachu_agent import PikachuAgent
from agents.dk_agent import DKAgent
from common.gamestate import GameState
from dolphin import event, gui, memory, controller

player1 = DKAgent(player_index=1)
player3 = PikachuAgent(player_index=3)
gamestate = GameState(players=[player1, player3])
player1.set_gamestate(gamestate)
player3.set_gamestate(gamestate)
usedUPB = False

while True:
    await event.frameadvance()
    gamestate.update_frame()
    #print("Current: ", gamestate.get_current_state())
    #print("Previous: ", gamestate.get_prev_state())
    if gamestate.is_game_active():
        player1.act()
        usedUPB = player3.main(player1, usedUPB)
        gamestate.set_prev_state(gamestate.get_current_state())
    else:
        print("Waiting for match to start...")