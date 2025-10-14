# graphics/assets.py - VRAIS BURGERS ET SALADES ULTRA DÉTAILLÉS

import pygame
import math

class AssetManager:
    def __init__(self):
        self.ingredient_images = {}
        self.font_cache = {}
        self.create_ingredient_images()
        print("✓ AssetManager initialisé avec images détaillées")
    
    def create_ingredient_images(self):
        """Crée des images ULTRA détaillées pour chaque ingrédient"""
        
        size = 32
        
        # 🥬 LAITUE - Feuille verte croquante
        laitue = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.ellipse(laitue, (50, 200, 50), (5, 8, 22, 20))
        pygame.draw.ellipse(laitue, (70, 220, 70), (6, 9, 20, 18))
        pygame.draw.ellipse(laitue, (40, 180, 40), (7, 10, 18, 16))
        for i in range(5):
            pygame.draw.line(laitue, (90, 240, 90), (16, 12 + i*2), (16, 14 + i*2), 1)
        for i in range(8):
            angle = i * 0.785
            x = 16 + int(10 * math.cos(angle))
            y = 18 + int(8 * math.sin(angle))
            pygame.draw.circle(laitue, (80, 230, 80), (x, y), 2)
        pygame.draw.circle(laitue, (120, 255, 120), (13, 14), 2)
        self.ingredient_images['laitue'] = laitue
        
        # 🍅 TOMATE - Tranche rouge juteuse
        tomate = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(tomate, (220, 50, 50), (16, 18), 11)
        pygame.draw.circle(tomate, (240, 70, 70), (16, 18), 10)
        pygame.draw.circle(tomate, (200, 40, 40), (16, 18), 9)
        for i in range(6):
            angle = i * 1.047
            x = 16 + int(5 * math.cos(angle))
            y = 18 + int(5 * math.sin(angle))
            pygame.draw.circle(tomate, (255, 200, 150), (x, y), 2)
        pygame.draw.circle(tomate, (255, 150, 150), (13, 14), 3)
        pygame.draw.circle(tomate, (255, 220, 220), (12, 13), 2)
        pygame.draw.polygon(tomate, (50, 150, 50), [(16, 7), (14, 9), (15, 8), (16, 11), (17, 8), (18, 9)])
        pygame.draw.ellipse(tomate, (60, 180, 60), (13, 5, 3, 6))
        pygame.draw.ellipse(tomate, (60, 180, 60), (17, 5, 3, 6))
        self.ingredient_images['tomate'] = tomate
        
        # 🍞 PAIN - Pain doré avec sésame
        pain = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.ellipse(pain, (180, 130, 60), (3, 9, 26, 16))
        pygame.draw.ellipse(pain, (200, 150, 80), (4, 10, 24, 14))
        pygame.draw.ellipse(pain, (220, 170, 100), (5, 11, 22, 12))
        pygame.draw.ellipse(pain, (240, 200, 130), (6, 12, 20, 10))
        for i in range(12):
            x = 7 + (i % 5) * 4
            y = 13 + (i // 5) * 3
            pygame.draw.circle(pain, (255, 240, 200), (x, y), 1)
            pygame.draw.circle(pain, (240, 220, 180), (x, y+1), 1)
        pygame.draw.arc(pain, (160, 110, 60), (3, 9, 26, 16), 0, 3.14, 2)
        pygame.draw.ellipse(pain, (255, 220, 150), (9, 13, 8, 4))
        self.ingredient_images['pain'] = pain
        
        # 🥩 STEAK - Viande grillée avec marques
        steak = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.ellipse(steak, (120, 70, 45), (5, 10, 22, 14))
        pygame.draw.ellipse(steak, (140, 80, 50), (6, 11, 20, 12))
        pygame.draw.ellipse(steak, (160, 100, 60), (7, 12, 18, 10))
        for i in range(5):
            y = 12 + i * 2
            pygame.draw.line(steak, (80, 50, 30), (8, y), (24, y), 2)
            pygame.draw.line(steak, (60, 35, 20), (9, y+1), (23, y+1), 1)
        for pos in [(11, 15), (19, 18), (15, 16)]:
            pygame.draw.circle(steak, (180, 120, 80), pos, 2)
            pygame.draw.circle(steak, (200, 140, 100), pos, 1)
        pygame.draw.ellipse(steak, (200, 130, 90), (10, 13, 6, 4))
        self.ingredient_images['steak'] = steak
        
        # 🧀 FROMAGE - Tranche jaune fondante
        fromage = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(fromage, (230, 200, 60), [(4, 14), (28, 14), (26, 20), (6, 20)])
        pygame.draw.polygon(fromage, (255, 220, 80), [(5, 15), (27, 15), (25, 19), (7, 19)])
        pygame.draw.polygon(fromage, (255, 240, 120), [(6, 16), (26, 16), (25, 18), (7, 18)])
        for pos in [(10, 17), (16, 17), (22, 17), (13, 17), (19, 17)]:
            pygame.draw.circle(fromage, (255, 200, 50), pos, 2)
            pygame.draw.circle(fromage, (255, 230, 100), pos, 1)
        pygame.draw.line(fromage, (255, 255, 180), (8, 16), (24, 16), 1)
        pygame.draw.line(fromage, (255, 250, 150), (8, 17), (24, 17), 1)
        self.ingredient_images['fromage'] = fromage
        
        # 🧅 OIGNON - Rondelle avec anneaux
        oignon = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(oignon, (180, 160, 120), (16, 16), 10)
        pygame.draw.circle(oignon, (200, 180, 140), (16, 16), 9)
        pygame.draw.circle(oignon, (220, 200, 160), (16, 16), 8)
        pygame.draw.circle(oignon, (200, 180, 140), (16, 16), 6, 1)
        pygame.draw.circle(oignon, (180, 160, 120), (16, 16), 4, 1)
        pygame.draw.circle(oignon, (160, 140, 100), (16, 16), 2, 1)
        for i in range(8):
            angle = i * 0.785
            x = 16 + int(6 * math.cos(angle))
            y = 16 + int(6 * math.sin(angle))
            pygame.draw.line(oignon, (190, 170, 130), (16, 16), (x, y), 1)
        pygame.draw.circle(oignon, (240, 220, 180), (13, 13), 2)
        self.ingredient_images['oignon'] = oignon
        
        # 🥗 SALADE (ingrédient simple)
        salade = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.ellipse(salade, (220, 220, 220), (5, 18, 22, 12))
        pygame.draw.ellipse(salade, (240, 240, 240), (6, 19, 20, 10))
        pygame.draw.ellipse(salade, (255, 255, 255), (7, 20, 18, 8))
        pygame.draw.ellipse(salade, (60, 180, 60), (7, 8, 18, 16))
        pygame.draw.ellipse(salade, (80, 200, 80), (8, 9, 16, 14))
        pygame.draw.ellipse(salade, (100, 220, 100), (9, 10, 14, 12))
        for pos in [(12, 14), (20, 13), (16, 17), (10, 16)]:
            pygame.draw.circle(salade, (220, 50, 50), pos, 2)
            pygame.draw.circle(salade, (255, 100, 100), pos, 1)
        pygame.draw.circle(salade, (255, 255, 255), (12, 22), 2)
        self.ingredient_images['salade'] = salade
        
        # 🍔 BURGER COMPLET ASSEMBLÉ
        burger = pygame.Surface((64, 64), pygame.SRCALPHA)
        cx, cy = 32, 32
        
        # Pain du bas avec texture
        pygame.draw.ellipse(burger, (180, 130, 60), (cx-26, cy+10, 52, 18))
        pygame.draw.ellipse(burger, (200, 150, 80), (cx-25, cy+11, 50, 16))
        pygame.draw.ellipse(burger, (220, 170, 100), (cx-24, cy+12, 48, 14))
        for i in range(16):
            x = cx - 20 + (i % 7) * 5
            y = cy + 14 + (i // 7) * 2
            pygame.draw.circle(burger, (255, 240, 200), (x, y), 1)
        
        # Laitue croquante
        pygame.draw.ellipse(burger, (50, 200, 50), (cx-24, cy+3, 48, 11))
        pygame.draw.ellipse(burger, (70, 220, 70), (cx-23, cy+4, 46, 9))
        pygame.draw.ellipse(burger, (90, 240, 90), (cx-22, cy+5, 44, 7))
        for i in range(6):
            x = cx - 18 + i * 6
            pygame.draw.line(burger, (110, 255, 110), (x, cy+6), (x, cy+10), 1)
        
        # Tomate juteuse
        pygame.draw.ellipse(burger, (200, 40, 40), (cx-23, cy-3, 46, 9))
        pygame.draw.ellipse(burger, (220, 50, 50), (cx-22, cy-2, 44, 8))
        pygame.draw.ellipse(burger, (240, 70, 70), (cx-21, cy-1, 42, 6))
        for i in range(5):
            x = cx - 16 + i * 7
            pygame.draw.circle(burger, (255, 150, 150), (x, cy), 2)
        
        # Fromage fondant qui déborde
        pygame.draw.polygon(burger, (230, 200, 60), [
            (cx-26, cy-9), (cx+26, cy-9), (cx+24, cy-5), (cx-24, cy-5)
        ])
        pygame.draw.polygon(burger, (255, 220, 80), [
            (cx-25, cy-8), (cx+25, cy-8), (cx+23, cy-6), (cx-23, cy-6)
        ])
        pygame.draw.polygon(burger, (255, 240, 120), [
            (cx-24, cy-7), (cx+24, cy-7), (cx+22, cy-6), (cx-22, cy-6)
        ])
        # Coulures de fromage
        for x in [cx-22, cx-10, cx+8, cx+20]:
            pygame.draw.line(burger, (255, 230, 100), (x, cy-5), (x-2, cy+2), 2)
        
        # Steak grillé épais
        pygame.draw.ellipse(burger, (100, 60, 40), (cx-25, cy-13, 50, 12))
        pygame.draw.ellipse(burger, (120, 70, 45), (cx-24, cy-12, 48, 11))
        pygame.draw.ellipse(burger, (140, 80, 50), (cx-23, cy-11, 46, 9))
        pygame.draw.ellipse(burger, (160, 100, 60), (cx-22, cy-10, 44, 7))
        for i in range(6):
            x = cx - 18 + i * 7
            pygame.draw.line(burger, (80, 50, 30), (x, cy-12), (x, cy-6), 2)
            pygame.draw.line(burger, (60, 35, 20), (x+1, cy-11), (x+1, cy-7), 1)
        for pos in [(cx-12, cy-9), (cx+8, cy-10), (cx-2, cy-8)]:
            pygame.draw.circle(burger, (180, 120, 80), pos, 2)
        
        # Pain du haut (dôme) avec sésame
        pygame.draw.ellipse(burger, (180, 130, 60), (cx-28, cy-28, 56, 20))
        pygame.draw.ellipse(burger, (200, 150, 80), (cx-27, cy-27, 54, 19))
        pygame.draw.ellipse(burger, (220, 170, 100), (cx-26, cy-26, 52, 18))
        pygame.draw.arc(burger, (160, 110, 60), (cx-28, cy-32, 56, 24), 0, 3.14, 3)
        for i in range(20):
            angle = i * 0.314
            r = 20 - abs(10 - i)
            x = cx + int(r * math.cos(angle))
            y = cy - 22 + int(8 * math.sin(angle))
            pygame.draw.circle(burger, (255, 240, 200), (x, y), 1)
        pygame.draw.ellipse(burger, (255, 255, 255), (cx-18, cy-24, 14, 7))
        pygame.draw.ellipse(burger, (255, 255, 255), (cx-16, cy-23, 10, 5))
        
        self.ingredient_images['burger'] = burger
        
        # 🥗 SALADE DRESSÉE DANS BOL
        salade_plat = pygame.Surface((64, 64), pygame.SRCALPHA)
        cx, cy = 32, 32
        
        # Bol blanc brillant
        pygame.draw.ellipse(salade_plat, (160, 160, 160), (cx-30, cy+6, 60, 28))
        pygame.draw.ellipse(salade_plat, (200, 200, 200), (cx-29, cy+7, 58, 26))
        pygame.draw.ellipse(salade_plat, (240, 240, 240), (cx-28, cy+8, 56, 24))
        pygame.draw.ellipse(salade_plat, (255, 255, 255), (cx-27, cy+9, 54, 22))
        pygame.draw.ellipse(salade_plat, (245, 245, 230), (cx-26, cy+10, 52, 20))
        pygame.draw.ellipse(salade_plat, (180, 180, 160), (cx-28, cy+8, 56, 24), 3)
        
        # Laitue volumineuse en spirale
        for i in range(12):
            angle = i * 0.524
            radius = 16 + (i % 3) * 4
            x = cx + int(radius * math.cos(angle))
            y = cy - 6 + int(radius * 0.5 * math.sin(angle))
            size = 10 + (i % 2) * 4
            pygame.draw.ellipse(salade_plat, (50, 200, 50), (x-size//2, y-size//2+2, size, size-2))
            pygame.draw.ellipse(salade_plat, (70, 220, 70), (x-size//2+1, y-size//2+3, size-2, size-4))
            pygame.draw.ellipse(salade_plat, (90, 240, 90), (x-size//2+2, y-size//2+4, size-4, size-6))
        
        # Centre de laitue
        pygame.draw.ellipse(salade_plat, (60, 180, 60), (cx-14, cy-12, 28, 18))
        pygame.draw.ellipse(salade_plat, (80, 200, 80), (cx-13, cy-11, 26, 16))
        pygame.draw.ellipse(salade_plat, (100, 220, 100), (cx-12, cy-10, 24, 14))
        pygame.draw.ellipse(salade_plat, (120, 240, 120), (cx-11, cy-9, 22, 12))
        
        # Tomates cerises brillantes
        for i, (px, py) in enumerate([(cx-16, cy-6), (cx+12, cy-4), (cx-4, cy+1), (cx+8, cy-10), (cx-10, cy+2)]):
            pygame.draw.circle(salade_plat, (200, 40, 40), (px+1, py+1), 6)
            pygame.draw.circle(salade_plat, (220, 50, 50), (px, py), 6)
            pygame.draw.circle(salade_plat, (240, 70, 70), (px, py), 5)
            pygame.draw.circle(salade_plat, (255, 150, 150), (px-2, py-2), 3)
            pygame.draw.circle(salade_plat, (255, 220, 220), (px-2, py-2), 2)
            pygame.draw.polygon(salade_plat, (50, 150, 50), [(px, py-6), (px-1, py-5), (px, py-4), (px+1, py-5)])
        
        # Rondelles d'oignon
        for pos in [(cx+14, cy+3), (cx-10, cy+5), (cx+2, cy-2)]:
            pygame.draw.circle(salade_plat, (180, 160, 120), pos, 5)
            pygame.draw.circle(salade_plat, (200, 180, 140), pos, 4)
            pygame.draw.circle(salade_plat, (220, 200, 160), pos, 3)
            pygame.draw.circle(salade_plat, (200, 180, 140), pos, 2, 1)
        
        # Brillances sur le bol
        pygame.draw.ellipse(salade_plat, (255, 255, 255), (cx-22, cy+11, 18, 7))
        pygame.draw.ellipse(salade_plat, (255, 255, 255), (cx-20, cy+12, 14, 5))
        pygame.draw.ellipse(salade_plat, (240, 240, 255), (cx+8, cy+14, 12, 5))
        
        self.ingredient_images['salade_plat'] = salade_plat
        
        print(f"✓ {len(self.ingredient_images)} images créées avec détails")
    
    def get_ingredient_image(self, ingredient_type):
        """Retourne l'image d'un ingrédient"""
        return self.ingredient_images.get(ingredient_type, None)
    
    def get_font(self, size):
        """Cache pour les polices"""
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        return self.font_cache[size]