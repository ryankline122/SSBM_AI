"""
This script is what Dolphin will run 
"""
import sys
sys.path.append("SSBM_AI\python-stubs\src") # Need this in order to import other files in src

from agents.base_agent import BaseAgent
from agents.sample_agent import SampleAgent
from agents.dk_agent import DKAgent 
from agents.pikachu_agent import PikachuAgent 
from common.gamestate import GameState
from dolphin import event, gui, memory, controller

player1 = PikachuAgent(player_index=1)
player3 = DKAgent(player_index=3) # P2 points to the same memory address as P1 for some reason, so CPU will be P3

gamestate = GameState(players=[player1, player3])

player1.set_gamestate(gamestate)
player3.set_gamestate(gamestate)

while True:
    await event.frameadvance()
    gamestate.update_frame()
    print("Current: ", gamestate.get_current_state())
    print("Previous: ", gamestate.get_prev_state())

    if gamestate.is_game_active():
        player1.main(player1, False)
        player3.act()

        gamestate.set_prev_state(gamestate.get_current_state())
    else:
        print("Waiting for match to start...")
