"""
Bot entity - Corrections pour la livraison des plats
"""
import time
import math
import game_state

class Bot:
    def __init__(self, x=350, y=400):
        # LOGIQUE IDENTIQUE - ne pas toucher
        self.x = x
        self.y = y
        self.inv = None  
        self.preparing = None  
        self.plating = False  
        self.prep_time = 0
        self.plate_time = 0
        self.prep_position = (0, 0)
        self.target_x = x
        self.target_y = y
        self.happiness = 100
        self.state = "idle"
        self.animation_time = 0
        
        self.BOT_SPEED = 3
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

        # NOUVELLES PROPRIÉTÉS VISUELLES UNIQUEMENT
        self.chef_name = "Chef Marcel"
        self.chef_hat_height = 25
        self.chef_body_color = (255, 255, 255)
        self.chef_hat_color = (240, 240, 240)
        self.chef_pants_color = (50, 50, 50)
        self.chef_skin_color = (255, 220, 177)

    # CHANGEMENT 1: Zone d'interaction mise à jour avec logs
    def update_interaction_zones(self, zones):
        """Met à jour les zones d'interaction et affiche les coordonnées"""
        self.interaction_zones = zones
        print(f"\n🗺️ ZONES D'INTERACTION MISES À JOUR:")
        for name, coords in zones.items():
            print(f"   - {name}: {coords}")
        print()

    def distance_to(self, target_pos):
        if isinstance(target_pos, dict):
            x2 = target_pos.get("x", 0) + target_pos.get("w", 0) // 2
            y2 = target_pos.get("y", 0) + target_pos.get("h", 0) // 2
        else:
            x2, y2 = target_pos
        return ((self.x - x2)**2 + (self.y - y2)**2)**0.5

    # CHANGEMENT 2: Augmentation de la tolérance
    def is_at_target(self):
        distance = self.distance_to((self.target_x, self.target_y))
        # AUGMENTÉ DE 30 À 50 pour une meilleure détection
        is_at = distance < 50
        
        # Debug pour la livraison
        if self.state == "going_to_delivery" and not is_at:
            print(f"🚚 En route vers livraison. Distance: {distance:.1f} (besoin < 50)")
        
        return is_at

    def get_next_needed_ingredient(self):
        if not game_state.current_order_name:
            return None
            
        if hasattr(game_state, 'available_ingredients'):
            recipe = game_state.available_ingredients.get(game_state.current_order_name, [])
        else:
            recipes = {
                "salade": ["laitue", "tomate"],
                "burger": ["pain", "steak", "laitue", "tomate"],
                "sandwich": ["pain", "fromage", "tomate"]
            }
            recipe = recipes.get(game_state.current_order_name, [])
        
        for ingredient in recipe:
            if ingredient not in game_state.prepared_ingredients:
                return ingredient
        return None

    def are_all_ingredients_ready(self):
        if not game_state.current_order_name:
            return False
            
        if hasattr(game_state, 'available_ingredients'):
            recipe = game_state.available_ingredients.get(game_state.current_order_name, [])
        else:
            recipes = {
                "salade": ["laitue", "tomate"],
                "burger": ["pain", "steak", "laitue", "tomate"],
                "sandwich": ["pain", "fromage", "tomate"]
            }
            recipe = recipes.get(game_state.current_order_name, [])
        
        return sorted(game_state.prepared_ingredients) == sorted(recipe)

    def update_logic(self):
        print(f"👨‍🍳 {self.chef_name} état: {self.state}, Position: ({int(self.x)}, {int(self.y)})")
        print(f"👨‍🍳 Commande actuelle: {game_state.current_order_name}")
        print(f"👨‍🍳 Ingrédients préparés: {game_state.prepared_ingredients}")
        print(f"👨‍🍳 Plat sur assiette: {getattr(game_state, 'plated_dish', None)}")
        
        if not game_state.current_order_name:
            self.state = "idle"
            self.target_x, self.target_y = (400, 400)
            return
        
        if self.preparing:
            self.state = "cutting"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            
            prep_time = self.prep_times.get(self.preparing, 1.5)
            if time.time() - self.prep_time >= prep_time:
                game_state.prepared_ingredients.append(self.preparing)
                print(f"✓ Chef a fini de préparer: {self.preparing}")
                self.preparing = None
                
                if self.are_all_ingredients_ready():
                    self.state = "ready_to_plate"
                    print("🍽️ Tous les ingrédients prêts, le chef va assembler le plat!")
                else:
                    self.state = "need_next_ingredient"
                    print(f"👨‍🍳 Prochain ingrédient nécessaire: {self.get_next_needed_ingredient()}")
            return
        
        if self.plating:
            self.state = "plating"
            self.target_x, self.target_y = self.interaction_zones['plating_station']
            
            if time.time() - self.plate_time >= self.PLATING_TIME:
                game_state.plated_dish = game_state.current_order_name
                self.plating = False
                self.inv = "plated_dish"
                print(f"✅ Chef a fini d'assembler le plat: {game_state.current_order_name}")
                self.state = "ready_to_deliver"
            return
        
        if self.state == "ready_to_plate":
            self.target_x, self.target_y = self.interaction_zones['plating_station']
            self.state = "going_to_plating"
            return
        
        if self.state == "ready_to_deliver":
            self.target_x, self.target_y = self.interaction_zones['delivery']
            self.state = "going_to_delivery"
            print(f"🚚 Chef se dirige vers la livraison: {self.interaction_zones['delivery']}")
            return
        
        if self.inv and self.inv != "plated_dish":
            self.state = "going_to_board"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            print(f"👨‍🍳 Le chef va découper: {self.inv}")
            return
        
        if not self.inv and not self.preparing and not self.plating:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                self.state = "going_to_fridge"
                self.target_x, self.target_y = self.interaction_zones['fridge_access']
                print(f"👨‍🍳 Le chef va chercher: {needed_ingredient}")
            elif self.are_all_ingredients_ready():
                self.state = "ready_to_plate"
        
        if self.state == "idle" and game_state.current_order_name:
            self.state = "need_next_ingredient"

    # CHANGEMENT 3: Logs de debug détaillés
    def handle_interactions(self):
        if not self.is_at_target():
            dist = self.distance_to((self.target_x, self.target_y))
            if self.state in ["going_to_delivery", "going_to_plating", "going_to_board", "going_to_fridge"]:
                print(f"⏳ {self.state}: Pas encore arrivé. Distance: {dist:.1f}, Cible: ({self.target_x}, {self.target_y})")
            return
        
        print(f"✅ Arrivé à destination pour état: {self.state}")
            
        if self.state == "going_to_fridge" and not self.inv:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                self.inv = needed_ingredient
                print(f"✓ Chef a pris: {needed_ingredient}")
                self.state = "going_to_board"
        
        elif self.state == "going_to_board" and self.inv and self.inv != "plated_dish":
            self.preparing = self.inv
            self.prep_time = time.time()
            self.prep_position = (self.interaction_zones['cutting_board'][0] + 50, 
                                 self.interaction_zones['cutting_board'][1] - 50)
            print(f"👨‍🍳 Le chef commence à préparer: {self.preparing}")
            self.inv = None
            self.state = "cutting"
        
        elif self.state == "going_to_plating" and not self.plating:
            if self.are_all_ingredients_ready():
                self.plating = True
                self.plate_time = time.time()
                print(f"🍽️ Le chef commence à assembler le plat: {game_state.current_order_name}")
                self.state = "plating"
            else:
                print("⚠️ Pas tous les ingrédients prêts pour l'assemblage!")
                self.state = "need_next_ingredient"
        
        # CHANGEMENT 4: Debug détaillé pour la livraison
        elif self.state == "going_to_delivery" and self.inv == "plated_dish":
            print(f"🚚 TENTATIVE DE LIVRAISON!")
            print(f"   - Position bot: ({self.x:.1f}, {self.y:.1f})")
            print(f"   - Cible: ({self.target_x}, {self.target_y})")
            print(f"   - Distance: {self.distance_to((self.target_x, self.target_y)):.1f}")
            print(f"   - Inventaire: {self.inv}")
            print(f"   - plated_dish dans game_state: {getattr(game_state, 'plated_dish', None)}")
            
            if hasattr(game_state, 'plated_dish') and game_state.plated_dish:
                dish_name = game_state.plated_dish
                recipe_length = len(game_state.prepared_ingredients)
                
                base_score = recipe_length * 50
                combo_bonus = game_state.combo * 10
                plating_bonus = 25
                total_score = base_score + combo_bonus + plating_bonus
                
                game_state.score += total_score
                game_state.combo += 1
                
                print(f"🎉🎉🎉 Chef a livré {dish_name} avec assiette! +{total_score} points")
                print(f"Score total: {game_state.score}, Combo: {game_state.combo}")
                
                game_state.current_order_name = None
                game_state.prepared_ingredients.clear()
                if hasattr(game_state, 'plated_dish'):
                    game_state.plated_dish = None
                self.inv = None
                self.state = "idle"
                self.target_x, self.target_y = (400, 400)
            else:
                print("❌ ERREUR: Pas de plat à livrer dans game_state!")
                print(f"   - hasattr plated_dish: {hasattr(game_state, 'plated_dish')}")
                if hasattr(game_state, 'plated_dish'):
                    print(f"   - Valeur plated_dish: {game_state.plated_dish}")
                self.state = "idle"

    def update_movement(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        if abs(dx) > 3:
            self.x += self.BOT_SPEED if dx > 0 else -self.BOT_SPEED
        if abs(dy) > 3:
            self.y += self.BOT_SPEED if dy > 0 else -self.BOT_SPEED
        
        self.x = max(60, min(740, self.x))
        self.y = max(120, min(540, self.y))
        
        self.animation_time += 0.04

    def update(self, dt=0):
        self.update_logic()
        self.update_movement()
        self.handle_interactions()

    def get_state_color(self):
        colors = {
            "idle": (255, 255, 255),
            "going_to_fridge": (100, 150, 255),
            "going_to_board": (255, 165, 0),
            "cutting": (255, 100, 100),
            "going_to_plating": (255, 150, 255),
            "plating": (200, 100, 255),
            "going_to_delivery": (100, 255, 100),
            "ready_to_plate": (255, 200, 100),
            "ready_to_deliver": (255, 215, 0),
            "waiting_for_ingredient": (255, 100, 255)
        }
        return colors.get(self.state, (255, 255, 255))

    def get_state_text(self):
        state_texts = {
            "idle": "Se repose",
            "going_to_fridge": "Va au stockage", 
            "going_to_board": "Va préparer",
            "cutting": "Découpe les ingrédients",
            "going_to_plating": "Va au dressage",
            "plating": "Dresse le plat",
            "going_to_delivery": "Va servir",
            "ready_to_plate": "Prêt à dresser",
            "ready_to_deliver": "Prêt à servir",
            "waiting_for_ingredient": "Attend un ingrédient",
            "need_next_ingredient": "Cherche un ingrédient"
        }
        return state_texts.get(self.state, self.state)

    def draw_chef(self, screen):
        """Dessine le chef cuisinier au lieu du bot basique"""
        import pygame
        
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
        
        if self.inv and self.inv != "plated_dish":
            ingredient_colors = {
                "laitue": (0, 255, 0),
                "tomate": (255, 0, 0),
                "pain": (222, 184, 135),
                "steak": (139, 69, 19),
                "fromage": (255, 255, 0)
            }
            color = ingredient_colors.get(self.inv, (255, 255, 255))
            pygame.draw.circle(screen, color, (int(self.x + 15), int(self.y - 5)), 5)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 15), int(self.y - 5)), 5, 1)
        
        elif self.inv == "plated_dish":
            pygame.draw.circle(screen, (240, 240, 240), (int(self.x + 15), int(self.y - 5)), 8)
            pygame.draw.circle(screen, (200, 200, 200), (int(self.x + 15), int(self.y - 5)), 8, 2)
            pygame.draw.circle(screen, (150, 100, 50), (int(self.x + 15), int(self.y - 5)), 5)

    def get_debug_info(self):
        return {
            "position": (int(self.x), int(self.y)),
            "target": (int(self.target_x), int(self.target_y)),
            "state": self.state,
            "inventory": self.inv,
            "preparing": self.preparing,
            "plating": self.plating,
            "distance_to_target": round(self.distance_to((self.target_x, self.target_y)), 1),
            "next_needed": self.get_next_needed_ingredient(),
            "all_ingredients_ready": self.are_all_ingredients_ready(),
            "plated_dish": getattr(game_state, 'plated_dish', None),
            "chef_name": self.chef_name
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
        elif self.state in ["going_to_plating", "ready_to_plate"]:
            task_type = "plating"
        elif self.state in ["going_to_delivery", "ready_to_deliver"]:
            task_type = "delivery"
        
        return {
            "position": (self.x, self.y),
            "state": self.state,
            "current_task": {"type": task_type},
            "interaction_timer": 0.0
        }