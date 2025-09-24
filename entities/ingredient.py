"""
Ingredient management - Gère les ingrédients et les recettes
"""
import time
from config import fridge, RESTOCK_INTERVAL
import game_state

class IngredientManager:
    def __init__(self):
        self.last_restock = 0

    def restock_fridge(self):
        """Réapprovisionne le frigo si nécessaire"""
        current_time = time.time()
        if current_time - self.last_restock < RESTOCK_INTERVAL:
            return
        
        for ing_type in ["T", "L", "B", "C", "H"]:
            available = sum(1 for ing in game_state.ingredients 
                          if ing["type"] == ing_type and not ing["taken"])
            if available < 2:
                # Ajouter un nouvel ingrédient
                new_slot = len([ing for ing in game_state.ingredients 
                              if ing["type"] == ing_type])
                game_state.ingredients.append({
                    "x": fridge["x"] + 10 + (new_slot % 2) * 30,
                    "y": fridge["y"] + 10 + ((new_slot + ord(ing_type)) % 6) * 18,
                    "type": ing_type, 
                    "taken": False, 
                    "spawn_time": current_time + 0.3
                })
        
        self.last_restock = current_time

    def get_available_ingredients(self, ingredient_type):
        """Retourne les ingrédients disponibles d'un type donné"""
        return [ing for ing in game_state.ingredients 
                if ing["type"] == ingredient_type and not ing["taken"]]

    def get_ingredient_colors(self, ingredient_type):
        """Retourne les couleurs associées à un type d'ingrédient"""
        colors = {
            "T": [(255, 69, 69), (255, 140, 0)],      # Tomate
            "L": [(50, 205, 50), (34, 139, 34)],      # Salade
            "B": [(222, 184, 135), (205, 133, 63)],   # Pain
            "C": [(255, 255, 0), (255, 215, 0)],      # Fromage
            "H": [(139, 69, 19), (160, 82, 45)]       # Steak
        }
        return colors.get(ingredient_type, [(255, 255, 255)])

    def get_ingredient_name(self, ingredient_type):
        """Retourne le nom lisible d'un ingrédient"""
        names = {
            "T": "Tomate",
            "L": "Salade", 
            "B": "Pain",
            "C": "Fromage",
            "H": "Steak"
        }
        return names.get(ingredient_type, "Inconnu")