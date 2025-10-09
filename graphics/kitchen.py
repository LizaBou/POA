# kitchen.py

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
        self.storage_area = {'x': 30, 'y': 100, 'w': 280, 'h': 320, 'floor_x': 30, 'floor_y': 420, 'floor_w': 280, 'floor_h': 80}
        self.work_area = {'x': 350, 'y': 120, 'w': 200, 'h': 140, 'floor_x': 350, 'floor_y': 260, 'floor_w': 200, 'floor_h': 80}
        self.plating_area = {'x': 570, 'y': 120, 'w': 200, 'h': 140, 'floor_x': 570, 'floor_y': 260, 'floor_w': 200, 'floor_h': 80}
        self.service_area = {'x': 790, 'y': 120, 'w': 120, 'h': 300, 'floor_x': 720, 'floor_y': 240, 'floor_w': 100, 'floor_h': 180}
        self.circulation = {'x': 320, 'y': 450, 'w': 450, 'h': 100}

    def draw_floor(self):
        tile_size = 50
        brown_light = (181, 101, 29)
        brown_dark = (130, 71, 22)
        for x in range(0, WIDTH, tile_size):
            for y in range(0, HEIGHT, tile_size):
                color = brown_light if (x // tile_size + y // tile_size) % 2 == 0 else brown_dark
                tile_rect = pygame.Rect(x, y, tile_size, tile_size)
                pygame.draw.rect(self.screen, color, tile_rect)
                pygame.draw.line(self.screen, (160, 90, 25), (x, y), (x + tile_size, y), 1)
                pygame.draw.line(self.screen, (160, 90, 25), (x, y), (x, y + tile_size), 1)
                pygame.draw.line(self.screen, (110, 60, 15), (x + tile_size, y), (x + tile_size, y + tile_size), 1)
                pygame.draw.line(self.screen, (110, 60, 15), (x, y + tile_size), (x + tile_size, y + tile_size), 1)
        for x, y, w, h in [
            (self.storage_area['floor_x'], self.storage_area['floor_y'], self.storage_area['floor_w'], self.storage_area['floor_h']),
            (self.work_area['floor_x'], self.work_area['floor_y'], self.work_area['floor_w'], self.work_area['floor_h']),
            (self.plating_area['floor_x'], self.plating_area['floor_y'], self.plating_area['floor_w'], self.plating_area['floor_h']),
            (self.service_area['floor_x'], self.service_area['floor_y'], self.service_area['floor_w'], self.service_area['floor_h']),
            (self.circulation['x'], self.circulation['y'], self.circulation['w'], self.circulation['h'])
        ]:
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((190, 160, 100, 50))
            self.screen.blit(overlay, (x, y))
            pygame.draw.rect(self.screen, (150, 120, 70), (x, y, w, h), 1)

    def draw_individual_ingredient_stations(self, asset_manager):
        import game_state
        current_time = time.time()
        title_bg = pygame.Rect(self.storage_area['x'], self.storage_area['y'] - 35, self.storage_area['w'], 30)
        draw_gradient_rect(self.screen, (110, 70, 30), (90, 60, 20), title_bg)
        title = self.font_medium.render("STOCKAGE DES INGRÉDIENTS", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.storage_area['x'] + self.storage_area['w']//2, self.storage_area['y'] - 20))
        self.screen.blit(title, title_rect)
        ingredient_types = list(set(ing["type"] for ing in game_state.ingredients))
        if not ingredient_types:
            ingredient_types = ["laitue", "tomate", "pain", "steak", "fromage"]
        cols = 4
        station_width = 65
        station_height = 70
        margin_x = 10
        margin_y = 12

        self.ingredient_positions = {}

        for i, ingredient_type in enumerate(ingredient_types):
            col = i % cols
            row = i // cols
            station_x = self.storage_area['x'] + margin_x + col * (station_width + 18)
            station_y = self.storage_area['y'] + margin_y + row * (station_height + 18)
            self.ingredient_positions[ingredient_type] = (station_x + station_width//2, station_y + station_height//2)
            station_rect = pygame.Rect(station_x, station_y, station_width, station_height)

            shadow_surf = pygame.Surface((station_width + 2, station_height + 2), pygame.SRCALPHA)
            shadow_surf.fill((0, 0, 0, 40))
            self.screen.blit(shadow_surf, (station_x + 2, station_y + 2))

            available_ingredients = [ing for ing in game_state.ingredients if ing["type"] == ingredient_type and not ing["taken"] and current_time >= ing.get("spawn_time", 0)]
            is_available = len(available_ingredients) > 0

            if is_available:
                draw_gradient_rect(self.screen, (240, 220, 180), (210, 180, 140), station_rect)
                border_color = (130, 90, 40)
                status_color = (170, 130, 70)
                glow_intensity = int(20 + 15 * math.sin(current_time * 3))
            else:
                draw_gradient_rect(self.screen, (225, 210, 200), (195, 180, 170), station_rect)
                border_color = (140, 120, 110)
                status_color = (160, 140, 130)
                glow_intensity = 0

            pygame.draw.rect(self.screen, border_color, station_rect, 2)

            if glow_intensity > 0:
                glow_surf = pygame.Surface((station_width + 10, station_height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (180, 140, 70, glow_intensity), (0, 0, station_width + 10, station_height + 10), 3)
                self.screen.blit(glow_surf, (station_x - 5, station_y - 5))

            storage_inner = pygame.Rect(station_x + 7, station_y + 25, 52, 34)
            pygame.draw.rect(self.screen, self.ingredient_config.get(ingredient_type, {"color": (150, 150, 150)})["color"], storage_inner)
            pygame.draw.rect(self.screen, (100, 70, 30), storage_inner, 1)

            if is_available:
                for j, ing in enumerate(available_ingredients[:4]):
                    ing_x = storage_inner.x + 14 + (j % 2) * 20
                    ing_y = storage_inner.y + 9 + (j // 2) * 16
                    ing["x"] = ing_x
                    ing["y"] = ing_y
                    float_y = ing_y + math.sin(current_time * 3 + j) * 1.5
                    try:
                        if asset_manager:
                            img = asset_manager.get_ingredient_image(ingredient_type)
                            if img:
                                scaled_img = pygame.transform.scale(img, (16, 16))
                                self.screen.blit(scaled_img, (ing_x - 8, float_y - 8))
                            else:
                                pygame.draw.circle(self.screen, self.ingredient_config.get(ingredient_type, {"color": (150, 150, 150)})["color"], (ing_x, int(float_y)), 7)
                        else:
                            pygame.draw.circle(self.screen, self.ingredient_config.get(ingredient_type, {"color": (150, 150, 150)})["color"], (ing_x, int(float_y)), 7)
                    except:
                        pygame.draw.circle(self.screen, self.ingredient_config.get(ingredient_type, {"color": (150, 150, 150)})["color"], (ing_x, int(float_y)), 7)

            label_bg = pygame.Rect(station_x, station_y, station_width, 20)
            overlay = pygame.Surface((station_width, 20), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 160))
            self.screen.blit(overlay, (station_x, station_y))

            label_text = self.font_small.render(ingredient_type.capitalize(), True, (50, 40, 20))
            label_rect = label_text.get_rect(center=(station_x + station_width // 2, station_y + 10))
            self.screen.blit(label_text, label_rect)

            led_x = station_x + station_width - 12
            led_y = station_y + 8

            if is_available:
                halo_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.circle(halo_surf, (status_color[0], status_color[1], status_color[2], 40), (8, 8), 7)
                self.screen.blit(halo_surf, (led_x - 8, led_y - 8))
            pygame.draw.circle(self.screen, status_color, (led_x, led_y), 4)
            pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y), 4, 1)
            pygame.draw.circle(self.screen, (255, 255, 255), (led_x - 1, led_y - 1), 1)
            if is_available:
                qty = len(available_ingredients)
                badge_color = (110, 70, 30) if qty > 2 else (150, 115, 80)
                pygame.draw.circle(self.screen, badge_color, (led_x, led_y + 18), 8)
                pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y + 18), 8, 1)
                qty_text = self.font_small.render(str(qty), True, (255, 255, 255))
                qty_rect = qty_text.get_rect(center=(led_x, led_y + 18))
                self.screen.blit(qty_text, qty_rect)


    def draw_work_station(self, asset_manager):
        """Plan de travail marron avec texture bois améliorée"""
        shadow = pygame.Surface((self.work_area['w'] + 6, self.work_area['h'] + 6), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 40))
        self.screen.blit(shadow, (self.work_area['x'] + 3, self.work_area['y'] + 3))
        
        work_rect = pygame.Rect(self.work_area['x'], self.work_area['y'], 
                              self.work_area['w'], self.work_area['h'])
        draw_gradient_rect(self.screen, (150, 90, 40), (110, 70, 20), work_rect)
        pygame.draw.rect(self.screen, (90, 50, 10), work_rect, 3)
        
        title_bg = pygame.Rect(self.work_area['x'], self.work_area['y'] - 30, 
                              self.work_area['w'], 25)
        draw_gradient_rect(self.screen, (90, 50, 10), (70, 40, 10), title_bg)
        title = self.font_small.render("PLAN DE TRAVAIL", True, (255, 255, 255))
        self.screen.blit(title, (self.work_area['x'] + 10, self.work_area['y'] - 25))
        
        cutting_x = self.work_area['x'] + 15
        cutting_y = self.work_area['y'] + 20
        cutting_w = 80
        cutting_h = 70
        
        cutting_rect = pygame.Rect(cutting_x, cutting_y, cutting_w, cutting_h)
        draw_gradient_rect(self.screen, (190, 140, 80), (160, 110, 60), cutting_rect)
        pygame.draw.rect(self.screen, (110, 70, 30), cutting_rect, 2)
        
        for i in range(5):
            line_x = cutting_x + 10 + i * 14
            pygame.draw.line(self.screen, (140, 90, 40), 
                             (line_x, cutting_y + 10), (line_x, cutting_y + 60), 1)
            pygame.draw.line(self.screen, (160, 110, 50), 
                             (line_x + 1, cutting_y + 10), (line_x + 1, cutting_y + 60), 1)
        
        self.draw_prepared_area(asset_manager)
        
        self.cutting_position = (cutting_x + cutting_w//2, cutting_y + cutting_h//2)


    def draw_prepared_area(self, asset_manager):
        import game_state
        current_time = time.time()
        
        prepared_x = self.work_area['x'] + 105
        prepared_y = self.work_area['y'] + 20
        prepared_w = 80
        prepared_h = 70
        
        prepared_rect = pygame.Rect(prepared_x, prepared_y, prepared_w, prepared_h)
        
        draw_gradient_rect(self.screen, (250, 245, 230), (220, 215, 190), prepared_rect)
        pygame.draw.rect(self.screen, (140, 130, 100), prepared_rect, 2)
        
        title_overlay = pygame.Surface((prepared_w, 16), pygame.SRCALPHA)
        title_overlay.fill((130, 100, 70, 180))
        self.screen.blit(title_overlay, (prepared_x, prepared_y - 16))
        
        title = self.font_small.render("PRÉPARÉS", True, (255, 255, 255))
        self.screen.blit(title, (prepared_x + 5, prepared_y - 15))
        
        for idx, ingredient in enumerate(game_state.prepared_ingredients):
            if idx >= 8:
                break
                
            pos_x = prepared_x + 12 + (idx % 4) * 18
            pos_y = prepared_y + 12 + (idx // 4) * 22
            
            float_offset = math.sin(current_time * 4 + idx) * 1.5
            
            ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
            
            glow_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            glow_color = ing_config["color"]
            pygame.draw.circle(glow_surf, (glow_color[0], glow_color[1], glow_color[2], 40), 
                               (16, 16), 14)
            self.screen.blit(glow_surf, (pos_x - 16, pos_y - 16 + float_offset))
            
            try:
                if asset_manager:
                    img = asset_manager.get_ingredient_image(ingredient)
                    if img:
                        scaled_img = pygame.transform.scale(img, (28, 28))
                        self.screen.blit(scaled_img, (pos_x - 14, pos_y - 14 + float_offset))
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                           (pos_x, int(pos_y + float_offset)), 12)
                else:
                    pygame.draw.circle(self.screen, ing_config["color"], 
                                       (pos_x, int(pos_y + float_offset)), 12)
            except:
                pygame.draw.circle(self.screen, ing_config["color"], 
                                   (pos_x, int(pos_y + float_offset)), 12)
            
            check_x, check_y = pos_x + 10, pos_y - 10
            pygame.draw.circle(self.screen, (120, 90, 40), (check_x, check_y), 5)
            pygame.draw.circle(self.screen, (255, 255, 255), (check_x, check_y), 5, 1)
            pygame.draw.circle(self.screen, (180, 140, 70), (check_x, check_y), 3)


    def draw_plating_station(self, asset_manager):
        import game_state
        current_time = time.time()
        
        shadow = pygame.Surface((self.plating_area['w'] + 6, self.plating_area['h'] + 6), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 40))
        self.screen.blit(shadow, (self.plating_area['x'] + 3, self.plating_area['y'] + 3))
        
        plating_rect = pygame.Rect(self.plating_area['x'], self.plating_area['y'], 
                                  self.plating_area['w'], self.plating_area['h'])
        draw_gradient_rect(self.screen, (230, 210, 180), (190, 170, 150), plating_rect)
        pygame.draw.rect(self.screen, (160, 130, 100), plating_rect, 3)
        
        title_bg = pygame.Rect(self.plating_area['x'], self.plating_area['y'] - 30, 
                              self.plating_area['w'], 25)
        draw_gradient_rect(self.screen, (160, 130, 100), (140, 110, 80), title_bg)
        title = self.font_small.render("STATION D'ASSEMBLAGE", True, (255, 255, 255))
        self.screen.blit(title, (self.plating_area['x'] + 10, self.plating_area['y'] - 25))
        
        empty_plates_x = self.plating_area['x'] + 15
        empty_plates_y = self.plating_area['y'] + 20
        empty_plates_w = 60
        empty_plates_h = 70
        
        empty_rect = pygame.Rect(empty_plates_x, empty_plates_y, empty_plates_w, empty_plates_h)
        draw_gradient_rect(self.screen, (255, 255, 255), (245, 245, 230), empty_rect)
        pygame.draw.rect(self.screen, (200, 200, 180), empty_rect, 2)
        
        for i in range(3):
            plate_y = empty_plates_y + 15 + i * 4
            plate_x = empty_plates_x + empty_plates_w//2
            
            pygame.draw.circle(self.screen, (180, 180, 150), (plate_x + 2, plate_y + 2), 16)
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_x, plate_y), 16)
            pygame.draw.circle(self.screen, (240, 245, 220), (plate_x, plate_y), 12)
            pygame.draw.circle(self.screen, (200, 200, 160), (plate_x, plate_y), 16, 1)
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_x - 4, plate_y - 4), 4)
        
        assembly_x = self.plating_area['x'] + 85
        assembly_y = self.plating_area['y'] + 20
        assembly_w = 70
        assembly_h = 70
        
        assembly_rect = pygame.Rect(assembly_x, assembly_y, assembly_w, assembly_h)
        
        if hasattr(game_state, 'plated_dish') and game_state.plated_dish:
            draw_gradient_rect(self.screen, (255, 250, 220), (245, 235, 200), assembly_rect)
            pygame.draw.rect(self.screen, (220, 180, 100), assembly_rect, 2)
            
            plate_center_x = assembly_x + assembly_w//2
            plate_center_y = assembly_y + assembly_h//2
            
            pygame.draw.circle(self.screen, (255, 255, 255), (plate_center_x, plate_center_y), 24)
            pygame.draw.circle(self.screen, (245, 245, 230), (plate_center_x, plate_center_y), 20)
            pygame.draw.circle(self.screen, (200, 200, 180), (plate_center_x, plate_center_y), 24, 2)
            
            pygame.draw.circle(self.screen, (255, 255, 255), 
                               (plate_center_x - 6, plate_center_y - 6), 6)
            
            for idx, ingredient in enumerate(game_state.prepared_ingredients):
                angle = (idx * 2 * math.pi) / max(1, len(game_state.prepared_ingredients))
                radius = 14
                rotation = current_time * 0.5 + idx
                
                ing_x = plate_center_x + math.cos(angle) * radius + math.cos(rotation) * 1.5
                ing_y = plate_center_y + math.sin(angle) * radius + math.sin(rotation) * 1.5
                
                ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
                
                glow_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
                glow_color = ing_config["color"]
                pygame.draw.circle(glow_surf, (glow_color[0], glow_color[1], glow_color[2], 40), 
                                   (16, 16), 14)
                self.screen.blit(glow_surf, (ing_x - 16, ing_y - 16))
                
                try:
                    if asset_manager:
                        img = asset_manager.get_ingredient_image(ingredient)
                        if img:
                            scaled_img = pygame.transform.scale(img, (24, 24))
                            self.screen.blit(scaled_img, (ing_x - 12, ing_y - 12))
                        else:
                            pygame.draw.circle(self.screen, ing_config["color"], 
                                               (int(ing_x), int(ing_y)), 10)
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                           (int(ing_x), int(ing_y)), 10)
                except:
                    pygame.draw.circle(self.screen, ing_config["color"], 
                                       (int(ing_x), int(ing_y)), 10)
            
            glow = int(15 + 10 * math.sin(current_time * 3))
            glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 150, glow), (30, 30), 28)
            self.screen.blit(glow_surf, (plate_center_x - 30, plate_center_y - 30))
            
        else:
            draw_gradient_rect(self.screen, (250, 250, 250), (235, 235, 230), assembly_rect)
            pygame.draw.rect(self.screen, (180, 180, 180), assembly_rect, 2)
            
            if game_state.prepared_ingredients:
                ready_text = self.font_small.render("PRÊT", True, (100, 220, 100))
                text_rect = ready_text.get_rect(center=(assembly_x + assembly_w//2, 
                                                       assembly_y + assembly_h//2))
                
                pulse = int(20 + 15 * math.sin(current_time * 4))
                glow_surf = pygame.Surface((60, 30), pygame.SRCALPHA)
                glow_surf.fill((100, 255, 100, pulse))
                self.screen.blit(glow_surf, (text_rect.x - 10, text_rect.y - 5))
                
                self.screen.blit(ready_text, text_rect)
        
        self.plating_position = (assembly_x + assembly_w//2, assembly_y + assembly_h//2)


    def draw_service_station(self):
        service_rect = pygame.Rect(self.service_area['x'], self.service_area['y'], 
                                   self.service_area['w'], self.service_area['h'])
        
        shadow = pygame.Surface((self.service_area['w'] + 6, self.service_area['h'] + 6), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 50))
        self.screen.blit(shadow, (self.service_area['x'] + 3, self.service_area['y'] + 3))
        
        glow_intensity = int(25 + 15 * math.sin(time.time() * 2))
        for i in range(4, 0, -1):
            alpha = glow_intensity // i
            glow_surf = pygame.Surface((self.service_area['w'] + i*6, 
                                        self.service_area['h'] + i*6), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 215, 0, alpha), 
                             (0, 0, self.service_area['w'] + i*6, self.service_area['h'] + i*6))
            self.screen.blit(glow_surf, (self.service_area['x'] - i*3, self.service_area['y'] - i*3))
        
        draw_gradient_rect(self.screen, (255, 210, 120), (230, 170, 80), service_rect)
        pygame.draw.rect(self.screen, (200, 150, 50), service_rect, 3)
        
        title_bg = pygame.Rect(self.service_area['x'], self.service_area['y'] - 30, 
                              self.service_area['w'], 25)
        draw_gradient_rect(self.screen, (200, 150, 50), (180, 130, 30), title_bg)
        title = self.font_small.render("SERVICE", True, (255, 255, 255))
        self.screen.blit(title, (self.service_area['x'] + 10, self.service_area['y'] - 25))
        
        for i in range(2):
            tray_y = self.service_area['y'] + 70 + i * 100
            tray_x = self.service_area['x'] + self.service_area['w']//2
            
            pygame.draw.circle(self.screen, (180, 180, 180), (tray_x + 2, tray_y + 2), 27)
            pygame.draw.circle(self.screen, (255, 255, 255), (tray_x, tray_y), 27)
            pygame.draw.circle(self.screen, (230, 230, 230), (tray_x, tray_y), 22)
            pygame.draw.circle(self.screen, (180, 180, 180), (tray_x, tray_y), 27, 2)
            
            pygame.draw.circle(self.screen, (255, 255, 255), (tray_x - 8, tray_y - 8), 6)
            pygame.draw.circle(self.screen, (240, 240, 240), (tray_x + 6, tray_y + 6), 4)


    def draw_chef_enhanced(self, bot, asset_manager):
        base_x, base_y = bot.x, bot.y
        current_time = time.time()
        
        if bot.state == "cutting" and bot.preparing:
            shake = math.sin(current_time * 25) * 1.5
            base_x += shake
            base_y += shake * 0.5
            
            if hasattr(self, 'cutting_position'):
                knife_x, knife_y = self.cutting_position
                knife_movement = math.sin(current_time * 12) * 8
                
                knife_color = (200, 200, 200)
                knife_handle = (160, 120, 80)
                
                pygame.draw.line(self.screen, knife_color, 
                                 (knife_x - 3, knife_y - 15 + knife_movement), 
                                 (knife_x + 3, knife_y + 5 + knife_movement), 4)
                pygame.draw.circle(self.screen, knife_handle, 
                                   (knife_x, knife_y + 10 + knife_movement), 8)
                
                if int(current_time * 20) % 4 == 0:
                    for _ in range(3):
                        px = knife_x + (hash(str(current_time)) % 20) - 10
                        py = knife_y + (hash(str(current_time*3)) % 15) - 5
                        pygame.draw.circle(self.screen, (255, 255, 150), (px, py), 1)
                
                if bot.preparing:
                    ing_config = self.ingredient_config.get(bot.preparing, {"color": (150, 150, 150)})
                    try:
                        if asset_manager:
                            img = asset_manager.get_ingredient_image(bot.preparing)
                            if img:
                                scaled_img = pygame.transform.scale(img, (50, 50))
                                self.screen.blit(scaled_img, (knife_x - 25, knife_y - 25))
                            else:
                                pygame.draw.circle(self.screen, ing_config["color"], 
                                                   (knife_x, knife_y), 22)
                        else:
                            pygame.draw.circle(self.screen, ing_config["color"], 
                                               (knife_x, knife_y), 22)
                    except:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                           (knife_x, knife_y), 22)
        
        elif bot.state == "plating" and hasattr(bot, 'plating') and bot.plating:
            mix_movement = math.sin(current_time * 10) * 3
            base_x += mix_movement
            
            if hasattr(self, 'plating_position'):
                spatula_x, spatula_y = self.plating_position
                spatula_angle = math.sin(current_time * 8) * 0.5
                
                pygame.draw.line(self.screen, (180, 180, 180),
                                 (spatula_x, spatula_y - 20),
                                 (spatula_x + math.cos(spatula_angle) * 15, 
                                  spatula_y + math.sin(spatula_angle) * 15), 3)
        
        elif bot.state in ["going_to_fridge", "going_to_board", "going_to_plating", "going_to_delivery"]:
            walk_cycle = math.sin(bot.animation_time * 8) * 3
            base_y -= abs(walk_cycle)
        
        original_x, original_y = bot.x, bot.y
        bot.x, bot.y = base_x, base_y
        bot.draw_chef(self.screen)
        bot.x, bot.y = original_x, original_y
        
        if bot.inv and bot.inv != "plated_dish":
            ing_config = self.ingredient_config.get(bot.inv, {"color": (150, 150, 150)})
            carry_x = base_x + 15
            carry_y = base_y - 25
            float_offset = math.sin(current_time * 5) * 2
            
            glow_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            glow_color = ing_config["color"]
            pygame.draw.circle(glow_surf, (glow_color[0], glow_color[1], glow_color[2], 50), 
                               (20, 20), 18)
            self.screen.blit(glow_surf, (carry_x - 20, carry_y - 20 + float_offset))
            
            try:
                if asset_manager:
                    img = asset_manager.get_ingredient_image(bot.inv)
                    if img:
                        scaled_img = pygame.transform.scale(img, (32, 32))
                        self.screen.blit(scaled_img, (carry_x - 16, carry_y - 16 + float_offset))
                    else:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                           (carry_x, int(carry_y + float_offset)), 14)
                else:
                    pygame.draw.circle(self.screen, ing_config["color"], 
                                       (carry_x, int(carry_y + float_offset)), 14)
            except:
                pygame.draw.circle(self.screen, ing_config["color"], 
                                   (carry_x, int(carry_y + float_offset)), 14)
        
        elif bot.inv == "plated_dish":
            import game_state
            
            carry_x = base_x + 20
            carry_y = base_y - 30
            float_offset = math.sin(current_time * 3) * 1.5
            
            pygame.draw.circle(self.screen, (255, 255, 255), 
                               (carry_x, int(carry_y + float_offset)), 20)
            pygame.draw.circle(self.screen, (240, 240, 240), 
                               (carry_x, int(carry_y + float_offset)), 16)
            pygame.draw.circle(self.screen, (200, 200, 200), 
                               (carry_x, int(carry_y + float_offset)), 20, 2)
            
            if hasattr(game_state, 'prepared_ingredients') and game_state.prepared_ingredients:
                for idx, ingredient in enumerate(game_state.prepared_ingredients):
                    angle = (idx * 2 * math.pi) / max(1, len(game_state.prepared_ingredients))
                    radius = 12
                    ing_x = carry_x + math.cos(angle) * radius
                    ing_y = carry_y + float_offset + math.sin(angle) * radius
                    
                    ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150)})
                    
                    try:
                        if asset_manager:
                            img = asset_manager.get_ingredient_image(ingredient)
                            if img:
                                scaled_img = pygame.transform.scale(img, (20, 20))
                                self.screen.blit(scaled_img, (ing_x - 10, ing_y - 10))
                            else:
                                pygame.draw.circle(self.screen, ing_config["color"], 
                                                   (int(ing_x), int(ing_y)), 8)
                        else:
                            pygame.draw.circle(self.screen, ing_config["color"], 
                                               (int(ing_x), int(ing_y)), 8)
                    except:
                        pygame.draw.circle(self.screen, ing_config["color"], 
                                           (int(ing_x), int(ing_y)), 8)
            
            glow = math.sin(current_time * 4) * 8 + 15
            glow_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 150, int(glow)), (25, 25), 22)
            self.screen.blit(glow_surf, (carry_x - 25, int(carry_y + float_offset) - 25))
        
        state_color = bot.get_state_color()
        pygame.draw.circle(self.screen, state_color, (int(base_x), int(base_y - 55)), 6)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(base_x), int(base_y - 55)), 6, 1)
        
        chef_info = f"{bot.chef_name}: {bot.get_state_text()}"
        info_text = self.font_small.render(chef_info, True, (60, 60, 60))
        info_rect = info_text.get_rect(center=(int(base_x), int(base_y - 70)))
        
        text_bg = pygame.Surface((info_rect.width + 8, info_rect.height + 4), pygame.SRCALPHA)
        text_bg.fill((255, 255, 255, 200))
        self.screen.blit(text_bg, (info_rect.x - 4, info_rect.y - 2))
        self.screen.blit(info_text, info_rect)


    def get_interaction_zones(self):
        return {
            'fridge_access': (self.storage_area['floor_x'] + 140, self.storage_area['floor_y'] + 40),
            'cutting_board': (self.work_area['floor_x'] + 60, self.work_area['floor_y'] + 40),
            'plating_station': (self.plating_area['floor_x'] + 100, self.plating_area['floor_y'] + 40),
            'delivery': (self.service_area['floor_x'] + 50, self.service_area['floor_y'] + 90)
        }


    def render_full_kitchen(self, bot, asset_manager, timer):
        self.draw_floor()
        self.draw_individual_ingredient_stations(asset_manager)
        
        self.draw_work_station(asset_manager)
        self.draw_plating_station(asset_manager)
        self.draw_service_station()
        
        bot.update_interaction_zones(self.get_interaction_zones())
        
        self.draw_chef_status(bot)
    
    def draw_chef_status(self, bot):
        import game_state
        
        status_y = HEIGHT - 60
        status_rect = pygame.Rect(10, status_y, WIDTH - 20, 50)
        
        status_bg = pygame.Surface((status_rect.width, status_rect.height), pygame.SRCALPHA)
        status_bg.fill((30, 30, 30, 220))
        self.screen.blit(status_bg, status_rect)
        pygame.draw.rect(self.screen, (100, 150, 200), status_rect, 2)
        
        info_lines = [
            f"👨‍🍳 {bot.chef_name} | État: {bot.get_state_text()}",
            f"📍 Position: ({int(bot.x)}, {int(bot.y)}) | Cible: ({int(bot.target_x)}, {int(bot.target_y)})",
        ]
        
        if game_state.current_order_name:
            order_info = f"🍽️ Commande: {game_state.current_order_name}"
            if game_state.prepared_ingredients:
                order_info += f" | Préparés: {', '.join(game_state.prepared_ingredients)}"
            if hasattr(game_state, 'plated_dish') and game_state.plated_dish:
                order_info += f" | Plat dressé: {game_state.plated_dish}"
            info_lines.append(order_info)
        
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
        
        for i, line in enumerate(info_lines):
            if i < 3:
                text = self.font_small.render(line, True, (255, 255, 255))
                self.screen.blit(text, (status_rect.x + 10, status_rect.y + 5 + i * 15))
