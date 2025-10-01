"""
Bot entity - Système multi-agents COMPÉTITIF
Deux chefs en compétition pour marquer le plus de points!
"""
import time
import math
import game_state

class BotManager:
    """Gestionnaire pour coordonner les bots EN COMPÉTITION"""
    def __init__(self):
        self.bots = []
        self.bot_scores = {}  # Score individuel de chaque bot
        self.bot_stats = {}   # Statistiques détaillées
        self.competition_mode = True
        self.frame_counter = 0  # Pour le debug périodique
        
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
        
    def claim_order(self, bot):
        """Un bot réclame la commande en cours"""
        if game_state.current_order_name and not hasattr(game_state, 'order_claimed_by'):
            game_state.order_claimed_by = bot.bot_id
            game_state.order_claimer_name = bot.chef_name
            print(f"🏆 {bot.chef_name} a pris la commande: {game_state.current_order_name}!")
            return True
        return False
    
    def complete_order(self, bot):
        """Un bot complète une commande et gagne des points"""
        if hasattr(game_state, 'order_claimed_by') and game_state.order_claimed_by == bot.bot_id:
            recipe_length = len(game_state.prepared_ingredients)
            
            # Calculer le score avec bonus de rapidité
            base_score = recipe_length * 50
            speed_bonus = max(0, int((30 - game_state.timer % 30) * 2))  # Bonus si rapide
            combo_bonus = game_state.combo * 10
            total_score = base_score + speed_bonus + combo_bonus
            
            # Attribuer le score au bot
            self.bot_scores[bot.bot_id] += total_score
            self.bot_stats[bot.bot_id]["dishes_delivered"] += 1
            
            # Score global
            game_state.score += total_score
            game_state.combo += 1
            
            print(f"🎉 {bot.chef_name} a livré et gagne {total_score} points!")
            print(f"   Score {bot.chef_name}: {self.bot_scores[bot.bot_id]}")
            
            # Nettoyage
            game_state.current_order_name = None
            game_state.prepared_ingredients.clear()
            game_state.plated_dish = None
            if hasattr(game_state, 'order_claimed_by'):
                delattr(game_state, 'order_claimed_by')
            if hasattr(game_state, 'order_claimer_name'):
                delattr(game_state, 'order_claimer_name')
            
            return total_score
        return 0
    
    def update(self):
        """Met à jour tous les bots en compétition"""
        self.frame_counter += 1
        
        # Chaque bot essaie de réclamer la commande s'il est libre
        if game_state.current_order_name and not hasattr(game_state, 'order_claimed_by'):
            # Le bot le plus proche peut réclamer - COURSE!
            available_bots = [b for b in self.bots if b.is_available()]
            if available_bots:
                print(f"\n🏁 COURSE! {len(available_bots)} chefs disponibles pour la commande!")
                for bot in available_bots:
                    dist = bot.distance_to(bot.interaction_zones['fridge_access'])
                    print(f"   - {bot.chef_name}: distance {dist:.1f}")
                
                # Le plus rapide (le plus proche du frigo) gagne
                closest_bot = min(available_bots, 
                                key=lambda b: b.distance_to(b.interaction_zones['fridge_access']))
                self.claim_order(closest_bot)
        
        # IMPORTANT: Mettre à jour TOUS les bots, même ceux qui attendent
        for bot in self.bots:
            bot.update()
            
        # Debug périodique pour vérifier que tous bougent
        if self.frame_counter % 120 == 0:  # Toutes les 2 secondes
            print(f"\n🔍 DEBUG MOUVEMENT (frame {self.frame_counter}):")
            for bot in self.bots:
                distance_to_target = math.sqrt((bot.target_x - bot.x)**2 + (bot.target_y - bot.y)**2)
                print(f"   {bot.chef_name}:")
                print(f"      - État: {bot.state}")
                print(f"      - Position: ({bot.x:.1f}, {bot.y:.1f})")
                print(f"      - Cible: ({bot.target_x}, {bot.target_y})")
                print(f"      - Distance: {distance_to_target:.1f}px")
                print(f"      - Vitesse: {bot.BOT_SPEED}")
                print(f"      - bot_id: {bot.bot_id}")
    
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
        self.prep_position = (0, 0)
        self.target_x = x
        self.target_y = y
        self.state = "idle"
        self.animation_time = 0
        self.bot_id = None
        self.frame_debug_counter = 0  # Pour le debug
        
        # ⭐ NOUVELLES PROPRIÉTÉS POUR LA COMPÉTITION
        self.my_order = False  # Est-ce que cette commande est la mienne?
        self.motivation = 100   # Niveau de motivation (affecte la vitesse)
        self.competitiveness = 0.5 + (color_variant * 0.3)  # Plus ou moins agressif
        
        self.BOT_SPEED = 3 + (color_variant * 0.5)  # Vitesse différente par bot
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

        # Personnalisation visuelle
        self.chef_name = chef_name
        self.chef_hat_height = 25
        
        color_variants = [
            {  # Chef 1 - Rouge (agressif)
                "body": (255, 240, 240),
                "hat": (255, 200, 200),
                "pants": (80, 20, 20),
                "skin": (255, 220, 177)
            },
            {  # Chef 2 - Bleu (calme)
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
        """Vérifie si le bot est disponible pour une nouvelle commande"""
        return (self.state == "idle" and 
                not self.inv and 
                not self.preparing and 
                not self.plating)

    def can_work_on_order(self):
        """Vérifie si ce bot peut travailler sur la commande actuelle"""
        if not game_state.current_order_name:
            return False
        
        # ⭐ COMPÉTITION: Seul le bot qui a réclamé la commande peut travailler dessus
        if hasattr(game_state, 'order_claimed_by'):
            return game_state.order_claimed_by == self.bot_id
        
        return False

    def get_next_needed_ingredient(self):
        """Retourne le prochain ingrédient nécessaire"""
        if not self.can_work_on_order():
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
        """Vérifie si tous les ingrédients sont prêts"""
        if not self.can_work_on_order():
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
        # Si pas de commande, retourner à l'idle mais BOUGER quand même
        if not game_state.current_order_name:
            if self.state != "idle":
                self.state = "idle"
                print(f"🏠 {self.chef_name} retourne au repos")
            # Position de repos différente pour chaque chef
            if self.bot_id is not None:
                self.target_x = 250 if self.bot_id % 2 == 0 else 550
                self.target_y = 450
            return
        
        # ⭐ SI CE N'EST PAS MA COMMANDE, JE BOUGE VERS MA ZONE D'ATTENTE
        if not self.can_work_on_order():
            self.state = "waiting"
            # Position d'attente BIEN VISIBLE et DIFFÉRENTE
            if self.bot_id is not None:
                wait_x = 100 if self.bot_id % 2 == 0 else 700
                wait_y = 500
                
                # Afficher seulement si la cible change vraiment
                if abs(self.target_x - wait_x) > 10 or abs(self.target_y - wait_y) > 10:
                    print(f"⏸️ {self.chef_name} va attendre à ({wait_x}, {wait_y})")
                
                self.target_x = wait_x
                self.target_y = wait_y
            # IMPORTANT: Ne pas return, continuer vers update_movement!
            return
        
        # Le reste du code pour le chef qui travaille...
        if self.preparing:
            self.state = "cutting"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            
            prep_time = self.prep_times.get(self.preparing, 1.5)
            # Bonus de vitesse selon motivation
            prep_time *= (1.0 - (self.motivation / 200))
            
            if time.time() - self.prep_time >= prep_time:
                game_state.prepared_ingredients.append(self.preparing)
                print(f"✓ {self.chef_name} a fini: {self.preparing}")
                self.preparing = None
                
                if self.are_all_ingredients_ready():
                    self.state = "ready_to_plate"
                else:
                    self.state = "need_next_ingredient"
            return
        
        # Dressage du plat
        if self.plating:
            self.state = "plating"
            self.target_x, self.target_y = self.interaction_zones['plating_station']
            
            if time.time() - self.plate_time >= self.PLATING_TIME:
                game_state.plated_dish = game_state.current_order_name
                self.plating = False
                self.inv = "plated_dish"
                print(f"✅ {self.chef_name} a dressé: {game_state.current_order_name}")
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
            print(f"🚚 {self.chef_name} va livrer pour GAGNER DES POINTS!")
            return
        
        if self.inv and self.inv != "plated_dish":
            self.state = "going_to_board"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            return
        
        if not self.inv and not self.preparing and not self.plating:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                self.state = "going_to_fridge"
                self.target_x, self.target_y = self.interaction_zones['fridge_access']
                print(f"👨‍🍳 {self.chef_name} va chercher: {needed_ingredient}")
            elif self.are_all_ingredients_ready():
                self.state = "ready_to_plate"

    def handle_interactions(self):
        if not self.is_at_target():
            return
            
        if self.state == "going_to_fridge" and not self.inv:
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
            else:
                # Fallback si pas de manager
                recipe_length = len(game_state.prepared_ingredients)
                base_score = recipe_length * 50
                game_state.score += base_score
                
                game_state.current_order_name = None
                game_state.prepared_ingredients.clear()
                game_state.plated_dish = None
            
            self.inv = None
            self.state = "idle"
            self.motivation = min(100, self.motivation + 10)  # Boost de motivation!

    def update_movement(self):
        """Met à jour le mouvement - TOUJOURS APPELÉ même en attente"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # Calculer la distance pour debug
        distance = math.sqrt(dx**2 + dy**2)
        
        # Vitesse variable selon motivation et état
        if self.state == "waiting":
            speed = self.BOT_SPEED * 0.8  # Vitesse normale en attente
        else:
            speed = self.BOT_SPEED * (0.8 + self.motivation / 500)
        
        # TOUJOURS SE DÉPLACER vers la cible si pas déjà arrivé
        if distance > 5:  # Seuil de 5 pixels
            # Normaliser le vecteur de direction
            if distance > 0:
                move_x = (dx / distance) * speed
                move_y = (dy / distance) * speed
                self.x += move_x
                self.y += move_y
                
                # Debug du mouvement
                if self.frame_debug_counter % 30 == 0:  # Toutes les 0.5 secondes
                    print(f"   🚶 {self.chef_name}: bouge de ({move_x:.1f}, {move_y:.1f}), distance={distance:.1f}")
        
        # Limites de l'écran
        self.x = max(60, min(740, self.x))
        self.y = max(120, min(540, self.y))
        
        self.animation_time += 0.04
        self.frame_debug_counter = getattr(self, 'frame_debug_counter', 0) + 1

    def update(self, dt=0):
        self.update_logic()
        self.update_movement()
        self.handle_interactions()

    def get_state_color(self):
        colors = {
            "idle": (200, 200, 200),
            "waiting": (100, 100, 100),
            "going_to_fridge": (100, 150, 255),
            "going_to_board": (255, 165, 0),
            "cutting": (255, 100, 100),
            "going_to_plating": (255, 150, 255),
            "plating": (200, 100, 255),
            "going_to_delivery": (100, 255, 100)
        }
        return colors.get(self.state, (255, 255, 255))

    def get_state_text(self):
        state_texts = {
            "idle": "En attente",
            "waiting": f"⏸️ Attend (commande de {getattr(game_state, 'order_claimer_name', 'autre')})",
            "going_to_fridge": "Va au stockage", 
            "going_to_board": "Va préparer",
            "cutting": f"Découpe {self.preparing or ''}",
            "going_to_plating": "Va dresser",
            "plating": "Dresse le plat",
            "going_to_delivery": "🏆 Va marquer des points!"
        }
        return state_texts.get(self.state, self.state)

    def draw_chef(self, screen):
        """Dessine le chef cuisinier"""
        import pygame
        
        # Corps avec indication de motivation (opacité)
        alpha = int(150 + (self.motivation * 1.05))
        
        body_rect = pygame.Rect(self.x - 12, self.y - 15, 24, 30)
        pygame.draw.rect(screen, self.chef_body_color, body_rect)
        pygame.draw.rect(screen, (200, 200, 200), body_rect, 2)
        
        # Pantalon
        pants_rect = pygame.Rect(self.x - 10, self.y + 10, 20, 15)
        pygame.draw.rect(screen, self.chef_pants_color, pants_rect)
        
        # Tête
        pygame.draw.circle(screen, self.chef_skin_color, (int(self.x), int(self.y - 25)), 10)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y - 25)), 10, 2)
        
        # Toque
        hat_rect = pygame.Rect(self.x - 8, self.y - 45, 16, self.chef_hat_height)
        pygame.draw.rect(screen, self.chef_hat_color, hat_rect)
        pygame.draw.rect(screen, (180, 180, 180), hat_rect, 2)
        
        # Yeux (expression selon état)
        if self.state == "waiting":
            # Yeux tristes quand il attend
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x - 3), int(self.y - 27)), 2)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 3), int(self.y - 27)), 2)
            pygame.draw.line(screen, (0, 0, 0), 
                           (int(self.x - 6), int(self.y - 20)), 
                           (int(self.x + 6), int(self.y - 18)), 2)  # Bouche triste
        else:
            # Yeux normaux
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x - 3), int(self.y - 27)), 2)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 3), int(self.y - 27)), 2)
        
        # Animation découpage
        if self.state == "cutting" and self.preparing:
            arm_offset = int(math.sin(self.animation_time * 8) * 3)
            pygame.draw.line(screen, self.chef_skin_color, 
                           (int(self.x + 12), int(self.y - 10)), 
                           (int(self.x + 18), int(self.y - 5 + arm_offset)), 3)
        
        # Ingrédient en main
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
        
        # Plat fini avec effet brillant (va marquer!)
        elif self.inv == "plated_dish":
            # Animation brillante
            glow = int(abs(math.sin(self.animation_time * 4)) * 50)
            pygame.draw.circle(screen, (240, 240, 240), (int(self.x + 15), int(self.y - 5)), 8)
            pygame.draw.circle(screen, (200 + glow, 200 + glow, 200), (int(self.x + 15), int(self.y - 5)), 8, 2)
            pygame.draw.circle(screen, (150, 100, 50), (int(self.x + 15), int(self.y - 5)), 5)
        
        # Nom du chef avec son score
        import pygame.font
        font = pygame.font.Font(None, 16)
        
        name_text = self.chef_name
        if hasattr(game_state, 'bot_manager') and self.bot_id in game_state.bot_manager.bot_scores:
            score = game_state.bot_manager.bot_scores[self.bot_id]
            name_text = f"{self.chef_name} ({score})"
        
        name_surf = font.render(name_text, True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(int(self.x), int(self.y + 35)))
        
        # Couleur de fond selon état
        if self.can_work_on_order():
            bg_color = (0, 100, 0, 180)  # Vert = travaille
        elif self.state == "waiting":
            bg_color = (100, 0, 0, 180)  # Rouge = attend
        else:
            bg_color = (0, 0, 0, 128)
            
        bg_rect = name_rect.inflate(6, 3)
        pygame.draw.rect(screen, bg_color, bg_rect)
        screen.blit(name_surf, name_rect)

    def get_debug_info(self):
        return {
            "name": self.chef_name,
            "position": (int(self.x), int(self.y)),
            "state": self.state,
            "inventory": self.inv,
            "preparing": self.preparing,
            "can_work": self.can_work_on_order(),
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