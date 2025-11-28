# kitchen.py - VERSION COMPLÈTE CORRIGÉE POUR ACCIDENTS VISIBLES ET COULEURS AMÉLIORÉES

import pygame
import time
import math
import random
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
            "laitue": {"color": (60, 220, 60), "icon": "🥬", "height": 8, "width": 45},
            "tomate": {"color": (240, 60, 60), "icon": "🍅", "height": 6, "width": 35},
            "pain": {"color": (220, 170, 90), "icon": "🍞", "height": 12, "width": 50},
            "steak": {"color": (160, 90, 60), "icon": "🥩", "height": 10, "width": 40},
            "fromage": {"color": (255, 230, 90), "icon": "🧀", "height": 4, "width": 38},
            "oignon": {"color": (210, 190, 150), "icon": "🧅", "height": 5, "width": 32},
            "salade": {"color": (90, 200, 90), "icon": "🥗", "height": 15, "width": 60}
        }
        self.setup_kitchen_layout()
        self.delivered_dishes = []
        self.cutting_animation = CuttingAnimation(screen)
        
        # Éléments visuels
        self.steam_particles = []
        self.sparkle_particles = []
        self.stress_particles = []
        
        # Animation d'assemblage
        self.plating_animation = {
            'active': False,
            'progress': 0,
            'current_ingredient_index': 0,
            'ingredients': [],
            'plate_center': (0, 0),
            'start_time': 0,
            'ingredient_progress': 0
        }

        # Système de stress
        self.kitchen_stress_level = 0
        self.last_stress_update = time.time()
        self.stress_events = []
        self.panic_mode = False

        # Système d'accidents - CORRIGÉ POUR ÊTRE VISIBLE
        self.kitchen_accidents = []
        self.accident_particles = []
        self.last_accident_check = time.time()
        self.accident_cooldown = 0
        self.total_accidents_count = 0  # ✅ COMPTEUR TOTAL DES ACCIDENTS

        # Système de stress des chefs
        self.chef_stress_system = ChefStressSystem()

    def setup_kitchen_layout(self):
        """Disposition de la cuisine"""
        self.storage_area = {'x': 40, 'y': 120, 'w': 280, 'h': 140}
        self.work_area = {'x': 330, 'y': 120, 'w': 300, 'h': 150}
        self.plating_area = {'x': 640, 'y': 120, 'w': 150, 'h': 150}
        self.service_area = {'x': 800, 'y': 120, 'w': 120, 'h': 300}

    def check_for_accidents(self, bot_manager):
        """Vérifie et déclenche des accidents aléatoires - CORRIGÉ POUR ÊTRE PLUS FRÉQUENT"""
        current_time = time.time()
        
        # Vérifier plus fréquemment
        if current_time - self.last_accident_check < 3.0:
            return
            
        self.last_accident_check = current_time
        
        # Augmenter les chances d'accident
        accident_chance = self.kitchen_stress_level / 150
        
        if random.random() < accident_chance and bot_manager and hasattr(bot_manager, 'bots'):
            eligible_bots = [bot for bot in bot_manager.bots if bot.inv]
            if not eligible_bots:
                return
                
            bot = random.choice(eligible_bots)
            
            accident_types = [
                "drop_plate",
                "slip_fall", 
                "ingredient_spill",
                "equipment_fail"
            ]
            
            accident_type = random.choice(accident_types)
            self.trigger_accident(bot, accident_type)

    def trigger_accident(self, bot, accident_type):
        """Déclenche un accident spécifique - CORRIGÉ POUR MEILLEURE VISIBILITÉ"""
        print(f"💥 ACCIDENT: {accident_type} pour {bot.chef_name}!")
        
        accident_data = {
            'bot': bot,
            'type': accident_type,
            'start_time': time.time(),
            'duration': 6.0,  # Durée augmentée pour mieux voir
            'progress': 0.0,
            'position': (bot.x, bot.y),
            'message': "💥 ACCIDENT !",
            'color': (255, 100, 100),
            'intensity': 1.0
        }
        
        if accident_type == "drop_plate" and bot.inv == "plated_dish":
            accident_data['message'] = "💥 PLAT TOMBÉ !"
            accident_data['color'] = (255, 50, 50)
            accident_data['intensity'] = 1.5
            self.create_plate_smash_effect(bot.x, bot.y)
            bot.inv = None
            if hasattr(bot, 'current_order'):
                bot.current_order = None
            
        elif accident_type == "slip_fall":
            accident_data['message'] = "⚠️ CHEF GLISSÉ !"
            accident_data['color'] = (255, 150, 50)
            self.create_slip_effect(bot.x, bot.y)
            
        elif accident_type == "ingredient_spill" and bot.inv:
            accident_data['message'] = f"🍅 {bot.inv.upper()} RENVERSÉ !"
            accident_data['color'] = (255, 200, 50)
            accident_data['intensity'] = 1.2
            self.create_spill_effect(bot.x, bot.y, bot.inv)
            bot.inv = None
            
        elif accident_type == "equipment_fail":
            accident_data['message'] = "🔧 PANNE D'ÉQUIPEMENT !"
            accident_data['color'] = (150, 150, 255)
            self.create_equipment_fail_effect()
        
        self.kitchen_accidents.append(accident_data)
        self.kitchen_stress_level = min(100, self.kitchen_stress_level + 20)
        self.total_accidents_count += 1  # ✅ INCRÉMENTER LE COMPTEUR TOTAL

    def create_plate_smash_effect(self, x, y):
        """Crée l'effet d'un plat qui se casse - PLUS SPECTACULAIRE"""
        # Effet principal de cassure
        for i in range(30):  # Plus de particules
            self.accident_particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-8, 8),
                'vy': random.uniform(-12, -4),
                'life': random.uniform(1.5, 3.0),
                'color': (255, 255, 255),
                'size': random.uniform(4, 10),
                'type': 'plate_shard'
            })
        
        # Éclaboussures de nourriture
        for i in range(40):
            self.accident_particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-6, 6),
                'vy': random.uniform(-8, 0),
                'life': random.uniform(2.0, 4.0),
                'color': random.choice([(240, 60, 60), (60, 220, 60), (255, 230, 90), (220, 170, 90)]),
                'size': random.uniform(3, 8),
                'type': 'food_splash'
            })
        
        # Étincelles
        for i in range(15):
            self.accident_particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-2, 2),
                'life': random.uniform(0.5, 1.5),
                'color': (255, 255, 200),
                'size': random.uniform(2, 5),
                'type': 'sparkle'
            })

    def create_slip_effect(self, x, y):
        """Crée l'effet de glissade - AMÉLIORÉ"""
        for i in range(20):
            self.accident_particles.append({
                'x': x,
                'y': y + 20,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-2, 2),
                'life': random.uniform(1.5, 2.5),
                'color': (200, 200, 255),
                'size': random.uniform(6, 12),
                'type': 'slip'
            })

    def create_spill_effect(self, x, y, ingredient):
        """Crée l'effet d'ingrédient renversé - PLUS VISIBLE"""
        ingredient_color = self.ingredient_config.get(ingredient, {}).get("color", (150, 150, 150))
        
        # Particules principales
        for i in range(50):
            self.accident_particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-8, 8),
                'vy': random.uniform(-6, 3),
                'life': random.uniform(1.5, 3.0),
                'color': ingredient_color,
                'size': random.uniform(4, 9),
                'type': 'spill'
            })
        
        # Éclaboussures
        for i in range(20):
            self.accident_particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-10, 10),
                'vy': random.uniform(-8, 0),
                'life': random.uniform(1.0, 2.0),
                'color': ingredient_color,
                'size': random.uniform(2, 6),
                'type': 'splash'
            })

    def create_equipment_fail_effect(self):
        """Crée l'effet de panne d'équipement - PLUS VISIBLE"""
        for i in range(25):
            x = random.randint(self.work_area['x'], self.work_area['x'] + self.work_area['w'])
            y = random.randint(self.work_area['y'], self.work_area['y'] + self.work_area['h'])
            
            self.accident_particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': random.uniform(0.8, 2.0),
                'color': (255, 255, 100),
                'size': random.uniform(3, 7),
                'type': 'spark'
            })

    def update_accidents(self):
        """Met à jour les animations d'accidents - CORRIGÉ POUR MEILLEURE PERFORMANCE"""
        current_time = time.time()
        
        # Mettre à jour les accidents
        for accident in self.kitchen_accidents[:]:
            elapsed = current_time - accident['start_time']
            accident['progress'] = elapsed / accident['duration']
            
            if accident['progress'] >= 1.0:
                self.kitchen_accidents.remove(accident)
        
        # Mettre à jour les particules avec gestion d'erreur
        try:
            for particle in self.accident_particles[:]:
                if not isinstance(particle, dict):
                    self.accident_particles.remove(particle)
                    continue
                    
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.2  # Gravité
                particle['life'] -= 0.04
                
                if particle['life'] <= 0:
                    self.accident_particles.remove(particle)
        except Exception as e:
            print(f"⚠ Erreur mise à jour particules: {e}")
            # Réinitialiser en cas d'erreur
            self.accident_particles = []

    def draw_accidents(self):
        """Dessine les effets d'accidents - CORRIGÉ POUR MEILLEURE VISIBILITÉ"""
        current_time = time.time()
        
        # Dessiner les particules d'accident
        for particle in self.accident_particles:
            try:
                alpha = int(255 * particle['life'])
                size = int(particle['size'] * particle['life'])
                
                if size > 0:
                    particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    
                    color = particle['color']
                    if isinstance(color, tuple) and len(color) == 3:
                        rgba_color = (*color, alpha)
                    else:
                        rgba_color = (255, 100, 100, alpha)
                    
                    if particle['type'] == 'plate_shard':
                        # Éclats d'assiette
                        points = [
                            (size, 0),
                            (size * 2, size),
                            (size, size * 2),
                            (0, size)
                        ]
                        pygame.draw.polygon(particle_surf, rgba_color, points)
                        
                    elif particle['type'] == 'food_splash':
                        # Éclaboussures de nourriture
                        pygame.draw.circle(particle_surf, rgba_color, (size, size), size)
                        
                    elif particle['type'] == 'sparkle':
                        # Étincelles
                        pygame.draw.circle(particle_surf, rgba_color, (size, size), size)
                        # Effet de lueur
                        glow_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
                        glow_color = (*color, alpha // 2)
                        pygame.draw.circle(glow_surf, glow_color, (size * 2, size * 2), size * 2)
                        self.screen.blit(glow_surf, (particle['x'] - size * 2, particle['y'] - size * 2))
                        
                    elif particle['type'] == 'slip':
                        # Effet de glissade
                        pygame.draw.ellipse(particle_surf, rgba_color, 
                                          (0, 0, size * 2, size))
                        
                    elif particle['type'] == 'spill':
                        # Renversement
                        pygame.draw.circle(particle_surf, rgba_color, (size, size), size)
                        
                    elif particle['type'] == 'splash':
                        # Éclaboussures
                        pygame.draw.circle(particle_surf, rgba_color, (size, size), size)
                        
                    elif particle['type'] == 'spark':
                        # Étincelles d'équipement
                        pygame.draw.circle(particle_surf, rgba_color, (size, size), size)
                    
                    else:
                        # Type par défaut
                        pygame.draw.circle(particle_surf, rgba_color, (size, size), size)
                    
                    self.screen.blit(particle_surf, (int(particle['x'] - size), int(particle['y'] - size)))
            except Exception as e:
                # Ignorer les particules corrompues
                continue
        
        # Dessiner les messages d'accident
        for accident in self.kitchen_accidents:
            progress = accident['progress']
            if progress < 0.9:  # Message visible plus longtemps
                alpha = int(255 * (1 - progress / 0.9))
                x, y = accident['position']
                
                # Animation de flottement
                float_offset = math.sin(current_time * 10) * 15
                
                message = accident.get('message', '💥 ACCIDENT !')
                color = accident.get('color', (255, 100, 100))
                
                # Texte principal avec effet de pulsation
                pulse = 1.0 + 0.2 * math.sin(current_time * 8)
                font_size = int(28 * pulse)
                accident_font = pygame.font.Font(None, font_size)
                text_surf = accident_font.render(message, True, color)
                text_rect = text_surf.get_rect(center=(x, y - 60 + float_offset))
                
                # Fond avec effet de brillance
                bg_width = text_rect.width + 40
                bg_height = text_rect.height + 20
                bg_surf = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
                
                # Fond gradient
                for i in range(bg_height):
                    ratio = i / bg_height
                    bg_color = (
                        max(0, color[0] - 50),
                        max(0, color[1] - 50),
                        max(0, color[2] - 50),
                        alpha // 3
                    )
                    pygame.draw.line(bg_surf, bg_color, (0, i), (bg_width, i))
                
                # Bordure
                pygame.draw.rect(bg_surf, (*color, alpha // 2), 
                              (0, 0, bg_width, bg_height), 3, border_radius=12)
                
                self.screen.blit(bg_surf, (text_rect.x - 20, text_rect.y - 10))
                self.screen.blit(text_surf, text_rect)
                
                # Effet de particules autour du message
                if random.random() < 0.3:
                    for _ in range(3):
                        self.accident_particles.append({
                            'x': x + random.uniform(-50, 50),
                            'y': y - 30 + float_offset,
                            'vx': random.uniform(-2, 2),
                            'vy': random.uniform(-1, 1),
                            'life': random.uniform(0.5, 1.5),
                            'color': color,
                            'size': random.uniform(2, 4),
                            'type': 'sparkle'
                        })

    def update_stress_system(self, bot_manager, order_manager):
        """Met à jour le système de stress - CORRIGÉ POUR MEILLEURE GESTION"""
        current_time = time.time()
        
        if current_time - self.last_stress_update > 2.0:
            self.last_stress_update = current_time
            
            stress_factors = 0
            
            if hasattr(order_manager, 'pending_orders'):
                pending_orders = len(order_manager.pending_orders)
                stress_factors += pending_orders * 15
            
            if hasattr(order_manager, 'chef_orders'):
                late_orders = 0
                for order_id, order_info in order_manager.chef_orders.items():
                    order_start = order_info.get('start_time', current_time)
                    if current_time - order_start > 60:
                        late_orders += 1
                stress_factors += late_orders * 25
            
            if bot_manager and hasattr(bot_manager, 'bots'):
                overloaded_chefs = 0
                for bot in bot_manager.bots:
                    if (hasattr(bot, 'personal_stress') and bot.personal_stress > 60):
                        overloaded_chefs += 1
                
                stress_factors += overloaded_chefs * 12
            
            if self.kitchen_accidents:
                stress_factors += len(self.kitchen_accidents) * 25  # Augmenté
            
            stress_factors += 8
            
            new_stress = min(100, stress_factors)
            
            if new_stress > self.kitchen_stress_level:
                self.kitchen_stress_level = min(100, self.kitchen_stress_level + 4)
            else:
                self.kitchen_stress_level = max(0, self.kitchen_stress_level - 1)
            
            if random.random() < 0.2:
                print(f"📊 STRESS: {self.kitchen_stress_level}% (Facteurs: {stress_factors})")
            
            if self.kitchen_stress_level >= 50 and not self.panic_mode:
                self.panic_mode = True
                self.trigger_panic_mode()
                print("🚨🚨🚨 MODE PANIQUE ACTIVÉ ! 🚨🚨🚨")
            elif self.kitchen_stress_level < 40 and self.panic_mode:
                self.panic_mode = False
                print("✅ Mode panique désactivé")
            
            if self.kitchen_stress_level > 30 and random.random() < 0.5:
                self.add_stress_event()

            # Vérifier les accidents plus fréquemment en mode panique
            accident_check_interval = 2.0 if self.panic_mode else 3.0
            if current_time - self.last_accident_check > accident_check_interval:
                self.check_for_accidents(bot_manager)

    def trigger_panic_mode(self):
        """Déclenche le mode panique - EFFETS RENFORCÉS"""
        print("🚨🚨🚨 MODE PANIQUE DANS LA CUISINE ! 🚨🚨🚨")
        
        for _ in range(50):
            self.create_stress_particle()
        
        panic_event = {
            'text': "🚨 MODE PANIQUE ! 🚨",
            'x': WIDTH // 2,
            'y': HEIGHT // 3,
            'start_time': time.time(),
            'duration': 6.0,
            'color': (255, 0, 0),
            'size': 1.5
        }
        self.stress_events.append(panic_event)

    def add_stress_event(self):
        """Ajoute un événement de stress visuel"""
        event_types = [
            "🔥 PLAT BRÛLÉ !",
            "⏰ COMMANDE EN RETARD !",
            "😫 CHEF EN STRESS !",
            "💥 ACCIDENT !",
            "🚨 URGENCE !",
            "😰 TROP DE COMMANDES !",
            "💀 CUISINE EN CRISE !"
        ]
        
        event = {
            'text': random.choice(event_types),
            'x': random.randint(100, WIDTH - 100),
            'y': random.randint(50, 200),
            'start_time': time.time(),
            'duration': 2.5,
            'color': (255, 50, 50)
        }
        
        self.stress_events.append(event)

    def create_stress_particle(self):
        """Crée des particules de stress/anxiété"""
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        
        self.stress_particles.append({
            'x': x,
            'y': y,
            'vx': random.uniform(-3, 3),
            'vy': random.uniform(-4, -1),
            'life': random.uniform(1.0, 3.0),
            'color': random.choice([(255, 50, 50), (255, 150, 50), (200, 50, 100)]),
            'size': random.uniform(2, 8),
            'type': random.choice(['stress', 'anxiety', 'panic'])
        })

    def update_stress_particles(self):
        """Met à jour les particules de stress"""
        for particle in self.stress_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 0.03
            
            if particle['type'] == 'anxiety':
                particle['vx'] += random.uniform(-0.5, 0.5)
                particle['vy'] += random.uniform(-0.2, 0.2)
            elif particle['type'] == 'panic':
                particle['vx'] *= 1.05
                particle['vy'] *= 1.05
            
            if particle['life'] <= 0:
                self.stress_particles.remove(particle)

    def draw_stress_effects(self):
        """Dessine les effets visuels du stress"""
        current_time = time.time()
        
        for particle in self.stress_particles:
            alpha = int(200 * particle['life'])
            size = int(particle['size'] * particle['life'])
            
            if size > 0:
                color = particle['color']
                if not isinstance(color, tuple) or len(color) != 3:
                    color = (255, 50, 50)
                
                if particle['type'] == 'stress':
                    stress_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(stress_surf, (*color, alpha), 
                                     (size, size), size)
                    self.screen.blit(stress_surf, 
                                   (int(particle['x'] - size), int(particle['y'] - size)))
                
                elif particle['type'] == 'anxiety':
                    anxiety_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
                    for i in range(3):
                        wave_size = size * (1 - i * 0.3)
                        wave_alpha = alpha * (1 - i * 0.3)
                        pygame.draw.circle(anxiety_surf, 
                                         (*color, int(wave_alpha)), 
                                         (size * 2, size * 2), 
                                         int(wave_size), 2)
                    self.screen.blit(anxiety_surf, 
                                   (int(particle['x'] - size * 2), 
                                    int(particle['y'] - size * 2)))
                
                elif particle['type'] == 'panic':
                    panic_surf = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
                    points = []
                    for i in range(5):
                        angle = random.uniform(0, 2 * math.pi)
                        radius = size * random.uniform(0.5, 1.5)
                        points.append((
                            size * 1.5 + math.cos(angle) * radius,
                            size * 1.5 + math.sin(angle) * radius
                        ))
                    pygame.draw.polygon(panic_surf, (*color, alpha), points)
                    self.screen.blit(panic_surf, 
                                   (int(particle['x'] - size * 1.5), 
                                    int(particle['y'] - size * 1.5)))
        
        for event in self.stress_events[:]:
            elapsed = current_time - event['start_time']
            progress = elapsed / event['duration']
            
            if progress >= 1.0:
                self.stress_events.remove(event)
                continue
            
            float_offset = math.sin(current_time * 8) * 5
            alpha = int(255 * (1 - progress))
            
            text_surf = self.font_small.render(event['text'], True, event['color'])
            text_rect = text_surf.get_rect(center=(event['x'], event['y'] + float_offset))
            
            halo_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(halo_surf, (255, 0, 0, alpha // 3), 
                          (0, 0, text_rect.width + 20, text_rect.height + 10), 
                          border_radius=10)
            self.screen.blit(halo_surf, (text_rect.x - 10, text_rect.y - 5))
            
            self.screen.blit(text_surf, text_rect)
        
        if self.panic_mode:
            panic_pulse = int(80 + 40 * math.sin(current_time * 10))
            panic_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            panic_overlay.fill((255, 0, 0, panic_pulse))
            self.screen.blit(panic_overlay, (0, 0))
        
        elif self.kitchen_stress_level > 30:
            stress_alpha = min(80, int(self.kitchen_stress_level * 0.8))
            stress_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            stress_overlay.fill((255, 50, 50, stress_alpha))
            self.screen.blit(stress_overlay, (0, 0))

    def draw_stress_meter(self):
        """Dessine le compteur de stress de la cuisine"""
        meter_x = WIDTH - 160
        meter_y = 20
        meter_width = 140
        meter_height = 30
        
        pygame.draw.rect(self.screen, (30, 30, 30), 
                        (meter_x, meter_y, meter_width, meter_height), 
                        border_radius=8)
        
        stress_width = int((self.kitchen_stress_level / 100) * meter_width)
        
        if self.kitchen_stress_level < 40:
            stress_color = (100, 200, 100)
        elif self.kitchen_stress_level < 70:
            stress_color = (255, 200, 50)
        else:
            stress_color = (255, 50, 50)
        
        pygame.draw.rect(self.screen, stress_color, 
                        (meter_x, meter_y, stress_width, meter_height), 
                        border_radius=8)
        
        border_color = (255, 255, 255) if self.panic_mode else (200, 200, 200)
        pygame.draw.rect(self.screen, border_color, 
                        (meter_x, meter_y, meter_width, meter_height), 
                        3, border_radius=8)
        
        stress_text = self.font_small.render(f"STRESSE: {self.kitchen_stress_level}%", True, (255, 255, 255))
        text_rect = stress_text.get_rect(center=(meter_x + meter_width//2, meter_y + meter_height//2))
        self.screen.blit(stress_text, text_rect)
        
        if self.panic_mode:
            alarm_icon = self.font_medium.render("🚨", True, (255, 50, 50))
            self.screen.blit(alarm_icon, (meter_x - 40, meter_y))

    def draw_floor(self):
        """Sol avec damier - COULEUR MODIFIÉE POUR DIFFÉRENCIER DES MURS"""
        tile_size = 50
        floor_light = (180, 180, 180)  # Gris clair pour le sol
        floor_dark = (160, 160, 160)   # Gris moyen pour contraste
        
        for x in range(0, WIDTH, tile_size):
            for y in range(0, HEIGHT, tile_size):
                color = floor_light if (x // tile_size + y // tile_size) % 2 == 0 else floor_dark
                pygame.draw.rect(self.screen, color, (x, y, tile_size, tile_size))
                
                if (x // tile_size + y // tile_size) % 2 == 0:
                    shine_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                    pygame.draw.circle(shine_surf, (255, 255, 255, 15), (tile_size // 2, tile_size // 2), tile_size // 3)
                    self.screen.blit(shine_surf, (x, y))
                
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x + tile_size, y), 1)
                pygame.draw.line(self.screen, (200, 200, 200), (x, y), (x, y + tile_size), 1)

    def draw_wall_decorations(self):
        """Décorations murales - COULEUR DIFFÉRENTE DU SOL"""
        current_time = time.time()
        
        # Fond des murs - COULEUR BEIGE CLAIR POUR DIFFÉRENCIER DU SOL
        wall_color = (240, 230, 210)  # Beige clair pour les murs
        self.screen.fill(wall_color, (0, 0, WIDTH, 120))  # Mur du haut
        
        # Murs latéraux
        pygame.draw.rect(self.screen, wall_color, (0, 0, 40, HEIGHT))  # Mur gauche
        pygame.draw.rect(self.screen, wall_color, (WIDTH - 40, 0, 40, HEIGHT))  # Mur droit
        
        clock_x, clock_y = WIDTH - 80, 50
        pygame.draw.circle(self.screen, (240, 240, 240), (clock_x, clock_y), 25)
        pygame.draw.circle(self.screen, (200, 200, 200), (clock_x, clock_y), 25, 3)
        
        hour_angle = (current_time % 43200) / 43200 * 2 * math.pi - math.pi / 2
        minute_angle = (current_time % 3600) / 3600 * 2 * math.pi - math.pi / 2
        
        pygame.draw.line(self.screen, (50, 50, 50), (clock_x, clock_y),
                        (clock_x + math.cos(hour_angle) * 12, clock_y + math.sin(hour_angle) * 12), 3)
        pygame.draw.line(self.screen, (50, 50, 50), (clock_x, clock_y),
                        (clock_x + math.cos(minute_angle) * 18, clock_y + math.sin(minute_angle) * 18), 2)
        
        pygame.draw.circle(self.screen, (200, 50, 50), (clock_x, clock_y), 3)
        
        shelf_y = 85
        shelf_color = (120, 80, 50)
        
        pygame.draw.rect(self.screen, shelf_color, (40, shelf_y, 280, 8))
        pygame.draw.rect(self.screen, (80, 50, 30), (40, shelf_y, 280, 8), 2)
        
        small_shelves = [
            (350, shelf_y - 10, 120, 6),
            (500, shelf_y - 15, 100, 6),
            (650, shelf_y - 5, 80, 6)
        ]
        
        for shelf_x, shelf_y_pos, shelf_w, shelf_h in small_shelves:
            pygame.draw.rect(self.screen, shelf_color, (shelf_x, shelf_y_pos, shelf_w, shelf_h))
            pygame.draw.rect(self.screen, (80, 50, 30), (shelf_x, shelf_y_pos, shelf_w, shelf_h), 1)
        
        pot_positions = [
            (80, shelf_y - 8, (200, 100, 100)),
            (140, shelf_y - 8, (100, 200, 100)),
            (200, shelf_y - 8, (100, 100, 200)),
            (260, shelf_y - 8, (200, 200, 100)),
            (380, shelf_y - 18, (150, 120, 80)),
            (480, shelf_y - 23, (120, 150, 100)),
            (680, shelf_y - 13, (180, 140, 120))
        ]
        
        for pot_x, pot_y, pot_color in pot_positions:
            pygame.draw.circle(self.screen, pot_color, (pot_x, pot_y), 8)
            pygame.draw.circle(self.screen, (255, 255, 255, 150), (pot_x - 2, pot_y - 10), 3)
            pygame.draw.rect(self.screen, (80, 60, 40), (pot_x - 6, pot_y + 5, 12, 4))

    def draw_overhead_lamps(self):
        """Lampes suspendues"""
        current_time = time.time()
        
        lamp_positions = [
            (180, 90, (255, 230, 150)),
            (480, 90, (255, 240, 200)),
            (715, 90, (255, 245, 220)),
        ]
        
        for lamp_x, lamp_y, light_color in lamp_positions:
            pygame.draw.line(self.screen, (80, 80, 80), (lamp_x, 0), (lamp_x, lamp_y), 2)
            
            lamp_rect = pygame.Rect(lamp_x - 20, lamp_y, 40, 15)
            pygame.draw.ellipse(self.screen, (100, 100, 100), lamp_rect)
            pygame.draw.ellipse(self.screen, (70, 70, 70), lamp_rect, 2)
            
            pulse = int(30 + 10 * math.sin(current_time * 2 + lamp_x))
            for radius in [80, 60, 40]:
                alpha = pulse // (radius // 20)
                light_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(light_surf, (*light_color, alpha), (radius, radius), radius)
                self.screen.blit(light_surf, (lamp_x - radius, lamp_y + 15 - radius))

    def draw_individual_ingredient_stations(self, asset_manager):
        """Stations d'ingrédients - COULEUR BRUN CLAIR POUR LES PLANS DE TRAVAIL"""
        import game_state
        current_time = time.time()
        
        storage_rect = pygame.Rect(self.storage_area['x'], self.storage_area['y'], 
                                   self.storage_area['w'], self.storage_area['h'])
        
        # COULEUR BRUN CLAIR POUR LES PLANS DE TRAVAIL - DIFFÉRENT DU SOL ET DES MURS
        plan_travail_color1 = (180, 150, 120)  # Brun clair
        plan_travail_color2 = (160, 130, 100)  # Brun moyen
        draw_gradient_rect(self.screen, plan_travail_color1, plan_travail_color2, storage_rect)
        
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
        
        cols = len(ingredient_types)
        station_width = (self.storage_area['w'] - 20) // cols - 5
        station_height = self.storage_area['h'] - 30
        self.ingredient_positions = {}

        for i, ingredient_type in enumerate(ingredient_types):
            station_x = self.storage_area['x'] + 10 + i * (station_width + 5)
            station_y = self.storage_area['y'] + 15
            self.ingredient_positions[ingredient_type] = (station_x + station_width//2, station_y + station_height//2)
            
            station_rect = pygame.Rect(station_x, station_y, station_width, station_height)
            
            available_ingredients = [ing for ing in game_state.ingredients 
                                    if ing["type"] == ingredient_type and not ing["taken"] 
                                    and current_time >= ing.get("spawn_time", 0)]
            is_available = len(available_ingredients) > 0

            # MÊME COULEUR BRUN CLAIR POUR TOUS LES PLANS DE TRAVAIL
            draw_gradient_rect(self.screen, plan_travail_color1, plan_travail_color2, station_rect)
            
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

            storage_inner = pygame.Rect(station_x + 5, station_y + 25, station_width - 10, station_height - 30)
            ingredient_color = self.ingredient_config.get(ingredient_type, {}).get("color", (150, 150, 150))
            pygame.draw.rect(self.screen, ingredient_color, storage_inner)
            pygame.draw.rect(self.screen, (80, 60, 40), storage_inner, 2)

            if is_available and asset_manager:
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
                        color = self.ingredient_config.get(ingredient_type, {}).get("color", (150, 150, 150))
                        pygame.draw.circle(self.screen, color, (ing_x, int(float_y)), 8)
                        pygame.draw.circle(self.screen, (255, 255, 255), (ing_x, int(float_y)), 8, 2)

            label_overlay = pygame.Surface((station_width, 20), pygame.SRCALPHA)
            label_overlay.fill((80, 60, 40, 220))
            self.screen.blit(label_overlay, (station_x, station_y))
            label_text = self.font_small.render(ingredient_type.capitalize(), True, (255, 255, 255))
            label_rect = label_text.get_rect(center=(station_x + station_width//2, station_y + 10))
            self.screen.blit(label_text, label_rect)

            led_x = station_x + station_width - 8
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
                badge_y = station_y + station_height - 10
                pygame.draw.circle(self.screen, badge_color, (station_x + station_width//2, badge_y), 8)
                pygame.draw.circle(self.screen, (255, 255, 255), (station_x + station_width//2, badge_y), 8, 1)
                qty_text = self.font_small.render(str(qty), True, (255, 255, 255))
                qty_rect = qty_text.get_rect(center=(station_x + station_width//2, badge_y))
                self.screen.blit(qty_text, qty_rect)

    def draw_work_station(self, asset_manager):
        """Station de travail - MÊME COULEUR BRUN CLAIR"""
        import game_state
        current_time = time.time()
        
        work_rect = pygame.Rect(self.work_area['x'], self.work_area['y'], 
                              self.work_area['w'], self.work_area['h'])
        
        # MÊME COULEUR BRUN CLAIR POUR LA COHÉRENCE
        plan_travail_color1 = (180, 150, 120)
        plan_travail_color2 = (160, 130, 100)
        draw_gradient_rect(self.screen, plan_travail_color1, plan_travail_color2, work_rect)
        
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
        
        # Zone de découpe
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
        
        knife_holder_x = cutting_x + cutting_w + 5
        knife_holder_y = cutting_y + 10
        pygame.draw.rect(self.screen, (100, 100, 100), (knife_holder_x, knife_holder_y, 8, 30))
        pygame.draw.polygon(self.screen, (180, 180, 180), 
                          [(knife_holder_x + 4, knife_holder_y + 5),
                           (knife_holder_x + 10, knife_holder_y + 12),
                           (knife_holder_x + 4, knife_holder_y + 12)])
        
        # Zone de cuisson
        hotplate_x = self.work_area['x'] + 120
        hotplate_y = self.work_area['y'] + 25
        hotplate_w = 100
        hotplate_h = 60
        
        hotplate_rect = pygame.Rect(hotplate_x, hotplate_y, hotplate_w, hotplate_h)
        
        is_cooking = False
        cooking_chef = None
        if hasattr(game_state, 'bot_manager'):
            for bot in game_state.bot_manager.bots:
                if hasattr(bot, '_is_cooking') and bot._is_cooking:
                    is_cooking = True
                    cooking_chef = bot
                    break
        
        pygame.draw.rect(self.screen, (80, 80, 80), hotplate_rect)
        
        if is_cooking:
            heat_pulse = int(200 + 55 * math.sin(current_time * 5))
            cooking_surface_color = (heat_pulse, heat_pulse // 3, 30)
        else:
            cooking_surface_color = (60, 60, 60)
        
        cooking_surface = pygame.Rect(hotplate_x + 5, hotplate_y + 5, hotplate_w - 10, hotplate_h - 10)
        draw_gradient_rect(self.screen, cooking_surface_color,
                          (max(0, cooking_surface_color[0] - 40),
                           max(0, cooking_surface_color[1] - 40),
                           max(0, cooking_surface_color[2] - 40)),
                          cooking_surface)
        
        for i in range(4):
            bar_y = hotplate_y + 10 + i * 12
            pygame.draw.line(self.screen, (40, 40, 40),
                            (hotplate_x + 7, bar_y),
                            (hotplate_x + hotplate_w - 7, bar_y), 2)
        
        pygame.draw.rect(self.screen, (50, 50, 50), hotplate_rect, 2)
        
        if is_cooking and cooking_chef:
            ing_x = hotplate_x + hotplate_w // 2
            ing_y = hotplate_y + hotplate_h // 2
            progress = cooking_chef.cooking_progress
            
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
            
            for dot_idx in range(3):
                spot_x = ing_x + (dot_idx - 1) * 8
                spot_y = ing_y + (dot_idx - 1) * 5
                pygame.draw.circle(self.screen, (80, 30, 20), (spot_x, spot_y), 3)
            
            if progress > 0.1:
                self.create_cooking_smoke(ing_x, ing_y, progress)
            
            bar_w = 70
            bar_h = 6
            bar_x = ing_x - bar_w // 2
            bar_y = ing_y + 25
            
            pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_w, bar_h))
            
            fill_width = int(bar_w * min(progress, 1.2))
            
            if progress < 0.75:
                bar_color = (100, 255, 100)
            elif progress < 1.0:
                bar_color = (255, 255, 100)
            elif progress < 1.2:
                bar_color = (255, 150, 0)
            else:
                bar_color = (255, 50, 50)
            
            pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, fill_width, bar_h))
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 1)
        
        for i in range(2):
            knob_x = hotplate_x + 15 + i * 35
            knob_y = hotplate_y + hotplate_h - 15
            
            pygame.draw.circle(self.screen, (100, 100, 100), (knob_x, knob_y), 6)
            pygame.draw.circle(self.screen, (60, 60, 60), (knob_x, knob_y), 6, 2)
            
            angle = (current_time * 0.5 + i) if is_cooking else i
            mark_x = knob_x + math.cos(angle) * 4
            mark_y = knob_y + math.sin(angle) * 4
            pygame.draw.circle(self.screen, (200, 50, 50), (int(mark_x), int(mark_y)), 1)
        
        led_x = hotplate_x + hotplate_w - 12
        led_y = hotplate_y + hotplate_h - 15
        
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
        self.cooking_position = (hotplate_x + hotplate_w//2, hotplate_y + hotplate_h//2)

    def draw_prepared_area(self, asset_manager):
        """Zone des ingrédients préparés"""
        import game_state
        current_time = time.time()
        
        prepared_x = self.work_area['x'] + 230
        prepared_y = self.work_area['y'] + 25
        prepared_w = 60
        prepared_h = 60
        
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
        
        for idx, ingredient in enumerate(all_prepared[:6]):
            pos_x = prepared_x + 15 + (idx % 3) * 18
            pos_y = prepared_y + 15 + (idx // 3) * 20
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
            
            check_x, check_y = pos_x + 8, pos_y - 8
            pygame.draw.circle(self.screen, (50, 180, 50), (check_x, check_y), 5)
            pygame.draw.circle(self.screen, (150, 255, 150), (check_x, check_y), 3)

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

    def update_steam_particles(self):
        """Met à jour la vapeur"""
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

    def start_plating_animation(self, ingredients, plate_center):
        """Démarre l'animation d'assemblage"""
        self.plating_animation = {
            'active': True,
            'progress': 0,
            'current_ingredient_index': 0,
            'ingredients': ingredients,
            'plate_center': plate_center,
            'start_time': time.time(),
            'ingredient_progress': 0
        }

    def update_plating_animation(self):
        """Met à jour l'animation d'assemblage"""
        if not self.plating_animation['active']:
            return False
            
        current_time = time.time()
        elapsed = current_time - self.plating_animation['start_time']
        
        total_duration = 3.0
        self.plating_animation['progress'] = min(elapsed / total_duration, 1.0)
        
        num_ingredients = len(self.plating_animation['ingredients'])
        if num_ingredients > 0:
            time_per_ingredient = total_duration / num_ingredients
            current_ingredient_time = elapsed % time_per_ingredient
            self.plating_animation['ingredient_progress'] = min(current_ingredient_time / (time_per_ingredient * 0.8), 1.0)
            self.plating_animation['current_ingredient_index'] = min(int(elapsed / time_per_ingredient), num_ingredients - 1)
        
        if self.plating_animation['progress'] >= 1.0:
            self.plating_animation['active'] = False
            return True
            
        return False

    def draw_plating_station(self, asset_manager):
        """Station d'assemblage - MÊME COULEUR BRUN CLAIR"""
        import game_state
        current_time = time.time()
        
        plating_rect = pygame.Rect(self.plating_area['x'], self.plating_area['y'], 
                                  self.plating_area['w'], self.plating_area['h'])
        
        # MÊME COULEUR BRUN CLAIR POUR LA COHÉRENCE
        plan_travail_color1 = (180, 150, 120)
        plan_travail_color2 = (160, 130, 100)
        draw_gradient_rect(self.screen, plan_travail_color1, plan_travail_color2, plating_rect)
        
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
        
        assembly_x = self.plating_area['x'] + 25
        assembly_y = self.plating_area['y'] + 25
        assembly_w = 100
        assembly_h = 100
        
        plating_chefs = []
        current_ingredients = []
        if hasattr(game_state, 'bot_manager'):
            for bot in game_state.bot_manager.bots:
                if bot.plating:
                    order = bot.get_my_order()
                    if order:
                        plating_chefs.append({'bot': bot, 'ingredients': order.get('prepared_ingredients', [])})
                        current_ingredients = order.get('prepared_ingredients', [])
        
        plate_center_x = assembly_x + assembly_w//2
        plate_center_y = assembly_y + assembly_h//2
        
        if plating_chefs and not self.plating_animation['active']:
            self.start_plating_animation(current_ingredients, (plate_center_x, plate_center_y))
        
        if self.plating_animation['active']:
            self.update_plating_animation()
        
        assembly_rect = pygame.Rect(assembly_x, assembly_y, assembly_w, assembly_h)
        draw_gradient_rect(self.screen, (210, 160, 100), (190, 140, 80), assembly_rect)
        pygame.draw.rect(self.screen, (120, 80, 40), assembly_rect, 2)
        
        if plating_chefs or self.plating_animation['active']:
            glow = int(60 + 40 * math.sin(current_time * 5))
            glow_surf = pygame.Surface((140, 140), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 200, glow), (70, 70), 65)
            self.screen.blit(glow_surf, (plate_center_x - 70, plate_center_y - 70))
        
        self.draw_plate(plate_center_x, plate_center_y)
        
        if self.plating_animation['active']:
            self.draw_animated_plating(asset_manager)
        elif plating_chefs:
            self.draw_assembled_dish_improved(plate_center_x, plate_center_y, current_ingredients, asset_manager)
            
            chef_data = plating_chefs[0]
            if hasattr(chef_data['bot'], 'plate_time'):
                plate_progress = (current_time - chef_data['bot'].plate_time) / chef_data['bot'].PLATING_TIME
                plate_progress = max(0, min(1.0, plate_progress))
                self.draw_progress_bar(plate_center_x, plate_center_y + 45, plate_progress, "Assemblage")
        else:
            self.draw_empty_plate(plate_center_x, plate_center_y)
        
        self.plating_position = (plate_center_x, plate_center_y + 40)

    def draw_plate(self, x, y):
        """Dessine une assiette réaliste"""
        shadow_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), (0, 0, 80, 15))
        self.screen.blit(shadow_surf, (x - 40, y + 25))
        
        pygame.draw.circle(self.screen, (220, 220, 220), (x, y), 38)
        pygame.draw.circle(self.screen, (240, 240, 240), (x, y), 36)
        
        for i in range(36, 25, -1):
            alpha = 150 - (36 - i) * 4
            color = (250, 250, 245, alpha)
            pygame.draw.circle(self.screen, color, (x, y), i)
        
        reflect_surf = pygame.Surface((50, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(reflect_surf, (255, 255, 255, 80), (0, 0, 50, 10))
        self.screen.blit(reflect_surf, (x - 25, y - 28))

    def draw_empty_plate(self, x, y):
        """Dessine une assiette vide"""
        invite_text = self.font_small.render("Plat vide", True, (180, 180, 180))
        invite_rect = invite_text.get_rect(center=(x, y))
        self.screen.blit(invite_text, invite_rect)
        
        plate_icon = self.font_medium.render("🍽️", True, (200, 200, 200))
        icon_rect = plate_icon.get_rect(center=(x, y - 15))
        self.screen.blit(plate_icon, icon_rect)

    def draw_animated_plating(self, asset_manager):
        """Animation d'assemblage"""
        x, y = self.plating_animation['plate_center']
        ingredients = self.plating_animation['ingredients']
        current_index = self.plating_animation['current_ingredient_index']
        progress = self.plating_animation['ingredient_progress']
        
        if not ingredients:
            return
            
        for i in range(current_index):
            if i < len(ingredients):
                ingredient = ingredients[i]
                self.draw_ingredient_with_effects(x, y, ingredient, i, ingredients, asset_manager, is_animated=False)
        
        if current_index < len(ingredients):
            current_ingredient = ingredients[current_index]
            
            drop_height = 50
            current_y = y - 20 - drop_height + (drop_height * progress)
            
            rotation = progress * 360
            
            if progress < 0.8:
                for trail in range(3):
                    trail_progress = progress - (trail + 1) * 0.1
                    if trail_progress > 0:
                        trail_y = y - 20 - drop_height + (drop_height * trail_progress)
                        trail_alpha = int(100 * (1 - trail * 0.3))
                        self.draw_ingredient_graphic(x, trail_y, current_ingredient, 
                                                   current_index, asset_manager, 
                                                   alpha=trail_alpha, rotation=rotation)
            
            if 0.7 < progress < 0.8:
                self.create_plating_sparks(x, y)
            
            self.draw_ingredient_with_effects(x, current_y, current_ingredient, 
                                           current_index, ingredients, asset_manager, 
                                           is_animated=True, rotation=rotation, 
                                           progress=progress)

    def draw_assembled_dish_improved(self, x, y, ingredients, asset_manager):
        """Affiche le plat fini"""
        if not ingredients:
            return
            
        current_time = time.time()
        pulse = math.sin(current_time * 3) * 3
        
        for i, ingredient in enumerate(ingredients):
            self.draw_ingredient_with_effects(x, y, ingredient, i, ingredients, asset_manager, 
                                           is_animated=False, pulse=pulse)

    def draw_ingredient_with_effects(self, x, y, ingredient, index, ingredients_list, asset_manager, 
                                   is_animated=False, rotation=0, progress=1.0, pulse=0):
        """Dessine un ingrédient avec des effets visuels"""
        ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150), "height": 8, "width": 40})
        
        base_height = sum(self.ingredient_config.get(ing, {"height": 8})["height"] 
                         for ing in ingredients_list[:index])
        ing_y = y + 15 - base_height + pulse
        
        shadow_offset = 2
        shadow_alpha = 80 - index * 10
        shadow_surf = pygame.Surface((ing_config["width"] + 10, ing_config["height"] + 5), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, shadow_alpha), 
                          (0, 0, ing_config["width"] + 10, ing_config["height"] + 3))
        self.screen.blit(shadow_surf, (x - ing_config["width"]//2 - 5 + shadow_offset, 
                                     ing_y - ing_config["height"]//2 + shadow_offset))
        
        if is_animated:
            halo_alpha = int(150 * (1 - progress))
            halo_surf = pygame.Surface((ing_config["width"] + 30, ing_config["height"] + 30), pygame.SRCALPHA)
            pygame.draw.ellipse(halo_surf, (*ing_config["color"][:3], halo_alpha), 
                              (0, 0, ing_config["width"] + 30, ing_config["height"] + 30))
            self.screen.blit(halo_surf, (x - ing_config["width"]//2 - 15, 
                                       ing_y - ing_config["height"]//2 - 15))
        
        self.draw_ingredient_graphic(x, ing_y, ingredient, index, asset_manager, 
                                   rotation=rotation if is_animated else 0)

    def draw_ingredient_graphic(self, x, y, ingredient, index, asset_manager, rotation=0, alpha=255):
        """Dessine la représentation graphique d'un ingrédient"""
        ing_config = self.ingredient_config.get(ingredient, {"color": (150, 150, 150), "height": 8, "width": 40})
        
        if asset_manager:
            img = asset_manager.get_ingredient_image(ingredient)
            if img:
                if rotation != 0:
                    img = pygame.transform.rotate(img, rotation)
                
                img_size = (ing_config["width"], ing_config["height"])
                scaled_img = pygame.transform.scale(img, img_size)
                
                if alpha < 255:
                    scaled_img.set_alpha(alpha)
                
                img_rect = scaled_img.get_rect(center=(x, y))
                self.screen.blit(scaled_img, img_rect)
                return
        
        self.draw_ingredient_fallback(x, y, ingredient, ing_config, alpha)

    def draw_ingredient_fallback(self, x, y, ingredient, config, alpha=255):
        """Dessin de fallback avec effets visuels"""
        color = config["color"]
        width = config["width"]
        height = config["height"]
        
        ing_surf = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
        
        if ingredient == 'pain':
            pygame.draw.ellipse(ing_surf, color, (5, 5, width, height))
            pygame.draw.ellipse(ing_surf, (200, 150, 60, alpha), (5, 5, width, height), 2)
            for seed_pos in [(15, 8), (35, 6), (25, 12), (40, 10)]:
                pygame.draw.ellipse(ing_surf, (180, 140, 40, alpha), 
                                  (seed_pos[0], seed_pos[1], 4, 2))
                
        elif ingredient == 'steak':
            pygame.draw.ellipse(ing_surf, color, (5, 5, width, height))
            pygame.draw.ellipse(ing_surf, (120, 60, 30, alpha), (5, 5, width, height), 2)
            for i in range(3):
                pygame.draw.line(ing_surf, (100, 40, 20, alpha), 
                               (10 + i*12, 7), (10 + i*12, height + 3), 2)
                
        elif ingredient == 'fromage':
            pygame.draw.ellipse(ing_surf, color, (5, 5, width, height))
            pygame.draw.ellipse(ing_surf, (220, 200, 70, alpha), (5, 5, width, height), 1)
            for hole_pos in [(15, 8), (30, 7), (25, 10)]:
                pygame.draw.circle(ing_surf, (230, 210, 100, alpha), hole_pos, 3)
                
        elif ingredient == 'tomate':
            pygame.draw.circle(ing_surf, color, (width//2 + 5, height//2 + 5), width//3)
            pygame.draw.circle(ing_surf, (200, 40, 40, alpha), (width//2 + 5, height//2 + 5), width//3, 2)
            pygame.draw.circle(ing_surf, (255, 150, 150, alpha), (width//2, height//3 + 3), 4)
            
        elif ingredient == 'laitue':
            pygame.draw.circle(ing_surf, color, (width//2 + 5, height//2 + 5), width//2.5)
            pygame.draw.circle(ing_surf, (40, 180, 40, alpha), (width//2 + 5, height//2 + 5), width//2.5, 2)
            for angle in [0, 72, 144, 216, 288]:
                leaf_x = width//2 + 5 + math.cos(math.radians(angle)) * (width//3)
                leaf_y = height//2 + 5 + math.sin(math.radians(angle)) * (width//3)
                pygame.draw.ellipse(ing_surf, (70, 220, 70, alpha), 
                                  (leaf_x - 6, leaf_y - 3, 12, 6))
                
        elif ingredient == 'oignon':
            pygame.draw.circle(ing_surf, color, (width//2 + 5, height//2 + 5), width//3)
            pygame.draw.circle(ing_surf, (180, 160, 120, alpha), (width//2 + 5, height//2 + 5), width//3, 2)
            pygame.draw.circle(ing_surf, (220, 200, 180, alpha), (width//2 + 5, height//2 + 5), width//4, 1)
            pygame.draw.circle(ing_surf, (220, 200, 180, alpha), (width//2 + 5, height//2 + 5), width//6, 1)
            
        elif ingredient == 'salade':
            pygame.draw.ellipse(ing_surf, color, (5, 5, width, height))
            pygame.draw.ellipse(ing_surf, (60, 160, 60, alpha), (5, 5, width, height), 2)
            for spot in [(10, 8), (30, 6), (20, 12), (35, 9)]:
                pygame.draw.circle(ing_surf, (100, 220, 100, alpha), spot, 2)
        
        else:
            pygame.draw.ellipse(ing_surf, color, (5, 5, width, height))
            pygame.draw.ellipse(ing_surf, (255, 255, 255, alpha), (5, 5, width, height), 2)
        
        self.screen.blit(ing_surf, (x - width//2 - 5, y - height//2 - 5))

    def create_plating_sparks(self, x, y):
        """Crée des étincelles lors de la pose d'un ingrédient"""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            self.sparkle_particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': (255, 255, 200),
                'size': random.uniform(2, 4)
            })

    def draw_progress_bar(self, x, y, progress, text):
        """Dessine une barre de progression"""
        bar_width = 80
        bar_height = 8
        bar_x = x - bar_width // 2
        bar_y = y
        
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            for i in range(fill_width):
                ratio = i / fill_width
                color = (
                    int(100 + 155 * ratio),
                    int(200 + 55 * (1 - ratio)),
                    100
                )
                pygame.draw.rect(self.screen, color, (bar_x + i, bar_y, 1, bar_height))
        
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=4)
        
        progress_text = self.font_small.render(f"{text}: {int(progress * 100)}%", True, (0, 100, 0))
        text_rect = progress_text.get_rect(center=(x, y + 15))
        self.screen.blit(progress_text, text_rect)

    def draw_service_station(self):
        """Station de service - MÊME COULEUR BRUN CLAIR"""
        current_time = time.time()
        service_rect = pygame.Rect(self.service_area['x'], self.service_area['y'], 
                                   self.service_area['w'], self.service_area['h'])
        
        glow = int(20 + 10 * math.sin(current_time * 2))
        for i in range(3, 0, -1):
            alpha = glow // i
            glow_surf = pygame.Surface((self.service_area['w'] + i*6, self.service_area['h'] + i*6), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 215, 0, alpha), (0, 0, self.service_area['w'] + i*6, self.service_area['h'] + i*6))
            self.screen.blit(glow_surf, (self.service_area['x'] - i*3, self.service_area['y'] - i*3))
        
        # MÊME COULEUR BRUN CLAIR POUR LA COHÉRENCE
        plan_travail_color1 = (180, 150, 120)
        plan_travail_color2 = (160, 130, 100)
        draw_gradient_rect(self.screen, plan_travail_color1, plan_travail_color2, service_rect)
        
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
        
        self.draw_sparkle_particles()

    def draw_delivered_dishes(self, current_time):
        """Dessine les plats livrés"""
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
        """Dessine un mini burger"""
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
        """Dessine une mini salade"""
        pygame.draw.ellipse(surface, (255, 255, 255, alpha), (x - 20, y + 5, 40, 15))
        pygame.draw.circle(surface, (90, 200, 90, alpha), (x, y - 5), 16)
        pygame.draw.circle(surface, (60, 180, 60, alpha), (x, y - 5), 16, 1)
        for offset in [(-8, 0), (8, -3), (0, 5)]:
            pygame.draw.circle(surface, (240, 60, 60, alpha), (x + offset[0], y + offset[1]), 3)

    def add_delivered_dish(self, order_name):
        """Ajoute un plat livré"""
        self.delivered_dishes.append({
            'name': order_name,
            'time': time.time()
        })
        
        center_x = self.service_area['x'] + self.service_area['w'] // 2
        center_y = self.service_area['y'] + 140
        
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 4)
            self.sparkle_particles.append({
                'x': center_x,
                'y': center_y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': (255, 215, 0),
                'size': random.uniform(2, 4)
            })

    def draw_sparkle_particles(self):
        """Dessine les particules d'étincelles"""
        for particle in self.sparkle_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2
            particle['life'] -= 0.02
            
            if particle['life'] <= 0:
                self.sparkle_particles.remove(particle)
                continue
            
            alpha = int(255 * particle['life'])
            size = int(particle['size'] * particle['life'])
            
            if size > 0:
                sparkle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(sparkle_surf, (*particle['color'], alpha), (size, size), size)
                self.screen.blit(sparkle_surf, (int(particle['x'] - size), int(particle['y'] - size)))

    def draw_chef_enhanced(self, bot, asset_manager):
        """Dessine un chef avec effets - CORRIGÉ POUR ACCIDENTS"""
        base_x, base_y = bot.x, bot.y
        current_time = time.time()
        
        # Appliquer les effets d'accident sur le chef
        for accident in self.kitchen_accidents:
            if accident['bot'] == bot:
                accident_progress = accident['progress']
                intensity = accident.get('intensity', 1.0)
                
                if accident['type'] == 'drop_plate':
                    # Secousse violente pour la chute de plat
                    shake_x = math.sin(current_time * 40) * 8 * intensity
                    shake_y = math.sin(current_time * 35) * 5 * intensity
                    base_x += shake_x
                    base_y += shake_y
                    
                elif accident['type'] == 'slip_fall':
                    # Glissade avec chute
                    slip_offset = accident_progress * 80 * intensity
                    base_y += slip_offset
                    base_x += math.sin(accident_progress * math.pi * 3) * 30 * intensity
                
                elif accident['type'] == 'ingredient_spill':
                    # Déséquilibre pour le renversement
                    tilt = math.sin(accident_progress * math.pi * 4) * 20 * intensity
                    base_x += tilt
        
        # [Le reste de la méthode reste identique mais avec gestion d'erreur]
        try:
            if bot.state == "plating" or (bot.state == "going_to_plating" and bot.plating):
                zones = self.get_interaction_zones()
                plating_zone = zones.get('plating', (base_x, base_y))
                base_x, base_y = plating_zone
            
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
            
        except Exception as e:
            print(f"⚠ Erreur dessin chef amélioré: {e}")
    
    def draw_fallback_burger(self, x, y):
        """Dessine un burger de fallback"""
        pygame.draw.circle(self.screen, (220, 170, 90), (x, y + 10), 25)
        pygame.draw.circle(self.screen, (60, 220, 60), (x, y), 23)
        pygame.draw.circle(self.screen, (240, 60, 60), (x, y - 5), 22)
        pygame.draw.circle(self.screen, (160, 90, 60), (x, y - 10), 21)
        pygame.draw.circle(self.screen, (255, 230, 90), (x, y - 15), 24)
        pygame.draw.circle(self.screen, (220, 170, 90), (x, y - 20), 26)
    
    def draw_fallback_salad(self, x, y):
        """Dessine une salade de fallback"""
        pygame.draw.ellipse(self.screen, (255, 255, 255), (x - 25, y + 5, 50, 20))
        pygame.draw.circle(self.screen, (90, 200, 90), (x, y - 5), 22)
        for pos in [(x - 10, y), (x + 10, y - 3), (x, y + 5)]:
            pygame.draw.circle(self.screen, (240, 60, 60), pos, 4)

    def get_interaction_zones(self):
        """Retourne les zones d'interaction"""
        fridge_x = self.storage_area['x'] + self.storage_area['w'] // 2
        fridge_y = self.storage_area['y'] + self.storage_area['h'] + 30
        
        cutting_x = self.work_area['x'] + 55
        cutting_y = self.work_area['y'] + self.work_area['h'] - 20
        
        cooking_x = self.work_area['x'] + 170
        cooking_y = self.work_area['y'] + self.work_area['h'] - 20
        
        plating_x = self.plating_area['x'] + self.plating_area['w'] // 2
        plating_y = self.plating_area['y'] + self.plating_area['h'] - 20
        
        delivery_x = self.service_area['x'] + self.service_area['w'] // 2
        delivery_y = self.service_area['y'] + self.service_area['h'] - 40
        
        return {
            'fridge': (fridge_x, fridge_y),
            'cutting': (cutting_x, cutting_y),
            'cooking': (cooking_x, cooking_y),
            'plating': (plating_x, plating_y),
            'delivery': (delivery_x, delivery_y)
        }

    def render_full_kitchen(self, bot_manager, asset_manager, timer, order_manager=None):
        """Render complet de la cuisine - CORRIGÉ POUR MEILLEURE STABILITÉ"""
        try:
            self.draw_floor()
            
            self.draw_overhead_lamps()
            self.draw_wall_decorations()
            
            self.draw_individual_ingredient_stations(asset_manager)
            self.draw_work_station(asset_manager)
            self.draw_plating_station(asset_manager)
            self.draw_service_station()
            
            if bot_manager and order_manager:
                self.update_stress_system(bot_manager, order_manager)
            
            # METTRE À JOUR LES ACCIDENTS AVANT DE LES DESSINER
            self.update_accidents()
            
            self.update_steam_particles()
            self.draw_steam_particles()
            
            self.update_stress_particles()
            self.draw_stress_effects()
            
            # DESSINER LES ACCIDENTS APRÈS LES AUTRES ÉLÉMENTS
            self.draw_accidents()
            
          # self.draw_stress_meter()
            
            if self.cutting_animation.active:
                self.cutting_animation.update()
                self.cutting_animation.draw()
            
            if bot_manager and hasattr(bot_manager, 'bots'):
                zones = self.get_interaction_zones()
                bins = {}
                if hasattr(self, 'ingredient_positions'):
                    bins = self.ingredient_positions
                
                for bot in bot_manager.bots:
                    try:
                        bot.update_interaction_zones(zones)
                        if bins:
                            bot.update_ingredient_bins(bins)
                        self.draw_chef_enhanced(bot, asset_manager)
                        self.draw_chef_status(bot)
                    except Exception as e:
                        print(f"⚠ Erreur dessin chef {bot.chef_name}: {e}")
                        continue
                    
        except Exception as e:
            print(f"⚠ Erreur rendu cuisine: {e}")
            # Afficher un écran d'erreur simple
            self.screen.fill((50, 50, 50))
            font = pygame.font.Font(None, 36)
            error_text = font.render("Erreur rendu cuisine", True, (255, 50, 50))
            self.screen.blit(error_text, (WIDTH//2 - 150, HEIGHT//2))
            
            # Réinitialiser les systèmes en erreur
            self.accident_particles = []
            self.kitchen_accidents = []

    def check_delivery_trigger(self, bot):
        """Vérifie si un plat est livré"""
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
        """Dessine le statut du chef"""
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


class ChefStressSystem:
    """Système de stress des chefs"""
    
    def __init__(self):
        self.chef_stress_levels = {}
        self.stress_particles = {}
        self.stress_effects = {}
        self.panic_chefs = set()
        self.last_stress_update = {}
        
    def update_chef_stress(self, bot, order_manager, current_time):
        """Met à jour le stress d'un chef"""
        
        if bot.chef_id not in self.chef_stress_levels:
            self.chef_stress_levels[bot.chef_id] = 0
            self.stress_particles[bot.chef_id] = []
            self.stress_effects[bot.chef_id] = {
                'head_shake': 0,
                'body_tremble': 0,
                'sweat_droplets': [],
                'angry_aura': 0,
                'fire_particles': [],
                'last_panic_trigger': 0
            }
        
        stress_delta = 0
        
        if bot.current_order and not bot.current_order.get('completed', False):
            order_time = current_time - bot.current_order.get('start_time', current_time)
            if order_time > 45:
                stress_delta += 25
            elif order_time > 30:
                stress_delta += 15
            elif order_time > 15:
                stress_delta += 8
            elif order_time > 5:
                stress_delta += 3
        
        if bot.waiting_for_ingredient:
            stress_delta += 12
        
        if bot.is_blocked or bot.collision_detected:
            stress_delta += 18
        
        if hasattr(bot, 'recent_mistake') and bot.recent_mistake:
            stress_delta += 30
        
        if bot.preparing:
            stress_delta += 5
        
        if hasattr(order_manager, 'chef_orders'):
            chef_orders = [o for o in order_manager.chef_orders.values() 
                          if o.get('assigned_to') == bot.chef_id]
            if len(chef_orders) > 1:
                stress_delta += 10 * (len(chef_orders) - 1)
        
        if not (bot.current_order or bot.preparing or bot.waiting_for_ingredient):
            stress_delta = -5
        
        current_stress = self.chef_stress_levels[bot.chef_id]
        
        if stress_delta > 0:
            new_stress = min(100, current_stress + stress_delta * 0.15)
        else:
            new_stress = max(0, current_stress + stress_delta * 0.05)
        
        self.chef_stress_levels[bot.chef_id] = new_stress
        
        if new_stress >= 70 and bot.chef_id not in self.panic_chefs:
            self.panic_chefs.add(bot.chef_id)
            self.trigger_chef_panic(bot)
        elif new_stress < 50 and bot.chef_id in self.panic_chefs:
            self.panic_chefs.remove(bot.chef_id)
        
        if new_stress > 30:
            self.create_stress_particles_for_chef(bot, new_stress)
    
    def trigger_chef_panic(self, bot):
        """Déclenche la panique d'un chef"""
        print(f"🚨🚨🚨 {bot.chef_name} EN PANIQUE TOTALE ! 🚨🚨🚨")
        
        effects = self.stress_effects[bot.chef_id]
        effects['last_panic_trigger'] = time.time()
        
        for _ in range(50):
            self.create_panic_effect(bot)
    
    def create_stress_particles_for_chef(self, bot, stress_level):
        """Crée des particules de stress"""
        if stress_level < 30:
            return
        
        num_particles = int((stress_level / 100) * 8)
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(30, 60)
            
            particle = {
                'x': bot.x + math.cos(angle) * distance,
                'y': bot.y + math.sin(angle) * distance,
                'vx': math.cos(angle) * random.uniform(0.5, 1.5),
                'vy': math.sin(angle) * random.uniform(0.5, 1.5),
                'life': random.uniform(0.8, 2.0),
                'max_life': 2.0,
                'type': random.choice(['stress_aura', 'sweat', 'fire']),
                'size': random.uniform(2, 6),
                'color': random.choice([
                    (255, 50, 50),
                    (255, 150, 50),
                    (255, 255, 100),
                ])
            }
            
            if bot.chef_id not in self.stress_particles:
                self.stress_particles[bot.chef_id] = []
            
            self.stress_particles[bot.chef_id].append(particle)
    
    def create_panic_effect(self, bot):
        """Crée un effet de panique"""
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        
        panic_particle = {
            'x': bot.x,
            'y': bot.y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'life': random.uniform(0.5, 1.5),
            'size': random.uniform(4, 10),
            'type': 'panic_burst',
            'color': random.choice([
                (255, 0, 0),
                (255, 100, 0),
            ])
        }
        
        if bot.chef_id not in self.stress_particles:
            self.stress_particles[bot.chef_id] = []
        
        self.stress_particles[bot.chef_id].append(panic_particle)
    
    def update_particles(self, bot):
        """Met à jour les particules"""
        if bot.chef_id not in self.stress_particles:
            return
        
        particles = self.stress_particles[bot.chef_id]
        
        for particle in particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            particle['vy'] += 0.1
            
            particle['life'] -= 0.02
            
            if particle['life'] <= 0:
                particles.remove(particle)
    
    def draw_chef_stress_visual(self, screen, bot, font_small, current_time):
        """Dessine la visualisation du stress"""
        
        stress_level = self.chef_stress_levels.get(bot.chef_id, 0)
        
        if stress_level < 10:
            return
        
        if stress_level > 30:
            aura_radius = 40 + (stress_level / 100) * 30
            aura_alpha = int((stress_level / 100) * 150)
            
            if stress_level < 70:
                aura_color = (255, 150 + int(stress_level), 50)
            else:
                pulse = int(100 + 100 * math.sin(current_time * 8))
                aura_color = (255, pulse, 50)
            
            aura_surf = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surf, (*aura_color, aura_alpha // 2), 
                             (aura_radius, aura_radius), aura_radius)
            screen.blit(aura_surf, (int(bot.x - aura_radius), int(bot.y - aura_radius)))
        
        effects = self.stress_effects.get(bot.chef_id, {})
        
        if stress_level > 50:
            effects['body_tremble'] = math.sin(current_time * 15) * (stress_level / 100) * 4
        
        if stress_level > 40:
            sweat_count = int((stress_level / 100) * 5)
            sweat_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            
            for i in range(sweat_count):
                sweat_x = 10 + math.sin(current_time * 3 + i) * 5
                sweat_y = 5 + (i * 3)
                
                pygame.draw.circle(sweat_surf, (150, 200, 255, 200), 
                                 (int(sweat_x), int(sweat_y)), 2)
                pygame.draw.circle(sweat_surf, (200, 230, 255, 150), 
                                 (int(sweat_x), int(sweat_y)), 2, 1)
            
            screen.blit(sweat_surf, (int(bot.x - 10), int(bot.y - 45)))
        
        stress_icons = []
        
        if stress_level > 30:
            stress_icons.append("😰")
        if stress_level > 50:
            stress_icons.append("😠")
        if stress_level > 70:
            stress_icons.append("🔥")
        if stress_level > 85:
            stress_icons.append("💥")
        
        if stress_icons:
            icon_text = " ".join(stress_icons)
            icon_surf = font_small.render(icon_text, True, (255, 100, 100))
            
            bounce = abs(math.sin(current_time * 6)) * 5
            screen.blit(icon_surf, (int(bot.x - 25), int(bot.y - 70 - bounce)))
        
        self.update_particles(bot)
        
        if bot.chef_id in self.stress_particles:
            for particle in self.stress_particles[bot.chef_id]:
                alpha = int(200 * (particle['life'] / particle['max_life']))
                size = int(particle['size'] * (particle['life'] / particle['max_life']))
                
                if size > 0:
                    particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    
                    if particle['type'] == 'stress_aura':
                        pygame.draw.circle(particle_surf, (*particle['color'], alpha), 
                                         (size, size), size)
                    
                    elif particle['type'] == 'sweat':
                        pygame.draw.circle(particle_surf, (150, 200, 255, alpha), 
                                         (size, size), size)
                    
                    elif particle['type'] == 'fire':
                        pygame.draw.circle(particle_surf, (*particle['color'], alpha), 
                                         (size, size), size)
                        pygame.draw.circle(particle_surf, (255, 255, 150, alpha // 2), 
                                         (size, size), size // 2)
                    
                    elif particle['type'] == 'panic_burst':
                        points = []
                        for i in range(6):
                            angle = (i / 6) * 2 * math.pi
                            px = size + math.cos(angle) * size
                            py = size + math.sin(angle) * size
                            points.append((px, py))
                        pygame.draw.polygon(particle_surf, (*particle['color'], alpha), points)
                    
                    screen.blit(particle_surf, (int(particle['x'] - size), int(particle['y'] - size)))
        
        self.draw_chef_stress_bar(screen, bot, stress_level, current_time, font_small)
    
    def draw_chef_stress_bar(self, screen, bot, stress_level, current_time, font_small):
        """Dessine la barre de stress personnelle"""
        
        bar_width = 50
        bar_height = 6
        bar_x = int(bot.x - bar_width // 2)
        bar_y = int(bot.y + 35)
        
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), 
                        border_radius=3)
        
        if stress_level < 30:
            bar_color = (100, 200, 100)
        elif stress_level < 60:
            bar_color = (255, 200, 50)
        elif stress_level < 80:
            bar_color = (255, 100, 50)
        else:
            pulse = int(100 + 155 * math.sin(current_time * 8))
            bar_color = (255, pulse // 2, 50)
        
        fill_width = int((stress_level / 100) * bar_width)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height), 
                        border_radius=3)
        
        border_color = (255, 255, 255) if stress_level > 70 else (200, 200, 200)
        pygame.draw.rect(screen, border_color, (bar_x, bar_y, bar_width, bar_height), 
                        2, border_radius=3)
        
        stress_text = font_small.render(f"{int(stress_level)}%", True, 
                                       (255, 255, 255) if stress_level > 50 else (0, 0, 0))
        text_rect = stress_text.get_rect(center=(int(bot.x), int(bar_y - 8)))
        screen.blit(stress_text, text_rect)