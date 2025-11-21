# kitchen.py - VERSION AVEC VISUELS AMÉLIORÉS - CORRIGÉE

import pygame
import time
import math
from config import COLORS, WIDTH, HEIGHT

def draw_gradient_rect(surface, color1, color2, rect):
    for i in range(rect.height):
        ratio = i / rect.height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))

class KitchenRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        self.ingredient_config = {
            "laitue": {"color": (60, 220, 60), "icon": "🥬"},
            "tomate": {"color": (240, 60, 60), "icon": "🍅"},
            "pain": {"color": (220, 170, 90), "icon": "🍞"},
            "steak": {"color": (160, 90, 60), "icon": "🥩"},
            "fromage": {"color": (255, 230, 90), "icon": "🧀"},
            "oignon": {"color": (210, 190, 150), "icon": "🧅"},
            "salade": {"color": (90, 200, 90), "icon": "🥗"}
        }
        self.setup_kitchen_layout()
        self.delivered_dishes = []
        self.cutting_animation = CuttingAnimation(screen)
        
        # ⭐ NOUVEAUX ÉLÉMENTS VISUELS
        self.steam_particles = []  # Vapeur au-dessus de la plaque
        self.sparkle_particles = []  # Étincelles à la livraison

    def setup_kitchen_layout(self):
        # ⭐ Plans de travail alignés en bois + zone de cuisson
        self.storage_area = {'x': 40, 'y': 120, 'w': 280, 'h': 140}
        self.work_area = {'x': 330, 'y': 120, 'w': 200, 'h': 140}
        self.cooking_area = {'x': 330, 'y': 270, 'w': 200, 'h': 120}  # ⭐ NOUVEAU
        self.plating_area = {'x': 540, 'y': 120, 'w': 200, 'h': 140}
        self.service_area = {'x': 790, 'y': 120, 'w': 120, 'h': 300}

    def draw_floor(self):
        """Sol avec damier et reflets"""
        tile_size = 50
        floor_light = (210, 210, 210)
        floor_dark = (190, 190, 190)
        
        for x in range(0, WIDTH, tile_size):
            for y in range(0, HEIGHT, tile_size):
                color = floor_light if (x // tile_size + y // tile_size) % 2 == 0 else floor_dark
                pygame.draw.rect(self.screen, color, (x, y, tile_size, tile_size))
                
                # ⭐ Reflet subtil sur les carreaux
                if (x // tile_size + y // tile_size) % 2 == 0:
                    shine_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                    pygame.draw.circle(shine_surf, (255, 255, 255, 15), (tile_size // 2, tile_size // 2), tile_size // 3)
                    self.screen.blit(shine_surf, (x, y))
                
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x + tile_size, y), 1)
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x, y + tile_size), 1)

    def draw_wall_decorations(self):
        """⭐ NOUVEAU : Décorations murales"""
        current_time = time.time()
        
        # Horloge murale
        clock_x, clock_y = WIDTH - 80, 50
        pygame.draw.circle(self.screen, (240, 240, 240), (clock_x, clock_y), 25)
        pygame.draw.circle(self.screen, (200, 200, 200), (clock_x, clock_y), 25, 3)
        
        # Aiguilles qui bougent
        hour_angle = (current_time % 43200) / 43200 * 2 * math.pi - math.pi / 2
        minute_angle = (current_time % 3600) / 3600 * 2 * math.pi - math.pi / 2
        
        pygame.draw.line(self.screen, (50, 50, 50), (clock_x, clock_y),
                        (clock_x + math.cos(hour_angle) * 12, clock_y + math.sin(hour_angle) * 12), 3)
        pygame.draw.line(self.screen, (50, 50, 50), (clock_x, clock_y),
                        (clock_x + math.cos(minute_angle) * 18, clock_y + math.sin(minute_angle) * 18), 2)
        
        # Centre de l'horloge
        pygame.draw.circle(self.screen, (200, 50, 50), (clock_x, clock_y), 3)
        
        # Étagères décoratives au-dessus du stockage
        shelf_y = 85
        shelf_color = (120, 80, 50)
        pygame.draw.rect(self.screen, shelf_color, (50, shelf_y, 250, 8))
        pygame.draw.rect(self.screen, (80, 50, 30), (50, shelf_y, 250, 8), 2)
        
        # Pots sur l'étagère
        pot_positions = [80, 140, 200, 260]
        for i, pot_x in enumerate(pot_positions):
            pot_color = [(200, 100, 100), (100, 200, 100), (100, 100, 200), (200, 200, 100)][i]
            pygame.draw.circle(self.screen, pot_color, (pot_x, shelf_y - 8), 8)
            pygame.draw.circle(self.screen, (255, 255, 255, 150), (pot_x - 2, shelf_y - 10), 3)

    def draw_overhead_lamps(self):
        """⭐ NOUVEAU : Lampes suspendues au-dessus des stations"""
        current_time = time.time()
        
        lamp_positions = [
            (180, 90, (255, 230, 150)),  # Au-dessus stockage
            (450, 90, (255, 240, 200)),  # Au-dessus plan de travail
            (670, 90, (255, 245, 220)),  # Au-dessus assemblage
        ]
        
        for lamp_x, lamp_y, light_color in lamp_positions:
            # Câble de suspension
            pygame.draw.line(self.screen, (80, 80, 80), (lamp_x, 0), (lamp_x, lamp_y), 2)
            
            # Corps de la lampe
            lamp_rect = pygame.Rect(lamp_x - 20, lamp_y, 40, 15)
            pygame.draw.ellipse(self.screen, (100, 100, 100), lamp_rect)
            pygame.draw.ellipse(self.screen, (70, 70, 70), lamp_rect, 2)
            
            # Halo de lumière (pulsant)
            pulse = int(30 + 10 * math.sin(current_time * 2 + lamp_x))
            for radius in [80, 60, 40]:
                alpha = pulse // (radius // 20)
                light_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(light_surf, (*light_color, alpha), (radius, radius), radius)
                self.screen.blit(light_surf, (lamp_x - radius, lamp_y + 15 - radius))

    def draw_individual_ingredient_stations(self, asset_manager):
        import game_state
        current_time = time.time()
        
        # ⭐ NOUVEAU : Plan de travail en bois unifié pour le stockage
        storage_rect = pygame.Rect(self.storage_area['x'], self.storage_area['y'], 
                                   self.storage_area['w'], self.storage_area['h'])
        draw_gradient_rect(self.screen, (160, 110, 70), (140, 90, 60), storage_rect)
        
        # Texture bois
        for i in range(0, self.storage_area['w'], 30):
            line_x = self.storage_area['x'] + i
            pygame.draw.line(self.screen, (140, 100, 65), 
                           (line_x, self.storage_area['y']), 
                           (line_x, self.storage_area['y'] + self.storage_area['h']), 1)
        
        pygame.draw.rect(self.screen, (100, 70, 40), storage_rect, 3)
        
        title_bg = pygame.Rect(self.storage_area['x'], self.storage_area['y'] - 30, self.storage_area['w'], 25)
        draw_gradient_rect(self.screen, (100, 70, 40), (80, 60, 30), title_bg)
        title = self.font_small.render("🧊 STOCKAGE", True, (255, 255, 255))
        self.screen.blit(title, (self.storage_area['x'] + 10, self.storage_area['y'] - 25))
        
        ingredient_types = list(set(ing["type"] for ing in game_state.ingredients))
        if not ingredient_types:
            ingredient_types = ["laitue", "tomate", "pain", "steak", "fromage"]
        
        # ⭐ NOUVEAU : Bacs en bois en ligne horizontale
        cols = len(ingredient_types)
        station_width = (self.storage_area['w'] - 20) // cols - 5
        station_height = self.storage_area['h'] - 30
        self.ingredient_positions = {}

        for i, ingredient_type in enumerate(ingredient_types):
            station_x = self.storage_area['x'] + 10 + i * (station_width + 5)
            station_y = self.storage_area['y'] + 15
            self.ingredient_positions[ingredient_type] = (station_x + station_width//2, station_y + station_height//2)
            
            # ⭐ Bac en bois
            station_rect = pygame.Rect(station_x, station_y, station_width, station_height)
            
            available_ingredients = [ing for ing in game_state.ingredients 
                                    if ing["type"] == ingredient_type and not ing["taken"] 
                                    and current_time >= ing.get("spawn_time", 0)]
            is_available = len(available_ingredients) > 0

            # ⭐ Bois clair pour les bacs
            draw_gradient_rect(self.screen, (210, 160, 100), (190, 140, 80), station_rect)
            
            if is_available:
                border_color = (100, 150, 100)
                status_color = (100, 180, 100)
                glow = int(25 + 15 * math.sin(current_time * 3))
            else:
                border_color = (120, 90, 60)
                status_color = (150, 120, 90)
                glow = 0

            pygame.draw.rect(self.screen, border_color, station_rect, 2)

            if glow > 0:
                glow_surf = pygame.Surface((station_width + 10, station_height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (100, 180, 100, glow), (0, 0, station_width + 10, station_height + 10), 3)
                self.screen.blit(glow_surf, (station_x - 5, station_y - 5))

            # Zone intérieure du bac
            storage_inner = pygame.Rect(station_x + 5, station_y + 25, station_width - 10, station_height - 30)
            pygame.draw.rect(self.screen, self.ingredient_config[ingredient_type]["color"], storage_inner)
            pygame.draw.rect(self.screen, (80, 60, 40), storage_inner, 2)

            if is_available and asset_manager:
                # Afficher les ingrédients empilés verticalement
                max_display = min(4, len(available_ingredients))
                for j, ing in enumerate(available_ingredients[:max_display]):
                    ing_x = storage_inner.centerx
                    ing_y = storage_inner.y + 15 + j * 20
                    ing["x"] = ing_x
                    ing["y"] = ing_y
                    float_y = ing_y + math.sin(current_time * 3 + j) * 1.5
                    
                    img = asset_manager.get_ingredient_image(ingredient_type)
                    if img:
                        scaled_img = pygame.transform.scale(img, (18, 18))
                        self.screen.blit(scaled_img, (ing_x - 9, float_y - 9))
                    else:
                        color = self.ingredient_config[ingredient_type]["color"]
                        pygame.draw.circle(self.screen, color, (ing_x, int(float_y)), 8)
                        pygame.draw.circle(self.screen, (255, 255, 255), (ing_x, int(float_y)), 8, 2)

            # Étiquette en haut
            label_overlay = pygame.Surface((station_width, 20), pygame.SRCALPHA)
            label_overlay.fill((80, 60, 40, 220))
            self.screen.blit(label_overlay, (station_x, station_y))
            label_text = self.font_small.render(ingredient_type.capitalize(), True, (255, 255, 255))
            label_rect = label_text.get_rect(center=(station_x + station_width//2, station_y + 10))
            self.screen.blit(label_text, label_rect)

            # LED d'état
            led_x = station_x + station_width - 8
            led_y = station_y + 8
            
            if is_available:
                halo_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.circle(halo_surf, (status_color[0], status_color[1], status_color[2], 60), (8, 8), 7)
                self.screen.blit(halo_surf, (led_x - 8, led_y - 8))
            pygame.draw.circle(self.screen, status_color, (led_x, led_y), 4)
            pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y), 4, 1)
            
            # Badge quantité
            if is_available:
                qty = len(available_ingredients)
                badge_color = (50, 150, 50) if qty > 2 else (100, 180, 100)
                badge_y = station_y + station_height - 10
                pygame.draw.circle(self.screen, badge_color, (station_x + station_width//2, badge_y), 8)
                pygame.draw.circle(self.screen, (255, 255, 255), (station_x + station_width//2, badge_y), 8, 1)
                qty_text = self.font_small.render(str(qty), True, (255, 255, 255))
                qty_rect = qty_text.get_rect(center=(station_x + station_width//2, badge_y))
                self.screen.blit(qty_text, qty_rect)

    
   # REMPLACE ENTIÈREMENT draw_work_station et tout après jusqu'à draw_plating_station

    def draw_work_station(self, asset_manager):
        import game_state
        current_time = time.time()
        
        work_rect = pygame.Rect(self.work_area['x'], self.work_area['y'], 
                              self.work_area['w'], self.work_area['h'])
        draw_gradient_rect(self.screen, (160, 110, 70), (140, 90, 60), work_rect)
        
        # ⭐ Texture bois
        for i in range(0, self.work_area['w'], 30):
            line_x = self.work_area['x'] + i
            pygame.draw.line(self.screen, (140, 100, 65), 
                           (line_x, self.work_area['y']), 
                           (line_x, self.work_area['y'] + self.work_area['h']), 1)
        
        pygame.draw.rect(self.screen, (100, 70, 40), work_rect, 3)
        
        title_bg = pygame.Rect(self.work_area['x'], self.work_area['y'] - 30, 
                              self.work_area['w'], 25)
        draw_gradient_rect(self.screen, (100, 70, 40), (80, 60, 30), title_bg)
        title = self.font_small.render("🔪 PLAN DE TRAVAIL", True, (255, 255, 255))
        self.screen.blit(title, (self.work_area['x'] + 10, self.work_area['y'] - 25))
        
        cutting_x = self.work_area['x'] + 15
        cutting_y = self.work_area['y'] + 20
        cutting_w = 80
        cutting_h = 70
        
        cutting_rect = pygame.Rect(cutting_x, cutting_y, cutting_w, cutting_h)
        draw_gradient_rect(self.screen, (210, 160, 100), (180, 130, 80), cutting_rect)
        pygame.draw.rect(self.screen, (120, 80, 40), cutting_rect, 2)
        
        # ⭐ Marques d'usure sur la planche
        for i in range(5):
            line_x = cutting_x + 10 + i * 14
            pygame.draw.line(self.screen, (160, 110, 60), (line_x, cutting_y + 10), (line_x, cutting_y + 60), 1)
        
        # ⭐ Couteau accroché quand pas utilisé
        knife_holder_x = cutting_x + cutting_w + 5
        knife_holder_y = cutting_y + 10
        pygame.draw.rect(self.screen, (100, 100, 100), (knife_holder_x, knife_holder_y, 8, 30))
        pygame.draw.polygon(self.screen, (180, 180, 180), 
                          [(knife_holder_x + 4, knife_holder_y + 5),
                           (knife_holder_x + 10, knife_holder_y + 12),
                           (knife_holder_x + 4, knife_holder_y + 12)])
        
        # ⭐⭐⭐ PLAQUE DE CUISSON VERTICALE COMPACTE ⭐⭐⭐
        hotplate_x = self.work_area['x'] + 120
        hotplate_y = self.work_area['y'] + 15
        hotplate_w = 65
        hotplate_h = 110
        
        hotplate_rect = pygame.Rect(hotplate_x, hotplate_y, hotplate_w, hotplate_h)
        
        # Vérifier si quelqu'un cuisine
        is_cooking = False
        cooking_chef = None
        if hasattr(game_state, 'bot_manager'):
            for bot in game_state.bot_manager.bots:
                if hasattr(bot, '_is_cooking') and bot._is_cooking:
                    is_cooking = True
                    cooking_chef = bot
                    break
        
        # Cadre métallique de la plaque
        pygame.draw.rect(self.screen, (80, 80, 80), hotplate_rect)
        
        # Surface de cuisson (avec gradient selon chaleur)
        if is_cooking:
            heat_pulse = int(200 + 55 * math.sin(current_time * 5))
            cooking_surface_color = (heat_pulse, heat_pulse // 3, 30)
        else:
            cooking_surface_color = (60, 60, 60)
        
        cooking_surface = pygame.Rect(hotplate_x + 5, hotplate_y + 5, hotplate_w - 10, 70)
        draw_gradient_rect(self.screen, cooking_surface_color,
                          (max(0, cooking_surface_color[0] - 40),
                           max(0, cooking_surface_color[1] - 40),
                           max(0, cooking_surface_color[2] - 40)),
                          cooking_surface)
        
        # Grille de cuisson
        for i in range(4):
            bar_y = hotplate_y + 10 + i * 15
            pygame.draw.line(self.screen, (40, 40, 40),
                            (hotplate_x + 7, bar_y),
                            (hotplate_x + hotplate_w - 7, bar_y), 2)
        
        # Contour
        pygame.draw.rect(self.screen, (50, 50, 50), hotplate_rect, 2)
        
        # Afficher l'ingrédient qui cuit si en cours
        if is_cooking and cooking_chef:
            ing_x = hotplate_x + hotplate_w // 2
            ing_y = hotplate_y + 35
            progress = cooking_chef.cooking_progress
            
            # Couleur selon cuisson
            if progress < 0.25:
                meat_color = (160, 60, 60)
            elif progress < 0.50:
                meat_color = (140, 50, 50)
            elif progress < 0.75:
                meat_color = (120, 70, 50)
            elif progress < 1.0:
                meat_color = (100, 60, 40)
            elif progress < 1.2:
                meat_color = (80, 40, 20)
            else:
                meat_color = (40, 20, 10)
            
            pygame.draw.circle(self.screen, meat_color, (ing_x, ing_y), 15)
            pygame.draw.circle(self.screen, (255, 255, 255), (ing_x, ing_y), 15, 1)
            
            # Fumée
            if progress > 0.1:
                self.create_cooking_smoke(ing_x, ing_y, progress)
            
            # Mini barre de progression
            bar_w = 50
            bar_h = 4
            bar_x = ing_x - bar_w // 2
            bar_y = ing_y + 22
            
            pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_w, bar_h))
            
            if progress < 0.75:
                bar_color = (100, 255, 100)
            elif progress < 1.0:
                bar_color = (255, 255, 100)
            elif progress < 1.2:
                bar_color = (255, 150, 0)
            else:
                bar_color = (255, 50, 50)
            
            fill_width = int(bar_w * min(progress, 1.2))
            pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, fill_width, bar_h))
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 1)
        
        # Contrôles (boutons rotatifs)
        for i in range(2):
            knob_x = hotplate_x + 10 + i * 35
            knob_y = hotplate_y + 85
            
            pygame.draw.circle(self.screen, (100, 100, 100), (knob_x, knob_y), 6)
            pygame.draw.circle(self.screen, (60, 60, 60), (knob_x, knob_y), 6, 2)
            
            angle = (current_time * 0.5 + i) if is_cooking else i
            mark_x = knob_x + math.cos(angle) * 4
            mark_y = knob_y + math.sin(angle) * 4
            pygame.draw.circle(self.screen, (200, 50, 50), (int(mark_x), int(mark_y)), 1)
        
        # LED d'état
        led_x = hotplate_x + hotplate_w - 8
        led_y = hotplate_y + 85
        
        if is_cooking:
            pulse = int(200 + 55 * math.sin(current_time * 4))
            led_color = (pulse, 50, 50)
            glow_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 100, 100, 80), (8, 8), 8)
            self.screen.blit(glow_surf, (led_x - 8, led_y - 8))
        else:
            led_color = (80, 80, 80)
        
        pygame.draw.circle(self.screen, led_color, (led_x, led_y), 3)
        pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y), 3, 1)
        
        self.draw_prepared_area(asset_manager)
        self.cutting_position = (cutting_x + cutting_w//2, cutting_y + cutting_h//2)
        self.hotplate_position = (hotplate_x + hotplate_w//2, hotplate_y + 35)

    def draw_cooking_station(self, asset_manager):
        """⭐ STATION DE CUISSON - AVEC STEAK VISIBLE"""
        import game_state
        current_time = time.time()
        
        # Plan de travail en bois
        cooking_rect = pygame.Rect(self.cooking_area['x'], self.cooking_area['y'], 
                                  self.cooking_area['w'], self.cooking_area['h'])
        draw_gradient_rect(self.screen, (160, 110, 70), (140, 90, 60), cooking_rect)
        
        # Texture bois
        for i in range(0, self.cooking_area['w'], 30):
            line_x = self.cooking_area['x'] + i
            pygame.draw.line(self.screen, (140, 100, 65), 
                           (line_x, self.cooking_area['y']), 
                           (line_x, self.cooking_area['y'] + self.cooking_area['h']), 1)
        
        pygame.draw.rect(self.screen, (100, 70, 40), cooking_rect, 3)
        
        # Titre
        title_bg = pygame.Rect(self.cooking_area['x'], self.cooking_area['y'] - 30, 
                              self.cooking_area['w'], 25)
        draw_gradient_rect(self.screen, (200, 80, 40), (180, 60, 20), title_bg)
        title = self.font_small.render("🔥 CUISSON", True, (255, 255, 255))
        self.screen.blit(title, (self.cooking_area['x'] + 10, self.cooking_area['y'] - 25))
        
        # Plaque de cuisson (grill)
        grill_x = self.cooking_area['x'] + 15
        grill_y = self.cooking_area['y'] + 20
        grill_w = 80
        grill_h = 70
        
        grill_rect = pygame.Rect(grill_x, grill_y, grill_w, grill_h)
        
        # Vérifier si quelqu'un cuisine
        is_cooking = False
        cooking_chef = None
        if hasattr(game_state, 'bot_manager'):
            for bot in game_state.bot_manager.bots:
                if hasattr(bot, '_is_cooking') and bot._is_cooking:
                    is_cooking = True
                    cooking_chef = bot
                    break
        
        # Fond de la plaque (métal)
        if is_cooking:
            # Chauffée : rouge/orange pulsant
            heat_pulse = int(200 + 55 * math.sin(current_time * 5))
            grill_color = (heat_pulse, heat_pulse // 3, 30)
        else:
            # Froide : gris foncé
            grill_color = (80, 80, 80)
        
        draw_gradient_rect(self.screen, grill_color, 
                          (max(0, grill_color[0] - 40), 
                           max(0, grill_color[1] - 40), 
                           max(0, grill_color[2] - 40)), 
                          grill_rect)
        
        # Grille (barres horizontales)
        for i in range(5):
            bar_y = grill_y + 10 + i * 12
            pygame.draw.line(self.screen, (60, 60, 60), 
                           (grill_x + 5, bar_y), 
                           (grill_x + grill_w - 5, bar_y), 3)
            
            # Reflets sur les barres
            pygame.draw.line(self.screen, (120, 120, 120), 
                           (grill_x + 5, bar_y - 1), 
                           (grill_x + grill_w - 5, bar_y - 1), 1)
        
        # Contour de la plaque
        pygame.draw.rect(self.screen, (50, 50, 50), grill_rect, 3)
        
        # ⭐⭐⭐ SI CUISSON EN COURS, AFFICHER LE STEAK ⭐⭐⭐
        if is_cooking and cooking_chef:
            ing_x = grill_x + grill_w // 2
            ing_y = grill_y + grill_h // 2
            
            # Progression de cuisson
            progress = cooking_chef.cooking_progress
            
            # Couleur selon cuisson (pour le steak)
            if progress < 0.25:
                meat_color = (160, 60, 60)      # Rouge saignant
            elif progress < 0.50:
                meat_color = (140, 50, 50)      # Rouge foncé
            elif progress < 0.75:
                meat_color = (120, 70, 50)      # Rosé
            elif progress < 1.0:
                meat_color = (100, 60, 40)      # Brun
            elif progress < 1.2:
                meat_color = (80, 40, 20)       # Brun foncé
            else:
                meat_color = (40, 20, 10)       # Brûlé
            
            # ⭐ DESSINER LE STEAK SUR LA PLAQUE
            # Corps principal du steak
            pygame.draw.circle(self.screen, meat_color, (ing_x, ing_y), 20)
            pygame.draw.circle(self.screen, (255, 200, 150), (ing_x, ing_y), 20, 2)
            
            # Marbrures et détails du steak
            for dot_idx in range(3):
                spot_x = ing_x + (dot_idx - 1) * 8
                spot_y = ing_y + (dot_idx - 1) * 5
                pygame.draw.circle(self.screen, (80, 30, 20), (spot_x, spot_y), 3)
            
            # Reflet sur le steak
            pygame.draw.circle(self.screen, (200, 100, 80), (ing_x - 7, ing_y - 7), 5)
            
            # Fumée intense si en train de cuire
            if progress > 0.1:
                self.create_cooking_smoke(ing_x, ing_y, progress)
            
            # Barre de progression
            bar_width = 60
            bar_height = 6
            bar_x = ing_x - bar_width // 2
            bar_y = ing_y + 30
            
            # Fond
            pygame.draw.rect(self.screen, (0, 0, 0), 
                           (bar_x, bar_y, bar_width, bar_height))
            
            # Remplissage selon progression
            fill_width = int(bar_width * min(progress, 1.2))
            
            if progress < 0.75:
                bar_color = (100, 255, 100)
            elif progress < 1.0:
                bar_color = (255, 255, 100)
            elif progress < 1.2:
                bar_color = (255, 150, 0)
            else:
                bar_color = (255, 50, 50)
            
            pygame.draw.rect(self.screen, bar_color,
                           (bar_x, bar_y, fill_width, bar_height))
            
            # Contour
            pygame.draw.rect(self.screen, (255, 255, 255),
                           (bar_x, bar_y, bar_width, bar_height), 1)
            
            # Pourcentage
            progress_text = self.font_small.render(f"{int(progress * 100)}%", 
                                                  True, (255, 255, 255))
            self.screen.blit(progress_text, (ing_x - 15, bar_y + 8))
        
        # Boutons de contrôle (décoratifs)
        for i in range(3):
            knob_x = self.cooking_area['x'] + self.cooking_area['w'] - 30
            knob_y = self.cooking_area['y'] + 30 + i * 25
            
            # Bouton rotatif
            pygame.draw.circle(self.screen, (100, 100, 100), (knob_x, knob_y), 8)
            pygame.draw.circle(self.screen, (60, 60, 60), (knob_x, knob_y), 8, 2)
            
            # Marque sur le bouton
            angle = (current_time * 0.5 + i) if is_cooking else i
            mark_x = knob_x + math.cos(angle) * 5
            mark_y = knob_y + math.sin(angle) * 5
            pygame.draw.circle(self.screen, (200, 50, 50), (int(mark_x), int(mark_y)), 2)
        
        # LED de status
        led_x = self.cooking_area['x'] + self.cooking_area['w'] - 30
        led_y = self.cooking_area['y'] + 10
        
        if is_cooking:
            # LED rouge pulsante
            pulse = int(200 + 55 * math.sin(current_time * 4))
            led_color = (pulse, 50, 50)
            
            # Halo lumineux
            glow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 100, 100, 80), (10, 10), 10)
            self.screen.blit(glow_surf, (led_x - 10, led_y - 10))
        else:
            led_color = (80, 80, 80)
        
        pygame.draw.circle(self.screen, led_color, (led_x, led_y), 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y), 4, 1)
        
        # Sauvegarder la position pour les bots - BIEN ALIGNÉE
        self.cooking_position = (grill_x + grill_w//2, grill_y + grill_h//2)
        self.cooking_area_center = (self.cooking_area['x'] + self.cooking_area['w']//2, 
                                   self.cooking_area['y'] + self.cooking_area['h']//2)

    def create_cooking_smoke(self, x, y, intensity):
        """Crée de la fumée pendant la cuisson"""
        if pygame.time.get_ticks() % 5 == 0:
            for _ in range(2):
                self.steam_particles.append({
                    'x': x + (pygame.time.get_ticks() % 20 - 10),
                    'y': y - 10,
                    'vy': -1.0 - (intensity * 0.5),
                    'size': 5 + intensity * 3,
                    'life': 1.0,
                    'color': (200, 200, 200) if intensity < 1.0 else (150, 150, 150)
                })

    def draw_prepared_area(self, asset_manager):
        import game_state
        current_time = time.time()
        
        prepared_x = self.work_area['x'] + 105
        prepared_y = self.work_area['y'] + 20
        prepared_w = 80
        prepared_h = 70
        
        prepared_rect = pygame.Rect(prepared_x, prepared_y, prepared_w, prepared_h)
        draw_gradient_rect(self.screen, (245, 240, 225), (235, 230, 215), prepared_rect)
        pygame.draw.rect(self.screen, (180, 160, 120), prepared_rect, 2)
        
        title_overlay = pygame.Surface((prepared_w, 16), pygame.SRCALPHA)
        title_overlay.fill((180, 140, 60, 200))
        self.screen.blit(title_overlay, (prepared_x, prepared_y - 16))
        title = self.font_small.render("✓ PRÉPARÉS", True, (255, 255, 255))
        self.screen.blit(title, (prepared_x + 5, prepared_y - 15))
        
        all_prepared = []
        if hasattr(game_state, 'order_manager'):
            for chef_id, order_info in game_state.order_manager.chef_orders.items():
                all_prepared.extend(order_info.get('prepared_ingredients', []))
        
        for idx, ingredient in enumerate(all_prepared[:8]):
            pos_x = prepared_x + 12 + (idx % 4) * 18
            pos_y = prepared_y + 12 + (idx // 4) * 22
            float_offset = math.sin(current_time * 4 + idx) * 1.5
            
            ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
            glow_pulse = int(60 + 30 * math.sin(current_time * 3 + idx))
            glow_surf = pygame.Surface((38, 38), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*ing_config["color"], glow_pulse), (19, 19), 17)
            self.screen.blit(glow_surf, (pos_x - 19, pos_y - 19 + float_offset))
            
            if asset_manager:
                img = asset_manager.get_ingredient_image(ingredient)
                if img:
                    scaled_img = pygame.transform.scale(img, (26, 26))
                    self.screen.blit(scaled_img, (pos_x - 13, pos_y - 13 + float_offset))
                else:
                    pygame.draw.circle(self.screen, ing_config["color"], (pos_x, int(pos_y + float_offset)), 12)
                    pygame.draw.circle(self.screen, (255, 255, 255), (pos_x, int(pos_y + float_offset)), 12, 2)
            
            # Checkmark
            check_x, check_y = pos_x + 10, pos_y - 10
            pygame.draw.circle(self.screen, (50, 180, 50), (check_x, check_y), 6)
            pygame.draw.circle(self.screen, (150, 255, 150), (check_x, check_y), 4)

    def update_steam_particles(self):
        """⭐ NOUVEAU : Gère la vapeur au-dessus de la plaque de cuisson"""
        import game_state
        
        # Mettre à jour les particules de vapeur
        for particle in self.steam_particles[:]:
            particle['y'] += particle['vy']
            particle['life'] -= 0.01
            particle['size'] += 0.1
            
            if particle['life'] <= 0:
                self.steam_particles.remove(particle)

    def draw_steam_particles(self):
        """Dessine la vapeur"""
        for particle in self.steam_particles:
            alpha = int(100 * particle['life'])
            steam_surf = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(steam_surf, (255, 255, 255, alpha), 
                             (int(particle['size']), int(particle['size'])), 
                             int(particle['size']))
            self.screen.blit(steam_surf, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))

    def draw_plating_station(self, asset_manager):
        import game_state
        current_time = time.time()
        
        # ⭐ NOUVEAU : Plan en bois comme les autres
        plating_rect = pygame.Rect(self.plating_area['x'], self.plating_area['y'], 
                                  self.plating_area['w'], self.plating_area['h'])
        draw_gradient_rect(self.screen, (160, 110, 70), (140, 90, 60), plating_rect)
        
        # Texture bois
        for i in range(0, self.plating_area['h'], 10):
            line_y = self.plating_area['y'] + i
            pygame.draw.line(self.screen, (140, 100, 65), 
                           (self.plating_area['x'], line_y), 
                           (self.plating_area['x'] + self.plating_area['w'], line_y), 1)
        
        pygame.draw.rect(self.screen, (100, 70, 40), plating_rect, 3)
        
        title_bg = pygame.Rect(self.plating_area['x'], self.plating_area['y'] - 30, 
                              self.plating_area['w'], 25)
        draw_gradient_rect(self.screen, (100, 70, 40), (80, 60, 30), title_bg)
        title = self.font_small.render("🍽️ ASSEMBLAGE", True, (255, 255, 255))
        self.screen.blit(title, (self.plating_area['x'] + 10, self.plating_area['y'] - 25))
        
        empty_plates_x = self.plating_area['x'] + 15
        empty_plates_y = self.plating_area['y'] + 20
        empty_plates_w = 60
        empty_plates_h = 70
        
        empty_rect = pygame.Rect(empty_plates_x, empty_plates_y, empty_plates_w, empty_plates_h)
        draw_gradient_rect(self.screen, (210, 160, 100), (190, 140, 80), empty_rect)
        pygame.draw.rect(self.screen, (120, 80, 40), empty_rect, 2)
        
        for i in range(3):
            plate_y = empty_plates_y + 15 + i * 4
            plate_x = empty_plates_x + empty_plates_w//2
            pygame.draw.circle(self.screen, (180, 180, 150), (plate_x + 2, plate_y + 2), 16)
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_x, plate_y), 16)
            pygame.draw.circle(self.screen, (240, 245, 220), (plate_x, plate_y), 12)
            pygame.draw.circle(self.screen, (200, 200, 160), (plate_x, plate_y), 16, 1)
        
        assembly_x = self.plating_area['x'] + 85
        assembly_y = self.plating_area['y'] + 20
        assembly_w = 70
        assembly_h = 70
        assembly_rect = pygame.Rect(assembly_x, assembly_y, assembly_w, assembly_h)
        
        plating_chefs = []
        if hasattr(game_state, 'bot_manager'):
            for bot in game_state.bot_manager.bots:
                if bot.plating:
                    order = bot.get_my_order()
                    if order:
                        plating_chefs.append({'bot': bot, 'ingredients': order.get('prepared_ingredients', [])})
        
        if plating_chefs:
            chef_data = plating_chefs[0]
            ingredients = chef_data['ingredients']
            
            draw_gradient_rect(self.screen, (210, 160, 100), (190, 140, 80), assembly_rect)
            pygame.draw.rect(self.screen, (120, 80, 40), assembly_rect, 2)
            
            plate_center_x = assembly_x + assembly_w//2
            plate_center_y = assembly_y + assembly_h//2
            
            glow = int(40 + 30 * math.sin(current_time * 4))
            glow_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 150, glow), (50, 50), 45)
            self.screen.blit(glow_surf, (plate_center_x - 50, plate_center_y - 50))
            
            pygame.draw.circle(self.screen, (180, 180, 180), (plate_center_x + 2, plate_center_y + 2), 32)
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_center_x, plate_center_y), 32)
            pygame.draw.circle(self.screen, (245, 245, 230), (plate_center_x, plate_center_y), 28)
            pygame.draw.circle(self.screen, (200, 200, 180), (plate_center_x, plate_center_y), 32, 3)
            
            for idx, ingredient in enumerate(ingredients):
                angle = (idx * 2 * math.pi) / max(1, len(ingredients))
                radius = 20
                rotation = current_time * 0.5
                ing_x = plate_center_x + math.cos(angle + rotation) * radius
                ing_y = plate_center_y + math.sin(angle + rotation) * radius
                
                ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
                glow_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*ing_config["color"], 120), (25, 25), 23)
                self.screen.blit(glow_surf, (ing_x - 25, ing_y - 25))
                
                if asset_manager:
                    img = asset_manager.get_ingredient_image(ingredient)
                    if img:
                        scaled_img = pygame.transform.scale(img, (32, 32))
                        self.screen.blit(scaled_img, (ing_x - 16, ing_y - 16))
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], (int(ing_x), int(ing_y)), 14)
                        pygame.draw.circle(self.screen, (255, 255, 255), (int(ing_x), int(ing_y)), 14, 2)
        else:
            draw_gradient_rect(self.screen, (210, 160, 100), (190, 140, 80), assembly_rect)
            pygame.draw.rect(self.screen, (120, 80, 40), assembly_rect, 2)
        
        self.plating_position = (assembly_x + assembly_w//2, assembly_y + assembly_h//2)

    def draw_service_station(self):
        current_time = time.time()
        service_rect = pygame.Rect(self.service_area['x'], self.service_area['y'], 
                                   self.service_area['w'], self.service_area['h'])
        
        glow = int(20 + 10 * math.sin(current_time * 2))
        for i in range(3, 0, -1):
            alpha = glow // i
            glow_surf = pygame.Surface((self.service_area['w'] + i*6, self.service_area['h'] + i*6), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 215, 0, alpha), (0, 0, self.service_area['w'] + i*6, self.service_area['h'] + i*6))
            self.screen.blit(glow_surf, (self.service_area['x'] - i*3, self.service_area['y'] - i*3))
        
        # ⭐ Plan en bois comme les autres stations
        draw_gradient_rect(self.screen, (160, 110, 70), (140, 90, 60), service_rect)
        
        # Texture bois verticale
        for i in range(0, self.service_area['h'], 10):
            line_y = self.service_area['y'] + i
            pygame.draw.line(self.screen, (140, 100, 65), 
                           (self.service_area['x'], line_y), 
                           (self.service_area['x'] + self.service_area['w'], line_y), 1)
        
        pygame.draw.rect(self.screen, (100, 70, 40), service_rect, 3)
        
        title_bg = pygame.Rect(self.service_area['x'], self.service_area['y'] - 30, self.service_area['w'], 25)
        draw_gradient_rect(self.screen, (180, 150, 80), (160, 130, 60), title_bg)
        title = self.font_small.render("🚀 SERVICE", True, (255, 255, 255))
        self.screen.blit(title, (self.service_area['x'] + 10, self.service_area['y'] - 25))
        
        # ⭐ Cloche de service (bell)
        bell_x = self.service_area['x'] + self.service_area['w'] // 2
        bell_y = self.service_area['y'] + 40
        pygame.draw.circle(self.screen, (200, 200, 200), (bell_x, bell_y), 15)
        pygame.draw.circle(self.screen, (220, 220, 220), (bell_x, bell_y), 12)
        pygame.draw.rect(self.screen, (180, 180, 180), (bell_x - 10, bell_y + 10, 20, 5))
        pygame.draw.circle(self.screen, (150, 150, 150), (bell_x, bell_y - 10), 3)
        
        self.draw_delivered_dishes(current_time)
        
        drop_zone_y = self.service_area['y'] + 100
        drop_zone_rect = pygame.Rect(self.service_area['x'] + 20, drop_zone_y, 80, 80)
        
        pulse = int(30 + 15 * math.sin(current_time * 3))
        glow_surf = pygame.Surface((90, 90), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (100, 255, 100, pulse), (0, 0, 90, 90), border_radius=10)
        self.screen.blit(glow_surf, (drop_zone_rect.x - 5, drop_zone_rect.y - 5))
        
        draw_gradient_rect(self.screen, (200, 255, 200), (150, 240, 150), drop_zone_rect)
        pygame.draw.rect(self.screen, (80, 200, 80), drop_zone_rect, 3, border_radius=8)
        
        icon_text = self.font_large.render("🚀", True, (40, 180, 40))
        icon_rect = icon_text.get_rect(center=drop_zone_rect.center)
        self.screen.blit(icon_text, icon_rect)
        
        deliver_text = self.font_small.render("LIVRER ICI", True, (40, 150, 40))
        text_rect = deliver_text.get_rect(center=(drop_zone_rect.centerx, drop_zone_rect.bottom + 15))
        self.screen.blit(deliver_text, text_rect)
        
        # ⭐ Dessiner particules d'étincelles
        self.draw_sparkle_particles()

    def draw_delivered_dishes(self, current_time):
        self.delivered_dishes = [d for d in self.delivered_dishes if current_time - d['time'] < 2.0]
        
        for dish in self.delivered_dishes:
            progress = (current_time - dish['time']) / 2.0
            
            start_y = self.service_area['y'] + 180
            end_y = self.service_area['y'] + 50
            current_y = start_y - (start_y - end_y) * progress
            
            alpha = int(255 * (1 - max(0, (progress - 0.7) / 0.3)))
            
            pos_x = self.service_area['x'] + self.service_area['w'] // 2
            
            dish_surf = pygame.Surface((70, 70), pygame.SRCALPHA)
            
            glow_size = int(80 - 20 * progress)
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (100, 255, 100, alpha // 2), (glow_size // 2, glow_size // 2), glow_size // 2)
            dish_surf.blit(glow_surf, (35 - glow_size // 2, 35 - glow_size // 2))
            
            if 'burger' in dish['name'].lower():
                self.draw_mini_burger(dish_surf, 35, 35, alpha)
            else:
                self.draw_mini_salad(dish_surf, 35, 35, alpha)
            
            check_size = int(15 + 5 * math.sin(current_time * 10))
            pygame.draw.circle(dish_surf, (100, 255, 100, alpha), (55, 15), check_size)
            pygame.draw.circle(dish_surf, (50, 200, 50, alpha), (55, 15), check_size, 2)
            
            check_text = self.font_small.render("✓ LIVRÉ", True, (255, 255, 255, alpha))
            text_bg = pygame.Surface((check_text.get_width() + 10, check_text.get_height() + 4), pygame.SRCALPHA)
            text_bg.fill((50, 200, 50, alpha))
            dish_surf.blit(text_bg, (5, 50))
            dish_surf.blit(check_text, (10, 52))
            
            self.screen.blit(dish_surf, (pos_x - 35, int(current_y) - 35))
    
    def draw_mini_burger(self, surface, x, y, alpha):
        colors = [
            ((220, 170, 90, alpha), 18),
            ((255, 230, 90, alpha), 16),
            ((160, 90, 60, alpha), 15),
            ((240, 60, 60, alpha), 14),
            ((60, 220, 60, alpha), 13),
            ((220, 170, 90, alpha), 16),
        ]
        offset = 0
        for color, radius in colors:
            pygame.draw.circle(surface, color, (x, y - offset), radius)
            pygame.draw.circle(surface, (100, 100, 100, alpha // 2), (x, y - offset), radius, 1)
            offset += 3
    
    def draw_mini_salad(self, surface, x, y, alpha):
        pygame.draw.ellipse(surface, (255, 255, 255, alpha), (x - 20, y + 5, 40, 15))
        pygame.draw.circle(surface, (90, 200, 90, alpha), (x, y - 5), 16)
        pygame.draw.circle(surface, (60, 180, 60, alpha), (x, y - 5), 16, 1)
        for offset in [(-8, 0), (8, -3), (0, 5)]:
            pygame.draw.circle(surface, (240, 60, 60, alpha), (x + offset[0], y + offset[1]), 3)

    def add_delivered_dish(self, order_name):
        """Ajoute un plat livré et crée des étincelles"""
        self.delivered_dishes.append({
            'name': order_name,
            'time': time.time()
        })
        
        # ⭐ Créer des étincelles à la livraison
        center_x = self.service_area['x'] + self.service_area['w'] // 2
        center_y = self.service_area['y'] + 140
        
        for _ in range(20):
            angle = (pygame.time.get_ticks() % 360) * math.pi / 180
            speed = 2 + pygame.time.get_ticks() % 3
            self.sparkle_particles.append({
                'x': center_x,
                'y': center_y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': (255, 215, 0)
            })

    def draw_sparkle_particles(self):
        """⭐ NOUVEAU : Étincelles dorées à la livraison"""
        for particle in self.sparkle_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravité
            particle['life'] -= 0.02
            
            if particle['life'] <= 0:
                self.sparkle_particles.remove(particle)
                continue
            
            alpha = int(255 * particle['life'])
            size = int(3 * particle['life'])
            
            if size > 0:
                sparkle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(sparkle_surf, (*particle['color'], alpha), (size, size), size)
                self.screen.blit(sparkle_surf, (int(particle['x'] - size), int(particle['y'] - size)))

    def draw_chef_enhanced(self, bot, asset_manager):
        base_x, base_y = bot.x, bot.y
        current_time = time.time()
        
        if bot.state == "cutting" and bot.preparing:
            board_x = self.work_area['x'] + 55
            board_y = self.work_area['y'] + 55
            
            if not self.cutting_animation.active:
                self.cutting_animation.start(bot.preparing, board_x, board_y)
            
            self.cutting_animation.update()
            self.cutting_animation.draw()
            
            shake = math.sin(current_time * 30) * 2
            base_x += shake
            base_y += shake * 0.5
        
        elif bot.state in ["going_to_fridge", "going_to_board", "going_to_plating", "going_to_delivery"]:
            walk_cycle = math.sin(bot.animation_time * 8) * 3
            base_y -= abs(walk_cycle)
        
        elif bot.state == "delivering":
            delivery_progress = (current_time - bot.delivery_start_time) if hasattr(bot, 'delivery_start_time') else 0
            if delivery_progress < 1.0:
                bounce = abs(math.sin(delivery_progress * math.pi * 4)) * 10
                base_y -= bounce
        
        original_x, original_y = bot.x, bot.y
        bot.x, bot.y = base_x, base_y
        bot.draw_chef(self.screen)
        bot.x, bot.y = original_x, original_y
        
        if bot.inv and bot.inv != "plated_dish":
            ing_config = self.ingredient_config.get(bot.inv, {"color": (150, 150, 150)})
            carry_x = base_x + 20
            carry_y = base_y - 30
            float_offset = math.sin(current_time * 6) * 3
            
            glow_pulse = int(100 + 50 * math.sin(current_time * 5))
            glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*ing_config["color"], glow_pulse), (30, 30), 28)
            self.screen.blit(glow_surf, (carry_x - 30, carry_y - 30 + float_offset))
            
            if asset_manager:
                img = asset_manager.get_ingredient_image(bot.inv)
                if img:
                    scaled_img = pygame.transform.scale(img, (40, 40))
                    self.screen.blit(scaled_img, (carry_x - 20, carry_y - 20 + float_offset))
                else:
                    pygame.draw.circle(self.screen, ing_config["color"], (carry_x, int(carry_y + float_offset)), 18)
                    pygame.draw.circle(self.screen, (255, 255, 255), (carry_x, int(carry_y + float_offset)), 18, 3)
        
        elif bot.inv == "plated_dish":
            carry_x = base_x + 30
            carry_y = base_y - 45
            float_offset = math.sin(current_time * 4) * 3
            
            glow_size = int(80 + 15 * math.sin(current_time * 3))
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 215, 0, 100), (glow_size // 2, glow_size // 2), glow_size // 2)
            self.screen.blit(glow_surf, (carry_x - glow_size // 2, carry_y - glow_size // 2 + float_offset))
            
            my_order = bot.get_my_order()
            if my_order:
                order_name = my_order['order_data']['name']
                
                if 'burger' in order_name.lower():
                    if asset_manager:
                        burger_img = asset_manager.get_ingredient_image('burger')
                        if burger_img:
                            self.screen.blit(burger_img, (carry_x - 32, carry_y - 32 + float_offset))
                        else:
                            self.draw_fallback_burger(carry_x, carry_y + float_offset)
                    else:
                        self.draw_fallback_burger(carry_x, carry_y + float_offset)
                
                elif 'salade' in order_name.lower():
                    if asset_manager:
                        salade_img = asset_manager.get_ingredient_image('salade_plat')
                        if salade_img:
                            self.screen.blit(salade_img, (carry_x - 32, carry_y - 32 + float_offset))
                        else:
                            self.draw_fallback_salad(carry_x, carry_y + float_offset)
                    else:
                        self.draw_fallback_salad(carry_x, carry_y + float_offset)
        
        state_color = bot.get_state_color()
        pygame.draw.circle(self.screen, state_color, (int(base_x), int(base_y - 60)), 7)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(base_x), int(base_y - 60)), 7, 2)
        
        chef_info = f"{bot.chef_name}: {bot.get_state_text()}"
        info_text = self.font_small.render(chef_info, True, (40, 40, 40))
        info_rect = info_text.get_rect(center=(int(base_x), int(base_y - 75)))
        text_bg = pygame.Surface((info_rect.width + 10, info_rect.height + 6), pygame.SRCALPHA)
        text_bg.fill((255, 255, 255, 230))
        self.screen.blit(text_bg, (info_rect.x - 5, info_rect.y - 3))
        self.screen.blit(info_text, info_rect)
    
    def draw_fallback_burger(self, x, y):
        pygame.draw.circle(self.screen, (220, 170, 90), (x, y + 10), 25)
        pygame.draw.circle(self.screen, (60, 220, 60), (x, y), 23)
        pygame.draw.circle(self.screen, (240, 60, 60), (x, y - 5), 22)
        pygame.draw.circle(self.screen, (160, 90, 60), (x, y - 10), 21)
        pygame.draw.circle(self.screen, (255, 230, 90), (x, y - 15), 24)
        pygame.draw.circle(self.screen, (220, 170, 90), (x, y - 20), 26)
    
    def draw_fallback_salad(self, x, y):
        pygame.draw.ellipse(self.screen, (255, 255, 255), (x - 25, y + 5, 50, 20))
        pygame.draw.circle(self.screen, (90, 200, 90), (x, y - 5), 22)
        for pos in [(x - 10, y), (x + 10, y - 3), (x, y + 5)]:
            pygame.draw.circle(self.screen, (240, 60, 60), pos, 4)
    
    def get_interaction_zones(self):
        """Retourne les positions correctes pour que les bots aillent cuire le steak"""
        # Position EXACTE où les bots doivent aller pour cuire
        # La plaque est à self.cooking_area['x'] + 15 et self.cooking_area['y'] + 20
        # On veut le centre de la plaque pour que le steak s'affiche dessus
        
        grill_x = self.cooking_area['x'] + 15
        grill_y = self.cooking_area['y'] + 20
        grill_w = 80
        grill_h = 70
        
        cooking_x = grill_x + grill_w // 2
        cooking_y = grill_y + grill_h // 2
        
        return {
            'fridge': (self.storage_area['x'] + 140, self.storage_area['y'] + 160),
            'cutting': (self.work_area['x'] + 60, self.work_area['y'] + 100),
            'cooking': (cooking_x, cooking_y),  # ⭐ POSITION CORRECTE DE LA PLAQUE
            'plating': (self.plating_area['x'] + 100, self.plating_area['y'] + 100),
            'delivery': (self.service_area['x'] + 60, self.service_area['y'] + 150)
        }
    def render_full_kitchen(self, bot_manager, asset_manager, timer):
        """Render complet avec TOUS les nouveaux visuels"""
        self.draw_floor()
        
        # ⭐ NOUVEAUX ÉLÉMENTS DÉCORATIFS
        self.draw_overhead_lamps()
        self.draw_wall_decorations()
        
        self.draw_individual_ingredient_stations(asset_manager)
        self.draw_work_station(asset_manager)
        self.draw_cooking_station(asset_manager)
        self.draw_plating_station(asset_manager)
        self.draw_service_station()
        
        # ⭐ Mettre à jour et dessiner vapeur
        self.update_steam_particles()
        self.draw_steam_particles()
        
        if self.cutting_animation.active:
            self.cutting_animation.update()
            self.cutting_animation.draw()
        
        if bot_manager and hasattr(bot_manager, 'bots'):
            zones = self.get_interaction_zones()
            bins = {}
            if hasattr(self, 'ingredient_positions'):
                bins = self.ingredient_positions
            
            for bot in bot_manager.bots:
                bot.update_interaction_zones(zones)
                if bins:
                    bot.update_ingredient_bins(bins)
                self.draw_chef_status(bot)
    
    def check_delivery_trigger(self, bot):
        """Vérifie si un bot vient de livrer"""
        if bot.state == "going_to_delivery" and bot.inv == "plated_dish":
            distance = ((bot.x - self.service_area['x'] - 60)**2 + 
                       (bot.y - self.service_area['y'] - 150)**2)**0.5
            
            if distance < 30:
                my_order = bot.get_my_order()
                if my_order:
                    self.add_delivered_dish(my_order['order_data']['name'])
                    return True
        return False
    
    def draw_chef_status(self, bot):
        """Affiche le statut d'UN chef"""
        import game_state
        
        if not hasattr(game_state, 'bot_manager'):
            return
        
        try:
            chef_index = game_state.bot_manager.bots.index(bot)
        except ValueError:
            return
        
        panel_width = 300
        panel_height = 70
        margin = 10
        
        status_x = 15 + (chef_index * (panel_width + margin))
        status_y = HEIGHT - 85
        
        if status_x + panel_width > WIDTH - 15:
            status_x = 15 + ((chef_index % 3) * (panel_width + margin))
            status_y = HEIGHT - 165
        
        status_rect = pygame.Rect(status_x, status_y, panel_width, panel_height)
        status_bg = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        status_bg.fill((255, 255, 255, 250))
        self.screen.blit(status_bg, status_rect)
        
        border_color = bot.get_state_color()
        pygame.draw.rect(self.screen, border_color, status_rect, 3)
        
        chef_line = f"👨‍🍳 {bot.chef_name}"
        chef_text = self.font_small.render(chef_line, True, (0, 0, 0))
        self.screen.blit(chef_text, (status_rect.x + 8, status_rect.y + 5))
        
        state_text = self.font_small.render(bot.get_state_text(), True, border_color)
        self.screen.blit(state_text, (status_rect.x + 8, status_rect.y + 22))
        
        my_order = bot.get_my_order()
        if my_order:
            order_name = my_order['order_data']['name']
            prepared = my_order.get('prepared_ingredients', [])
            total = len(my_order['order_data']['ingredients'])
            
            order_info = f"📋 {order_name} ({len(prepared)}/{total})"
            order_text = self.font_small.render(order_info, True, (0, 100, 0))
            self.screen.blit(order_text, (status_rect.x + 8, status_rect.y + 39))
            
            action_info = ""
            if bot.inv == "plated_dish":
                action_info = "🚀 Livre le plat"
            elif bot.inv:
                action_info = f"🥕 Porte {bot.inv}"
            elif hasattr(bot, '_is_cooking') and bot._is_cooking:
                cook_progress = int(bot.cooking_progress * 100)
                action_info = f"🔥 Cuit {bot._is_cooking} ({cook_progress}%)"
            elif bot.preparing:
                prep_time_left = bot.prep_times.get(bot.preparing, 1.5) - (time.time() - bot.prep_time)
                action_info = f"🔪 {bot.preparing} ({prep_time_left:.1f}s)"
            elif bot.plating:
                plate_time_left = bot.PLATING_TIME - (time.time() - bot.plate_time)
                action_info = f"🍽️ Assemble ({plate_time_left:.1f}s)"
            
            if action_info:
                action_text = self.font_small.render(action_info, True, (200, 100, 0))
                self.screen.blit(action_text, (status_rect.x + 8, status_rect.y + 53))


class CuttingAnimation:
    """Animation COMPACTE de découpe"""
    
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.ingredient = None
        self.start_time = 0
        self.duration = 1.0
        self.particles = []
        self.board_pos = None
        
        self.ingredient_config = {
            'tomate': {'slices': 2, 'slice_color': (255, 107, 107), 'main_color': (230, 57, 70)},
            'laitue': {'slices': 2, 'slice_color': (82, 183, 136), 'main_color': (45, 106, 79)},
            'oignon': {'slices': 3, 'slice_color': (229, 212, 193), 'main_color': (200, 182, 166)},
            'steak': {'slices': 2, 'slice_color': (160, 82, 45), 'main_color': (139, 69, 19)},
            'pain': {'slices': 1, 'slice_color': (244, 229, 194), 'main_color': (218, 165, 32)},
            'fromage': {'slices': 1, 'slice_color': (255, 230, 120), 'main_color': (255, 220, 80)}
        }
    
    def start(self, ingredient_type, board_x, board_y):
        if ingredient_type not in self.ingredient_config:
            return
        self.active = True
        self.ingredient = ingredient_type
        self.start_time = time.time()
        self.board_pos = (board_x, board_y)
        self.particles = []
    
    def stop(self):
        self.active = False
        self.ingredient = None
        self.particles = []
    
    def update(self):
        if not self.active:
            return False
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        if progress < 0.7 and len(self.particles) < 15:
            if pygame.time.get_ticks() % 5 == 0:
                self.create_particles()
        self.update_particles()
        if progress >= 1.0:
            self.stop()
            return True
        return False
    
    def create_particles(self):
        if not self.board_pos:
            return
        config = self.ingredient_config[self.ingredient]
        board_x, board_y = self.board_pos
        for _ in range(2):
            particle = {
                'x': board_x + (pygame.time.get_ticks() % 10 - 5),
                'y': board_y,
                'vx': (pygame.time.get_ticks() % 4 - 2) * 0.3,
                'vy': -(pygame.time.get_ticks() % 3 + 1),
                'size': 1 + pygame.time.get_ticks() % 2,
                'color': config['slice_color'],
                'life': 1.0
            }
            self.particles.append(particle)
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.25
            particle['life'] -= 0.03
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self):
        if not self.active or not self.board_pos:
            return
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        board_x, board_y = self.board_pos
        config = self.ingredient_config[self.ingredient]
        self.draw_slices_compact(board_x, board_y, progress, config)
        if progress < 0.7:
            self.draw_knife_compact(board_x, board_y, progress)
        self.draw_particles()
    
    def draw_slices_compact(self, board_x, board_y, progress, config):
        num_slices = config['slices']
        separation = min(progress * 2.5, 1.0) * 8
        for i in range(num_slices):
            offset_x = (i - num_slices / 2) * 15
            slice_x = int(board_x + offset_x + (i - num_slices / 2) * separation)
            slice_y = board_y
            pygame.draw.circle(self.screen, config['main_color'], (slice_x, slice_y), 8)
            pygame.draw.circle(self.screen, config['slice_color'], (slice_x, slice_y), 6)
            pygame.draw.circle(self.screen, (255, 255, 255), (slice_x, slice_y), 8, 1)
    
    def draw_knife_compact(self, board_x, board_y, progress):
        knife_y = board_y - 25 + progress * 50
        knife_x = board_x - 10
        shake = math.sin(progress * math.pi * 6) * 1.5
        knife_x += shake
        blade_points = [
            (knife_x, knife_y - 15),
            (knife_x + 8, knife_y),
            (knife_x - 2, knife_y)
        ]
        shadow_points = [(p[0] + 1, p[1] + 1) for p in blade_points]
        pygame.draw.polygon(self.screen, (100, 100, 100, 150), shadow_points)
        pygame.draw.polygon(self.screen, (220, 220, 220), blade_points)
        pygame.draw.polygon(self.screen, (180, 180, 180), blade_points, 1)
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (knife_x + 1, knife_y - 13), 
                        (knife_x + 3, knife_y - 8), 1)
        handle_rect = pygame.Rect(knife_x - 3, knife_y, 6, 12)
        pygame.draw.rect(self.screen, (107, 68, 35), handle_rect)
        pygame.draw.rect(self.screen, (70, 70, 70), handle_rect, 1)
    
    def draw_particles(self):
        for particle in self.particles:
            alpha = int(200 * particle['life'])
            color = (*particle['color'][:3], alpha)
            if particle['size'] > 0:
                particle_surf = pygame.Surface((particle['size'] * 2 + 2, particle['size'] * 2 + 2), 
                                              pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, color, 
                                 (particle['size'] + 1, particle['size'] + 1), 
                                 particle['size'])
                self.screen.blit(particle_surf, 
                               (int(particle['x'] - particle['size']), 
                                int(particle['y'] - particle['size'])))