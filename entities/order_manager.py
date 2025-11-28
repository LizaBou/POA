"""
Gestionnaire de commandes pour le système multi-agents compétitif
Permet à chaque chef d'avoir SA PROPRE commande simultanément
"""
import time


class OrderManager:
    """
    Gère les commandes disponibles et les assigne aux chefs
    ✅ VRAIE COMPÉTITION - Chaque chef prend sa propre commande
    ❌ PLUS D'ATTENTE
    """
    
    def __init__(self):
        # File de commandes disponibles (en attente d'être prises)
        self.available_orders = []
        
        # Commandes actives (assignées aux chefs)
        # Format: {bot_id: order_info}
        self.chef_orders = {}
        
        # Historique des commandes complétées
        self.completed_orders = []
        
        print("✅ OrderManager initialisé - Système de commandes multiples prêt!")
    
    def add_order(self, order_name, ingredients):
        """
        Ajoute une nouvelle commande à la file des commandes disponibles
        
        Args:
            order_name: Nom du plat (ex: "burger", "salade")
            ingredients: Liste des ingrédients nécessaires
        """
        order = {
            'name': order_name,
            'ingredients': ingredients.copy(),
            'added_time': time.time()
        }
        
        self.available_orders.append(order)
        print(f"📋 Nouvelle commande disponible: {order_name} ({len(ingredients)} ingrédients)")
        return True
    
    def assign_order_to_chef(self, bot_id, chef_name):
        """
        Assigne la première commande disponible à un chef
        
        Args:
            bot_id: ID unique du bot
            chef_name: Nom du chef
            
        Returns:
            dict ou None: Les détails de la commande assignée
        """
        # Vérifier qu'il y a des commandes disponibles
        if not self.available_orders:
            return None
        
        # Vérifier que le chef n'a pas déjà une commande
        if bot_id in self.chef_orders:
            return self.chef_orders[bot_id]
        
        # Prendre la première commande de la file
        order_data = self.available_orders.pop(0)
        
        # Créer l'assignation
        order_info = {
            'order_data': order_data,
            'chef_name': chef_name,
            'bot_id': bot_id,
            'prepared_ingredients': [],
            'plated': False,
            'start_time': time.time()
        }
        
        self.chef_orders[bot_id] = order_info
        
        print(f"✅ {chef_name} a pris la commande: {order_data['name']}")
        print(f"   Ingrédients: {', '.join(order_data['ingredients'])}")
        print(f"   📊 Commandes disponibles restantes: {len(self.available_orders)}")
        
        return order_info
    
    def get_chef_order(self, bot_id):
        """Récupère la commande active d'un chef"""
        return self.chef_orders.get(bot_id)
    
    def add_ingredient_to_chef(self, bot_id, ingredient):
        """
        Ajoute un ingrédient préparé à la commande du chef
        
        Returns:
            bool: True si l'ingrédient était nécessaire
        """
        if bot_id not in self.chef_orders:
            return False
        
        order_info = self.chef_orders[bot_id]
        required = order_info['order_data']['ingredients']
        prepared = order_info['prepared_ingredients']
        
        # Vérifier si l'ingrédient est nécessaire et pas encore ajouté
        if ingredient in required and ingredient not in prepared:
            prepared.append(ingredient)
            print(f"✓ {order_info['chef_name']}: {ingredient} ajouté ({len(prepared)}/{len(required)})")
            return True
        
        return False
    
    def set_chef_plated(self, bot_id, plated=True):
        """Marque que le chef a platté son plat"""
        if bot_id in self.chef_orders:
            self.chef_orders[bot_id]['plated'] = plated
            if plated:
                print(f"🍽️ {self.chef_orders[bot_id]['chef_name']}: Plat platté!")
    
    def complete_chef_order(self, bot_id):
        """
        Complète et retire la commande d'un chef
        
        Returns:
            dict ou None: Les détails de la commande complétée
        """
        if bot_id not in self.chef_orders:
            return None
        
        order_info = self.chef_orders.pop(bot_id)
        
        # Ajouter à l'historique
        completion_data = {
            'order_name': order_info['order_data']['name'],
            'chef_name': order_info['chef_name'],
            'bot_id': bot_id,
            'completion_time': time.time(),
            'duration': time.time() - order_info['start_time']
        }
        
        self.completed_orders.append(completion_data)
        
        print(f"✅ {order_info['chef_name']}: Commande {order_info['order_data']['name']} livrée!")
        print(f"   ⏱️ Temps: {completion_data['duration']:.1f}s")
        
        return completion_data
    
    def get_chef_progress(self, bot_id):
   
     if bot_id not in self.chef_orders:
        return None
    
     order_info = self.chef_orders[bot_id]
     required = order_info['order_data']['ingredients']
     prepared = order_info['prepared_ingredients']
    
     # Ingrédients manquants
     needed = [ing for ing in required if ing not in prepared]
    
     # ✅ CORRECTION : Structure cohérente avec BDIBot
     return {
        'prepared_ingredients': prepared,  # ✅ AU LIEU DE 'prepared'
        'ingredients_needed': needed,      # ✅ DÉJÀ CORRECT
        'is_ready': len(needed) == 0,      # ✅ DÉJÀ CORRECT
        'plated': order_info['plated'],
        'order_name': order_info['order_data']['name'],  # ✅ POUR COMPATIBILITÉ
        'total_ingredients': len(required)  # ✅ POUR COMPATIBILITÉ
    }
    
    def get_available_count(self):
        """Nombre de commandes disponibles"""
        return len(self.available_orders)
    
    def get_active_count(self):
        """Nombre de commandes actives (en cours)"""
        return len(self.chef_orders)
    
    def get_completed_count(self):
        """Nombre de commandes complétées"""
        return len(self.completed_orders)
    
    def get_status_summary(self):
  
     chefs_working = []
     for bot_id, order_info in self.chef_orders.items():
        progress = self.get_chef_progress(bot_id)
        # ✅ CORRECTION : Utiliser la nouvelle structure
        prepared_count = len(progress['prepared_ingredients'])
        total_count = len(order_info['order_data']['ingredients'])
        
        chefs_working.append({
            'chef': order_info['chef_name'],
            'order': progress['order_name'],
            'progress': f"{prepared_count}/{total_count}"  # ✅ CORRECT
        })
    
     return {
        'available_orders': len(self.available_orders),
        'active_orders': len(self.chef_orders),
        'completed_orders': len(self.completed_orders),
        'chefs_working': chefs_working
    }
    
    def reset(self):
        """Réinitialise complètement le système"""
        self.available_orders.clear()
        self.chef_orders.clear()
        self.completed_orders.clear()
        print("🔄 OrderManager réinitialisé")