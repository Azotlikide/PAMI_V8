from U2D2_Module import Dxl
from pami_settings import PAMISettings
import math


class Motion:
    def __init__(self):
        self.dxl = Dxl()
        # Import les Parametre des PAMI
        self.pami_settings = PAMISettings()
        self.ID_Servo = self.pami_settings.ID_Servo
        self.P1, self.P2 = self.pami_settings.P1, self.pami_settings.P2
        self.Entraxe = self.pami_settings.Entraxe

        self.POS_Actuelle = (self.dxl.LirePosition(self.ID_Servo[0]))[1], (self.dxl.LirePosition(self.ID_Servo[1]))[1]
        
        # Initialisation parametrage des servo
        self.dxl.ModeRot(self.ID_Servo[0], 4)   # Définit le mode de rotation à (Extended Position Control Mode (Multi-turn))
        self.dxl.ModeRot(self.ID_Servo[1], 4)   # Définit le mode de rotation à (Extended Position Control Mode (Multi-turn))


        Vitesse = 50   # Vittesse en %

        if self.P1 > self.P2: 
            V2 = 32767 / 100 * Vitesse
            V1 = (V2 / self.P1) * self.P2
        elif self.P1 < self.P2: 
            V1 = 32767 / 100 * Vitesse 
            V2 = (V1 / self.P2) * self.P1
        else:
            V1 = 32767
            V2 = 32767

        self.dxl.EcrireVitesse(self.ID_Servo[0], int(V1))  # Définit la Vitesse du Servo Gauche
        self.dxl.EcrireVitesse(self.ID_Servo[1], int(V2))  # Définit la Vitesse du Servo Droite


        self.dxl.TorqueON(self.ID_Servo[0])     # Met le torque a 1 
        self.dxl.TorqueON(self.ID_Servo[1])     # Met le torque a 1
        self.dxl.ProfileAcceleration(self.ID_Servo[0],60)   # Définit le profile d'acceleration pour atteindre la vitesse voulue du Servo
        self.dxl.ProfileAcceleration(self.ID_Servo[1],60)   # Définit le profile d'acceleration pour atteindre la vitesse voulue du Servo
        self.waited = 0   
       #self.dxl.PositionGoal(self.ID_Servo[0],(0))    # vas à la position 0 du Servo
       #self.dxl.PositionGoal(self.ID_Servo[1],(0))    # vas à la position 0 du Servo

    def waiting(self, i):
        if i == 4:
            return 0, True
        else:
            return i + 1, False 
            
    def avancer(self, distance_mm, Step_case_mtn, Step_case_apres):
        print("step_case en cours = ", Step_case_mtn)

        Distance1 = distance_mm / self.P1
        Distance2 = distance_mm / self.P2
        Pos_1 = int(Distance1 * 4096)    # Resolution = 4096 [pulse/rev]
        Pos_2 = int(Distance2 * 4096 * -1)    # Resolution = 4096 [pulse/rev]

        # Exemple de stockage des positions cibles pour les servomoteurs 1 et 2
        self.dxl.StockPosition(self.ID_Servo[0], self.POS_Actuelle[0] + Pos_1)
        self.dxl.StockPosition(self.ID_Servo[1], self.POS_Actuelle[1] + Pos_2)
        self.dxl.MoveSyncro()

        self.waited, Start = self.waiting(self.waited)

        if Start and self.dxl.EnMouvement(self.ID_Servo[0])[1] == 0 and self.dxl.EnMouvement(self.ID_Servo[1])[1] == 0:
            self.POS_Actuelle = (self.dxl.LirePosition(self.ID_Servo[0]))[1], (self.dxl.LirePosition(self.ID_Servo[1]))[1]
            print("Avance FINI")
            return Step_case_apres
        elif self.dxl.EnMouvement(self.ID_Servo[0])[1] == 1 or self.dxl.EnMouvement(self.ID_Servo[1])[1] == 1:
            print("Avance en cours")
            return Step_case_mtn
        else:
            return Step_case_mtn


    def tourner(self, angle_deg, Step_case_mtn, Step_case_apres):
        print("step_case en cours = ", Step_case_mtn)
        distance_mm = (angle_deg * math.pi * self.Entraxe) / 360
        Distance1 = distance_mm / self.P1
        Distance2 = distance_mm / self.P2
        Pos_1 = int(Distance1 * 4096)    # Resolution = 4096 [pulse/rev]
        Pos_2 = int(Distance2 * 4096)    # Resolution = 4096 [pulse/rev]

        
        # Exemple de stockage des positions cibles pour les servomoteurs 1 et 2
        self.dxl.StockPosition(self.ID_Servo[0], self.POS_Actuelle[0] + Pos_1)
        self.dxl.StockPosition(self.ID_Servo[1], self.POS_Actuelle[1] + Pos_2)
        self.dxl.MoveSyncro()

        self.waited, Start = self.waiting(self.waited)

        if Start and self.dxl.EnMouvement(self.ID_Servo[0])[1] == 0 and self.dxl.EnMouvement(self.ID_Servo[1])[1] == 0:
            self.POS_Actuelle = (self.dxl.LirePosition(self.ID_Servo[0]))[1], (self.dxl.LirePosition(self.ID_Servo[1]))[1]
            print("Rotation FINI")
            return Step_case_apres
        elif self.dxl.EnMouvement(self.ID_Servo[0])[1] == 1 or self.dxl.EnMouvement(self.ID_Servo[1])[1] == 1:
            print("Rotation en cours")
            return Step_case_mtn
        else:
            return Step_case_mtn
        
    def STOP(self):
        print("STOOOOOOPPPP")
        self.dxl.PositionGoal(self.ID_Servo[0],(self.dxl.LirePosition(self.ID_Servo[0]))[1])
        self.dxl.PositionGoal(self.ID_Servo[1],(self.dxl.LirePosition(self.ID_Servo[1]))[1])

