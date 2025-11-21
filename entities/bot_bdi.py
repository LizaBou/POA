"""
Bot avec Architecture BDI + ÉMOTIONS & STRESS
Nouvelle version avec système émotionnel et cuisson réelle
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


class EmotionType(Enum):
    """Types d'émotions"""
    CALM = "calm"           # 😌 Calme
    FOCUSED = "focused"     # 🎯 Concentré
    STRESSED = "stressed"   # 😰 Stressé
    PANICKED = "panicked"   # 😱 Paniqué
    HAPPY = "happy"         # 😊 Heureux
    FRUSTRATED = "frustrated"  # 😤 Frustré


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
    Agent BDI avec ÉMOTIONS et STRESS
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
        
        # 😊 SYSTÈME ÉMOTIONNEL
        self.stress_level = 0.0
        self.current_emotion = EmotionType.CALM
        self.emotion_duration = 0.0
        self.last_success_time = time.time()
        self.consecutive_failures = 0
        self.workload = 0
        
        # Seuils émotionnels
        self.STRESS_THRESHOLD_FOCUSED = 0.3
        self.STRESS_THRESHOLD_STRESSED = 0.6
        self.STRESS_THRESHOLD_PANICKED = 0.85
        
        # Capacités physiques
        self.base_speed = 3 + (color_variant * 0.5)
        self.BOT_SPEED = self.base_speed
        self.inv = None
        self.animation_time = 0
        
        # Zones d'interaction
        self.interaction_zones = {}
        self.ingredient_bins = {}
        
        # Statistiques
        self.motivation = 100
        self.competitiveness = 0.5 + (color_variant * 0.3)
        
        # Durées des actions
        self.base_prep_times = {
            "laitue": 1.0,
            "tomate": 1.2,
            "pain": 0.8,
            "steak": 0.0,
            "fromage": 0.5,
            "oignon": 1.5
        }
        self.prep_times = self.base_prep_times.copy()
        
        # 🔥 SYSTÈME DE CUISSON
        self.base_cook_times = {
            "steak": 3.0
        }
        self.cook_times = self.base_cook_times.copy()
        self.cook_states = {
            "raw": 0.0,
            "rare": 0.25,
            "medium": 0.50,
            "welldone": 0.75,
            "burnt": 1.2
        }
        
        # Variables de cuisson
        self._is_cooking = None
        self.cooking_start_time = 0
        self.cooking_progress = 0.0
        
        # Variables pour compatibilité renderer
        self.PLATING_TIME = 2.0
        self.prep_time = 0
        self.cook_time = 0
        self.plate_time = 0
        self._is_preparing = None
        self._is_plating = False
        
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
        
        # Animation tremblements
        self.shake_offset_x = 0
        self.shake_offset_y = 0

    # ==================== SYSTÈME ÉMOTIONNEL ====================
    
    def update_stress(self):
        """Met à jour le niveau de stress selon la situation"""
        current_time = time.time()
        stress_factors = 0.0
        
        # 1. Charge de travail
        if hasattr(game_state, 'order_manager'):
            my_order = game_state.order_manager.get_chef_order(self.bot_id)
            if my_order:
                progress = game_state.order_manager.get_chef_progress(self.bot_id)
                if progress:
                    total = len(my_order['order_data']['ingredients'])
                    remaining = len(progress['ingredients_needed'])
                    stress_factors += (remaining / max(1, total)) * 0.3
            
            available = len(game_state.order_manager.available_orders)
            stress_factors += min(available / 5, 0.3)
        
        # 2. Échecs consécutifs
        stress_factors += min(self.consecutive_failures * 0.1, 0.2)
        
        # 3. Temps depuis dernier succès
        time_since_success = current_time - self.last_success_time
        if time_since_success > 30:
            stress_factors += min((time_since_success - 30) / 60, 0.2)
        
        # 4. Action bloquée
        if self.current_intention:
            elapsed = current_time - self.current_intention.start_time
            if elapsed > 8:
                stress_factors += 0.3
        
        # Mise à jour progressive
        target_stress = min(stress_factors, 1.0)
        
        if target_stress > self.stress_level:
            self.stress_level = min(1.0, self.stress_level + 0.02)
        else:
            self.stress_level = max(0.0, self.stress_level - 0.01)
        
        # Relaxation rapide après succès
        if time_since_success < 5:
            self.stress_level *= 0.95
    
    def update_emotion(self):
        """Détermine l'émotion selon le stress"""
        old_emotion = self.current_emotion
        
        if self.stress_level < self.STRESS_THRESHOLD_FOCUSED:
            self.current_emotion = EmotionType.CALM
        elif self.stress_level < self.STRESS_THRESHOLD_STRESSED:
            self.current_emotion = EmotionType.FOCUSED
        elif self.stress_level < self.STRESS_THRESHOLD_PANICKED:
            self.current_emotion = EmotionType.STRESSED
        else:
            self.current_emotion = EmotionType.PANICKED
        
        if time.time() - self.last_success_time < 2:
            self.current_emotion = EmotionType.HAPPY
        
        if self.consecutive_failures >= 3:
            self.current_emotion = EmotionType.FRUSTRATED
        
        if old_emotion != self.current_emotion:
            emoji = self.get_emotion_emoji()
            print(f"{emoji} {self.chef_name} ressent: {self.current_emotion.value}")
            self.emotion_duration = 0
        else:
            self.emotion_duration += 0.04
    
    def apply_stress_effects(self):
        """Applique les effets du stress"""
        if self.current_emotion == EmotionType.PANICKED:
            self.BOT_SPEED = self.base_speed * 0.6
        elif self.current_emotion == EmotionType.STRESSED:
            self.BOT_SPEED = self.base_speed * 0.85
        elif self.current_emotion == EmotionType.FOCUSED:
            self.BOT_SPEED = self.base_speed * 1.15
        else:
            self.BOT_SPEED = self.base_speed
        
        stress_multiplier = 1.0 + (self.stress_level * 0.5)
        for ing in self.base_prep_times:
            self.prep_times[ing] = self.base_prep_times[ing] * stress_multiplier
        
        for ing in self.base_cook_times:
            self.cook_times[ing] = self.base_cook_times[ing] * stress_multiplier
        
        if self.stress_level > 0.4:
            shake_intensity = (self.stress_level - 0.4) * 5
            self.shake_offset_x = math.sin(time.time() * 15) * shake_intensity
            self.shake_offset_y = math.cos(time.time() * 20) * shake_intensity
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0
    
    def get_emotion_emoji(self) -> str:
        """Retourne l'emoji correspondant à l'émotion"""
        emojis = {
            EmotionType.CALM: "😌",
            EmotionType.FOCUSED: "🎯",
            EmotionType.STRESSED: "😰",
            EmotionType.PANICKED: "😱",
            EmotionType.HAPPY: "😊",
            EmotionType.FRUSTRATED: "😤"
        }
        return emojis.get(self.current_emotion, "😐")
    
    def get_emotion_color(self):
        """Couleur selon l'émotion"""
        colors = {
            EmotionType.CALM: (100, 200, 255),
            EmotionType.FOCUSED: (100, 255, 100),
            EmotionType.STRESSED: (255, 200, 100),
            EmotionType.PANICKED: (255, 100, 100),
            EmotionType.HAPPY: (255, 255, 100),
            EmotionType.FRUSTRATED: (200, 100, 200)
        }
        return colors.get(self.current_emotion, (200, 200, 200))
    
    def on_success(self):
        """Appelé lors d'un succès"""
        self.last_success_time = time.time()
        self.consecutive_failures = 0
        self.stress_level = max(0, self.stress_level - 0.2)
    
    def on_failure(self):
        """Appelé lors d'un échec"""
        self.consecutive_failures += 1
        self.stress_level = min(1.0, self.stress_level + 0.15)

    # ==================== PHASE 1: PERCEPTION ====================
    
    def perceive_world(self):
        """PERCEIVE: Observer le monde"""
        current_time = time.time()
        
        self.update_belief(BeliefType.SELF, "position",
            f"at_{int(self.x)}_{int(self.y)}", 1.0)
        
        self.update_belief(BeliefType.SELF, "has_inventory",
            str(self.inv is not None), 1.0)
        
        if self.inv:
            self.update_belief(BeliefType.SELF, "carrying",
                f"holding_{self.inv}", 1.0)
        
        self.update_belief(BeliefType.SELF, "stress_level",
            f"stress_{int(self.stress_level * 100)}", 1.0)
        
        self.update_belief(BeliefType.SELF, "emotion",
            f"feeling_{self.current_emotion.value}", 1.0)
        
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
        """DELIBERATION: Générer des options"""
        options = self.generate_options()
        self.desires = self.filter_options(options)
    
    def generate_options(self) -> List[Desire]:
        """Génère tous les désirs possibles"""
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
            priority = 0.9
            if self.current_emotion == EmotionType.PANICKED:
                priority *= 0.7
            
            options.append(Desire(
                goal="claim_order",
                priority=priority,
                preconditions=["environment_orders_available"],
                effects=["environment_has_order"]
            ))
        
        # Option 2: Obtenir un ingrédient
        if my_order and not self.inv:
            if progress and progress['ingredients_needed']:
                needed = progress['ingredients_needed'][0]
                
                priority = 0.8
                if self.current_emotion == EmotionType.STRESSED:
                    priority *= 1.2
                
                options.append(Desire(
                    goal=f"obtain_ingredient_{needed}",
                    priority=priority,
                    preconditions=["environment_has_order"],
                    effects=[f"self_carrying_holding_{needed}"]
                ))
        
        # Option 3: Préparer/cuire l'ingrédient
        if self.inv and self.inv != "plated_dish" and not self._is_cooking:
            needs_cooking = self.inv in self.cook_times
            
            if needs_cooking:
                options.append(Desire(
                    goal=f"cook_ingredient_{self.inv}",
                    priority=0.90,
                    preconditions=[f"self_carrying_holding_{self.inv}"],
                    effects=["ingredient_cooked"]
                ))
            else:
                options.append(Desire(
                    goal=f"prepare_ingredient_{self.inv}",
                    priority=0.85,
                    preconditions=[f"self_carrying_holding_{self.inv}"],
                    effects=["ingredient_prepared"]
                ))
        
        # Option 4: Assembler le plat
        if my_order and not self.inv:
            if progress and progress['is_ready']:
                priority = 0.95
                if self.current_emotion == EmotionType.HAPPY:
                    priority = 1.0
                
                options.append(Desire(
                    goal="assemble_dish",
                    priority=priority,
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
        """Filter: Sélectionne les désirs réalisables"""
        filtered = []
        
        for desire in options:
            is_achievable = True
            conflicts = not self.conflicts_with_intentions(desire)
            
            if is_achievable and conflicts:
                filtered.append(desire)
        
        filtered.sort(key=lambda d: d.priority, reverse=True)
        return filtered
    
    def conflicts_with_intentions(self, desire: Desire) -> bool:
        """Vérifie les conflits"""
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

    # ==================== CYCLE BDI PRINCIPAL ====================
    
    def update(self, dt=0):
        """Cycle BDI complet"""
        # Système émotionnel
        self.update_stress()
        self.update_emotion()
        self.apply_stress_effects()
        
        # 1. PERCEIVE
        self.perceive_world()
        
        # 2 & 3. DELIBERATE
        self.deliberate()
        
        # Détection de blocage
        if self.current_intention:
            elapsed = time.time() - self.current_intention.start_time
            
            timeout = 5.0
            if self.current_intention.plan:
                action_name = self.current_intention.plan[0].name
                if action_name in ["cut_ingredient"]:
                    timeout = 8.0
                elif action_name == "cook_ingredient":
                    timeout = 10.0
                elif action_name == "plate_dish":
                    timeout = 8.0
                elif action_name == "move_to":
                    timeout = 10.0
            
            if elapsed > timeout:
                print(f"⚠️ {self.chef_name}: Intention bloquée - ABANDON!")
                self.current_intention = None
                self.action_start_time = 0
                self.current_action = None
                self._is_preparing = None
                self._is_cooking = None
                self._is_plating = False
                self.on_failure()
        
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
                emoji = self.get_emotion_emoji()
                print(f"{emoji} {self.chef_name} s'engage: {best_desire.goal}")
        
        # 5. EXECUTE
        self.execute()
        
        self.animation_time += dt if dt > 0 else 0.04
        self.update_movement()

    # ==================== PHASE 3: MEANS-ENDS REASONING ====================
    
    def means_ends_reasoning(self, desire: Desire) -> List[Action]:
        """PLANNING: Génère un plan"""
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
        
        elif desire.goal.startswith("cook_ingredient_"):
            ingredient = desire.goal.replace("cook_ingredient_", "")
            target = self.interaction_zones.get('cooking_area', (430, 330))
            
            plan.append(Action(
                name="move_to",
                parameters={"target": target, "reason": "cook"},
                preconditions=[],
                delete_list=[],
                add_list=["at_cooking_area"],
                duration=1.5
            ))
            
            plan.append(Action(
                name="cook_ingredient",
                parameters={"ingredient": ingredient},
                preconditions=["at_cooking_area"],
                delete_list=[f"self_carrying_holding_{ingredient}"],
                add_list=["ingredient_cooked"],
                duration=self.cook_times.get(ingredient, 3.0)
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
            self.on_success()
            return
        
        action = self.current_intention.plan[0]
        
        if not hasattr(self, '_last_action_log') or self._last_action_log != action.name:
            emoji = self.get_emotion_emoji()
            print(f"{emoji} {self.chef_name} exécute: {action.name}")
            self._last_action_log = action.name
        
        if self.execute_action(action):
            self.current_intention.plan.pop(0)
            self.action_start_time = 0
            self.current_action = None
            self._last_action_log = None
    
    def execute_action(self, action: Action) -> bool:
        """Exécute une action atomique"""
        
        if action.name == "try_claim_order":
            if hasattr(game_state, 'order_manager'):
                existing_order = game_state.order_manager.get_chef_order(self.bot_id)
                if existing_order:
                    return True
                
                if len(game_state.order_manager.available_orders) == 0:
                    self.on_failure()
                    return False
                
                order_info = game_state.order_manager.assign_order_to_chef(
                    self.bot_id, self.chef_name
                )
                if order_info:
                    print(f"🎯 {self.chef_name} a pris: {order_info['order_data']['name']}")
                    self.on_success()
                    return True
                else:
                    self.on_failure()
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
        
        elif action.name == "cook_ingredient":
            ingredient = action.parameters.get("ingredient")
            
            if self.action_start_time == 0:
                self.action_start_time = time.time()
                self.cooking_start_time = time.time()
                self.current_action = action
                self.cook_time = time.time()
                self._is_cooking = ingredient
                self.cooking_progress = 0.0
                print(f"🔥 {self.chef_name} commence à cuire: {ingredient}")
                return False
            
            # Calculer la progression
            elapsed = time.time() - self.action_start_time
            duration = self.cook_times.get(ingredient, 3.0)
            self.cooking_progress = elapsed / duration
            
            # Vérifier l'état de cuisson
            if self.cooking_progress >= 1.2:
                # BRÛLÉ !
                print(f"🔥💀 {self.chef_name} a BRÛLÉ le {ingredient}!")
                self.inv = None
                self._is_cooking = None
                self.cooking_progress = 0.0
                self.on_failure()
                if hasattr(game_state, 'order_manager'):
                    game_state.order_manager.remove_chef_order(self.bot_id)
                return True
            
            # Cuisson parfaite entre 75% et 110%
            if 0.75 <= self.cooking_progress <= 1.1:
                if hasattr(game_state, 'order_manager'):
                    game_state.order_manager.add_ingredient_to_chef(self.bot_id, ingredient)
                self.inv = None
                self._is_cooking = None
                self.cooking_progress = 0.0
                print(f"✅ {self.chef_name} a cuit parfaitement: {ingredient}")
                self.on_success()
                return True
            
            return False
        
        elif action.name == "cut_ingredient":
            ingredient = action.parameters.get("ingredient")
            
            if self.action_start_time == 0:
                self.action_start_time = time.time()
                self.current_action = action
                self.prep_time = time.time()
                self._is_preparing = ingredient
                print(f"🔪 {self.chef_name} commence à préparer: {ingredient}")
                return False
            
            duration = self.prep_times.get(ingredient, 1.5)
            if time.time() - self.action_start_time >= duration:
                if hasattr(game_state, 'order_manager'):
                    game_state.order_manager.add_ingredient_to_chef(self.bot_id, ingredient)
                self.inv = None
                self._is_preparing = None
                print(f"✅ {self.chef_name} a préparé: {ingredient}")
                self.on_success()
                return True
            
            return False
        
        elif action.name == "plate_dish":
            if self.inv == "plated_dish":
                return True
            
            if hasattr(game_state, 'order_manager'):
                progress = game_state.order_manager.get_chef_progress(self.bot_id)
                if not progress or not progress['is_ready']:
                    return False
            
            if self.action_start_time == 0:
                self.action_start_time = time.time()
                self.current_action = action
                self.plate_time = time.time()
                self._is_plating = True
                print(f"🍽️ {self.chef_name} commence à assembler le plat...")
                return False
            
            elapsed = time.time() - self.action_start_time
            
            if elapsed < self.PLATING_TIME:
                return False
            
            if hasattr(game_state, 'order_manager'):
                game_state.order_manager.set_chef_plated(self.bot_id, True)
            self.inv = "plated_dish"
            self._is_plating = False
            print(f"✅ {self.chef_name} a assemblé le plat!")
            self.on_success()
            return True
        
        elif action.name == "deliver":
            if hasattr(game_state, 'bot_manager'):
                score = game_state.bot_manager.complete_order(self)
                print(f"🚀 {self.chef_name} a livré! (+{score} points)")
                self.inv = None
                self.on_success()
                return True
            return False
        
        return False

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
        """Retourne le texte d'état avec émotion"""
        emoji = self.get_emotion_emoji()
        
        if self.current_intention:
            if self.current_intention.plan:
                current_action_obj = self.current_intention.plan[0]
                current_action = current_action_obj.name
                
                if "move" in current_action:
                    reason = current_action_obj.parameters.get("reason", "")
                    return f"{emoji} Se déplace ({reason[:10]})"
                elif "pick" in current_action:
                    ing = current_action_obj.parameters.get("ingredient", "?")
                    return f"{emoji} Prend {ing}"
                elif "cook" in current_action:
                    ing = current_action_obj.parameters.get("ingredient", "?")
                    if self.action_start_time > 0:
                        progress = int(self.cooking_progress * 100)
                        
                        if progress < 25:
                            status = "🥩 Cru"
                        elif progress < 50:
                            status = "🍖 Saignant"
                        elif progress < 75:
                            status = "🥩 À point"
                        elif progress < 100:
                            status = "🍖 Bien cuit"
                        elif progress < 120:
                            status = "⚠️ Risque!"
                        else:
                            status = "🔥 BRÛLE!"
                        
                        return f"{emoji} Cuit {ing} {progress}% {status}"
                    return f"{emoji} Va cuire {ing}"
                elif "cut" in current_action:
                    ing = current_action_obj.parameters.get("ingredient", "?")
                    if self.action_start_time > 0:
                        elapsed = time.time() - self.action_start_time
                        duration = self.prep_times.get(ing, 1.5)
                        progress = min(100, int((elapsed / duration) * 100))
                        return f"{emoji} Coupe {ing} ({progress}%)"
                    return f"{emoji} Va couper {ing}"
                elif "plate" in current_action:
                    if self.action_start_time > 0:
                        elapsed = time.time() - self.action_start_time
                        progress = min(100, int((elapsed / self.PLATING_TIME) * 100))
                        return f"{emoji} Assemble ({progress}%)"
                    return f"{emoji} Va assembler"
                elif "deliver" in current_action:
                    return f"{emoji} Livre"
                elif "claim" in current_action:
                    return f"{emoji} Prend commande"
            
            goal = self.current_intention.desire.goal
            if "claim" in goal:
                return f"{emoji} Prend commande"
            elif "obtain" in goal:
                ing = goal.replace("obtain_ingredient_", "")
                return f"{emoji} Cherche {ing}"
            elif "cook" in goal:
                ing = goal.replace("cook_ingredient_", "")
                return f"{emoji} Cuit {ing}"
            elif "prepare" in goal:
                ing = goal.replace("prepare_ingredient_", "")
                return f"{emoji} Prépare {ing}"
            elif "assemble" in goal:
                return f"{emoji} Assemble"
            elif "deliver" in goal:
                return f"{emoji} Livre"
            return f"{emoji} {goal[:15]}"
        elif self.desires:
            return f"{emoji} {len(self.desires)} options"
        return f"{emoji} Réfléchit..."
    
    def get_state_color(self):
        """Retourne la couleur selon l'émotion"""
        return self.get_emotion_color()
    
    def get_stress_bar_info(self):
        """Informations pour afficher la barre de stress"""
        return {
            'level': self.stress_level,
            'color': self.get_emotion_color(),
            'emoji': self.get_emotion_emoji()
        }
    
    # ==================== COMPATIBILITÉ AVEC BOT MANAGER ====================
    
    def is_available(self) -> bool:
        """Vérifie si le bot est disponible"""
        if not self.current_intention:
            return True
        
        if "claim" in self.current_intention.desire.goal:
            return True
        
        return False
    
    @property
    def state(self) -> str:
        """Property pour compatibilité"""
        if not self.current_intention:
            return "idle"
        
        goal = self.current_intention.desire.goal
        
        if "claim" in goal:
            return "claiming_order"
        elif "obtain" in goal:
            return "going_to_fridge"
        elif "cook" in goal:
            if self._is_cooking:
                return "cooking"
            return "going_to_cooking"
        elif "prepare" in goal:
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
    def cooking(self):
        """Property pour savoir si en train de cuire"""
        return self._is_cooking
    
    @cooking.setter
    def cooking(self, value):
        """Setter pour compatibilité"""
        self._is_cooking = value
    
    @property
    def plating(self) -> bool:
        """Property pour compatibilité"""
        return self._is_plating
    
    @property
    def plating_progress(self) -> float:
        """Retourne la progression de l'assemblage"""
        if self._is_plating and self.action_start_time > 0:
            elapsed = time.time() - self.action_start_time
            return min(1.0, elapsed / self.PLATING_TIME)
        return 0.0
    
    @plating.setter
    def plating(self, value: bool):
        """Setter pour compatibilité"""
        self._is_plating = value
    
    def draw_chef(self, screen):
  
     import pygame
    
     draw_x = self.x + self.shake_offset_x
     draw_y = self.y + self.shake_offset_y
    
     # ============ PIEDS ============
     pygame.draw.ellipse(screen, (0, 0, 0), (draw_x - 8, draw_y + 12, 6, 5))
     pygame.draw.ellipse(screen, (0, 0, 0), (draw_x + 2, draw_y + 12, 6, 5))
    
     # ============ PANTALON ============
     pants_rect = pygame.Rect(draw_x - 10, draw_y, 20, 12)
     pygame.draw.rect(screen, self.chef_pants_color, pants_rect)
     pygame.draw.rect(screen, (50, 50, 50), pants_rect, 1)
    
     # Ceinture
     pygame.draw.line(screen, (100, 100, 100), (draw_x - 10, draw_y + 12), (draw_x + 10, draw_y + 12), 2)
    
     # ============ CORPS (VESTE) ============
     body_rect = pygame.Rect(draw_x - 12, draw_y - 15, 24, 15)
     pygame.draw.rect(screen, self.chef_body_color, body_rect)
     pygame.draw.rect(screen, (200, 200, 200), body_rect, 2)
    
     # Boutons
     pygame.draw.circle(screen, (255, 215, 0), (int(draw_x - 2), int(draw_y - 10)), 1)
     pygame.draw.circle(screen, (255, 215, 0), (int(draw_x - 2), int(draw_y - 5)), 1)
     pygame.draw.circle(screen, (255, 215, 0), (int(draw_x + 2), int(draw_y - 10)), 1)
     pygame.draw.circle(screen, (255, 215, 0), (int(draw_x + 2), int(draw_y - 5)), 1)
    
     # ============ BRAS GAUCHE ============
     pygame.draw.line(screen, self.chef_skin_color, (draw_x - 12, draw_y - 10), (draw_x - 18, draw_y - 5), 3)
     pygame.draw.circle(screen, self.chef_skin_color, (int(draw_x - 18), int(draw_y - 5)), 4)
    
     # ============ BRAS DROIT ============
     pygame.draw.line(screen, self.chef_skin_color, (draw_x + 12, draw_y - 10), (draw_x + 18, draw_y - 5), 3)
     pygame.draw.circle(screen, self.chef_skin_color, (int(draw_x + 18), int(draw_y - 5)), 4)
    
     # ============ COU ============
     neck_rect = pygame.Rect(draw_x - 4, draw_y - 20, 8, 5)
     pygame.draw.rect(screen, self.chef_skin_color, neck_rect)
    
     # ============ TÊTE ============
     pygame.draw.circle(screen, self.chef_skin_color, (int(draw_x), int(draw_y - 28)), 10)
     pygame.draw.circle(screen, (200, 150, 120), (int(draw_x), int(draw_y - 28)), 10, 1)
    
     # Yeux
     pygame.draw.circle(screen, (0, 0, 0), (int(draw_x - 4), int(draw_y - 30)), 2)
     pygame.draw.circle(screen, (0, 0, 0), (int(draw_x + 4), int(draw_y - 30)), 2)
     pygame.draw.circle(screen, (255, 255, 255), (int(draw_x - 3), int(draw_y - 31)), 1)
     pygame.draw.circle(screen, (255, 255, 255), (int(draw_x + 5), int(draw_y - 31)), 1)
    
     # Nez
     pygame.draw.polygon(screen, (180, 120, 90), 
                       [(draw_x, draw_y - 27), 
                        (draw_x - 1, draw_y - 25), 
                        (draw_x + 1, draw_y - 25)])
    
     # Bouche (sourire selon émotion)
     emotion = self.current_emotion.value if hasattr(self, 'current_emotion') else 'calm'
     if emotion == 'happy':
        pygame.draw.arc(screen, (0, 0, 0), (draw_x - 3, draw_y - 23, 6, 4), 0, 3.14, 2)
     elif emotion in ['stressed', 'panicked']:
        pygame.draw.line(screen, (0, 0, 0), (draw_x - 2, draw_y - 22), (draw_x + 2, draw_y - 22), 1)
     else:
        pygame.draw.line(screen, (0, 0, 0), (draw_x - 2, draw_y - 22), (draw_x + 2, draw_y - 22), 1)
    
     # ============ TOQUE (CHAPEAU) ============
     hat_width = 20
     hat_height = 18
     hat_rect = pygame.Rect(draw_x - hat_width // 2, draw_y - 48, hat_width, hat_height)
    
     # Dégradé de couleur pour la toque
     for i in range(hat_height):
        ratio = i / hat_height
        r = int(self.chef_hat_color[0] * (1 - ratio * 0.3))
        g = int(self.chef_hat_color[1] * (1 - ratio * 0.3))
        b = int(self.chef_hat_color[2] * (1 - ratio * 0.3))
        pygame.draw.line(screen, (r, g, b), 
                        (draw_x - hat_width // 2, draw_y - 48 + i),
                        (draw_x + hat_width // 2, draw_y - 48 + i))
    
     # Contour toque
     pygame.draw.rect(screen, (100, 100, 100), hat_rect, 1)
    
     # Pompon sur la toque
     pygame.draw.circle(screen, self.chef_hat_color, (int(draw_x), int(draw_y - 50)), 3)
     pygame.draw.circle(screen, (255, 255, 255), (int(draw_x), int(draw_y - 50)), 3, 1)
    
     # ============ BARRE DE STRESS ============
     if self.stress_level > 0.1:
        bar_width = 45
        bar_height = 5
        bar_x = draw_x - bar_width // 2
        bar_y = draw_y - 70
        
        # Fond noir
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
        
        # Remplissage couleur selon stress
        fill_width = int(bar_width * self.stress_level)
        stress_color = self.get_emotion_color()
        pygame.draw.rect(screen, stress_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Contour
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Emoji émotion
        emoji = self.get_emotion_emoji()
        font = pygame.font.Font(None, 16)
        emoji_text = font.render(emoji, True, (255, 255, 255))
        screen.blit(emoji_text, (int(bar_x - 20), int(bar_y - 2)))
