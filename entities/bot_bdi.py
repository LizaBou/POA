"""
Bot avec Architecture BDI (Belief-Desire-Intention)
Application des concepts du cours BDI Agents
VERSION CORRIGÉE - Affichage cuisine pendant assemblage
"""
import time
import math
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum
import game_state


class BeliefType(Enum):
    """Types de croyances selon le cours BDI"""
    ENVIRONMENT = "environment"
    SELF = "self"
    OTHER_AGENTS = "other_agents"
    CAPABILITY = "capability"


@dataclass
class Belief:
    """Croyance de l'agent (Belief)"""
    type: BeliefType
    content: str
    confidence: float
    timestamp: float
    
    def is_valid(self) -> bool:
        return time.time() - self.timestamp < 10.0


@dataclass
class Desire:
    """Désir de l'agent (Desire) - États à atteindre"""
    goal: str
    priority: float
    preconditions: List[str]
    effects: List[str]
    
    def is_achievable(self, beliefs: Dict[str, Belief]) -> bool:
        for precond in self.preconditions:
            if precond not in beliefs or not beliefs[precond].is_valid():
                return False
        return True


@dataclass
class Intention:
    """Intention de l'agent (Intention) - Engagement vers un but"""
    desire: Desire
    plan: List['Action']
    start_time: float
    committed: bool = True
    
    def is_completed(self) -> bool:
        return len(self.plan) == 0
    
    def execute_next_step(self) -> Optional['Action']:
        if self.plan:
            return self.plan.pop(0)
        return None


@dataclass
class Action:
    """Action atomique avec préconditions et effets (STRIPS-like)"""
    name: str
    parameters: Dict[str, any]
    preconditions: List[str]
    delete_list: List[str]
    add_list: List[str]
    duration: float
    
    def can_execute(self, beliefs: Dict[str, Belief]) -> bool:
        for precond in self.preconditions:
            if precond not in beliefs:
                return False
        return True


class BDIBot:
    """
    Agent BDI complet selon le cours
    Implémente le cycle: Perceive → Believe → Desire → Intend → Act
    """
    
    def __init__(self, x=350, y=400, chef_name="Chef", color_variant=0):
        # Position physique
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        
        # Identité
        self.chef_name = chef_name
        self.bot_id = None
        self.color_variant = color_variant
        
        # 🧠 COMPOSANTS BDI
        self.beliefs: Dict[str, Belief] = {}
        self.desires: List[Desire] = []
        self.intentions: List[Intention] = []
        self.current_intention: Optional[Intention] = None
        
        # Capacités physiques
        self.BOT_SPEED = 3 + (color_variant * 0.5)
        self.inv = None
        self.animation_time = 0
        
        # Zones d'interaction
        self.interaction_zones = {}
        self.ingredient_bins = {}
        
        # Statistiques
        self.motivation = 100
        self.competitiveness = 0.5 + (color_variant * 0.3)
        
        # Durées des actions
        self.prep_times = {
            "laitue": 1.0,
            "tomate": 1.2,
            "pain": 0.8,
            "steak": 0.0,  # ⭐ Pas de découpe, juste cuisson
            "fromage": 0.5
        }
        
        # ⭐ NOUVEAU : Durées de cuisson
        self.cook_times = {
            "steak": 3.0  # 3 secondes de cuisson
        }
        
        # ⭐ CORRECTION: Variables pour compatibilité renderer
        self.PLATING_TIME = 2.0
        self.prep_time = 0  # Timer pour préparation
        self.cook_time = 0  # ⭐ Timer pour cuisson
        self.plate_time = 0  # Timer pour assemblage
        self._is_preparing = None  # Ingrédient en cours de préparation
        self._is_cooking = None  # ⭐ Ingrédient en cours de cuisson
        self._is_plating = False  # Est en train d'assembler
        
        # Visuels
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
        variant = color_variants[color_variant % 2]
        self.chef_body_color = variant["body"]
        self.chef_hat_color = variant["hat"]
        self.chef_pants_color = variant["pants"]
        self.chef_skin_color = variant["skin"]
        
        # État pour l'exécution d'actions
        self.action_start_time = 0
        self.current_action = None

    # ==================== PHASE 1: PERCEPTION ====================
    
    def perceive_world(self):
        """PERCEIVE: Observer le monde et mettre à jour les croyances"""
        current_time = time.time()
        
        self.update_belief(BeliefType.SELF, "position",
            f"at_{int(self.x)}_{int(self.y)}", 1.0)
        
        self.update_belief(BeliefType.SELF, "has_inventory",
            str(self.inv is not None), 1.0)
        
        if self.inv:
            self.update_belief(BeliefType.SELF, "carrying",
                f"holding_{self.inv}", 1.0)
        
        if hasattr(game_state, 'order_manager'):
            my_order = game_state.order_manager.get_chef_order(self.bot_id)
            
            if my_order:
                self.update_belief(BeliefType.ENVIRONMENT, "has_order",
                    f"order_{my_order['order_data']['name']}", 1.0)
                
                prepared = my_order.get('prepared_ingredients', [])
                total = len(my_order['order_data']['ingredients'])
                self.update_belief(BeliefType.ENVIRONMENT, "order_progress",
                    f"progress_{len(prepared)}_{total}", 0.9)
            else:
                self.update_belief(BeliefType.ENVIRONMENT, "has_order",
                    "no_order", 1.0)
            
            available = len(game_state.order_manager.available_orders)
            self.update_belief(BeliefType.ENVIRONMENT, "orders_available",
                f"available_{available}", 0.8)
        
        if hasattr(game_state, 'bot_manager'):
            other_busy = sum(
                1 for bot in game_state.bot_manager.bots
                if bot.bot_id != self.bot_id and 
                game_state.order_manager.get_chef_order(bot.bot_id)
            )
            self.update_belief(BeliefType.OTHER_AGENTS, "competitors_busy",
                f"busy_{other_busy}", 0.7)
        
        self.beliefs = {k: v for k, v in self.beliefs.items() if v.is_valid()}
    
    def update_belief(self, belief_type: BeliefType, key: str, 
                     content: str, confidence: float):
        """Ajoute ou met à jour une croyance"""
        belief_key = f"{belief_type.value}_{key}"
        self.beliefs[belief_key] = Belief(
            type=belief_type,
            content=content,
            confidence=confidence,
            timestamp=time.time()
        )

    # ==================== PHASE 2: DELIBERATION ====================
    
    def deliberate(self):
        """DELIBERATION: Générer des options (desires) et filtrer"""
        options = self.generate_options()
        self.desires = self.filter_options(options)
    
    def generate_options(self) -> List[Desire]:
        """Option Generation: Génère tous les désirs possibles"""
        options = []
        
        my_order = None
        available_count = 0
        progress = None
        
        if hasattr(game_state, 'order_manager'):
            my_order = game_state.order_manager.get_chef_order(self.bot_id)
            available_count = len(game_state.order_manager.available_orders)
            if my_order:
                progress = game_state.order_manager.get_chef_progress(self.bot_id)
        
        # Option 1: Prendre une nouvelle commande
        if not my_order and available_count > 0:
            options.append(Desire(
                goal="claim_order",
                priority=0.9,
                preconditions=["environment_orders_available"],
                effects=["environment_has_order"]
            ))
        
        # Option 2: Obtenir un ingrédient
        if my_order and not self.inv:
            if progress and progress['ingredients_needed']:
                needed = progress['ingredients_needed'][0]
                options.append(Desire(
                    goal=f"obtain_ingredient_{needed}",
                    priority=0.8,
                    preconditions=["environment_has_order"],
                    effects=[f"self_carrying_holding_{needed}"]
                ))
        
        # Option 3: Préparer l'ingrédient en main
        if self.inv and self.inv != "plated_dish":
            options.append(Desire(
                goal=f"prepare_ingredient_{self.inv}",
                priority=0.85,
                preconditions=[f"self_carrying_holding_{self.inv}"],
                effects=["ingredient_prepared"]
            ))
        
        # Option 4: Assembler le plat
        if my_order and not self.inv:
            if progress and progress['is_ready']:
                options.append(Desire(
                    goal="assemble_dish",
                    priority=0.95,
                    preconditions=["all_ingredients_ready"],
                    effects=["self_carrying_holding_plated_dish"]
                ))
        
        # Option 5: Livrer le plat
        if self.inv == "plated_dish":
            options.append(Desire(
                goal="deliver_dish",
                priority=1.0,
                preconditions=["self_carrying_holding_plated_dish"],
                effects=["order_completed", "points_gained"]
            ))
        
        return options
    
    def filter_options(self, options: List[Desire]) -> List[Desire]:
        """Filter: Sélectionne les désirs réalisables et non-conflictuels"""
        filtered = []
        
        for desire in options:
            is_achievable = True
            conflicts = not self.conflicts_with_intentions(desire)
            
            if is_achievable and conflicts:
                filtered.append(desire)
        
        filtered.sort(key=lambda d: d.priority, reverse=True)
        return filtered
    
    def conflicts_with_intentions(self, desire: Desire) -> bool:
        """Vérifie si un désir entre en conflit avec les intentions actuelles"""
        if not self.current_intention:
            return False
        
        conflicts = {
            "claim_order": ["deliver_dish", "assemble_dish"],
            "deliver_dish": ["claim_order", "obtain_ingredient"],
        }
        
        current_goal = self.current_intention.desire.goal
        if current_goal in conflicts:
            return desire.goal in conflicts[current_goal]
        
        return False

    # ==================== PHASE 3: MEANS-ENDS REASONING ====================
    
    def means_ends_reasoning(self, desire: Desire) -> List[Action]:
        """PLANNING: Génère un plan pour réaliser un désir"""
        plan = []
        
        if desire.goal == "claim_order":
            plan.append(Action(
                name="try_claim_order",
                parameters={},
                preconditions=["environment_orders_available"],
                delete_list=["environment_has_order_no_order"],
                add_list=["environment_has_order"],
                duration=0.1
            ))
        
        elif desire.goal.startswith("obtain_ingredient_"):
            ingredient = desire.goal.replace("obtain_ingredient_", "")
            
            if ingredient in self.ingredient_bins:
                target = self.ingredient_bins[ingredient]
            else:
                target = self.interaction_zones.get('fridge_access', (150, 350))
            
            plan.append(Action(
                name="move_to",
                parameters={"target": target, "reason": f"get_{ingredient}"},
                preconditions=[],
                delete_list=[],
                add_list=["at_ingredient_bin"],
                duration=2.0
            ))
            
            plan.append(Action(
                name="pick_ingredient",
                parameters={"ingredient": ingredient, "target": target},
                preconditions=["at_ingredient_bin"],
                delete_list=["hands_empty"],
                add_list=[f"self_carrying_holding_{ingredient}"],
                duration=0.5
            ))
        
        elif desire.goal.startswith("prepare_ingredient_"):
            ingredient = desire.goal.replace("prepare_ingredient_", "")
            target = self.interaction_zones.get('cutting_board', (350, 270))
            
            plan.append(Action(
                name="move_to",
                parameters={"target": target, "reason": "prepare"},
                preconditions=[],
                delete_list=[],
                add_list=["at_cutting_board"],
                duration=1.5
            ))
            
            plan.append(Action(
                name="cut_ingredient",
                parameters={"ingredient": ingredient},
                preconditions=["at_cutting_board"],
                delete_list=[f"self_carrying_holding_{ingredient}"],
                add_list=["ingredient_prepared"],
                duration=self.prep_times.get(ingredient, 1.5)
            ))
        
        elif desire.goal == "assemble_dish":
            target = self.interaction_zones.get('plating_station', (525, 420))
            
            plan.append(Action(
                name="move_to",
                parameters={"target": target, "reason": "plate"},
                preconditions=[],
                delete_list=[],
                add_list=["at_plating"],
                duration=1.0
            ))
            
            plan.append(Action(
                name="plate_dish",
                parameters={},
                preconditions=["at_plating", "all_ingredients_ready"],
                delete_list=[],
                add_list=["self_carrying_holding_plated_dish"],
                duration=2.0
            ))
        
        elif desire.goal == "deliver_dish":
            target = self.interaction_zones.get('delivery', (850, 270))
            
            plan.append(Action(
                name="move_to",
                parameters={"target": target, "reason": "deliver"},
                preconditions=[],
                delete_list=[],
                add_list=["at_delivery"],
                duration=2.0
            ))
            
            plan.append(Action(
                name="deliver",
                parameters={},
                preconditions=["at_delivery", "self_carrying_holding_plated_dish"],
                delete_list=["self_carrying_holding_plated_dish"],
                add_list=["order_completed"],
                duration=0.5
            ))
        
        return plan

    # ==================== PHASE 4: EXECUTION ====================
    
    def execute(self):
        """EXECUTE: Exécute l'intention courante"""
        if not self.current_intention:
            return
        
        if self.current_intention.is_completed():
            print(f"✅ {self.chef_name}: Intention '{self.current_intention.desire.goal}' accomplie!")
            self.current_intention = None
            return
        
        action = self.current_intention.plan[0]
        
        if not hasattr(self, '_last_action_log') or self._last_action_log != action.name:
            print(f"▶️ {self.chef_name} exécute: {action.name} {action.parameters}")
            self._last_action_log = action.name
        
        if self.execute_action(action):
            print(f"   ✅ {action.name} terminée!")
            self.current_intention.plan.pop(0)
            self.action_start_time = 0
            self.current_action = None
            self._last_action_log = None
    
    def execute_action(self, action: Action) -> bool:
        """Exécute une action atomique et retourne True si terminée"""
        
        if action.name == "try_claim_order":
            if hasattr(game_state, 'order_manager'):
                existing_order = game_state.order_manager.get_chef_order(self.bot_id)
                if existing_order:
                    return True
                
                if len(game_state.order_manager.available_orders) == 0:
                    return False
                
                order_info = game_state.order_manager.assign_order_to_chef(
                    self.bot_id, self.chef_name
                )
                if order_info:
                    print(f"🎯 {self.chef_name} a pris: {order_info['order_data']['name']}")
                    return True
                else:
                    return False
            return False
        
        elif action.name == "move_to":
            target = action.parameters.get("target")
            if target:
                self.target_x, self.target_y = target
                self.update_movement()
                
                distance = math.sqrt(
                    (self.x - self.target_x)**2 + 
                    (self.y - self.target_y)**2
                )
                return distance < 30
            return False
        
        elif action.name == "pick_ingredient":
            ingredient = action.parameters.get("ingredient")
            target = action.parameters.get("target")
            
            if target:
                distance = math.sqrt(
                    (self.x - target[0])**2 + 
                    (self.y - target[1])**2
                )
                if distance > 40:
                    return False
            
            if not self.inv:
                self.inv = ingredient
                print(f"✓ {self.chef_name} a pris: {ingredient}")
                return True
            else:
                return True
        
        elif action.name == "cut_ingredient":
            ingredient = action.parameters.get("ingredient")
            
            # ⭐ CORRECTION: Mettre à jour _is_preparing pour le renderer
            if self.action_start_time == 0:
                self.action_start_time = time.time()
                self.current_action = action
                self.prep_time = time.time()  # Pour le renderer
                self._is_preparing = ingredient  # Pour le renderer
                print(f"🔪 {self.chef_name} commence à préparer: {ingredient}")
                return False
            
            duration = self.prep_times.get(ingredient, 1.5)
            if time.time() - self.action_start_time >= duration:
                if hasattr(game_state, 'order_manager'):
                    game_state.order_manager.add_ingredient_to_chef(self.bot_id, ingredient)
                self.inv = None
                self._is_preparing = None  # Réinitialiser
                print(f"✅ {self.chef_name} a préparé: {ingredient}")
                return True
            
            return False
        
        elif action.name == "plate_dish":
            if self.inv == "plated_dish":
                return True
            
            if hasattr(game_state, 'order_manager'):
                progress = game_state.order_manager.get_chef_progress(self.bot_id)
                if not progress or not progress['is_ready']:
                    return False
            
            # ⭐ CORRECTION: Mettre à jour _is_plating pour le renderer
            if self.action_start_time == 0:
                self.action_start_time = time.time()
                self.current_action = action
                self.plate_time = time.time()  # Pour le renderer
                self._is_plating = True  # Pour le renderer
                print(f"🍽️ {self.chef_name} commence à assembler le plat...")
                return False
            
            elapsed = time.time() - self.action_start_time
            
            if elapsed < self.PLATING_TIME:
                return False
            
            if hasattr(game_state, 'order_manager'):
                game_state.order_manager.set_chef_plated(self.bot_id, True)
            self.inv = "plated_dish"
            self._is_plating = False  # Réinitialiser
            print(f"✅ {self.chef_name} a assemblé le plat en {elapsed:.1f}s!")
            return True
        
        elif action.name == "deliver":
            if hasattr(game_state, 'bot_manager'):
                score = game_state.bot_manager.complete_order(self)
                print(f"🚀 {self.chef_name} a livré! (+{score} points)")
                self.inv = None
                return True
            return False
        
        return False

    # ==================== CYCLE BDI PRINCIPAL ====================
    
    def update(self, dt=0):
        """Cycle BDI complet: Perceive → Believe → Desire → Intend → Act"""
        # 1. PERCEIVE
        self.perceive_world()
        
        # 2 & 3. DELIBERATE
        self.deliberate()
        
        # 🔧 DÉTECTION DE BLOCAGE
        if self.current_intention:
            elapsed = time.time() - self.current_intention.start_time
            
            timeout = 5.0
            if self.current_intention.plan:
                action_name = self.current_intention.plan[0].name
                if action_name in ["cut_ingredient"]:
                    timeout = 6.0
                elif action_name == "plate_dish":
                    timeout = 8.0
                elif action_name == "move_to":
                    timeout = 10.0
            
            if elapsed > timeout:
                print(f"⚠️ {self.chef_name}: Intention bloquée depuis {elapsed:.1f}s - ABANDON!")
                self.current_intention = None
                self.action_start_time = 0
                self.current_action = None
                self._is_preparing = None
                self._is_plating = False
        
        # 4. INTEND
        if not self.current_intention and self.desires:
            best_desire = self.desires[0]
            plan = self.means_ends_reasoning(best_desire)
            
            if plan:
                self.current_intention = Intention(
                    desire=best_desire,
                    plan=plan,
                    start_time=time.time(),
                    committed=True
                )
                print(f"🎯 {self.chef_name} s'engage: {best_desire.goal}")
        
        # 5. EXECUTE
        self.execute()
        
        self.animation_time += dt if dt > 0 else 0.04
        self.update_movement()

    # ==================== MÉTHODES AUXILIAIRES ====================
    
    def get_my_order(self):
        """Récupère la commande actuelle"""
        if hasattr(game_state, 'order_manager'):
            return game_state.order_manager.get_chef_order(self.bot_id)
        return None
    
    def update_movement(self):
        """Met à jour la position physique"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 5:
            speed = self.BOT_SPEED * (0.8 + self.motivation / 500)
            move_x = (dx / distance) * speed
            move_y = (dy / distance) * speed
            
            self.x += move_x
            self.y += move_y
            
            self.x = max(60, min(880, self.x))
            self.y = max(120, min(540, self.y))
    
    def update_interaction_zones(self, zones):
        """Met à jour les zones d'interaction"""
        self.interaction_zones = zones
    
    def update_ingredient_bins(self, bins):
        """Met à jour les positions des bacs"""
        self.ingredient_bins = bins
    
    def get_state_text(self) -> str:
        """Retourne le texte d'état pour l'affichage"""
        if self.current_intention:
            if self.current_intention.plan:
                current_action_obj = self.current_intention.plan[0]
                current_action = current_action_obj.name
                
                if "move" in current_action:
                    reason = current_action_obj.parameters.get("reason", "")
                    return f"🚶 Se déplace ({reason[:10]})"
                elif "pick" in current_action:
                    ing = current_action_obj.parameters.get("ingredient", "?")
                    return f"📦 Prend {ing}"
                elif "cut" in current_action:
                    ing = current_action_obj.parameters.get("ingredient", "?")
                    if self.action_start_time > 0:
                        elapsed = time.time() - self.action_start_time
                        duration = self.prep_times.get(ing, 1.5)
                        progress = min(100, int((elapsed / duration) * 100))
                        return f"🔪 Coupe {ing} ({progress}%)"
                    return f"🔪 Va couper {ing}"
                elif "plate" in current_action:
                    if self.action_start_time > 0:
                        elapsed = time.time() - self.action_start_time
                        progress = min(100, int((elapsed / self.PLATING_TIME) * 100))
                        return f"🍽️ Assemble ({progress}%)"
                    return f"🍽️ Va assembler"
                elif "deliver" in current_action:
                    return "🚀 Livre"
                elif "claim" in current_action:
                    return "🎯 Prend commande"
            
            goal = self.current_intention.desire.goal
            if "claim" in goal:
                return "🎯 Prend commande"
            elif "obtain" in goal:
                ing = goal.replace("obtain_ingredient_", "")
                return f"📦 Cherche {ing}"
            elif "prepare" in goal:
                ing = goal.replace("prepare_ingredient_", "")
                return f"🔪 Prépare {ing}"
            elif "assemble" in goal:
                return "🍽️ Assemble"
            elif "deliver" in goal:
                return "🚀 Livre"
            return f"🎯 {goal[:15]}"
        elif self.desires:
            return f"💭 {len(self.desires)} options"
        return "🤔 Réfléchit..."
    
    def get_state_color(self):
        """Retourne la couleur selon l'état"""
        if self.current_intention:
            goal = self.current_intention.desire.goal
            if "deliver" in goal:
                return (100, 255, 100)
            elif "claim" in goal:
                return (255, 215, 0)
            elif "prepare" in goal:
                return (255, 100, 100)
            else:
                return (255, 165, 0)
        return (200, 200, 200)
    
    # ==================== COMPATIBILITÉ AVEC BOT MANAGER ====================
    
    def is_available(self) -> bool:
        """Vérifie si le bot est disponible pour prendre une commande"""
        if not self.current_intention:
            return True
        
        if "claim" in self.current_intention.desire.goal:
            return True
        
        return False
    
    @property
    def state(self) -> str:
        """Property pour compatibilité - État basé sur l'intention BDI"""
        if not self.current_intention:
            return "idle"
        
        goal = self.current_intention.desire.goal
        
        if "claim" in goal:
            return "claiming_order"
        elif "obtain" in goal:
            return "going_to_fridge"
        elif "prepare" in goal:
            # ⭐ CORRECTION: Retourner "cutting" pendant la préparation
            if self._is_preparing:
                return "cutting"
            return "going_to_board"
        elif "assemble" in goal:
            return "plating"
        elif "deliver" in goal:
            return "delivering"
        
        return "idle"
    
    @state.setter
    def state(self, value: str):
        """Setter pour compatibilité"""
        pass
    
    @property
    def preparing(self):
        """Property pour compatibilité avec le renderer"""
        return self._is_preparing
    
    @preparing.setter
    def preparing(self, value):
        """Setter pour compatibilité"""
        self._is_preparing = value
    
    @property
    def plating(self) -> bool:
        """Property pour compatibilité - indique si en train d'assembler"""
        return self._is_plating
    
    @property
    def plating_progress(self) -> float:
        """Retourne la progression de l'assemblage (0.0 à 1.0)"""
        if self._is_plating and self.action_start_time > 0:
            elapsed = time.time() - self.action_start_time
            return min(1.0, elapsed / self.PLATING_TIME)
        return 0.0
    
    @plating.setter
    def plating(self, value: bool):
        """Setter pour compatibilité"""
        self._is_plating = value
    
    def draw_chef(self, screen):
        """Dessine le chef"""
        import pygame
        
        body_rect = pygame.Rect(self.x - 12, self.y - 15, 24, 30)
        pygame.draw.rect(screen, self.chef_body_color, body_rect)
        pygame.draw.rect(screen, (200, 200, 200), body_rect, 2)
        
        pygame.draw.circle(screen, self.chef_skin_color, 
                          (int(self.x), int(self.y - 25)), 10)
        
        hat_rect = pygame.Rect(self.x - 8, self.y - 45, 16, 25)
        pygame.draw.rect(screen, self.chef_hat_color, hat_rect)
        
        import pygame.font
        font = pygame.font.Font(None, 16)
        text = font.render(self.get_state_text(), True, (255, 255, 255))
        screen.blit(text, (int(self.x - 40), int(self.y + 35)))