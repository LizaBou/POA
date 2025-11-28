"""
Graphics module - Contient tout le code d'affichage
"""

from .assets import AssetManager
from .ui import UIRenderer
from .kitchen import KitchenRenderer
from .kitchen import ChefStressSystem
__all__ = ['AssetManager', 'UIRenderer', 'KitchenRenderer']


kitchen.chef_stress_system = ChefStressSystem()