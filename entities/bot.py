"""
Bot entity - Système multi-agents VRAIMENT COMPÉTITIF
✅ Chaque chef prend SA PROPRE commande
✅ Travail simultané - AUCUNE attente
✅ Va DIRECTEMENT au bac de l'ingrédient spécifique 🎯
✅ Utilise OrderManager pour gérer les commandes multiples
"""
import time
import math
import game_state

class BotManager:
    """Gestionnaire pour coordonner les bots EN VRAIE COMPÉTITION"""
    def __init__(self):
        self.bots = []
        self.bot_scores = {}
        self.bot_stats = {}
        self.competition_mode = True
        self.frame_counter = 0
        
    def add_bot(self, bot):
        """Ajoute un bot à la compétition"""
        self.bots.append(bot)
        self.bot_scores[id(bot)] = 0
        self.bot_stats[id(bot)] = {
            "dishes_delivered": 0,
            "ingredients_prepared": 0,
            "time_worked": 0,
            "efficiency": 0
        }
        bot.bot_id = id(bot)
        
    def try_claim_order(self, bot):
        """Un bot essaie de prendre une commande de la file"""
        if not hasattr(game_state, 'order_manager'):
            return False
        
        # Vérifier si le bot a déjà une commande
        if game_state.order_manager.get_chef_order(bot.bot_id):
            return False
        
        # Essayer de prendre une commande
        order_info = game_state.order_manager.assign_order_to_chef(bot.bot_id, bot.chef_name)
        
        if order_info:
            print(f"🏁 {bot.chef_name} PREND une commande: {order_info['order_data']['name']}")
            return True
        
        return False
    
    def complete_order(self, bot):
        """Un bot complète SA commande et gagne des points"""
        if not hasattr(game_state, 'order_manager'):
            return 0
        
        completion_data = game_state.order_manager.complete_chef_order(bot.bot_id)
        
        if completion_data:
            # Calculer le score
            duration = completion_data['duration']
            base_score = 100
            speed_bonus = max(0, int((30 - duration) * 5))  # Bonus si rapide
            total_score = base_score + speed_bonus
            
            # Attribuer le score
            self.bot_scores[bot.bot_id] += total_score
            self.bot_stats[bot.bot_id]["dishes_delivered"] += 1
            
            # Score global
            game_state.score += total_score
            
            print(f"🎉 {bot.chef_name} a livré {completion_data['order_name']} et gagne {total_score} points!")
            print(f"   Score {bot.chef_name}: {self.bot_scores[bot.bot_id]}")
            
            return total_score
        
        return 0
    
    def update(self):
        """Met à jour tous les bots - CHACUN travaille sur SA commande"""
        self.frame_counter += 1
        
        # IMPORTANT: Tous les bots essaient de prendre une commande s'ils sont libres
        for bot in self.bots:
            if bot.is_available():
                self.try_claim_order(bot)
        
        # Mettre à jour tous les bots
        for bot in self.bots:
            bot.update()
        
        # Debug périodique
        if self.frame_counter % 120 == 0:
            print(f"\n🔍 DEBUG COMPÉTITION (frame {self.frame_counter}):")
            
            if hasattr(game_state, 'order_manager'):
                status = game_state.order_manager.get_status_summary()
                print(f"   📋 Commandes disponibles: {status['available_orders']}")
                print(f"   ⚙️ Commandes actives: {status['active_orders']}")
                print(f"   ✅ Commandes complétées: {status['completed_orders']}")
            
            for bot in self.bots:
                print(f"   {bot.chef_name}:")
                print(f"      - État: {bot.state}")
                print(f"      - Position: ({bot.x:.1f}, {bot.y:.1f})")
                
                if hasattr(game_state, 'order_manager'):
                    progress = game_state.order_manager.get_chef_progress(bot.bot_id)
                    if progress:
                        print(f"      - Commande: {progress['order_name']}")
                        print(f"      - Progression: {progress['prepared']}/{progress['required']}")
    
    def draw_all(self, screen):
        """Dessine tous les bots"""
        for bot in self.bots:
            bot.draw_chef(screen)
    
    def get_leaderboard(self):
        """Retourne le classement"""
        leaderboard = []
        for bot in self.bots:
            leaderboard.append({
                "name": bot.chef_name,
                "score": self.bot_scores[bot.bot_id],
                "stats": self.bot_stats[bot.bot_id]
            })
        return sorted(leaderboard, key=lambda x: x["score"], reverse=True)


class Bot:
    def __init__(self, x=350, y=400, chef_name="Chef", color_variant=0):
        self.x = x
        self.y = y
        self.inv = None
        self.preparing = None
        self.plating = False
        self.prep_time = 0
        self.plate_time = 0
        self.target_x = x
        self.target_y = y
        self.state = "idle"
        self.animation_time = 0
        self.bot_id = None
        self.frame_debug_counter = 0
        
        self.my_order = None  # Référence à MA commande
        self.motivation = 100
        self.competitiveness = 0.5 + (color_variant * 0.3)
        
        self.BOT_SPEED = 3 + (color_variant * 0.5)
        self.prep_times = {
            "laitue": 1.0,
            "tomate": 1.2,
            "pain": 0.8,
            "steak": 2.0,
            "fromage": 0.5
        }
        self.PLATING_TIME = 2.0
        
        self.interaction_zones = {
            'fridge_access': (150, 350),
            'cutting_board': (350, 270),
            'plating_station': (525, 420),
            'delivery': (670, 330)
        }
        
        # 🎯 POSITIONS PRÉCISES DES BACS D'INGRÉDIENTS
        self.ingredient_bins = {
            'laitue': (120, 200),      # Bac de laitue
            'tomate': (120, 280),      # Bac de tomates
            'pain': (120, 360),        # Bac de pain
            'steak': (120, 440),       # Bac de steak
            'fromage': (120, 520)      # Bac de fromage
        }

        self.chef_name = chef_name
        self.chef_hat_height = 25
        
        color_variants = [
            {
                "body": (255, 240, 240),
                "hat": (255, 200, 200),
                "pants": (80, 20, 20),
                "skin": (255, 220, 177)
            },
            {
                "body": (240, 240, 255),
                "hat": (200, 200, 255),
                "pants": (20, 20, 80),
                "skin": (245, 200, 160)
            }
        ]
        
        variant = color_variants[color_variant % len(color_variants)]
        self.chef_body_color = variant["body"]
        self.chef_hat_color = variant["hat"]
        self.chef_pants_color = variant["pants"]
        self.chef_skin_color = variant["skin"]

    def update_interaction_zones(self, zones):
        """Met à jour les zones d'interaction"""
        self.interaction_zones = zones
    
    def update_ingredient_bins(self, bins):
        """Met à jour les positions des bacs d'ingrédients"""
        self.ingredient_bins = bins

    def distance_to(self, target_pos):
        if isinstance(target_pos, dict):
            x2 = target_pos.get("x", 0) + target_pos.get("w", 0) // 2
            y2 = target_pos.get("y", 0) + target_pos.get("h", 0) // 2
        else:
            x2, y2 = target_pos
        return ((self.x - x2)**2 + (self.y - y2)**2)**0.5

    def is_at_target(self):
        distance = self.distance_to((self.target_x, self.target_y))
        return distance < 50

    def is_available(self):
        """Vérifie si le bot est disponible pour prendre une nouvelle commande"""
        has_order = False
        if hasattr(game_state, 'order_manager'):
            has_order = game_state.order_manager.get_chef_order(self.bot_id) is not None
        
        return (self.state == "idle" and 
                not has_order and
                not self.inv and 
                not self.preparing and 
                not self.plating)

    def get_my_order(self):
        """Récupère MA commande actuelle"""
        if not hasattr(game_state, 'order_manager'):
            return None
        return game_state.order_manager.get_chef_order(self.bot_id)

    def get_next_needed_ingredient(self):
        """Retourne le prochain ingrédient nécessaire pour MA commande"""
        if not hasattr(game_state, 'order_manager'):
            return None
        
        progress = game_state.order_manager.get_chef_progress(self.bot_id)
        if not progress or not progress['ingredients_needed']:
            return None
        
        return progress['ingredients_needed'][0]

    def are_all_ingredients_ready(self):
        """Vérifie si tous MES ingrédients sont prêts"""
        if not hasattr(game_state, 'order_manager'):
            return False
        
        progress = game_state.order_manager.get_chef_progress(self.bot_id)
        if not progress:
            return False
        
        return progress['is_ready']

    def update_logic(self):
        """Logique principale - Chaque chef travaille sur SA commande"""
        
        # Si je n'ai pas de commande, je suis idle
        my_order = self.get_my_order()
        if not my_order:
            if self.state != "idle":
                self.state = "idle"
                self.target_x = 250 if (self.bot_id or 0) % 2 == 0 else 550
                self.target_y = 450
            return
        
        # Je travaille sur MA commande
        if self.preparing:
            self.state = "cutting"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            
            prep_time = self.prep_times.get(self.preparing, 1.5)
            prep_time *= (1.0 - (self.motivation / 200))
            
            if time.time() - self.prep_time >= prep_time:
                # Ajouter à MA commande
                if hasattr(game_state, 'order_manager'):
                    game_state.order_manager.add_ingredient_to_chef(self.bot_id, self.preparing)
                
                print(f"✓ {self.chef_name} a fini: {self.preparing}")
                self.preparing = None
                
                if self.are_all_ingredients_ready():
                    self.state = "ready_to_plate"
                else:
                    self.state = "need_next_ingredient"
            return
        
        # Dressage de MON plat
        if self.plating:
            self.state = "plating"
            self.target_x, self.target_y = self.interaction_zones['plating_station']
            
            if time.time() - self.plate_time >= self.PLATING_TIME:
                # Marquer comme platté
                if hasattr(game_state, 'order_manager'):
                    game_state.order_manager.set_chef_plated(self.bot_id, True)
                
                self.plating = False
                self.inv = "plated_dish"
                print(f"✅ {self.chef_name} a dressé son plat!")
                self.state = "ready_to_deliver"
            return
        
        # États de transition
        if self.state == "ready_to_plate":
            self.target_x, self.target_y = self.interaction_zones['plating_station']
            self.state = "going_to_plating"
            return
        
        if self.state == "ready_to_deliver":
            self.target_x, self.target_y = self.interaction_zones['delivery']
            self.state = "going_to_delivery"
            print(f"🚚 {self.chef_name} va livrer!")
            return
        
        if self.inv and self.inv != "plated_dish":
            self.state = "going_to_board"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            return
        
        if not self.inv and not self.preparing and not self.plating:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                # 🎯 VA DIRECTEMENT AU BAC DE L'INGRÉDIENT SPÉCIFIQUE
                if needed_ingredient in self.ingredient_bins:
                    self.target_x, self.target_y = self.ingredient_bins[needed_ingredient]
                    self.state = f"going_to_{needed_ingredient}_bin"
                    print(f"🎯 {self.chef_name} va au bac de {needed_ingredient} à ({self.target_x}, {self.target_y})")
                else:
                    # Fallback si le bac n'existe pas
                    self.state = "going_to_fridge"
                    self.target_x, self.target_y = self.interaction_zones['fridge_access']
                    print(f"⚠️ {self.chef_name} va au frigo générique pour: {needed_ingredient}")
            elif self.are_all_ingredients_ready():
                self.state = "ready_to_plate"

    def handle_interactions(self):
        if not self.is_at_target():
            return
        
        # 🎯 GESTION DES BACS D'INGRÉDIENTS SPÉCIFIQUES
        if self.state.startswith("going_to_") and self.state.endswith("_bin") and not self.inv:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                self.inv = needed_ingredient
                print(f"✓ {self.chef_name} a pris {needed_ingredient} du bac spécifique!")
                self.state = "going_to_board"
        
        # Fallback pour ancien système
        elif self.state == "going_to_fridge" and not self.inv:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                self.inv = needed_ingredient
                print(f"✓ {self.chef_name} a pris: {needed_ingredient}")
                self.state = "going_to_board"
        
        elif self.state == "going_to_board" and self.inv and self.inv != "plated_dish":
            self.preparing = self.inv
            self.prep_time = time.time()
            print(f"👨‍🍳 {self.chef_name} prépare: {self.preparing}")
            self.inv = None
            self.state = "cutting"
        
        elif self.state == "going_to_plating" and not self.plating:
            if self.are_all_ingredients_ready():
                self.plating = True
                self.plate_time = time.time()
                print(f"🍽️ {self.chef_name} assemble!")
                self.state = "plating"
        
        elif self.state == "going_to_delivery" and self.inv == "plated_dish":
            print(f"🏆 {self.chef_name} LIVRE ET MARQUE DES POINTS!")
            
            # Appeler le manager pour attribuer les points
            if hasattr(game_state, 'bot_manager'):
                game_state.bot_manager.complete_order(self)
            
            self.inv = None
            self.state = "idle"
            self.motivation = min(100, self.motivation + 10)

    def update_movement(self):
        """Met à jour le mouvement"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        speed = self.BOT_SPEED * (0.8 + self.motivation / 500)
        
        if distance > 5:
            if distance > 0:
                move_x = (dx / distance) * speed
                move_y = (dy / distance) * speed
                self.x += move_x
                self.y += move_y
        
        self.x = max(60, min(740, self.x))
        self.y = max(120, min(540, self.y))
        self.animation_time += 0.04
        self.frame_debug_counter += 1

    def update(self, dt=0):
        self.update_logic()
        self.update_movement()
        self.handle_interactions()

    def get_state_color(self):
        colors = {
            "idle": (200, 200, 200),
            "going_to_fridge": (100, 150, 255),
            "going_to_board": (255, 165, 0),
            "cutting": (255, 100, 100),
            "going_to_plating": (255, 150, 255),
            "plating": (200, 100, 255),
            "going_to_delivery": (100, 255, 100)
        }
        return colors.get(self.state, (255, 255, 255))

    def get_state_text(self):
        my_order = self.get_my_order()
        if not my_order:
            return "Cherche commande"
        
        order_name = my_order['order_data']['name']
        
        # 🎯 Gestion des états de bacs spécifiques
        if self.state.startswith("going_to_") and self.state.endswith("_bin"):
            ingredient = self.state.replace("going_to_", "").replace("_bin", "")
            return f"Va chercher {ingredient} 🎯"
        
        state_texts = {
            "idle": f"Travaille sur {order_name}",
            "going_to_fridge": f"Va chercher ({order_name})",
            "going_to_board": f"Va préparer ({order_name})",
            "cutting": f"Découpe {self.preparing or ''}",
            "going_to_plating": f"Va dresser {order_name}",
            "plating": f"Dresse {order_name}",
            "going_to_delivery": f"🏆 Va livrer {order_name}!"
        }
        return state_texts.get(self.state, self.state)

    def draw_chef(self, screen):
        """Dessine le chef cuisinier"""
        import pygame
        
        alpha = int(150 + (self.motivation * 1.05))
        
        body_rect = pygame.Rect(self.x - 12, self.y - 15, 24, 30)
        pygame.draw.rect(screen, self.chef_body_color, body_rect)
        pygame.draw.rect(screen, (200, 200, 200), body_rect, 2)
        
        pants_rect = pygame.Rect(self.x - 10, self.y + 10, 20, 15)
        pygame.draw.rect(screen, self.chef_pants_color, pants_rect)
        
        pygame.draw.circle(screen, self.chef_skin_color, (int(self.x), int(self.y - 25)), 10)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y - 25)), 10, 2)
        
        hat_rect = pygame.Rect(self.x - 8, self.y - 45, 16, self.chef_hat_height)
        pygame.draw.rect(screen, self.chef_hat_color, hat_rect)
        pygame.draw.rect(screen, (180, 180, 180), hat_rect, 2)
        
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x - 3), int(self.y - 27)), 2)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 3), int(self.y - 27)), 2)
        
        if self.state == "cutting" and self.preparing:
            arm_offset = int(math.sin(self.animation_time * 8) * 3)
            pygame.draw.line(screen, self.chef_skin_color, 
                           (int(self.x + 12), int(self.y - 10)), 
                           (int(self.x + 18), int(self.y - 5 + arm_offset)), 3)
        
        # ✅ INGRÉDIENTS PLUS VISIBLES
        if self.inv and self.inv != "plated_dish":
            ingredient_colors = {
                "laitue": (0, 255, 0),
                "tomate": (255, 0, 0),
                "pain": (222, 184, 135),
                "steak": (139, 69, 19),
                "fromage": (255, 255, 0)
            }
            color = ingredient_colors.get(self.inv, (255, 255, 255))
            
            # Animation de flottement
            bob = math.sin(self.animation_time * 5) * 2
            
            # Ombre portée
            shadow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surf, (0, 0, 0, 100), (10, 10), 9)
            screen.blit(shadow_surf, (int(self.x + 12), int(self.y - 8 + bob)))
            
            # Ingrédient avec bordure épaisse
            pygame.draw.circle(screen, color, (int(self.x + 20), int(self.y - 10 + bob)), 8)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 20), int(self.y - 10 + bob)), 8, 2)
            
            # Effet de brillance
            glow_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 255, 150), (4, 4), 3)
            screen.blit(glow_surf, (int(self.x + 13), int(self.y - 17 + bob)))
        
        elif self.inv == "plated_dish":
            glow = int(abs(math.sin(self.animation_time * 4)) * 50)
            pygame.draw.circle(screen, (240, 240, 240), (int(self.x + 15), int(self.y - 5)), 8)
            pygame.draw.circle(screen, (200 + glow, 200 + glow, 200), (int(self.x + 15), int(self.y - 5)), 8, 2)
            pygame.draw.circle(screen, (150, 100, 50), (int(self.x + 15), int(self.y - 5)), 5)
        
        import pygame.font
        font = pygame.font.Font(None, 16)
        
        name_text = self.chef_name
        if hasattr(game_state, 'bot_manager') and self.bot_id in game_state.bot_manager.bot_scores:
            score = game_state.bot_manager.bot_scores[self.bot_id]
            name_text = f"{self.chef_name} ({score})"
        
        name_surf = font.render(name_text, True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(int(self.x), int(self.y + 35)))
        
        # Couleur selon s'il a une commande
        my_order = self.get_my_order()
        if my_order:
            bg_color = (0, 100, 0, 180)  # Vert = travaille
        else:
            bg_color = (100, 100, 0, 180)  # Jaune = cherche commande
            
        bg_rect = name_rect.inflate(6, 3)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surf.fill(bg_color)
        screen.blit(bg_surf, bg_rect)
        screen.blit(name_surf, name_rect)

    def get_debug_info(self):
        return {
            "name": self.chef_name,
            "position": (int(self.x), int(self.y)),
            "state": self.state,
            "inventory": self.inv,
            "preparing": self.preparing,
            "has_order": self.get_my_order() is not None,
            "motivation": self.motivation
        }

    def get_position(self):
        return (self.x, self.y)
    
    def get_state(self):
        task_type = "idle"
        if self.inv == "plated_dish":
            task_type = "delivery"
        elif self.inv or self.preparing:
            task_type = "ingredient"
        elif self.plating:
            task_type = "plating"
        
        return {
            "position": (self.x, self.y),
            "state": self.state,
            "current_task": {"type": task_type},
            "interaction_timer": 0.0
        }