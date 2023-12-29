from visu import Visu
from motion import Motion
from handle_events import Visu_handle_event
from pami_settings import PAMISettings
import sys
import pygame


class Case:
    def __init__(self, Motion_, Display_):
        self.pami_settings = PAMISettings()
        if Motion_: self.motion = Motion()
        if Display_: self.visu = Visu(); self.Visu_handle_event = Visu_handle_event()
        self.Motion_step = 1
        self.Display_step = 1
        self.cycle = 0
        self.B_Exit, self.B_Bleu, self.B_Jaune, self.B_Switch_C = 1, 1, 1, 0
        #TODO: faire en sorte que tout les boutton soit inscrit dans une liste de liste avec les parametre de pos de couleur ect...ect...


    def MainCase(self, Motion_, Display_):

        if Display_ == True:
            Result_Boutton  = self.Visu_handle_event.handle_events([self.B_Exit, self.B_Bleu, self.B_Jaune, self.B_Switch_C])
            
            if Result_Boutton[0] == 1:
                print("Quite")
                pygame.quit()
                sys.exit() 
            
            if self.Display_step == 1:
                self.visu.fill_screen("WHITE")
                self.visu.draw_screen_border("RED")
                self.visu.draw_button("BLUE", 500,0, 800,300+15//2, 15)
                self.visu.draw_button("YELLOW", 500,300-15//2, 800,600, 15)
                self.visu.draw_num_pami((250, 300))
                if Result_Boutton[1] == 1: self.Display_step = 2; print("Team Bleu") ; self.B_Bleu = 0; self.B_Jaune = 0; self.B_Switch_C = 1
                if Result_Boutton[2] == 1: self.Display_step = 3; print("Team Jaune"); self.B_Bleu = 0; self.B_Jaune = 0; self.B_Switch_C = 1
                
            elif self.Display_step == 2:   
                self.visu.fill_screen("BLUE")
                self.visu.draw_screen_border("GREEN")
                self.visu.draw_button("GREEN", 500,0, 800,600)
                self.visu.draw_button("YELLOW", 550,350, 750,550 ,15)
                if Result_Boutton[3] == 1: self.Display_step = 3; print("Team Jaune")
                self.visu.draw_num_pami((250, 300))
                
            elif self.Display_step == 3:   
                self.visu.fill_screen("YELLOW")
                self.visu.draw_screen_border("GREEN")
                self.visu.draw_button("GREEN", 500,0, 800,600)
                self.visu.draw_button("BLUE", 550,350, 750,550 ,15)
                if Result_Boutton[3] == 1: self.Display_step = 2; print("Team Bleu")
                self.visu.draw_num_pami((250, 300))

            elif self.Display_step == 4:   
                if self.cycle % 40 == 0:
                    self.visu.draw_coccinelle("Gauche")
                elif self.cycle % 40 == 10:
                    self.visu.draw_coccinelle("Milieu")
                elif self.cycle % 40 == 20:
                    self.visu.draw_coccinelle("Droite")

            self.visu.draw_cross_button()
            self.visu.update()


        if Motion_ == True:

            if self.Motion_step == 1:
                self.Motion_step = self.motion.tourner(-3600, 1, 5)

            elif self.Motion_step == 2:
                self.Motion_step = self.motion.tourner(180, 2, 3)

            elif self.Motion_step == 3:
                self.Motion_step = self.motion.avancer(500, 3, 4)

            elif self.Motion_step == 4:
                self.Motion_step = self.motion.tourner(-180, 4, 1)

            elif self.Motion_step == 5:
                self.motion.STOP()

        self.cycle += 1