# graphics/assets.py - AVEC VRAIES IMAGES

import pygame
import os

class AssetManager:
    def __init__(self):
        self.ingredient_images = {}
        self.font_cache = {}
        
        # 🎨 Créer des images procédurales si les fichiers n'existent pas
        self.create_ingredient_images()
        
        print("✓ AssetManager initialisé avec images procédurales")
    
    def create_ingredient_images(self):
        """Crée des images procédurales détaillées pour chaque ingrédient"""
        
        size = 32  # Taille de base (sera redimensionnée selon le besoin)
        
        # 🥬 LAITUE
        laitue = pygame.Surface((size, size), pygame.SRCALPHA)
        size = 32  # Taille de base (sera redimensionnée selon le besoin)
        
        # 🥬 LAITUE
        laitue = pygame.Surface((size, size), pygame.SRCALPHA)
        # Feuille principale
        pygame.draw.ellipse(laitue, (80, 200, 80), (5, 8, 22, 20))
        pygame.draw.ellipse(laitue, (60, 180, 60), (6, 9, 20, 18))
        # Nervures
        for i in range(3):
            pygame.draw.line(laitue, (100, 220, 100), 
                           (16, 10 + i*5), (16, 15 + i*5), 1)
        # Bord dentelé
        for i in range(6):
            angle = i * 1.047  # 60 degrés
            x = 16 + int(11 * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
            y = 18 + int(10 * pygame.math.Vector2(0, 1).rotate_rad(angle).y)
            pygame.draw.circle(laitue, (90, 210, 90), (x, y), 2)
        self.ingredient_images['laitue'] = laitue
        
        # 🍅 TOMATE
        tomate = pygame.Surface((size, size), pygame.SRCALPHA)
        # Corps de la tomate
        pygame.draw.circle(tomate, (220, 50, 50), (16, 18), 10)
        pygame.draw.circle(tomate, (200, 40, 40), (16, 18), 9)
        # Brillance
        pygame.draw.circle(tomate, (255, 150, 150), (13, 14), 3)
        pygame.draw.circle(tomate, (255, 200, 200), (12, 13), 2)
        # Tige verte
        pygame.draw.polygon(tomate, (50, 150, 50), [
            (16, 8), (14, 10), (15, 9), (16, 12), (17, 9), (18, 10)
        ])
        # Feuilles
        pygame.draw.ellipse(tomate, (60, 180, 60), (13, 6, 3, 5))
        pygame.draw.ellipse(tomate, (60, 180, 60), (17, 6, 3, 5))
        self.ingredient_images['tomate'] = tomate
        
        # 🍞 PAIN
        pain = pygame.Surface((size, size), pygame.SRCALPHA)
        # Pain brun doré
        pygame.draw.ellipse(pain, (200, 150, 80), (4, 10, 24, 14))
        pygame.draw.ellipse(pain, (220, 170, 100), (5, 11, 22, 12))
        # Texture (graines de sésame)
        for i in range(8):
            x = 8 + (i % 4) * 5
            y = 14 + (i // 4) * 3
            pygame.draw.circle(pain, (255, 240, 200), (x, y), 1)
        # Croûte plus foncée
        pygame.draw.arc(pain, (160, 110, 60), (4, 10, 24, 14), 0, 3.14, 2)
        self.ingredient_images['pain'] = pain
        
        # 🥩 STEAK
        steak = pygame.Surface((size, size), pygame.SRCALPHA)
        # Steak cuit
        pygame.draw.ellipse(steak, (140, 80, 50), (6, 11, 20, 12))
        pygame.draw.ellipse(steak, (120, 70, 45), (7, 12, 18, 10))
        # Marques de grill
        for i in range(3):
            y = 13 + i * 3
            pygame.draw.line(steak, (90, 50, 30), (8, y), (24, y), 1)
        # Jus/brillance
        pygame.draw.circle(steak, (180, 120, 80), (11, 15), 2)
        pygame.draw.circle(steak, (180, 120, 80), (19, 18), 1)
        self.ingredient_images['steak'] = steak
        
        # 🧀 FROMAGE
        fromage = pygame.Surface((size, size), pygame.SRCALPHA)
        # Tranche de fromage jaune
        pygame.draw.polygon(fromage, (255, 220, 80), [
            (5, 15), (27, 15), (25, 19), (7, 19)
        ])
        pygame.draw.polygon(fromage, (255, 240, 120), [
            (6, 16), (26, 16), (25, 18), (7, 18)
        ])
        # Trous de fromage
        pygame.draw.circle(fromage, (255, 200, 50), (10, 17), 1)
        pygame.draw.circle(fromage, (255, 200, 50), (16, 17), 2)
        pygame.draw.circle(fromage, (255, 200, 50), (22, 17), 1)
        # Brillance
        pygame.draw.line(fromage, (255, 255, 180), (8, 16), (24, 16), 1)
        self.ingredient_images['fromage'] = fromage
        
        # 🧅 OIGNON
        oignon = pygame.Surface((size, size), pygame.SRCALPHA)
        # Rondelle d'oignon
        pygame.draw.circle(oignon, (200, 180, 140), (16, 16), 9)
        pygame.draw.circle(oignon, (220, 200, 160), (16, 16), 8)
        # Anneaux
        pygame.draw.circle(oignon, (200, 180, 140), (16, 16), 6, 1)
        pygame.draw.circle(oignon, (180, 160, 120), (16, 16), 4, 1)
        # Texture
        for i in range(6):
            angle = i * 1.047
            x = 16 + int(5 * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
            y = 16 + int(5 * pygame.math.Vector2(0, 1).rotate_rad(angle).y)
            pygame.draw.line(oignon, (190, 170, 130), (16, 16), (x, y), 1)
        self.ingredient_images['oignon'] = oignon
        
        # 🥗 SALADE (assemblage)
        salade = pygame.Surface((size, size), pygame.SRCALPHA)
        # Bol
        pygame.draw.ellipse(salade, (240, 240, 240), (6, 19, 20, 10))
        pygame.draw.ellipse(salade, (220, 220, 220), (7, 20, 18, 8))
        # Laitue dans le bol
        pygame.draw.ellipse(salade, (80, 200, 80), (8, 10, 16, 15))
        pygame.draw.ellipse(salade, (60, 180, 60), (9, 11, 14, 13))
        # Tomates sur le dessus
        pygame.draw.circle(salade, (220, 50, 50), (12, 15), 2)
        pygame.draw.circle(salade, (220, 50, 50), (20, 14), 2)
        pygame.draw.circle(salade, (220, 50, 50), (16, 18), 2)
        self.ingredient_images['salade'] = salade
        
        print(f"✓ {len(self.ingredient_images)} images d'ingrédients créées")
    
    def get_ingredient_image(self, ingredient_type):
        """Retourne l'image d'un ingrédient"""
        img = self.ingredient_images.get(ingredient_type, None)
        if img is None:
            print(f"⚠ Image non trouvée pour: {ingredient_type}")
            print(f"   Images disponibles: {list(self.ingredient_images.keys())}")
        return img
    
    def get_font(self, size):
        """Cache pour les polices"""
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        return self.font_cache[size]
    
    def load_image(self, path, size=None):
        """Charge une image depuis un fichier (fallback)"""
        try:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                if size:
                    img = pygame.transform.scale(img, size)
                return img
        except Exception as e:
            print(f"⚠ Erreur chargement {path}: {e}")
        return None