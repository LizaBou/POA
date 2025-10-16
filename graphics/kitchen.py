# kitchen.py - VERSION AVEC ANIMATION DE DÉCOUPE RÉALISTE

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

    def setup_kitchen_layout(self):
        self.storage_area = {'x': 40, 'y': 110, 'w': 280, 'h': 320}
        self.work_area = {'x': 350, 'y': 120, 'w': 200, 'h': 140}
        self.plating_area = {'x': 570, 'y': 120, 'w': 200, 'h': 140}
        self.service_area = {'x': 790, 'y': 120, 'w': 120, 'h': 300}

    def draw_floor(self):
        tile_size = 50
        floor_light = (210, 210, 210)
        floor_dark = (190, 190, 190)
        for x in range(0, WIDTH, tile_size):
            for y in range(0, HEIGHT, tile_size):
                color = floor_light if (x // tile_size + y // tile_size) % 2 == 0 else floor_dark
                pygame.draw.rect(self.screen, color, (x, y, tile_size, tile_size))
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x + tile_size, y), 1)
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x, y + tile_size), 1)

    def draw_individual_ingredient_stations(self, asset_manager):
        import game_state
        current_time = time.time()
        
        title_bg = pygame.Rect(self.storage_area['x'], self.storage_area['y'] - 30, self.storage_area['w'], 25)
        draw_gradient_rect(self.screen, (100, 100, 100), (80, 80, 80), title_bg)
        title = self.font_small.render("STOCKAGE DES INGRÉDIENTS", True, (255, 255, 255))
        self.screen.blit(title, (self.storage_area['x'] + 10, self.storage_area['y'] - 25))
        
        ingredient_types = list(set(ing["type"] for ing in game_state.ingredients))
        if not ingredient_types:
            ingredient_types = ["laitue", "tomate", "pain", "steak", "fromage"]
        
        cols = 3
        station_width = 85
        station_height = 70
        self.ingredient_positions = {}

        for i, ingredient_type in enumerate(ingredient_types):
            col = i % cols
            row = i // cols
            station_x = self.storage_area['x'] + 10 + col * (station_width + 10)
            station_y = self.storage_area['y'] + 15 + row * (station_height + 15)
            self.ingredient_positions[ingredient_type] = (station_x + station_width//2, station_y + station_height//2)
            
            station_rect = pygame.Rect(station_x, station_y, station_width, station_height)
            
            available_ingredients = [ing for ing in game_state.ingredients 
                                    if ing["type"] == ingredient_type and not ing["taken"] 
                                    and current_time >= ing.get("spawn_time", 0)]
            is_available = len(available_ingredients) > 0

            if is_available:
                draw_gradient_rect(self.screen, (250, 245, 235), (240, 230, 220), station_rect)
                border_color = (100, 150, 100)
                status_color = (100, 180, 100)
                glow = int(25 + 15 * math.sin(current_time * 3))
            else:
                draw_gradient_rect(self.screen, (235, 235, 235), (220, 220, 220), station_rect)
                border_color = (150, 150, 150)
                status_color = (170, 170, 170)
                glow = 0

            pygame.draw.rect(self.screen, border_color, station_rect, 2)

            if glow > 0:
                glow_surf = pygame.Surface((station_width + 10, station_height + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (100, 180, 100, glow), (0, 0, station_width + 10, station_height + 10), 3)
                self.screen.blit(glow_surf, (station_x - 5, station_y - 5))

            storage_inner = pygame.Rect(station_x + 7, station_y + 25, 72, 34)
            pygame.draw.rect(self.screen, self.ingredient_config[ingredient_type]["color"], storage_inner)
            pygame.draw.rect(self.screen, (80, 60, 40), storage_inner, 2)

            if is_available and asset_manager:
                for j, ing in enumerate(available_ingredients[:4]):
                    ing_x = storage_inner.x + 18 + (j % 2) * 25
                    ing_y = storage_inner.y + 9 + (j // 2) * 16
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

            label_overlay = pygame.Surface((station_width, 20), pygame.SRCALPHA)
            label_overlay.fill((80, 80, 80, 200))
            self.screen.blit(label_overlay, (station_x, station_y))
            label_text = self.font_small.render(ingredient_type.capitalize(), True, (255, 255, 255))
            self.screen.blit(label_text, (station_x + 10, station_y + 5))

            led_x = station_x + station_width - 12
            led_y = station_y + 8
            
            if is_available:
                halo_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.circle(halo_surf, (status_color[0], status_color[1], status_color[2], 60), (8, 8), 7)
                self.screen.blit(halo_surf, (led_x - 8, led_y - 8))
            pygame.draw.circle(self.screen, status_color, (led_x, led_y), 4)
            pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y), 4, 1)
            
            if is_available:
                qty = len(available_ingredients)
                badge_color = (50, 150, 50) if qty > 2 else (100, 180, 100)
                pygame.draw.circle(self.screen, badge_color, (led_x, led_y + 18), 8)
                pygame.draw.circle(self.screen, (255, 255, 255), (led_x, led_y + 18), 8, 1)
                qty_text = self.font_small.render(str(qty), True, (255, 255, 255))
                qty_rect = qty_text.get_rect(center=(led_x, led_y + 18))
                self.screen.blit(qty_text, qty_rect)

    def draw_work_station(self, asset_manager):
        work_rect = pygame.Rect(self.work_area['x'], self.work_area['y'], 
                              self.work_area['w'], self.work_area['h'])
        draw_gradient_rect(self.screen, (160, 110, 70), (140, 90, 60), work_rect)
        pygame.draw.rect(self.screen, (100, 70, 40), work_rect, 3)
        
        title_bg = pygame.Rect(self.work_area['x'], self.work_area['y'] - 30, 
                              self.work_area['w'], 25)
        draw_gradient_rect(self.screen, (100, 70, 40), (80, 60, 30), title_bg)
        title = self.font_small.render("PLAN DE TRAVAIL", True, (255, 255, 255))
        self.screen.blit(title, (self.work_area['x'] + 10, self.work_area['y'] - 25))
        
        cutting_x = self.work_area['x'] + 15
        cutting_y = self.work_area['y'] + 20
        cutting_w = 80
        cutting_h = 70
        
        cutting_rect = pygame.Rect(cutting_x, cutting_y, cutting_w, cutting_h)
        draw_gradient_rect(self.screen, (210, 160, 100), (180, 130, 80), cutting_rect)
        pygame.draw.rect(self.screen, (120, 80, 40), cutting_rect, 2)
        
        for i in range(5):
            line_x = cutting_x + 10 + i * 14
            pygame.draw.line(self.screen, (160, 110, 60), (line_x, cutting_y + 10), (line_x, cutting_y + 60), 1)
        
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
        draw_gradient_rect(self.screen, (245, 240, 225), (235, 230, 215), prepared_rect)
        pygame.draw.rect(self.screen, (180, 160, 120), prepared_rect, 2)
        
        title_overlay = pygame.Surface((prepared_w, 16), pygame.SRCALPHA)
        title_overlay.fill((180, 140, 60, 200))
        self.screen.blit(title_overlay, (prepared_x, prepared_y - 16))
        title = self.font_small.render("PRÉPARÉS", True, (255, 255, 255))
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
            
            check_x, check_y = pos_x + 10, pos_y - 10
            pygame.draw.circle(self.screen, (50, 180, 50), (check_x, check_y), 6)
            pygame.draw.circle(self.screen, (150, 255, 150), (check_x, check_y), 4)

    def draw_plating_station(self, asset_manager):
        import game_state
        current_time = time.time()
        
        plating_rect = pygame.Rect(self.plating_area['x'], self.plating_area['y'], 
                                  self.plating_area['w'], self.plating_area['h'])
        draw_gradient_rect(self.screen, (220, 225, 235), (200, 205, 215), plating_rect)
        pygame.draw.rect(self.screen, (140, 150, 170), plating_rect, 3)
        
        title_bg = pygame.Rect(self.plating_area['x'], self.plating_area['y'] - 30, 
                              self.plating_area['w'], 25)
        draw_gradient_rect(self.screen, (140, 150, 170), (120, 130, 150), title_bg)
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
            
            draw_gradient_rect(self.screen, (255, 250, 220), (245, 235, 200), assembly_rect)
            pygame.draw.rect(self.screen, (220, 180, 100), assembly_rect, 2)
            
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
            draw_gradient_rect(self.screen, (250, 250, 250), (235, 235, 230), assembly_rect)
            pygame.draw.rect(self.screen, (180, 180, 180), assembly_rect, 2)
        
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
        
        draw_gradient_rect(self.screen, (250, 220, 140), (230, 200, 120), service_rect)
        pygame.draw.rect(self.screen, (180, 150, 80), service_rect, 3)
        
        title_bg = pygame.Rect(self.service_area['x'], self.service_area['y'] - 30, self.service_area['w'], 25)
        draw_gradient_rect(self.screen, (180, 150, 80), (160, 130, 60), title_bg)
        title = self.font_small.render("SERVICE", True, (255, 255, 255))
        self.screen.blit(title, (self.service_area['x'] + 10, self.service_area['y'] - 25))
        
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
        self.delivered_dishes.append({
            'name': order_name,
            'time': time.time()
        })

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
        return {
            'fridge_access': (self.storage_area['x'] + 140, self.storage_area['y'] + 160),
            'cutting_board': (self.work_area['x'] + 60, self.work_area['y'] + 100),
            'plating_station': (self.plating_area['x'] + 100, self.plating_area['y'] + 100),
            'delivery': (self.service_area['x'] + 60, self.service_area['y'] + 150)
        }

    def render_full_kitchen(self, bot_manager, asset_manager, timer):
        """Render complet de la cuisine avec TOUS les chefs"""
        self.draw_floor()
        self.draw_individual_ingredient_stations(asset_manager)
        self.draw_work_station(asset_manager)
        self.draw_plating_station(asset_manager)
        self.draw_service_station()
        
        # Animation de découpe si active
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
        """Vérifie si un bot vient de livrer et déclenche l'animation"""
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
        """Affiche le statut d'UN chef en panneau compact"""
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
    """Gère l'animation réaliste de découpe des ingrédients"""
    
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.ingredient = None
        self.start_time = 0
        self.duration = 1.2
        self.particles = []
        self.board_pos = None
        
        self.ingredient_config = {
            'tomate': {
                'slices': 4,
                'slice_color': (255, 107, 107),
                'seed_color': (255, 203, 119),
                'main_color': (230, 57, 70)
            },
            'laitue': {
                'slices': 6,
                'slice_color': (82, 183, 136),
                'leaf_color': (149, 213, 178),
                'main_color': (45, 106, 79)
            },
            'oignon': {
                'slices': 5,
                'slice_color': (229, 212, 193),
                'ring_color': (248, 241, 229),
                'main_color': (200, 182, 166)
            },
            'steak': {
                'slices': 3,
                'slice_color': (160, 82, 45),
                'grill_color': (101, 67, 33),
                'main_color': (139, 69, 19)
            },
            'pain': {
                'slices': 4,
                'slice_color': (244, 229, 194),
                'crust_color': (139, 115, 85),
                'main_color': (218, 165, 32)
            },
            'fromage': {
                'slices': 3,
                'slice_color': (255, 230, 120),
                'hole_color': (255, 200, 50),
                'main_color': (255, 220, 80)
            }
        }
    
    def start(self, ingredient_type, board_x, board_y):
        """Démarre l'animation de découpe"""
        if ingredient_type not in self.ingredient_config:
            return
        
        self.active = True
        self.ingredient = ingredient_type
        self.start_time = time.time()
        self.board_pos = (board_x, board_y)
        self.particles = []
        print(f"🔪 Découpe de {ingredient_type} commencée!")
    
    def stop(self):
        """Arrête l'animation"""
        self.active = False
        self.ingredient = None
        self.particles = []
    
    def update(self):
        """Met à jour l'animation"""
        if not self.active:
            return False
        
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        if progress < 0.8 and len(self.particles) < 30:
            if pygame.time.get_ticks() % 3 == 0:
                self.create_particles()
        
        self.update_particles()
        
        if progress >= 1.0:
            self.stop()
            return True
        
        return False
    
    def create_particles(self):
        """Crée des particules de découpe"""
        if not self.board_pos:
            return
        
        config = self.ingredient_config[self.ingredient]
        board_x, board_y = self.board_pos
        
        for _ in range(3):
            particle = {
                'x': board_x + (pygame.time.get_ticks() % 20 - 10),
                'y': board_y,
                'vx': (pygame.time.get_ticks() % 8 - 4) * 0.5,
                'vy': -(pygame.time.get_ticks() % 6 + 2),
                'size': 2 + pygame.time.get_ticks() % 3,
                'color': config['slice_color'],
                'life': 1.0
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Met à jour la physique des particules"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3
            particle['life'] -= 0.02
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self):
        """Dessine l'animation de découpe"""
        if not self.active or not self.board_pos:
            return
        
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        board_x, board_y = self.board_pos
        config = self.ingredient_config[self.ingredient]
        
        self.draw_slices(board_x, board_y, progress, config)
        
        if progress < 0.8:
            self.draw_knife(board_x, board_y, progress)
        
        self.draw_particles()
    
    def draw_slices(self, board_x, board_y, progress, config):
        """Dessine les tranches qui se séparent"""
        num_slices = config['slices']
        slice_spacing = 100 / num_slices
        separation = min(progress * 2, 1.0) * 15
        
        for i in range(num_slices):
            offset = (i - num_slices / 2) * slice_spacing
            slice_x = int(board_x + offset + (i - num_slices / 2) * separation)
            slice_y = board_y
            
            if self.ingredient == 'tomate':
                self.draw_tomato_slice(slice_x, slice_y, config)
            elif self.ingredient == 'laitue':
                self.draw_lettuce_slice(slice_x, slice_y, config)
            elif self.ingredient == 'oignon':
                self.draw_onion_slice(slice_x, slice_y, config)
            elif self.ingredient == 'steak':
                self.draw_steak_slice(slice_x, slice_y, config)
            elif self.ingredient == 'pain':
                self.draw_bread_slice(slice_x, slice_y, config)
            elif self.ingredient == 'fromage':
                self.draw_cheese_slice(slice_x, slice_y, config)
    
    def draw_tomato_slice(self, x, y, config):
        """Dessine une tranche de tomate avec pépins"""
        pygame.draw.circle(self.screen, config['slice_color'], (x, y), 20)
        pygame.draw.circle(self.screen, config['main_color'], (x, y), 17)
        
        for i in range(6):
            angle = (i / 6) * 2 * math.pi
            px = x + int(math.cos(angle) * 10)
            py = y + int(math.sin(angle) * 10)
            pygame.draw.circle(self.screen, config['seed_color'], (px, py), 2)
        
        pygame.draw.circle(self.screen, (255, 200, 200), (x - 6, y - 6), 4)
    
    def draw_lettuce_slice(self, x, y, config):
        """Dessine une feuille de laitue coupée"""
        rect = pygame.Rect(x - 18, y - 22, 36, 44)
        pygame.draw.ellipse(self.screen, config['slice_color'], rect)
        
        inner_rect = pygame.Rect(x - 15, y - 19, 30, 38)
        pygame.draw.ellipse(self.screen, config['leaf_color'], inner_rect)
        
        pygame.draw.line(self.screen, (255, 255, 255), (x, y - 20), (x, y + 20), 2)
    
    def draw_onion_slice(self, x, y, config):
        """Dessine une rondelle d'oignon avec anneaux"""
        pygame.draw.circle(self.screen, config['ring_color'], (x, y), 20)
        
        for radius in [18, 14, 10, 6]:
            pygame.draw.circle(self.screen, config['slice_color'], (x, y), radius, 2)
        
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            end_x = x + int(math.cos(angle) * 18)
            end_y = y + int(math.sin(angle) * 18)
            pygame.draw.line(self.screen, config['main_color'], (x, y), (end_x, end_y), 1)
    
    def draw_steak_slice(self, x, y, config):
        """Dessine une tranche de steak avec marques de grill"""
        rect = pygame.Rect(x - 20, y - 15, 40, 30)
        pygame.draw.ellipse(self.screen, config['slice_color'], rect)
        
        for i in range(4):
            y_pos = y - 12 + i * 8
            pygame.draw.line(self.screen, config['grill_color'], 
                           (x - 18, y_pos), (x + 18, y_pos), 3)
    
    def draw_bread_slice(self, x, y, config):
        """Dessine une tranche de pain avec alvéoles"""
        rect = pygame.Rect(x - 15, y - 20, 30, 40)
        pygame.draw.rect(self.screen, config['crust_color'], rect)
        
        inner_rect = pygame.Rect(x - 12, y - 17, 24, 34)
        pygame.draw.rect(self.screen, config['slice_color'], inner_rect)
    
    def draw_cheese_slice(self, x, y, config):
        """Dessine une tranche de fromage avec trous"""
        points = [(x - 15, y - 10), (x + 15, y - 10), 
                 (x + 12, y + 10), (x - 12, y + 10)]
        pygame.draw.polygon(self.screen, config['main_color'], points)
        pygame.draw.polygon(self.screen, config['slice_color'], points, 2)
        
        for hole_pos in [(-6, -3), (4, 2), (-2, 5)]:
            hx = x + hole_pos[0]
            hy = y + hole_pos[1]
            pygame.draw.circle(self.screen, config['hole_color'], (hx, hy), 3)
    
    def draw_knife(self, board_x, board_y, progress):
        """Dessine le couteau qui coupe"""
        knife_y = board_y - 50 + progress * 100
        knife_x = board_x - 20
        
        shake = math.sin(progress * math.pi * 8) * 3
        knife_x += shake
        
        blade_points = [
            (knife_x, knife_y - 30),
            (knife_x + 15, knife_y),
            (knife_x - 3, knife_y)
        ]
        
        shadow_points = [(p[0] + 2, p[1] + 2) for p in blade_points]
        pygame.draw.polygon(self.screen, (100, 100, 100), shadow_points)
        pygame.draw.polygon(self.screen, (200, 200, 200), blade_points)
        
        reflet_points = [
            (knife_x + 2, knife_y - 28),
            (knife_x + 6, knife_y - 15),
            (knife_x + 4, knife_y - 15)
        ]
        pygame.draw.polygon(self.screen, (255, 255, 255), reflet_points)
        
        pygame.draw.line(self.screen, (150, 150, 150), 
                        blade_points[1], blade_points[2], 2)
        
        handle_rect = pygame.Rect(knife_x - 5, knife_y, 10, 20)
        pygame.draw.rect(self.screen, (70, 70, 70), handle_rect)
        
        inner_handle = pygame.Rect(knife_x - 4, knife_y + 1, 8, 18)
        pygame.draw.rect(self.screen, (107, 68, 35), inner_handle)
        
        for rivet_y in [knife_y + 5, knife_y + 15]:
            pygame.draw.circle(self.screen, (50, 50, 50), (knife_x, rivet_y), 2)
    
    def draw_particles(self):
        """Dessine les particules volantes"""
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            color = (*particle['color'], alpha)
            
            particle_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), 
                                          pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, 
                             (particle['size'], particle['size']), 
                             particle['size'])
            
            self.screen.blit(particle_surf, 
                           (int(particle['x'] - particle['size']), 
                            int(particle['y'] - particle['size'])))