"""
Kitchen rendering - Vue cuisine avec bacs individuels pour chaque ingrédient et système d'assiettes
Adapté pour le bot-chef cuisinier
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
        """Configure la disposition de la cuisine - Layout côte à côte"""
        # Zone de stockage avec bacs individuels (gauche) - plus petite
        self.storage_area = {
            'x': 30, 'y': 100, 'w': 280, 'h': 320,
            'floor_x': 30, 'floor_y': 420, 'floor_w': 280, 'floor_h': 80
        }
        
        # Plan de travail (centre-gauche) - côte à côte avec assemblage
        self.work_area = {
            'x': 350, 'y': 120, 'w': 200, 'h': 140,
            'floor_x': 350, 'floor_y': 260, 'floor_w': 200, 'floor_h': 80
        }
        
        # Zone d'assemblage avec assiettes (centre-droite) - côte à côte avec travail
        self.plating_area = {
            'x': 570, 'y': 120, 'w': 200, 'h': 140,
            'floor_x': 570, 'floor_y': 260, 'floor_w': 200, 'floor_h': 80
        }
        
        # Zone de service (droite)
        self.service_area = {
            'x': 790, 'y': 120, 'w': 120, 'h': 300,
            'floor_x': 720, 'floor_y': 240, 'floor_w': 100, 'floor_h': 180
        }
        
        # Zone centrale de circulation élargie
        self.circulation = {
            'x': 320, 'y': 450, 'w': 450, 'h': 100
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
            (self.plating_area['floor_x'], self.plating_area['floor_y'], 
             self.plating_area['floor_w'], self.plating_area['floor_h']),
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
        """Dessine des stations individuelles pour chaque type d'ingrédient - version dézoomée"""
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
        
        # Organiser en grille 3x3 mais avec des stations plus petites (dézoomé)
        cols = 3
        station_width = 70  # Réduit de 80 à 70
        station_height = 75  # Réduit de 90 à 75
        margin_x = 15  # Réduit de 20 à 15
        margin_y = 15  # Réduit de 20 à 15
        
        for i, ingredient_type in enumerate(ingredient_types):
            col = i % cols
            row = i // cols
            
            station_x = self.storage_area['x'] + margin_x + col * (station_width + 12)  # Espacement réduit
            station_y = self.storage_area['y'] + margin_y + row * (station_height + 12)  # Espacement réduit
            
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
            
            # Zone de stockage dans la station - plus petite
            storage_rect = pygame.Rect(station_x + 8, station_y + 25, 54, 35)  # Tailles réduites
            pygame.draw.rect(self.screen, ing_config["color"], storage_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), storage_rect, 1)
            
            # Ingrédients disponibles dans la station
            if is_available:
                for j, ing in enumerate(available_ingredients[:4]):  # Max 4 ingrédients affichés
                    # Position de l'ingrédient pour interaction
                    ing_x = storage_rect.x + 13 + (j % 2) * 22  # Espacement ajusté
                    ing_y = storage_rect.y + 8 + (j // 2) * 18  # Espacement ajusté
                    
                    # Mise à jour position pour le bot
                    ing["x"] = ing_x
                    ing["y"] = ing_y
                    
                    # Animation de flottement
                    float_y = ing_y + math.sin(current_time * 3 + j) * 1
                    
                    try:
                        if asset_manager:
                            img = asset_manager.get_ingredient_image(ingredient_type)
                            if img:
                                scaled_img = pygame.transform.scale(img, (16, 16))  # Taille réduite
                                self.screen.blit(scaled_img, (ing_x - 8, float_y - 8))
                            else:
                                pygame.draw.circle(self.screen, ing_config["color"], 
                                                 (ing_x, int(float_y)), 7)  # Rayon réduit
                        else:
                            pygame.draw.circle(self.screen, ing_config["color"], 
                                             (ing_x, int(float_y)), 7)  # Rayon réduit
                    except:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                         (ing_x, int(float_y)), 7)  # Rayon réduit
            
            # Étiquette de l'ingrédient
            label_text = self.font_small.render(ingredient_type.capitalize(), True, (60, 60, 60))
            label_rect = label_text.get_rect(center=(station_x + station_width//2, station_y + 12))
            self.screen.blit(label_text, label_rect)
            
            # Indicateur de statut (LED) - plus petit
            led_x = station_x + station_width - 12
            led_y = station_y + 8
            pygame.draw.circle(self.screen, status_color, (led_x, led_y), 4)  # Rayon réduit
            pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y), 4, 1)
            
            # Quantité disponible
            if is_available:
                qty_text = self.font_small.render(f"{len(available_ingredients)}", True, (40, 120, 40))
                self.screen.blit(qty_text, (led_x - 8, led_y + 12))

    def draw_work_station(self, asset_manager):
        """Station de travail pour la préparation"""
        # Plan de travail principal
        work_rect = pygame.Rect(self.work_area['x'], self.work_area['y'], 
                               self.work_area['w'], self.work_area['h'])
        draw_gradient_rect(self.screen, (200, 160, 120), (180, 140, 100), work_rect)
        pygame.draw.rect(self.screen, (120, 80, 40), work_rect, 3)
        
        # Titre de la station
        title = self.font_small.render("Plan de Travail", True, (80, 60, 40))
        self.screen.blit(title, (self.work_area['x'] + 10, self.work_area['y'] - 18))
        
        # Zone de découpe
        cutting_x = self.work_area['x'] + 15
        cutting_y = self.work_area['y'] + 20
        cutting_w = 80
        cutting_h = 70
        
        cutting_rect = pygame.Rect(cutting_x, cutting_y, cutting_w, cutting_h)
        draw_gradient_rect(self.screen, (220, 180, 140), (200, 160, 120), cutting_rect)
        pygame.draw.rect(self.screen, (140, 100, 60), cutting_rect, 2)
        
        # Marques d'utilisation sur la planche
        for i in range(4):
            line_x = cutting_x + 12 + i * 15
            pygame.draw.line(self.screen, (160, 120, 80), 
                           (line_x, cutting_y + 12), (line_x, cutting_y + 58), 1)
        
        # Zone des ingrédients préparés
        self.draw_prepared_area(asset_manager)
        
        # Position de découpe pour le bot
        self.cutting_position = (cutting_x + cutting_w//2, cutting_y + cutting_h//2)

    def draw_prepared_area(self, asset_manager):
        """Zone d'affichage des ingrédients préparés"""
        import game_state
        current_time = time.time()
        
        # Zone des préparés à droite du plan de travail
        prepared_x = self.work_area['x'] + 105
        prepared_y = self.work_area['y'] + 20
        prepared_w = 80
        prepared_h = 70
        
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
                
            pos_x = prepared_x + 12 + (idx % 4) * 18
            pos_y = prepared_y + 12 + (idx // 4) * 22
            
            # Animation
            float_offset = math.sin(current_time * 4 + idx) * 1
            
            # Couleur de l'ingrédient
            ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
            
            try:
                if asset_manager:
                    img = asset_manager.get_ingredient_image(ingredient)
                    if img:
                        scaled_img = pygame.transform.scale(img, (14, 14))
                        self.screen.blit(scaled_img, (pos_x - 7, pos_y - 7 + float_offset))
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                         (pos_x, int(pos_y + float_offset)), 6)
                else:
                    pygame.draw.circle(self.screen, ing_config["color"], 
                                     (pos_x, int(pos_y + float_offset)), 6)
            except:
                pygame.draw.circle(self.screen, ing_config["color"], 
                                 (pos_x, int(pos_y + float_offset)), 6)
            
            # Marque de validation
            pygame.draw.circle(self.screen, (50, 200, 50), (pos_x + 6, pos_y - 6), 2)

    def draw_plating_station(self, asset_manager):
        """Station d'assemblage avec assiettes - côte à côte avec le plan de travail"""
        import game_state
        current_time = time.time()
        
        # Plan d'assemblage
        plating_rect = pygame.Rect(self.plating_area['x'], self.plating_area['y'], 
                                  self.plating_area['w'], self.plating_area['h'])
        draw_gradient_rect(self.screen, (240, 230, 220), (220, 210, 200), plating_rect)
        pygame.draw.rect(self.screen, (180, 150, 120), plating_rect, 3)
        
        # Titre de la station
        title = self.font_small.render("Station d'Assemblage", True, (80, 70, 60))
        self.screen.blit(title, (self.plating_area['x'] + 10, self.plating_area['y'] - 18))
        
        # Zone des assiettes vides (gauche)
        empty_plates_x = self.plating_area['x'] + 15
        empty_plates_y = self.plating_area['y'] + 20
        empty_plates_w = 60
        empty_plates_h = 70
        
        empty_rect = pygame.Rect(empty_plates_x, empty_plates_y, empty_plates_w, empty_plates_h)
        pygame.draw.rect(self.screen, (255, 255, 255), empty_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), empty_rect, 2)
        
        # Assiettes empilées
        for i in range(3):
            plate_y = empty_plates_y + 12 + i * 3
            plate_x = empty_plates_x + empty_plates_w//2
            
            # Assiette vide avec ombre
            pygame.draw.circle(self.screen, (220, 220, 220), (plate_x + 1, plate_y + 1), 15)
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_x, plate_y), 15)
            pygame.draw.circle(self.screen, (200, 200, 200), (plate_x, plate_y), 15, 1)
            pygame.draw.circle(self.screen, (240, 240, 240), (plate_x, plate_y), 10)
        
        # Zone d'assemblage du plat (centre)
        assembly_x = self.plating_area['x'] + 85
        assembly_y = self.plating_area['y'] + 20
        assembly_w = 70
        assembly_h = 70
        
        assembly_rect = pygame.Rect(assembly_x, assembly_y, assembly_w, assembly_h)
        
        # Vérifier s'il y a un plat en cours d'assemblage
        if hasattr(game_state, 'plated_dish') and game_state.plated_dish:
            # Assiette avec plat assemblé
            pygame.draw.rect(self.screen, (250, 250, 200), assembly_rect)
            pygame.draw.rect(self.screen, (200, 180, 100), assembly_rect, 2)
            
            # Assiette de base
            plate_center_x = assembly_x + assembly_w//2
            plate_center_y = assembly_y + assembly_h//2
            
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_center_x, plate_center_y), 22)
            pygame.draw.circle(self.screen, (240, 240, 240), (plate_center_x, plate_center_y), 18)
            pygame.draw.circle(self.screen, (200, 200, 200), (plate_center_x, plate_center_y), 22, 2)
            
            # Ingrédients sur l'assiette
            dish_name = game_state.plated_dish
            for idx, ingredient in enumerate(game_state.prepared_ingredients):
                angle = (idx * 2 * math.pi) / max(1, len(game_state.prepared_ingredients))
                radius = 10
                ing_x = plate_center_x + math.cos(angle) * radius
                ing_y = plate_center_y + math.sin(angle) * radius
                
                # Animation de rotation lente
                rotation = current_time * 0.5 + idx
                final_x = ing_x + math.cos(rotation) * 1.5
                final_y = ing_y + math.sin(rotation) * 1.5
                
                ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
                
                try:
                    if asset_manager:
                        img = asset_manager.get_ingredient_image(ingredient)
                        if img:
                            scaled_img = pygame.transform.scale(img, (10, 10))
                            self.screen.blit(scaled_img, (final_x - 5, final_y - 5))
                        else:
                            pygame.draw.circle(self.screen, ing_config["color"], 
                                             (int(final_x), int(final_y)), 4)
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                         (int(final_x), int(final_y)), 4)
                except:
                    pygame.draw.circle(self.screen, ing_config["color"], 
                                     (int(final_x), int(final_y)), 4)
            
            # Effet de brillance sur le plat fini
            glow = math.sin(current_time * 3) * 8 + 12
            glow_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 150, int(glow)), (25, 25), 24)
            self.screen.blit(glow_surf, (plate_center_x - 25, plate_center_y - 25))
            
        else:
            # Zone d'assemblage vide
            pygame.draw.rect(self.screen, (245, 245, 245), assembly_rect)
            pygame.draw.rect(self.screen, (180, 180, 180), assembly_rect, 2)
            
            # Indicateur "Prêt à assembler"
            if game_state.prepared_ingredients:
                ready_text = self.font_small.render("Prêt", True, (100, 200, 100))
                text_rect = ready_text.get_rect(center=(assembly_x + assembly_w//2, assembly_y + assembly_h//2))
                self.screen.blit(ready_text, text_rect)
        
        # Zone de plats finis (droite) - plus petite
        finished_x = self.plating_area['x'] + 165
        finished_y = self.plating_area['y'] + 20
        finished_w = 30
        finished_h = 70
        
        finished_rect = pygame.Rect(finished_x, finished_y, finished_w, finished_h)
        pygame.draw.rect(self.screen, (200, 255, 200), finished_rect)
        pygame.draw.rect(self.screen, (150, 200, 150), finished_rect, 2)
        
        # Position pour l'assemblage
        self.plating_position = (assembly_x + assembly_w//2, assembly_y + assembly_h//2)

    def draw_service_station(self):
        """Station de service pour la livraison finale"""
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
        
        # Titre
        title = self.font_small.render("Service", True, (120, 80, 30))
        self.screen.blit(title, (self.service_area['x'] + 10, self.service_area['y'] - 18))
        
        # Zone de livraison avec plateaux
        for i in range(2):
            tray_y = self.service_area['y'] + 60 + i * 90
            tray_x = self.service_area['x'] + self.service_area['w']//2
            
            # Plateau de service
            pygame.draw.circle(self.screen, (255, 255, 255), (tray_x, tray_y), 25)
            pygame.draw.circle(self.screen, (220, 220, 220), (tray_x, tray_y), 20)
            pygame.draw.circle(self.screen, (180, 180, 180), (tray_x, tray_y), 25, 2)

    def draw_chef_enhanced(self, bot, asset_manager):
        """Chef avec animations améliorées spécifiques à son apparence"""
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
        
        # Animation d'assemblage
        elif bot.state == "plating" and hasattr(bot, 'plating') and bot.plating:
            # Animation de mélange/assemblage
            mix_movement = math.sin(current_time * 10) * 3
            base_x += mix_movement
            
            # Spatule animée
            if hasattr(self, 'plating_position'):
                spatula_x, spatula_y = self.plating_position
                spatula_angle = math.sin(current_time * 8) * 0.5
                
                # Dessiner la spatule
                spatula_color = (180, 180, 180)
                pygame.draw.line(self.screen, spatula_color,
                               (spatula_x, spatula_y - 20),
                               (spatula_x + math.cos(spatula_angle) * 15, 
                                spatula_y + math.sin(spatula_angle) * 15), 3)
        
        # Animation de marche
        elif bot.state in ["going_to_fridge", "going_to_board", "going_to_plating", "going_to_delivery"]:
            walk_cycle = math.sin(bot.animation_time * 8) * 3
            base_y -= abs(walk_cycle)
        
        # Utiliser la méthode draw_chef du bot au lieu de dessiner un cercle
        # Sauvegarder position actuelle et temporairement modifier pour l'animation
        original_x, original_y = bot.x, bot.y
        bot.x, bot.y = base_x, base_y
        bot.draw_chef(self.screen)  # Utilise la méthode du chef
        bot.x, bot.y = original_x, original_y
        
        # Indicateur d'état du bot au-dessus de la toque
        state_color = bot.get_state_color()
        pygame.draw.circle(self.screen, state_color, (int(base_x), int(base_y - 55)), 6)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(base_x), int(base_y - 55)), 6, 1)
        
        # Affichage du nom du chef et de son état
        chef_info = f"{bot.chef_name}: {bot.get_state_text()}"
        info_text = self.font_small.render(chef_info, True, (60, 60, 60))
        info_rect = info_text.get_rect(center=(int(base_x), int(base_y - 70)))
        
        # Fond semi-transparent pour le texte
        text_bg = pygame.Surface((info_rect.width + 8, info_rect.height + 4), pygame.SRCALPHA)
        text_bg.fill((255, 255, 255, 180))
        self.screen.blit(text_bg, (info_rect.x - 4, info_rect.y - 2))
        self.screen.blit(info_text, info_rect)

    def get_interaction_zones(self):
        """Zones d'interaction pour le bot"""
        return {
            'fridge_access': (self.storage_area['floor_x'] + 140, self.storage_area['floor_y'] + 40),
            'cutting_board': (self.work_area['floor_x'] + 60, self.work_area['floor_y'] + 40),
            'plating_station': (self.plating_area['floor_x'] + 100, self.plating_area['floor_y'] + 40),
            'delivery': (self.service_area['floor_x'] + 50, self.service_area['floor_y'] + 90)
        }

    def render_full_kitchen(self, bot, asset_manager, timer):
        """Rendu complet de la cuisine avec le chef cuisinier"""
        # Sol
        self.draw_floor()
        
        # Stations individuelles d'ingrédients
        self.draw_individual_ingredient_stations(asset_manager)
        
        # Station de travail
        self.draw_work_station(asset_manager)
        
        # Station d'assemblage avec assiettes
        self.draw_plating_station(asset_manager)
        
        # Station de service
        self.draw_service_station()
        
        # Mettre à jour les zones d'interaction pour le chef
        bot.update_interaction_zones(self.get_interaction_zones())
        
        # Chef avec animations spécifiques
        self.draw_chef_enhanced(bot, asset_manager)
        
        # Affichage des informations du chef en bas
        self.draw_chef_status(bot)
    
    def draw_chef_status(self, bot):
        """Affiche le statut détaillé du chef"""
        import game_state
        
        # Zone d'information du chef
        status_y = HEIGHT - 60
        status_rect = pygame.Rect(10, status_y, WIDTH - 20, 50)
        
        # Fond avec transparence
        status_bg = pygame.Surface((status_rect.width, status_rect.height), pygame.SRCALPHA)
        status_bg.fill((30, 30, 30, 200))
        self.screen.blit(status_bg, status_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), status_rect, 2)
        
        # Informations du chef
        info_lines = [
            f"👨‍🍳 {bot.chef_name} | État: {bot.get_state_text()}",
            f"📍 Position: ({int(bot.x)}, {int(bot.y)}) | Cible: ({int(bot.target_x)}, {int(bot.target_y)})",
        ]
        
        # Informations sur la commande en cours
        if game_state.current_order_name:
            order_info = f"🍽️ Commande: {game_state.current_order_name}"
            if game_state.prepared_ingredients:
                order_info += f" | Préparés: {', '.join(game_state.prepared_ingredients)}"
            if hasattr(game_state, 'plated_dish') and game_state.plated_dish:
                order_info += f" | Plat dressé: {game_state.plated_dish}"
            info_lines.append(order_info)
        
        # Informations sur l'inventaire
        if bot.inv:
            if bot.inv == "plated_dish":
                info_lines.append(f"🍽️ Transporte: Plat dressé prêt à servir")
            else:
                info_lines.append(f"🥕 Transporte: {bot.inv}")
        
        if bot.preparing:
            prep_time_left = bot.prep_times.get(bot.preparing, 1.5) - (time.time() - bot.prep_time)
            info_lines.append(f"🔪 Prépare: {bot.preparing} (encore {prep_time_left:.1f}s)")
        
        if bot.plating:
            plate_time_left = bot.PLATING_TIME - (time.time() - bot.plate_time)
            info_lines.append(f"🍽️ Assemble le plat (encore {plate_time_left:.1f}s)")
        
        # Affichage du texte
        for i, line in enumerate(info_lines):
            if i < 3:  # Limite à 3 lignes pour éviter le débordement
                text = self.font_small.render(line, True, (255, 255, 255))
                self.screen.blit(text, (status_rect.x + 10, status_rect.y + 5 + i * 15))