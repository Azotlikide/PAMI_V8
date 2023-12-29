import pygame
from pami_settings import PAMISettings
import os

class Visu:

    def __init__(self):
        self.pami_settings = PAMISettings()
        
        # Pygame and Screen
        pygame.init()
        pygame.display.set_caption(f"Pami: {self.pami_settings.Num_PAMI}")
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)  # ,pygame.FULLSCREEN
        
        # Couleurs
        self.BLUE = (0, 91, 140)         # Couleur bleue  
        self.YELLOW = (247, 181, 0)      # Couleur jaune  
        self.RED = (255, 10, 10)         # Couleur rouge  
        self.BLACK = (0, 0, 0)           # Couleur noire  
        self.WHITE = (255, 255, 255)     # Couleur blanche
        self.GREEN = (0, 255, 0)         # Couleur verte
        
        # Fonts
        self.BIG_FONT = pygame.font.Font("Fonts/courier-prime.bold.ttf", 800)
        
        # Pami Visu Visage Droite
        Coccinelle_Droite = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pami_Visu", "Droite.jpg")
        self.Coccinelle_Droite = pygame.transform.scale(pygame.image.load(Coccinelle_Droite), self.screen_size)
        self.Coccinelle_Droite_rect = self.Coccinelle_Droite.get_rect()
        # Pami Visu Visage Milieu
        Coccinelle_Milieu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pami_Visu", "Milieu.jpg")
        self.Coccinelle_Milieu = pygame.transform.scale(pygame.image.load(Coccinelle_Milieu), self.screen_size)
        self.Coccinelle_Milieu_rect = self.Coccinelle_Milieu.get_rect()
        # Pami Visu Visage Gauche
        Coccinelle_Gauche = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pami_Visu", "Gauche.jpg")
        self.Coccinelle_Gauche = pygame.transform.scale(pygame.image.load(Coccinelle_Gauche), self.screen_size)
        self.Coccinelle_Gauche_rect = self.Coccinelle_Gauche.get_rect()


    def draw_screen_border(self, color=(0, 0, 0), border_thickness=15):   # F
        # Vérifier si la couleur spécifiée est un tuple RGB
        if isinstance(color, tuple) and len(color) == 3:
            # Crée un bordure au toure l'écran avec la couleur demandée
            pygame.draw.rect(self.screen, color, (0, 0, self.screen_size[0], self.screen_size[1]), border_thickness)
        else:
            # Vérifier si la couleur spécifiée correspond à une couleur prédéfinie
            predefined_color = getattr(self, color, None)
            if predefined_color:
            # Crée un bordure au toure l'écran avec la couleur demandée
                pygame.draw.rect(self.screen, predefined_color, (0, 0, self.screen_size[0], self.screen_size[1]), border_thickness)
            else:
                raise ValueError(f"La couleur spécifiée {color} n'est pas valide.")
            

    def fill_screen(self, color=(255, 255, 255)):   # F
        # Vérifier si la couleur spécifiée est un tuple RGB
        if isinstance(color, tuple) and len(color) == 3:
            # Remplit l'écran avec la couleur demandée
            self.screen.fill(color)
        else:
            # Vérifier si la couleur spécifiée correspond à une couleur prédéfinie
            predefined_color = getattr(self, color, None)
            if predefined_color:
                # Remplit l'écran avec la couleur demandée
                self.screen.fill(predefined_color)
            else:
                raise ValueError(f"La couleur spécifiée {color} n'est pas valide.")


    def draw_num_pami(self, position, color=(0, 0, 0)):   # F
        # Vérifier si la couleur spécifiée est un tuple RGB
        if isinstance(color, tuple) and len(color) == 3:
            num_surface = self.BIG_FONT.render(str(self.pami_settings.Num_PAMI), True, color)
        else:
            # Vérifier si la couleur spécifiée correspond à une couleur prédéfinie
            predefined_color = getattr(self, color, None)
            if predefined_color:
                # Crée une surface avec le numéro PAMI rendu sur celle-ci
                num_surface = self.BIG_FONT.render(str(self.pami_settings.Num_PAMI), True, predefined_color)
            else:
                raise ValueError(f"La couleur spécifiée {color} n'est pas valide.")

        # Obtient la position rectangulaire pour centrer le texte à la position donnée
        num_rect = self.get_text_position(position, num_surface)
        self.screen.blit(num_surface, num_rect.topleft)
        

    def get_text_position(self, position, surface):   # F
        screen_width, screen_height = self.screen_size
        text_width, text_height = surface.get_size()
        pad_x = 0
        pad_y = 78

        if isinstance(position, tuple) and len(position) == 2:
            # Si la position est déjà un tuple de coordonnées, créer un Rect avec ces coordonnées
            return pygame.Rect(position[0] - text_width // 2 - pad_x, position[1] - text_height // 2 + pad_y, text_width, text_height)
        elif position == "centre":
            return pygame.Rect(1 * screen_width // 2 - text_width // 2 - pad_x, 1 * screen_height // 2 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "centre-gauche": 
            return pygame.Rect(1 * screen_width // 4 - text_width // 2 - pad_x, 1 * screen_height // 2 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "centre-droite": 
            return pygame.Rect(3 * screen_width // 4 - text_width // 2 - pad_x, 1 * screen_height // 2 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "haut": 
            return pygame.Rect(1 * screen_width // 2 - text_width // 2 - pad_x, 1 * screen_height // 4 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "bas": 
            return pygame.Rect(1 * screen_width // 2 - text_width // 2 - pad_x, 3 * screen_height // 4 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "haut-gauche": 
            return pygame.Rect(1 * screen_width // 4 - text_width // 2 - pad_x, 1 * screen_height // 4 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "haut-droite": 
            return pygame.Rect(3 * screen_width // 4 - text_width // 2 - pad_x, 1 * screen_height // 4 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "bas-gauche": 
            return pygame.Rect(1 * screen_width // 4 - text_width // 2 - pad_x, 3 * screen_height // 4 - text_height // 2 + pad_y , text_width, text_height)
        elif position == "bas-droite": 
            return pygame.Rect(3 * screen_width // 4 - text_width // 2 - pad_x, 3 * screen_height // 4 - text_height // 2 + pad_y , text_width, text_height)
        else:
            raise ValueError(f"Position spécifiée non prise en charge : {position}")


    def draw_cross_button(self):   # F
        # Dessine le bouton de fermeture rouge avec une bordure noire
        pygame.draw.rect(self.screen, self.RED, (0, 0, 50, 50))
        pygame.draw.rect(self.screen, self.BLACK, (0, 0, 50, 50), 2)

        # Dessinez une croix blanche sur le bouton de fermeture avec une bordure blanche
        pygame.draw.line(self.screen, self.WHITE, (10, 10), (40, 40), 5)
        pygame.draw.line(self.screen, self.WHITE, (10, 40), (40, 10), 5)


    def draw_button(self, color, x1, y1, x2, y2, border_thickness=None): 
        # Vérifier si la couleur spécifiée est un tuple RGB
        button_rect = pygame.Rect(x1, y1, x2-x1, y2-y1)
        if isinstance(color, tuple) and len(color) == 3:
            # Dessine le bouton avec une bordure noire
            pygame.draw.rect(self.screen, color, button_rect)
            if border_thickness != None:
                pygame.draw.rect(self.screen, self.BLACK, button_rect, border_thickness)
        else:
            # Vérifier si la couleur spécifiée correspond à une couleur prédéfinie
            predefined_color = getattr(self, color, None)
            if predefined_color:
                # Dessine le bouton avec une bordure noire
                pygame.draw.rect(self.screen, predefined_color, button_rect)
                if border_thickness != None:
                    pygame.draw.rect(self.screen, self.BLACK, button_rect, border_thickness)
            else:
                raise ValueError(f"La couleur spécifiée {color} n'est pas valide.")
        

    def draw_coccinelle(self, direction):
        if direction == "Droite":
            self.screen.blit(self.Coccinelle_Droite, self.Coccinelle_Droite_rect)

        if direction == "Milieu":
            self.screen.blit(self.Coccinelle_Milieu, self.Coccinelle_Milieu_rect)

        if direction == "Gauche":
            self.screen.blit(self.Coccinelle_Gauche, self.Coccinelle_Gauche_rect)


    def update(self):   # F 
        pygame.display.flip()
        
        
        
        