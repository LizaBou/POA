"""
Configuration et constantes du jeu Mini Overcooked
"""

# Configuration de l'écran
WIDTH, HEIGHT = 900, 650
WINDOW_TITLE = "🍳 Mini Overcooked Bot - Version Finale"

# Couleurs personnalisées
COLORS = {
    'wood_dark': (101, 67, 33),
    'wood_light': (205, 133, 63),
    'metal': (192, 192, 192),
    'gold': (255, 215, 0),
    'red': (255, 69, 69),
    'green': (50, 205, 50),
    'blue': (100, 149, 237),
    'purple': (138, 43, 226),
    'orange': (255, 140, 0),
    'white': (255, 255, 255),
    'shadow': (50, 50, 50, 100)
}

# Zones de la cuisine
fridge = {"x": 50, "y": 80, "w": 80, "h": 120}
cutting_board = {"x": 200, "y": 250, "w": 300, "h": 150}
delivery_counter = {"x": WIDTH - 150, "y": 200, "w": 100, "h": 80}
trash_bin = {"x": 20, "y": HEIGHT - 100, "w": 60, "h": 80}

# Recettes - CHAQUE PLAT EST UNE COMMANDE SÉPARÉE
recipes = {
    "salade": ["L", "T"],
    "steak": ["H"],
    "burger": ["B", "H", "L", "T", "C"],
    "sandwich": ["B", "C", "T"],
    "steak_salade": ["H", "L", "T"]
}

# Temps de préparation pour chaque ingrédient
prep_times = {"L": 1.5, "T": 1.0, "B": 2.0, "C": 1.2, "H": 2.5}

# Configuration du jeu
GAME_DURATION = 60  # secondes
BOT_SPEED = 3
PARTICLE_COUNT = 6
RESTOCK_INTERVAL = 4  # secondes