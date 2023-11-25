from .base_agent import BaseAgent
from dolphin import controller, event
import random


class PikachuAgent(BaseAgent):

    """
    A Sample Agent class to help get you started creating your own agents.
    """
    def __init__(self, player_index):
        super().__init__(player_index)
        self.jumped_at_frame = 0
        self.jumped = False
        self.gamestate = None

    def set_gamestate(self, gamestate):
        self.gamestate = gamestate

    def go_to(self, coords):
        """
        This method determines the distance between the agent and a pair of (x,y) coordinates
        and performs actions to close the distance such that the agent is within (+/-target_x, 0)
        with respect to the goal.
        """
        diff_x, diff_y = super().get_distance_to_opponent(coords)
        frames_since_last_jump = self.gamestate.frame - self.jumped_at_frame

        if self.jumped and frames_since_last_jump > 20:
            self.jumped = False

        #Keeps agent from getting stuck when oppoent is on end of platform
        target_x = 10 if diff_y >= 0 else 5

        # Adjust X position
        if diff_x < -target_x:
            super().action("right")
        elif diff_x > target_x:
            super().action("left")

        # Handle jumping
        if diff_y < -10 and not self.jumped:
            super().action("jump")
            self.jumped = True
            self.jumped_at_frame = self.gamestate.frame
        elif diff_y < -5 and frames_since_last_jump > 5 and self.jumped:
            super().action("jump")

    def recover(self, usedUPB):
        """
        Performs actions to recover.
        """
        x, y = super().get_position()
        #print(x)
        print("recovering...")
        #print("usedUPB: " + str(usedUPB))

        if( (y < -2 or (x < -70 and x > -75) or (x > 70 and x < 75)) and not usedUPB ):
            super().action("b_up")
            usedUPB = True
            #print("b_up")
        elif( x > 68.4 and x < 75):
            if (not usedUPB):
                super().action("b_up")
                usedUPB = True
            else:
                super().action("left")
        elif(x > 75):
            if (not usedUPB):
                super().action("b_left")
                #print("b_left")
            else:
                super().action("up_left")
                #print("up_left")
                #print("RESET: " + str(x))
                usedUPB = False
        elif( x < -68.4 and x > -75):
            if (not usedUPB):
                super().action("b_up")
                usedUPB = True
            else:
                super().action("right")
        elif (x < -75):
            if (not usedUPB):
                super().action("b_right")
                #print("b_right")
            else:
                super().action("up_right")
                #print("up_right")
                #print("RESET: " + str(x))
                usedUPB = False
        else:
            super().reset_buttons()
            #print("none")

        return usedUPB

    def main(self, player1, usedUPB):

        if self.gamestate.frame % 10 != 0:
            x, y = self.get_position()
            x2, y2 = player1.get_position()
            if (x < 68.4 and x > -68.4) and usedUPB:
                usedUPB = False
            if (y > 25 and x < 65 and x > -65 and y2 < y):
                self.action("down")
                #print("fall")
            if (y < -2 or x > 68.4 or x < -68.4):
                usedUPB = self.recover(usedUPB)
                #print("recover")
            else:
                diff_x, diff_y = self.get_distance_to_opponent(player1.get_position())
                if (x < 70 and x > 65):
                    self.action("b_left")
                    #print("edge left")
                elif (x > -70 and x < -65):
                    self.action("b_right")
                    #print("edge right")
                elif ((diff_x < 10 and diff_x > -10) and (diff_y < 10 and diff_y > -10) and self.gamestate.frame % 10 != 0):
                    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                    choice = random.choice(list)
                    #print("attack")
                    if (player1.get_percentage() > 70):
                        if (choice <= 6):
                            self.action("smash_up")
                        elif (choice <= 14):
                            self.action("smash_down")
                    else:
                        if (choice <= 6):
                            self.action("tilt_up")
                        elif (choice <= 13):
                            self.action("tilt_down")
                        elif (choice == 14):
                            self.action("grab")
                elif (x < 65 and x > -65):
                    if (y > 0 and (y2) > y + 20 and (diff_x < 10 and diff_x > -10) and (
                            (x > -40 and x < 40) or y > 60)):
                        self.action("b_down")
                        #print("thunder")
                    if diff_x > 0 and self.get_facing_direction() == "right":
                        super().action("left")
                    elif diff_x < 0 and self.get_facing_direction() == "left":
                        super().action("right")
                    elif (y2 < y + 5) and x2 > x + 40:
                        self.action("special")
                        #print("special")
                    else:
                        self.go_to(player1.get_position())
                        #print("goto")
                else:
                    self.reset_buttons()
                    #print("none")
        else:
            self.reset_buttons()

        return usedUPB


