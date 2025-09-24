"""
Kitchen rendering - Vue cuisine avec bacs individuels pour chaque ingrédient
"""
import pygame
import time
import math
from config import COLORS, WIDTH, HEIGHT

def draw_gradient_rect(surface, color1, color2, rect):
    """Dessine un rectangle avec un dégradé"""
    for i in range(rect.height):
        ratio = i / rect.height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), 
                        (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))

class KitchenRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        
        # Configuration des ingrédients avec couleurs spécifiques
        self.ingredient_config = {
            "laitue": {"color": (50, 200, 50), "icon": "🥬"},
            "tomate": {"color": (220, 50, 50), "icon": "🍅"},
            "pain": {"color": (200, 150, 80), "icon": "🍞"},
            "steak": {"color": (140, 80, 50), "icon": "🥩"},
            "fromage": {"color": (255, 220, 80), "icon": "🧀"},
            "oignon": {"color": (200, 180, 140), "icon": "🧅"},
            "salade": {"color": (80, 180, 80), "icon": "🥗"}
        }
        
        self.setup_kitchen_layout()

    def setup_kitchen_layout(self):
        """Configure la disposition de la cuisine"""
        # Zone de stockage avec bacs individuels (gauche)
        self.storage_area = {
            'x': 50, 'y': 120, 'w': 300, 'h': 350,
            'floor_x': 50, 'floor_y': 470, 'floor_w': 300, 'floor_h': 80
        }
        
        # Plan de travail (centre-haut)
        self.work_area = {
            'x': 400, 'y': 120, 'w': 250, 'h': 120,
            'floor_x': 400, 'floor_y': 240, 'floor_w': 250, 'floor_h': 100
        }
        
        # Zone de service (droite)
        self.service_area = {
            'x': 700, 'y': 120, 'w': 120, 'h': 300,
            'floor_x': 620, 'floor_y': 240, 'floor_w': 100, 'floor_h': 180
        }
        
        # Zone centrale de circulation
        self.circulation = {
            'x': 350, 'y': 350, 'w': 300, 'h': 150
        }

    def draw_floor(self):
        """Sol avec carrelage moderne"""
        # Carrelage de base
        tile_size = 50
        for x in range(0, WIDTH, tile_size):
            for y in range(0, HEIGHT, tile_size):
                # Alternance de couleurs
                if (x//tile_size + y//tile_size) % 2 == 0:
                    color = (245, 245, 245)
                else:
                    color = (230, 230, 230)
                
                tile_rect = pygame.Rect(x, y, tile_size, tile_size)
                pygame.draw.rect(self.screen, color, tile_rect)
                pygame.draw.rect(self.screen, (200, 200, 200), tile_rect, 1)
        
        # Zones de circulation spéciales
        circulation_zones = [
            (self.storage_area['floor_x'], self.storage_area['floor_y'], 
             self.storage_area['floor_w'], self.storage_area['floor_h']),
            (self.work_area['floor_x'], self.work_area['floor_y'], 
             self.work_area['floor_w'], self.work_area['floor_h']),
            (self.service_area['floor_x'], self.service_area['floor_y'], 
             self.service_area['floor_w'], self.service_area['floor_h']),
            (self.circulation['x'], self.circulation['y'], 
             self.circulation['w'], self.circulation['h'])
        ]
        
        for x, y, w, h in circulation_zones:
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((180, 200, 220, 50))
            self.screen.blit(overlay, (x, y))

    def draw_individual_ingredient_stations(self, asset_manager):
        """Dessine des stations individuelles pour chaque type d'ingrédient"""
        import game_state
        current_time = time.time()
        
        # Fond de la zone de stockage
        storage_rect = pygame.Rect(self.storage_area['x'], self.storage_area['y'], 
                                  self.storage_area['w'], self.storage_area['h'])
        draw_gradient_rect(self.screen, (240, 245, 250), (220, 225, 230), storage_rect)
        pygame.draw.rect(self.screen, (150, 160, 170), storage_rect, 3)
        
        # Récupérer tous les types d'ingrédients disponibles
        ingredient_types = list(set(ing["type"] for ing in game_state.ingredients))
        if not ingredient_types:
            # Fallback avec ingrédients par défaut
            ingredient_types = ["laitue", "tomate", "pain", "steak", "fromage"]
        
        # Organiser en grille 3x3
        cols = 3
        station_width = 80
        station_height = 90
        margin_x = 20
        margin_y = 20
        
        for i, ingredient_type in enumerate(ingredient_types):
            col = i % cols
            row = i // cols
            
            station_x = self.storage_area['x'] + margin_x + col * (station_width + 15)
            station_y = self.storage_area['y'] + margin_y + row * (station_height + 15)
            
            # Configuration de l'ingrédient
            ing_config = self.ingredient_config.get(ingredient_type, {
                "color": (150, 150, 150), 
                "icon": "?"
            })
            
            # Vérifier disponibilité
            available_ingredients = [ing for ing in game_state.ingredients 
                                   if ing["type"] == ingredient_type 
                                   and not ing["taken"] 
                                   and current_time >= ing.get("spawn_time", 0)]
            
            is_available = len(available_ingredients) > 0
            
            # Station individuelle
            station_rect = pygame.Rect(station_x, station_y, station_width, station_height)
            
            if is_available:
                # Station active - couleur verte
                draw_gradient_rect(self.screen, (220, 255, 220), (180, 220, 180), station_rect)
                border_color = (50, 180, 50)
                status_color = (50, 200, 50)
            else:
                # Station vide - couleur grise
                draw_gradient_rect(self.screen, (240, 240, 240), (200, 200, 200), station_rect)
                border_color = (150, 150, 150)
                status_color = (180, 180, 180)
            
            pygame.draw.rect(self.screen, border_color, station_rect, 2)
            
            # Zone de stockage dans la station
            storage_rect = pygame.Rect(station_x + 10, station_y + 30, 60, 40)
            pygame.draw.rect(self.screen, ing_config["color"], storage_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), storage_rect, 1)
            
            # Ingrédients disponibles dans la station
            if is_available:
                for j, ing in enumerate(available_ingredients[:4]):  # Max 4 ingrédients affichés
                    # Position de l'ingrédient pour interaction
                    ing_x = storage_rect.x + 15 + (j % 2) * 25
                    ing_y = storage_rect.y + 10 + (j // 2) * 20
                    
                    # Mise à jour position pour le bot
                    ing["x"] = ing_x
                    ing["y"] = ing_y
                    
                    # Animation de flottement
                    float_y = ing_y + math.sin(current_time * 3 + j) * 1
                    
                    try:
                        if asset_manager:
                            img = asset_manager.get_ingredient_image(ingredient_type)
                            if img:
                                scaled_img = pygame.transform.scale(img, (18, 18))
                                self.screen.blit(scaled_img, (ing_x - 9, float_y - 9))
                            else:
                                pygame.draw.circle(self.screen, ing_config["color"], 
                                                 (ing_x, int(float_y)), 8)
                        else:
                            pygame.draw.circle(self.screen, ing_config["color"], 
                                             (ing_x, int(float_y)), 8)
                    except:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                         (ing_x, int(float_y)), 8)
            
            # Étiquette de l'ingrédient
            label_text = self.font_small.render(ingredient_type.capitalize(), True, (60, 60, 60))
            label_rect = label_text.get_rect(center=(station_x + station_width//2, station_y + 15))
            self.screen.blit(label_text, label_rect)
            
            # Indicateur de statut (LED)
            led_x = station_x + station_width - 15
            led_y = station_y + 10
            pygame.draw.circle(self.screen, status_color, (led_x, led_y), 5)
            pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y), 5, 1)
            
            # Quantité disponible
            if is_available:
                qty_text = self.font_small.render(f"{len(available_ingredients)}", True, (40, 120, 40))
                self.screen.blit(qty_text, (led_x - 10, led_y + 15))

    def draw_work_station(self, asset_manager):
        """Station de travail pour la préparation"""
        # Plan de travail principal
        work_rect = pygame.Rect(self.work_area['x'], self.work_area['y'], 
                               self.work_area['w'], self.work_area['h'])
        draw_gradient_rect(self.screen, (200, 160, 120), (180, 140, 100), work_rect)
        pygame.draw.rect(self.screen, (120, 80, 40), work_rect, 3)
        
        # Zone de découpe
        cutting_x = self.work_area['x'] + 20
        cutting_y = self.work_area['y'] + 20
        cutting_w = 100
        cutting_h = 80
        
        cutting_rect = pygame.Rect(cutting_x, cutting_y, cutting_w, cutting_h)
        draw_gradient_rect(self.screen, (220, 180, 140), (200, 160, 120), cutting_rect)
        pygame.draw.rect(self.screen, (140, 100, 60), cutting_rect, 2)
        
        # Marques d'utilisation sur la planche
        for i in range(4):
            line_x = cutting_x + 15 + i * 18
            pygame.draw.line(self.screen, (160, 120, 80), 
                           (line_x, cutting_y + 15), (line_x, cutting_y + 65), 1)
        
        # Zone des ingrédients préparés
        self.draw_prepared_area(asset_manager)
        
        # Position de découpe pour le bot
        self.cutting_position = (cutting_x + cutting_w//2, cutting_y + cutting_h//2)

    def draw_prepared_area(self, asset_manager):
        """Zone d'affichage des ingrédients préparés"""
        import game_state
        current_time = time.time()
        
        # Zone des préparés à droite du plan de travail
        prepared_x = self.work_area['x'] + 140
        prepared_y = self.work_area['y'] + 20
        prepared_w = 100
        prepared_h = 80
        
        prepared_rect = pygame.Rect(prepared_x, prepared_y, prepared_w, prepared_h)
        pygame.draw.rect(self.screen, (250, 250, 250), prepared_rect)
        pygame.draw.rect(self.screen, (150, 150, 150), prepared_rect, 2)
        
        # Titre
        title = self.font_small.render("Préparés", True, (100, 100, 100))
        self.screen.blit(title, (prepared_x + 5, prepared_y - 18))
        
        # Afficher les ingrédients préparés
        for idx, ingredient in enumerate(game_state.prepared_ingredients):
            if idx >= 8:  # Limite d'affichage
                break
                
            pos_x = prepared_x + 15 + (idx % 4) * 20
            pos_y = prepared_y + 15 + (idx // 4) * 25
            
            # Animation
            float_offset = math.sin(current_time * 4 + idx) * 1
            
            # Couleur de l'ingrédient
            ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
            
            try:
                if asset_manager:
                    img = asset_manager.get_ingredient_image(ingredient)
                    if img:
                        scaled_img = pygame.transform.scale(img, (16, 16))
                        self.screen.blit(scaled_img, (pos_x - 8, pos_y - 8 + float_offset))
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                         (pos_x, int(pos_y + float_offset)), 7)
                else:
                    pygame.draw.circle(self.screen, ing_config["color"], 
                                     (pos_x, int(pos_y + float_offset)), 7)
            except:
                pygame.draw.circle(self.screen, ing_config["color"], 
                                 (pos_x, int(pos_y + float_offset)), 7)
            
            # Marque de validation
            pygame.draw.circle(self.screen, (50, 200, 50), (pos_x + 8, pos_y - 8), 3)

    def draw_service_station(self):
        """Station de service sans texte"""
        # Comptoir de service
        service_rect = pygame.Rect(self.service_area['x'], self.service_area['y'], 
                                  self.service_area['w'], self.service_area['h'])
        
        # Effet lumineux
        glow_intensity = int(20 + 10 * math.sin(time.time() * 2))
        for i in range(3, 0, -1):
            alpha = glow_intensity // i
            glow_surf = pygame.Surface((self.service_area['w'] + i*4, 
                                      self.service_area['h'] + i*4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 215, 0, alpha), 
                           (0, 0, self.service_area['w'] + i*4, self.service_area['h'] + i*4))
            self.screen.blit(glow_surf, (self.service_area['x'] - i*2, self.service_area['y'] - i*2))
        
        draw_gradient_rect(self.screen, (255, 200, 100), (220, 160, 60), service_rect)
        pygame.draw.rect(self.screen, (200, 150, 50), service_rect, 3)
        
        # Plateaux de service
        for i in range(3):
            plate_y = self.service_area['y'] + 40 + i * 80
            plate_x = self.service_area['x'] + self.service_area['w']//2
            
            # Plateau
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_x, plate_y), 25)
            pygame.draw.circle(self.screen, (220, 220, 220), (plate_x, plate_y), 20)
            pygame.draw.circle(self.screen, (180, 180, 180), (plate_x, plate_y), 25, 2)

    def draw_bot_enhanced(self, bot, asset_manager):
        """Bot avec animations améliorées"""
        base_x, base_y = bot.x, bot.y
        current_time = time.time()
        
        # Animation selon l'état
        if bot.state == "cutting" and bot.preparing:
            # Vibration pendant la découpe
            shake = math.sin(current_time * 25) * 1.5
            base_x += shake
            base_y += shake * 0.5
            
            # Couteau animé
            if hasattr(self, 'cutting_position'):
                knife_x, knife_y = self.cutting_position
                knife_movement = math.sin(current_time * 12) * 8
                
                # Dessiner le couteau
                knife_color = (200, 200, 200)
                knife_handle = (160, 120, 80)
                
                # Lame
                pygame.draw.line(self.screen, knife_color, 
                               (knife_x - 3, knife_y - 15 + knife_movement), 
                               (knife_x + 3, knife_y + 5 + knife_movement), 4)
                # Manche
                pygame.draw.circle(self.screen, knife_handle, 
                                 (knife_x, knife_y + 10 + knife_movement), 8)
                
                # Particules
                if int(current_time * 20) % 4 == 0:
                    for _ in range(3):
                        px = knife_x + (hash(str(current_time)) % 20) - 10
                        py = knife_y + (hash(str(current_time*3)) % 15) - 5
                        pygame.draw.circle(self.screen, (255, 255, 150), (px, py), 1)
        
        # Animation de marche
        elif bot.state in ["going_to_fridge", "going_to_board", "going_to_delivery"]:
            walk_cycle = math.sin(bot.animation_time * 8) * 3
            base_y -= abs(walk_cycle)
        
        # Dessiner le bot
        bot_size = 35
        try:
            if asset_manager:
                bot_img = asset_manager.get_player_image()
                if bot_img:
                    self.screen.blit(bot_img, (int(base_x - bot_size//2), int(base_y - bot_size//2)))
                else:
                    pygame.draw.circle(self.screen, (100, 150, 255), 
                                     (int(base_x), int(base_y)), bot_size//2)
            else:
                pygame.draw.circle(self.screen, (100, 150, 255), 
                                 (int(base_x), int(base_y)), bot_size//2)
        except:
            pygame.draw.circle(self.screen, (100, 150, 255), 
                             (int(base_x), int(base_y)), bot_size//2)
        
        # Ingrédient transporté
        if bot.inv:
            carry_x = base_x + 25 + math.sin(bot.animation_time * 5) * 2
            carry_y = base_y - 35 + math.sin(bot.animation_time * 7) * 1
            
            ing_config = self.ingredient_config.get(bot.inv, {"color": (150, 150, 150)})
            
            # Aura autour de l'ingrédient
            aura_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(aura_surf, (*ing_config["color"], 60), (20, 20), 18)
            self.screen.blit(aura_surf, (carry_x - 20, carry_y - 20))
            
            # Ingrédient
            try:
                if asset_manager:
                    ing_img = asset_manager.get_ingredient_image(bot.inv)
                    if ing_img:
                        scaled = pygame.transform.scale(ing_img, (20, 20))
                        self.screen.blit(scaled, (carry_x - 10, carry_y - 10))
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                         (int(carry_x), int(carry_y)), 10)
                else:
                    pygame.draw.circle(self.screen, ing_config["color"], 
                                     (int(carry_x), int(carry_y)), 10)
            except:
                pygame.draw.circle(self.screen, ing_config["color"], 
                                 (int(carry_x), int(carry_y)), 10)
        
        # Indicateur d'état du bot
        state_color = bot.get_state_color()
        pygame.draw.circle(self.screen, state_color, (int(bot.x), int(bot.y - 45)), 6)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(bot.x), int(bot.y - 45)), 6, 1)

    def get_interaction_zones(self):
        """Zones d'interaction pour le bot"""
        return {
            'fridge_access': (self.storage_area['floor_x'] + 150, self.storage_area['floor_y'] + 40),
            'cutting_board': (self.work_area['floor_x'] + 70, self.work_area['floor_y'] + 50),
            'delivery': (self.service_area['floor_x'] + 50, self.service_area['floor_y'] + 90)
        }

    def render_full_kitchen(self, bot, asset_manager, timer):
        """Rendu complet de la cuisine"""
        # Sol
        self.draw_floor()
        
        # Stations individuelles d'ingrédients
        self.draw_individual_ingredient_stations(asset_manager)
        
        # Station de travail
        self.draw_work_station(asset_manager)
        
        # Station de service
        self.draw_service_station()
        
        # Mettre à jour les zones d'interaction
        bot.update_interaction_zones(self.get_interaction_zones())
        
        # Bot avec animations
        self.draw_bot_enhanced(bot, asset_manager)