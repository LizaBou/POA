"""
Asset creation - Crée toutes les surfaces et images du jeu
"""
import pygame
import math
from config import COLORS

class AssetManager:
    def __init__(self):
        self.player_img = None
        self.knife_img = None
        self.ingredient_imgs = {}
        self.create_all_assets()

    def create_player_surface(self):
        """Crée la surface du joueur/bot"""
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Tête
        pygame.draw.circle(surf, (255, 220, 177), (25, 15), 12)
        # Corps
        pygame.draw.ellipse(surf, COLORS['blue'], (15, 20, 20, 25))
        # Bras
        pygame.draw.circle(surf, (255, 220, 177), (10, 30), 5)
        pygame.draw.circle(surf, (255, 220, 177), (40, 30), 5)
        # Jambes
        pygame.draw.ellipse(surf, (139, 90, 43), (18, 40, 6, 10))
        pygame.draw.ellipse(surf, (139, 90, 43), (26, 40, 6, 10))
        # Yeux
        pygame.draw.circle(surf, (0, 0, 0), (22, 12), 2)
        pygame.draw.circle(surf, (0, 0, 0), (28, 12), 2)
        return surf

    def create_knife_surface(self):
        """Crée la surface du couteau"""
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Manche
        pygame.draw.rect(surf, (139, 90, 43), (5, 15, 15, 10))
        # Lame
        points = [(20, 20), (35, 18), (38, 22), (20, 24)]
        pygame.draw.polygon(surf, COLORS['metal'], points)
        # Reflet sur la lame
        pygame.draw.line(surf, COLORS['white'], (22, 20), (33, 19), 1)
        return surf

    def create_ingredient_surface(self, ingredient_type):
        """Crée la surface d'un ingrédient"""
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        if ingredient_type == "T":  # Tomate
            pygame.draw.circle(surf, COLORS['red'], (20, 20), 15)
            pygame.draw.arc(surf, (150, 255, 150), (15, 10, 10, 8), 0, math.pi, 2)
        
        elif ingredient_type == "L":  # Salade
            pygame.draw.ellipse(surf, COLORS['green'], (5, 8, 30, 24))
            for i in range(3):
                pygame.draw.arc(surf, (34, 139, 34), (8+i*8, 12, 8, 16), 0, math.pi, 1)
        
        elif ingredient_type == "B":  # Pain
            pygame.draw.ellipse(surf, (222, 184, 135), (5, 10, 30, 20))
            for i in range(4):
                pygame.draw.circle(surf, (205, 133, 63), (10+i*5, 20), 2)
        
        elif ingredient_type == "C":  # Fromage
            pygame.draw.rect(surf, (255, 255, 0), (8, 12, 24, 16))
            for i in range(2):
                for j in range(3):
                    pygame.draw.circle(surf, (255, 215, 0), (12+j*8, 16+i*6), 2)
        
        elif ingredient_type == "H":  # Steak
            pygame.draw.ellipse(surf, (139, 69, 19), (5, 8, 30, 24))
            pygame.draw.ellipse(surf, (160, 82, 45), (8, 12, 24, 16))
        
        return surf

    def create_all_assets(self):
        """Crée tous les assets du jeu"""
        self.player_img = self.create_player_surface()
        self.knife_img = self.create_knife_surface()
        
        # Créer toutes les images d'ingrédients
        for ing_type in ["T", "L", "B", "C", "H"]:
            self.ingredient_imgs[ing_type] = self.create_ingredient_surface(ing_type)

    def get_player_image(self):
        """Retourne l'image du joueur"""
        return self.player_img

    def get_knife_image(self):
        """Retourne l'image du couteau"""
        return self.knife_img

    def get_ingredient_image(self, ingredient_type):
        """Retourne l'image d'un ingrédient"""
        return self.ingredient_imgs.get(ingredient_type)