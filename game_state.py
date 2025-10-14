"""
État global du jeu Mini Overcooked - AVEC MAPPING
"""
import time
from config import fridge, recipes, delivery_counter

# Variables globales de l'état du jeu
score = 0
combo = 0
timer = 60
user_input = ""

# État des commandes
current_order_name = None
current_order = []
prepared_ingredients = []
delivered_plates = []

# Ingrédients dans le frigo
ingredients = []

# Particules pour effets visuels
particles = []

# Managers multi-agents
order_manager = None
bot_manager = None

# 🔥 MAPPING des lettres vers noms complets
INGREDIENT_MAPPING = {
    "T": "tomate",
    "L": "laitue", 
    "B": "pain",
    "C": "fromage",
    "H": "steak",
    "O": "oignon"
}

INGREDIENT_REVERSE = {v: k for k, v in INGREDIENT_MAPPING.items()}

def get_ingredient_full_name(short_name):
    """Convertit T -> tomate, L -> laitue, etc."""
    return INGREDIENT_MAPPING.get(short_name, short_name)

def get_ingredient_short_name(full_name):
    """Convertit tomate -> T, laitue -> L, etc."""
    return INGREDIENT_REVERSE.get(full_name, full_name)

def initialize_ingredients():
    """Initialise les ingrédients dans le frigo"""
    global ingredients
    ingredients = []
    
    current_time = time.time()
    
    for short_type in ["T", "L", "B", "C", "H"]:
        full_type = get_ingredient_full_name(short_type)  # T -> tomate
        
        for i in range(4):
            ingredients.append({
                "x": fridge["x"] + 10 + (i % 2) * 30,
                "y": fridge["y"] + 10 + ((i + ord(short_type)) % 6) * 18,
                "type": full_type,  # ✅ Stocker "tomate" au lieu de "T"
                "short_type": short_type,  # Garder "T" pour compatibilité
                "taken": False,
                "spawn_time": current_time
            })
    
    print(f"✓ {len(ingredients)} ingrédients initialisés")
    print(f"✓ Exemples: {[ing['type'] for ing in ingredients[:5]]}")

def reset_order():
    """Réinitialise la commande actuelle"""
    global current_order_name, current_order, prepared_ingredients
    current_order_name = None
    current_order = []
    prepared_ingredients = []

def start_new_order(order_name):
    """Démarre une nouvelle commande"""
    global current_order_name, current_order, prepared_ingredients
    if order_name in recipes:
        current_order_name = order_name
        current_order = recipes[order_name].copy()
        prepared_ingredients = []
        return True
    return False

def complete_order():
    """Complete la commande actuelle et calcule les points"""
    global score, combo
    if current_order_name and prepared_ingredients:
        recipe_ingredients = sorted(recipes[current_order_name])
        if sorted(prepared_ingredients) == recipe_ingredients:
            base_points = 30
            combo_bonus = combo * 3
            total_points = base_points + combo_bonus
            score += total_points
            combo += 1
            
            delivered_plates.append({
                "name": current_order_name,
                "points": total_points,
                "x": delivery_counter["x"],
                "y": delivery_counter["y"],
                "time": time.time(),
                "ingredients": prepared_ingredients.copy()
            })
            reset_order()
            return total_points
        else:
            combo = max(0, combo - 1)
    return 0

def update_timer(elapsed):
    """Met à jour le timer de la partie"""
    global timer
    timer = max(0, timer - elapsed)

def initialize_game():
    """Initialisation complète du jeu"""
    global score, combo, timer, user_input
    score = 0
    combo = 0
    timer = 60
    user_input = ""
    reset_order()
    initialize_ingredients()
    delivered_plates.clear()
    particles.clear()

def get_available_ingredient(ingredient_type):
    """Récupère un ingrédient disponible d'un type donné"""
    current_time = time.time()
    
    for ing in ingredients:
        if (ing["type"] == ingredient_type and 
            not ing["taken"] and 
            current_time >= ing.get("spawn_time", 0)):
            ing["taken"] = True
            return ing
    
    return None

def return_ingredient(ingredient_type):
    """Remet un ingrédient dans le stock"""
    for ing in ingredients:
        if ing["type"] == ingredient_type and ing["taken"]:
            ing["taken"] = False
            return True
    return False

def respawn_ingredient(ingredient_type, delay=3.0):
    """Fait réapparaître un ingrédient après un délai"""
    spawn_time = time.time() + delay
    
    ingredients.append({
        "type": ingredient_type,
        "taken": False,
        "spawn_time": spawn_time,
        "x": 0,
        "y": 0
    })
    
    print(f"✓ {ingredient_type} va réapparaître dans {delay}s")