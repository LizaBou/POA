"""
Bot entity - Logique corrigée pour prendre les ingrédients
"""
import time
import math
import game_state

class Bot:
    def __init__(self, x=350, y=400):
        self.x = x
        self.y = y
        self.inv = None  # Ingrédient porté
        self.preparing = None  # Ingrédient en cours de préparation
        self.prep_time = 0
        self.prep_position = (0, 0)
        self.target_x = x
        self.target_y = y
        self.happiness = 100
        self.state = "idle"
        self.animation_time = 0
        
        # Constantes pour la vitesse et les temps
        self.BOT_SPEED = 3
        self.prep_times = {
            "laitue": 1.0,
            "tomate": 1.2,
            "pain": 0.8,
            "steak": 2.0,
            "fromage": 0.5
        }
        
        # Positions d'interaction (compatibles avec config.py)
        self.interaction_zones = {
            'fridge_access': (150, 350),      # Devant le frigo
            'cutting_board': (350, 270),      # Devant le plan de travail
            'delivery': (530, 330)            # Devant le comptoir de livraison
        }

    def update_interaction_zones(self, zones):
        """Met à jour les zones d'interaction depuis le renderer"""
        self.interaction_zones = zones

    def distance_to(self, target_pos):
        """Calcule la distance vers une position (x, y)"""
        if isinstance(target_pos, dict):
            x2 = target_pos.get("x", 0) + target_pos.get("w", 0) // 2
            y2 = target_pos.get("y", 0) + target_pos.get("h", 0) // 2
        else:
            x2, y2 = target_pos
        return ((self.x - x2)**2 + (self.y - y2)**2)**0.5

    def is_at_target(self):
        """Vérifie si le bot est arrivé à sa destination"""
        return self.distance_to((self.target_x, self.target_y)) < 30

    def get_next_needed_ingredient(self):
        """Trouve le prochain ingrédient nécessaire pour la commande"""
        if not game_state.current_order_name:
            return None
            
        # Utiliser available_ingredients au lieu de recipes
        if hasattr(game_state, 'available_ingredients'):
            recipe = game_state.available_ingredients.get(game_state.current_order_name, [])
        else:
            # Fallback si available_ingredients n'existe pas
            recipes = {
                "salade": ["laitue", "tomate"],
                "burger": ["pain", "steak", "laitue", "tomate"],
                "sandwich": ["pain", "fromage", "tomate"]
            }
            recipe = recipes.get(game_state.current_order_name, [])
        
        # Trouver les ingrédients manquants
        for ingredient in recipe:
            if ingredient not in game_state.prepared_ingredients:
                return ingredient
        return None

    def update_logic(self):
        """Met à jour la logique du bot"""
        print(f"🤖 Bot état: {self.state}, Position: ({int(self.x)}, {int(self.y)})")
        print(f"🤖 Commande actuelle: {game_state.current_order_name}")
        print(f"🤖 Ingrédients préparés: {game_state.prepared_ingredients}")
        
        # Pas de commande = idle au centre
        if not game_state.current_order_name:
            self.state = "idle"
            self.target_x, self.target_y = (400, 400)  # Centre de la cuisine
            return
        
        # En train de couper
        if self.preparing:
            self.state = "cutting"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            
            prep_time = self.prep_times.get(self.preparing, 1.5)
            if time.time() - self.prep_time >= prep_time:
                # Découpe terminée
                game_state.prepared_ingredients.append(self.preparing)
                print(f"✓ Bot a fini de préparer: {self.preparing}")
                self.preparing = None
                
                # Vérifier si la commande est complète
                needed = self.get_next_needed_ingredient()
                if needed is None:
                    self.state = "ready_to_deliver"
                    print("🎉 Commande complète, prêt à livrer!")
                else:
                    self.state = "need_next_ingredient"
                    print(f"🤖 Prochain ingrédient nécessaire: {needed}")
            return
        
        # Prêt à livrer
        if self.state == "ready_to_deliver":
            self.target_x, self.target_y = self.interaction_zones['delivery']
            self.state = "going_to_delivery"
            return
        
        # A un ingrédient, aller à la planche de découpe
        if self.inv:
            self.state = "going_to_board"
            self.target_x, self.target_y = self.interaction_zones['cutting_board']
            print(f"🤖 Va découper: {self.inv}")
            return
        
        # Besoin d'un ingrédient
        if not self.inv and not self.preparing:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                # Aller chercher l'ingrédient au frigo
                self.state = "going_to_fridge"
                self.target_x, self.target_y = self.interaction_zones['fridge_access']
                print(f"🤖 Va chercher: {needed_ingredient}")
            else:
                # Tous les ingrédients sont prêts
                self.state = "ready_to_deliver"
        
        # Cas par défaut
        if self.state == "idle" and game_state.current_order_name:
            self.state = "need_next_ingredient"

    def handle_interactions(self):
        """Gère les interactions du bot avec l'environnement"""
        if not self.is_at_target():
            return  # Pas encore arrivé à destination
            
        # Prendre ingrédient au frigo (VERSION SIMPLIFIÉE)
        if self.state == "going_to_fridge" and not self.inv:
            needed_ingredient = self.get_next_needed_ingredient()
            if needed_ingredient:
                # Prendre directement l'ingrédient (simulation)
                self.inv = needed_ingredient
                print(f"✓ Bot a pris: {needed_ingredient}")
                self.state = "going_to_board"
        
        # Commencer à couper à la planche
        elif self.state == "going_to_board" and self.inv:
            self.preparing = self.inv
            self.prep_time = time.time()
            self.prep_position = (self.interaction_zones['cutting_board'][0] + 50, 
                                 self.interaction_zones['cutting_board'][1] - 50)
            print(f"🤖 Bot commence à préparer: {self.preparing}")
            self.inv = None
            self.state = "cutting"
        
        # Livrer au comptoir
        elif self.state == "going_to_delivery":
            if game_state.current_order_name:
                # Vérifier que tous les ingrédients sont prêts
                if hasattr(game_state, 'available_ingredients'):
                    recipe = game_state.available_ingredients.get(game_state.current_order_name, [])
                else:
                    recipes = {
                        "salade": ["laitue", "tomate"],
                        "burger": ["pain", "steak", "laitue", "tomate"],
                        "sandwich": ["pain", "fromage", "tomate"]
                    }
                    recipe = recipes.get(game_state.current_order_name, [])
                
                if sorted(game_state.prepared_ingredients) == sorted(recipe):
                    # Livraison réussie
                    base_score = len(recipe) * 50
                    combo_bonus = game_state.combo * 10
                    total_score = base_score + combo_bonus
                    
                    game_state.score += total_score
                    game_state.combo += 1
                    
                    print(f"🎉 Commande {game_state.current_order_name} livrée! +{total_score} points")
                    print(f"Score total: {game_state.score}, Combo: {game_state.combo}")
                    
                    # Réinitialiser pour la prochaine commande
                    game_state.current_order_name = None
                    game_state.prepared_ingredients.clear()
                    self.state = "idle"
                    self.target_x, self.target_y = (400, 400)
                else:
                    print(f"⚠ Commande incomplète! Requis: {recipe}, Préparé: {game_state.prepared_ingredients}")
                    self.state = "need_next_ingredient"

    def update_movement(self):
        """Met à jour le mouvement du bot"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # Mouvement plus fluide
        if abs(dx) > 3:
            self.x += self.BOT_SPEED if dx > 0 else -self.BOT_SPEED
        if abs(dy) > 3:
            self.y += self.BOT_SPEED if dy > 0 else -self.BOT_SPEED
        
        # Limites de l'écran
        self.x = max(60, min(740, self.x))  # Supposant WIDTH = 800
        self.y = max(120, min(540, self.y))  # Supposant HEIGHT = 600
        
        # Animation
        self.animation_time += 0.04

    def update(self, dt=0):
        """Met à jour le bot (logique + mouvement + interactions)"""
        self.update_logic()
        self.update_movement()
        self.handle_interactions()

    def get_state_color(self):
        """Retourne la couleur correspondant à l'état du bot"""
        colors = {
            "idle": (255, 255, 255),          # blanc
            "going_to_fridge": (100, 150, 255),  # bleu
            "going_to_board": (255, 165, 0),     # orange
            "cutting": (255, 100, 100),          # rouge
            "going_to_delivery": (100, 255, 100), # vert
            "waiting_for_ingredient": (255, 100, 255), # magenta
            "ready_to_deliver": (255, 215, 0)    # gold
        }
        return colors.get(self.state, (255, 255, 255))

    def get_state_text(self):
        """Retourne le texte d'état lisible"""
        state_texts = {
            "idle": "En attente",
            "going_to_fridge": "Va au stockage", 
            "going_to_board": "Va préparer",
            "cutting": "Découpe ingrédients",
            "going_to_delivery": "Va livrer",
            "waiting_for_ingredient": "Attend ingrédient",
            "ready_to_deliver": "Prêt à livrer",
            "need_next_ingredient": "Cherche ingrédient"
        }
        return state_texts.get(self.state, self.state)

    def get_debug_info(self):
        """Informations de debug pour le développement"""
        return {
            "position": (int(self.x), int(self.y)),
            "target": (int(self.target_x), int(self.target_y)),
            "state": self.state,
            "inventory": self.inv,
            "preparing": self.preparing,
            "distance_to_target": round(self.distance_to((self.target_x, self.target_y)), 1),
            "next_needed": self.get_next_needed_ingredient()
        }

    # Méthodes pour compatibilité avec le main.py
    def get_position(self):
        """Retourne la position actuelle du bot"""
        return (self.x, self.y)
    
    def get_state(self):
        """Retourne l'état actuel du bot"""
        return {
            "position": (self.x, self.y),
            "state": self.state,
            "current_task": {"type": "ingredient" if self.inv or self.preparing else "delivery" if self.state == "going_to_delivery" else "idle"},
            "interaction_timer": 0.0
        }