"""
État global du jeu Mini Overcooked
"""
import time
from config import fridge, recipes, delivery_counter

# Variables globales de l'état du jeu
score = 0
combo = 0
timer = 180
user_input = ""

# État des commandes
current_order_name = None
current_order = []  # Ingrédients restants pour la commande actuelle
prepared_ingredients = []  # Ingrédients déjà préparés pour cette commande
delivered_plates = []  # Liste des assiettes livrées

# Ingrédients dans le frigo
ingredients = []

# Particules pour effets visuels
particles = []

def initialize_ingredients():
    """Initialise les ingrédients dans le frigo"""
    global ingredients
    ingredients = []
    for t in ["T", "L", "B", "C", "H"]:
        for i in range(4):  # Plus d'ingrédients
            ingredients.append({
                "x": fridge["x"] + 10 + (i % 2) * 30, 
                "y": fridge["y"] + 10 + ((i + ord(t)) % 6) * 18, 
                "type": t,
                "taken": False,
                "spawn_time": time.time()
            })

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

            # Ajouter l'assiette livrée
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
    timer = 180
    user_input = ""
    reset_order()
    initialize_ingredients()
    delivered_plates.clear()
    particles.clear()
