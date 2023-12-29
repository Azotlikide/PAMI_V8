import pygame
import sys

class Visu_handle_event:
    def handle_events(self, Bouton_Actif):
        print(Bouton_Actif)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if (Bouton_Actif[0]) and (0 <= x <= 50 and 0 <= y <= 50):
                    for i in range(len(Bouton_Actif)): Bouton_Actif[i] = 0; Bouton_Actif[0] = 1
                    return Bouton_Actif
                elif (Bouton_Actif[1]) and (500 <= x <= 800 and 0 <= y <= 300):
                    for i in range(len(Bouton_Actif)): Bouton_Actif[i] = 0; Bouton_Actif[1] = 1
                    return Bouton_Actif
                elif (Bouton_Actif[2]) and (500 <= x <= 800 and 300 <= y <= 600):
                    for i in range(len(Bouton_Actif)): Bouton_Actif[i] = 0; Bouton_Actif[2] = 1
                    return Bouton_Actif
                elif (Bouton_Actif[3]) and (550 <= x <= 750 and 350 <= y <= 550):
                    for i in range(len(Bouton_Actif)): Bouton_Actif[i] = 0; Bouton_Actif[3] = 1
                    return Bouton_Actif

        # Si aucun bloc if n'est évalué comme vrai, retournez une liste vide
        for i in range(len(Bouton_Actif)):
            Bouton_Actif[i] = 0
        return Bouton_Actif
