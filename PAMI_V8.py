""" Auteur: Wehren Tim
    Date:   04.10.2023

    Programme pour les PAMI avec un RaspBerry V4
    SANS STEP CASE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# Importation des bibliothèques nécessaires
import math                     # Module math pour les calculs mathématiques
import pygame                   # Bibliothèque pour la création d'interfaces graphiques
import sys                      # Module pour l'interaction avec le système d'exploitation
from U2D2_Module import Dxl     # Importe la classe Dxl du module U2D2_Module
import time                     # Pour gèrer tout ce qui est "Temps"
import signal

####################################################################################################
# Variable Constantes (normalement pas besoin de les changer)                                      #                     
SCREEN_W = 800              # Largeur de l'écran                                                   #         
SCREEN_H = 600              # Hauteur de l'écran                                                   #         
BLUE = (0, 91, 140)         # Couleur bleue                                                        #     
YELLOW = (247, 181, 0)      # Couleur jaune                                                        #         
RED = (255, 10, 10)         # Couleur rouge                                                        #     
BLACK = (0, 0, 0)           # Couleur noire                                                        #     
WHITE = (255, 255, 255)     # Couleur blanche                                                      #             
BIG_FONT = 800              # Taille de la police de caractères                                    #  
SMALL_FONT = 120            # Taille de la police de caractères                                    #   
TIMER_FONT = 400            # Taille de la police de caractères                                    #                    
####################################################################################################


class PAMI: # Classe PAMI ou tout le programme vas ce faire 


    def __init__(self):
        # Initialisation de pygame et création de la fenêtre + Titre fenetre
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN) #, pygame.FULLSCREEN     #  Enlever le "pygame.FULLSCREEN" peut aider a programmer la visu sur PC  
        pygame.display.set_caption("Pami_Visu")
        self.BIG_FONT = pygame.font.Font(None, BIG_FONT)
        self.SMALL_FONT = pygame.font.Font(None, SMALL_FONT)
        self.TIMER_FONT = pygame.font.Font(None, TIMER_FONT)
    

        ####################################################################################################
        # Paramètres des servomoteurs (à changer pour chaque PAMI)
        self.ID_Servo = [30, 31]
        self.D1, self.D2 = 41.73, 41.73
        self.Entraxe = 63
        self.Num_PAMI = 12
        ####################################################################################################


        def close(signal, frame):
            print("\nTurning off ultrasonic distance detection...\n")
            GPIO.cleanup() 
            sys.exit(0)


        # Initialisation GPIO (lybrary disponible que sur Raspberry) 
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            print("import GPIO succesful")
            self.GPIO.setmode(GPIO.BCM)
            print("GPIO setmode succesful")
            self.button_pin = 26
            self.pinTrigger = 20
            self.pinEcho = 21
            signal.signal(signal.SIGINT, close)
            print("signal close succesful")
            self.GPIO.setwarnings(False)
            print("setwarnings False succesful")
            self.GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.GPIO.setup(self.pinTrigger, GPIO.OUT)
            self.GPIO.setup(self.pinEcho,    GPIO.IN )
            print("setup IN / OUT succesful")
        except:
            print("GPIO NNOOTT succesful")
            pass


        # Initialisation de Dxl
        self.dxl = Dxl()                        # Import de U2D2 la classe Dxl sous le nom dxl

        # Initialisation parametrage des servo
        self.dxl.ModeRot(self.ID_Servo[0], 4)   # Définit le mode de rotation à (Extended Position Control Mode (Multi-turn))
        self.dxl.ModeRot(self.ID_Servo[1], 4)   # Définit le mode de rotation à (Extended Position Control Mode (Multi-turn))
        self.dxl.EcrireVitesse(self.ID_Servo[0],32767)
        self.dxl.EcrireVitesse(self.ID_Servo[1],32767)
        self.dxl.TorqueON(self.ID_Servo[0])     # Met le torque a 1 
        self.dxl.TorqueON(self.ID_Servo[1])     # Met le torque a 1
        self.dxl.ProfileAcceleration(self.ID_Servo[0],40)
        self.dxl.ProfileAcceleration(self.ID_Servo[1],40)
        self.dxl.PositionGoal(self.ID_Servo[0],(0))
        self.dxl.PositionGoal(self.ID_Servo[1],(0))

        # Initialisation d'autres variables
        self.POS_Actuelle = [0, 0]
        self.Pos_0 = (self.dxl.LirePosition(self.ID_Servo[0]))[1], (self.dxl.LirePosition(self.ID_Servo[1]))[1]
        self.step_case = 0
        self.background_color = BLACK  
        self.Bouton_J = 0   # Bouton Jeaune
        self.Bouton_B = 0   # Bouton Bleu
        self.Bouton_Actif = [1, 1, 0]
        self.color_SMALL_num_pami = WHITE


    def GPIO_Gestion(self):
        try:
            # print("START GPIO GESTIONNNNNNNNNNNNNNNNNNNNNNNN")
            # set Trigger to HIGH
            self.GPIO.output(self.pinTrigger, True)
            # print("2")
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            # print("2")
            self.GPIO.output(self.pinTrigger, False)
            # print("3")
            # print("mesure done")
            startTime = time.time()
            stopTime = time.time()

            # save start time
            while 0 == self.GPIO.input(self.pinEcho):
                startTime = time.time()
                print("chui keblo dans la 1")

            # save time of arrival
            while 1 == self.GPIO.input(self.pinEcho):
                stopTime = time.time()
                print("chui keblo dans la 2")
            # print("2x wile passe")
            # time difference between start and arrival
            TimeElapsed = stopTime - startTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
            print ("Distance: %.1f cm" % distance)
        except: 
            print("Capteur Ultra-Son fonctione pas")
            pass


    def draw_buttons(self): # Méthode pour dessiner les boutons
        button_height = 300
        button_width = 200
        border_thickness = 8

        # Dessine le bouton bleu avec une bordure noire
        pygame.draw.rect(self.screen, BLUE, (600, 0, button_width, button_height))
        pygame.draw.rect(self.screen, BLACK, (600, 0, button_width, button_height), border_thickness)

        # Dessine le bouton jaune avec une bordure noire
        pygame.draw.rect(self.screen, YELLOW, (600, 300, button_width, button_height))
        pygame.draw.rect(self.screen, BLACK, (600, 300, button_width, button_height), border_thickness)
    

    def draw_cross_button(self):    # Méthode pour dessiner le bouton de fermeture
        # Dessine le bouton de fermeture rouge avec une bordure noire
        pygame.draw.rect(self.screen, RED, (0, 0, 50, 50))
        pygame.draw.rect(self.screen, BLACK, (0, 0, 50, 50), 2)

        # Dessinez une croix blanche sur le bouton de fermeture avec une bordure blanche
        pygame.draw.line(self.screen, WHITE, (10, 10), (40, 40), 5)
        pygame.draw.line(self.screen, WHITE, (10, 40), (40, 10), 5)


    def draw_timer(self): 
        # Afficher le timer
        current_time = time.time()
        elapsed_time = current_time - self.wait_start_time
        timer_text = f"{5-elapsed_time:.0f}"

        # Rotation du texte à la verticale
        rotated_text = pygame.transform.rotate(self.TIMER_FONT.render(timer_text, True, WHITE), 90)
        self.screen.blit(rotated_text, ((SCREEN_W/2)-(rotated_text.get_size()[0]/2), (SCREEN_H/2)-(rotated_text.get_size()[1]/2)))
 

    def draw_BIG_num_pami(self):
        if self.Bouton_B == 1:
            self.color_SMALL_num_pami = BLUE
            self.color_BIG_num_pami = WHITE
        elif self.Bouton_J == 1:
            self.color_SMALL_num_pami = YELLOW
            self.color_BIG_num_pami = WHITE
        else : self.color_BIG_num_pami = BLACK
        
        rotated_1 = pygame.transform.rotate(self.BIG_FONT.render(str(self.Num_PAMI), True, self.color_BIG_num_pami), 90)
        self.screen.blit(rotated_1, (0, (SCREEN_H / 2) - rotated_1.get_size()[1] / 2))


    def draw_SMALL_num_pami(self):
        if self.Bouton_B == 1:
            self.color_SMALL_num_pami = BLUE
        elif self.Bouton_J == 1:
            self.color_SMALL_num_pami = YELLOW
        rotated_1 = pygame.transform.rotate(self.SMALL_FONT.render(str(self.Num_PAMI), True, self.color_SMALL_num_pami), 90)
        self.screen.blit(rotated_1, (10, (SCREEN_H - rotated_1.get_size()[1]) - 15))


    def fill_screen(self,color):
        self.screen.fill(color)


    def draw_border_screen(self):
        # Dessine un contour noir tout autour de la visu
        border_thickness = 15
        pygame.draw.rect(self.screen, self.color_SMALL_num_pami, (0, 0, SCREEN_W, SCREEN_H), border_thickness)


    def draw_ready_box(self):
        ready_box_width = 300
        ready_box_height = SCREEN_H
        ready_box_x = SCREEN_W - ready_box_width
        ready_box_y = 0
        pygame.draw.rect(self.screen, (0, 255, 0), (ready_box_x, ready_box_y, ready_box_width, ready_box_height))

        # Écrit "PRÊT" à la verticale au milieu du rectangle
        font = pygame.font.Font(None, 300)  # Taille de la police
        text_surface = font.render("PRÊT", True, BLACK)

        # Rotation du texte à la verticale
        rotated_text = pygame.transform.rotate(text_surface, 90)

        # Positionner le texte au milieu du rectangle
        text_x = ready_box_x + ready_box_width // 2 - rotated_text.get_width() // 2
        text_y = ready_box_y + ready_box_height // 2 - rotated_text.get_height() // 2
        self.screen.blit(rotated_text, (text_x, text_y))


    def draw_circle(self, x, y, diameter, color):
        pygame.draw.circle(self.screen, color, (x, y), diameter // 2)


    def draw_elipse(self,x ,y ,largeur, hauteur, color):
        pygame.draw.ellipse(self.screen, color, (x, y, largeur, hauteur))


    def draw_coccinelle(self,direction):
        # tete coccinelle
        self.draw_circle(700, 300, 850, BLACK) # tete
        #pygame.draw.line(self.screen, BLACK, (0, 300), (300, 300), 27)
        pygame.draw.polygon(self.screen, BLACK, [(0, 270), (0, 330), (490,300)])
        # Antenne 1 (droite)
        pygame.draw.circle(self.screen, BLACK, (200, 80), 30)  # Rond noir
        pygame.draw.line(self.screen, BLACK, (200, 80), (330, 150), 15)
        pygame.draw.circle(self.screen, WHITE, (200, 80), 20)  # Rond BLANC
        # Antenne 2 (gauche)
        pygame.draw.circle(self.screen, BLACK, (200, 520), 30)  # Rond noir
        pygame.draw.line(self.screen, BLACK, (200, 520), (330, 450), 15)
        pygame.draw.circle(self.screen, WHITE, (200, 520), 20)  # Rond BLANC
        # tache noir 
        pygame.draw.circle(self.screen, BLACK, (70, 490), 45)
        pygame.draw.circle(self.screen, BLACK, (70, 110), 45) 
        pygame.draw.circle(self.screen, BLACK, (200, 200), 45)  
        pygame.draw.circle(self.screen, BLACK, (200, 400), 45)    


        if direction == "gauche":
            # Dessin des yeux à gauche
            self.draw_elipse(400, 100, 450, 250, WHITE) # Ovale blanc droite
            self.draw_elipse(400, 350, 450, 250, WHITE) # Ovale blanc Gauche
            self.draw_elipse(500, 150, 350, 150, BLACK) # Ovale noir droite
            self.draw_elipse(500, 400, 350, 150, BLACK) # Ovale noir Gauche
            self.draw_elipse(520, 155, 100, 65 , WHITE) # Ovale blanc Gauche
            self.draw_elipse(520, 405, 100, 65 , WHITE) # Ovale blanc droite

        elif direction == "droite":
            # Dessin des yeux à droite
            self.draw_elipse(400, 0  , 450, 250, WHITE) # Ovale blanc droite
            self.draw_elipse(400, 250, 450, 250, WHITE) # Ovale blanc Gauche
            self.draw_elipse(500, 50 , 350, 150, BLACK) # Ovale noir droite
            self.draw_elipse(500, 300, 350, 150, BLACK) # Ovale noir Gauche
            self.draw_elipse(520, 55 , 100, 65 , WHITE) # Ovale blanc Gauche
            self.draw_elipse(520, 305, 100, 65 , WHITE) # Ovale blanc droite

        elif direction == "milieu":
            # Dessin des yeux au millieux
            self.draw_elipse(400, 50 , 450, 250, WHITE) # Ovale blanc droite
            self.draw_elipse(400, 300, 450, 250, WHITE) # Ovale blanc Gauche
            self.draw_elipse(500, 100, 350, 150, BLACK) # Ovale noir droite
            self.draw_elipse(500, 350, 350, 150, BLACK) # Ovale noir Gauche
            self.draw_elipse(520, 105, 100, 65 , WHITE) # Ovale blanc Gauche
            self.draw_elipse(520, 355, 100, 65 , WHITE) # Ovale blanc droite


    def draw_timer_temps_pami_10sec(self):
        # Afficher le timer
        current_time = time.time()
        elapsed_time = current_time - self.wait_start_time_3 
        timer_text = f"{10-elapsed_time:.0f}"
        if 0.1 > float(timer_text): 
            timer_text = "0"

        # Rotation du texte à la verticale
        rotated_text = pygame.transform.rotate(self.TIMER_FONT.render(timer_text, True, WHITE), 90)
        self.screen.blit(rotated_text, ((0), (SCREEN_H/2)-(rotated_text.get_size()[1]/2)))


    def draw_choix_couleur_apres_choix_couleur(self):
        button_height = 100
        button_width = 100
        border_thickness = 5
        # Dessine le bouton avec une bordure noire
        if self.color_SMALL_num_pami == YELLOW:
            pygame.draw.rect(self.screen, BLUE, (0, 500, button_width, button_height))
            pygame.draw.rect(self.screen, BLACK, (0, 500, button_width, button_height), border_thickness)
        elif self.color_SMALL_num_pami == BLUE:
            pygame.draw.rect(self.screen, YELLOW, (0, 500, button_width, button_height))
            pygame.draw.rect(self.screen, BLACK, (0, 500, button_width, button_height), border_thickness)



    def VISU(self,VISU): # Géstionnaire visu PAMI
        if VISU == 0: # Visu 0: Start et choix couleur
            self.fill_screen(WHITE)
            self.draw_BIG_num_pami()
            self.draw_buttons()
            self.draw_cross_button()

        elif VISU == 1: # Visu 1: Attente début match
            self.fill_screen(self.color_SMALL_num_pami)
            self.draw_ready_box()
            self.draw_border_screen()
            self.draw_BIG_num_pami()
            self.draw_cross_button()
            self.draw_choix_couleur_apres_choix_couleur()

        elif VISU == "milieu": # VISU: Coccinelle regarde millieu
            self.fill_screen(RED)
            self.draw_border_screen()
            self.draw_cross_button()
            self.draw_coccinelle("milieu")
            self.draw_SMALL_num_pami()

        elif VISU == "gauche": # VISU: Coccinelle regarde Gauche
            self.fill_screen(RED)
            self.draw_border_screen()
            self.draw_cross_button()
            self.draw_coccinelle("gauche")
            self.draw_SMALL_num_pami()
        
        elif VISU == "droite": # VISU: Coccinelle regarde droite
            self.fill_screen(RED)
            self.draw_border_screen()
            self.draw_cross_button()
            self.draw_coccinelle("droite")
            self.draw_SMALL_num_pami()
            

    def handle_events(self):    # Méthode pour gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if (self.Bouton_Actif[1]) and (600 <= x <= 800):
                    if 0 <= y <= 300:
                        self.Bouton_B = 1
                        self.Bouton_Actif[1] = 0
                    elif 300 <= y <= 600:
                        self.Bouton_J = 1
                        self.Bouton_Actif[1] = 0
                    else:
                        self.Bouton_J, self.Bouton_B = 0
                if (self.Bouton_Actif[0]) and (0 <= x <= 50 and 0 <= y <= 50):
                    pygame.quit()
                    sys.exit()
                if (self.Bouton_Actif[2]) and (0 <= x <= 500 and 0 <= y <= 600):
                    if self.Bouton_J == 1:
                        self.Bouton_J = 0
                        self.Bouton_B = 1
                        self.Bouton_Actif[2] = 0
                    elif self.Bouton_B == 1:
                        self.Bouton_B = 0
                        self.Bouton_J = 1
                        self.Bouton_Actif[2] = 0

    
    def update_visu(self):  # Méthode pour mettre à jour l'affichage
        pygame.display.flip()


    def avancer(self, distance_mm, Step_case):
        print("step_case = ", self.step_case)
        Distance = (360 / (self.D1 + self.D2 / 2)) * distance_mm
        Pos_1 = int(Distance * (4096 / 360))    # Resolution = 4096 [pulse/rev]
        Pos_2 = int(Distance * (4096 / 360) * -1)    # Resolution = 4096 [pulse/rev]
        self.dxl.PositionGoal(self.ID_Servo[0], self.POS_Actuelle[0] + Pos_1)
        self.dxl.PositionGoal(self.ID_Servo[1], self.POS_Actuelle[1] + Pos_2)

        if self.dxl.EnMouvement(self.ID_Servo[0])[1] == 0 and self.dxl.EnMouvement(self.ID_Servo[1])[1] == 0:
            self.POS_Actuelle = (self.dxl.LirePosition(self.ID_Servo[0]))[1], (self.dxl.LirePosition(self.ID_Servo[1]))[1]
            print("Avance FINI")
            self.step_case = Step_case
        elif self.dxl.EnMouvement(self.ID_Servo[0])[1] == 1 or self.dxl.EnMouvement(self.ID_Servo[1])[1] == 1:
            print("Avance en cours")


    def tourner(self, angle, Step_case):
        Pos_1 = int(angle * (4096 / 360))   # Resolution = 4096 [pulse/rev]
        Pos_2 = int(angle * (4096 / 360))   # Resolution = 4096 [pulse/rev]
        self.dxl.PositionGoal(self.ID_Servo[0], self.POS_Actuelle[0] + Pos_1)
        self.dxl.PositionGoal(self.ID_Servo[1], self.POS_Actuelle[1] - Pos_2)

        if self.dxl.EnMouvement(self.ID_Servo[0])[1] == 0 and self.dxl.EnMouvement(self.ID_Servo[1])[1] == 0:
            self.POS_Actuelle = (self.dxl.LirePosition(self.ID_Servo[0]))[1], (self.dxl.LirePosition(self.ID_Servo[1]))[1]
            print("Rotation FINI")
            self.step_case = Step_case
        elif self.dxl.EnMouvement(self.ID_Servo[0])[1] == 1 or self.dxl.EnMouvement(self.ID_Servo[1])[1] == 1:
            print("Rotation en cours")


    def Time_Record(self):
        # Enregistrez le temps de départ
        self.start_time = time.time()


    def STOP(self):
        self.dxl.PositionGoal(self.ID_Servo[0],(self.dxl.LirePosition(self.ID_Servo[0]))[1])
        self.dxl.PositionGoal(self.ID_Servo[1],(self.dxl.LirePosition(self.ID_Servo[1]))[1])


    def Gestion_temps_pami(self):
        if 999 > self.step_case >= 20:
            current_time_3 = time.time()
            self.draw_timer_temps_pami_10sec()
            if current_time_3 - self.wait_start_time_3 >=10: # Attendre 5 secondes
                self.step_case = 1000 
                self.wait_start_time_3 = time.time()
            print(current_time_3 - self.wait_start_time_3)


    def run(self):

        self.visu = 0
        
        self.Time_Record()

        while True:

            self.handle_events()

            #self.GPIO_Gestion()
            
            self.VISU(self.visu)

        ########################################################################################################################################################
            if self.step_case == 0: # Attente choix couleur (équipe)

                self.visu = 0                               # visu choix couleur

                if self.Bouton_B or self.Bouton_J == 1:     # attente choix couleur
                    self.step_case = 5                      # passe a la prochaine étape
                    self.wait_start_time_1 = time.time()    # Enregistrez le moment où vous commencez à attendre pour la prochaine case


        ########################################################################################################################################################
            elif self.step_case == 5: # attendre début MATCH (capteur distance)

                self.visu = 1                               # visu PRET avec  chiffre pami en gros
                self.Bouton_Actif = [1,0,1]                   # Desactivation bouton Jeaune et Bleu 
                
                ############################################################################
                print("normalement attente capteur")
                current_time_1 = time.time()
                if current_time_1 - self.wait_start_time_1 >=5: # Attendre 5 secondes
                    self.step_case = 10 
                    self.wait_start_time_2 = time.time()
                print(current_time_1 - self.wait_start_time_1)
                ############################################################################
            

        ########################################################################################################################################################
            elif self.step_case == 10: # attendre Début pami

                self.visu = "milieu"                        # visu coccinelle visage millieu

                ############################################################################
                current_time_2 = time.time()
                if current_time_2 - self.wait_start_time_2 >=5: # Attendre 5 secondes
                    self.step_case = 20 
                    self.wait_start_time_3 = time.time()
                print(current_time_2 - self.wait_start_time_2)
                ############################################################################


        ########################################################################################################################################################
            elif self.step_case == 20: # attendre Début pami
                self.visu = "milieu"
                self.avancer(2000, 30)


        ########################################################################################################################################################
            #elif self.step_case == 30: 
                #self.visu = "gauche"
                #self.tourner(180, 40)


        ########################################################################################################################################################
            elif self.step_case == 40: # attendre Début pami
                self.visu = "milieu"
                self.avancer(2000, 1000)
            

        ########################################################################################################################################################
            elif self.step_case == 1000:
                self.visu = "milieu"
                self.STOP()
                print("FIN")

            self.Gestion_temps_pami()

            self.update_visu()      

if __name__ == "__main__":
    pami = PAMI()
    pami.run()
