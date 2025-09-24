from config import recipes

def distance(obj1, obj2):
    """Calcule la distance entre deux objets ayant x et y"""
    x1 = obj1.get("x", 0)
    y1 = obj1.get("y", 0)
    x2 = obj2.get("x", 0)
    y2 = obj2.get("y", 0)
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def print_startup_message():
    """Affiche le message de démarrage"""
    print("🍳 Mini Overcooked Bot démarré!")
    print("Commandes disponibles:", ", ".join(recipes.keys()))
    
def clamp(value, min_value, max_value):
    """Limite une valeur entre min et max"""
    return max(min_value, min(max_value, value))

def lerp(start, end, t):
    """Interpolation linéaire entre start et end avec le facteur t (0-1)"""
    return start + (end - start) * t

def normalize(value, min_value, max_value):
    """Normalise une valeur entre 0 et 1 selon un intervalle défini"""
    if max_value - min_value == 0:
        return 0
    return (value - min_value) / (max_value - min_value)

def sign(x):
    """Retourne le signe de x : -1 si négatif, 1 si positif, 0 si nul"""
    return (x > 0) - (x < 0)

def direction(obj1, obj2):
    """Renvoie le vecteur directionnel normalisé de obj1 vers obj2"""
    dx = obj2.get("x", 0) - obj1.get("x", 0)
    dy = obj2.get("y", 0) - obj1.get("y", 0)
    dist = distance(obj1, obj2)
    if dist == 0:
        return {"x": 0, "y": 0}
    return {"x": dx / dist, "y": dy / dist}

def limit_vector(vec, max_length):
    """Limite la norme du vecteur à max_length"""
    norm = (vec["x"]**2 + vec["y"]**2)**0.5
    if norm == 0 or norm <= max_length:
        return vec
    factor = max_length / norm
    return {"x": vec["x"] * factor, "y": vec["y"] * factor}
