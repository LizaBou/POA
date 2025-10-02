"""
Game logic - Gère la logique principale du jeu
✅ AVEC SYSTÈME DE COMMANDES MULTIPLES INTÉGRÉ
Chaque chef peut avoir sa propre commande simultanément
"""
import time
from config import GAME_DURATION
import game_state


class OrderManager:
    """Gère les commandes individuelles pour chaque chef"""
    
    def __init__(self):
        # Chaque chef a sa propre commande active
        self.chef_orders = {}  # {bot_id: OrderInstance}
        
        # File globale de commandes disponibles
        self.available_orders = []
        
        # Historique des commandes complétées
        self.completed_orders = []
        
    def add_order(self, order_name, ingredients_required):
        """Ajoute une nouvelle commande disponible"""
        order = {
            'name': order_name,
            'ingredients': ingredients_required.copy(),
            'timestamp': time.time(),
            'id': f"{order_name}_{int(time.time() * 1000)}"
        }
        self.available_orders.append(order)
        print(f"📋 Nouvelle commande disponible: {order_name}")
        return order
    
    def claim_order(self, bot_id, chef_name):
        """Un chef réclame la prochaine commande disponible"""
        # Vérifier si le chef a déjà une commande
        if bot_id in self.chef_orders:
            return None
        
        # Prendre la première commande dispo
        if not self.available_orders:
            return None
        
        order = self.available_orders.pop(0)
        
        # Créer une instance de commande pour ce chef
        chef_order = {
            'order_data': order,
            'claimed_by': bot_id,
            'chef_name': chef_name,
            'prepared_ingredients': [],
            'plated': False,
            'claim_time': time.time()
        }
        
        self.chef_orders[bot_id] = chef_order
        print(f"✅ {chef_name} réclame: {order['name']}")
        return chef_order
    
    def add_ingredient_to_chef_order(self, bot_id, ingredient):
        """Ajoute un ingrédient à la commande du chef"""
        if bot_id not in self.chef_orders:
            return False
        
        chef_order = self.chef_orders[bot_id]
        required = chef_order['order_data']['ingredients']
        
        # Vérifier si l'ingrédient est requis et pas déjà ajouté
        if ingredient in required and ingredient not in chef_order['prepared_ingredients']:
            chef_order['prepared_ingredients'].append(ingredient)
            print(f"  {chef_order['chef_name']} prépare: {ingredient}")
            return True
        
        return False
    
    def is_order_ready_to_plate(self, bot_id):
        """Vérifie si tous les ingrédients sont prêts"""
        if bot_id not in self.chef_orders:
            return False
        
        chef_order = self.chef_orders[bot_id]
        required = set(chef_order['order_data']['ingredients'])
        prepared = set(chef_order['prepared_ingredients'])
        
        return required == prepared
    
    def plate_order(self, bot_id):
        """Marque la commande comme assemblée"""
        if bot_id not in self.chef_orders:
            return False
        
        chef_order = self.chef_orders[bot_id]
        
        if not self.is_order_ready_to_plate(bot_id):
            return False
        
        chef_order['plated'] = True
        print(f"  {chef_order['chef_name']} assemble le plat!")
        return True
    
    def deliver_order(self, bot_id):
        """Livre la commande et libère le chef"""
        if bot_id not in self.chef_orders:
            return None
        
        chef_order = self.chef_orders[bot_id]
        
        if not chef_order['plated']:
            return None
        
        # Calculer le temps de préparation
        prep_time = time.time() - chef_order['claim_time']
        
        # Archiver la commande
        completed = {
            'order_name': chef_order['order_data']['name'],
            'chef_name': chef_order['chef_name'],
            'prep_time': prep_time,
            'completion_time': time.time()
        }
        self.completed_orders.append(completed)
        
        # Libérer le chef
        del self.chef_orders[bot_id]
        
        print(f"🎉 {completed['chef_name']} LIVRE: {completed['order_name']} (en {prep_time:.1f}s)")
        return completed
    
    def get_chef_order(self, bot_id):
        """Récupère la commande active d'un chef"""
        return self.chef_orders.get(bot_id)
    
    def get_chef_progress(self, bot_id):
        """Obtient la progression d'un chef"""
        chef_order = self.get_chef_order(bot_id)
        if not chef_order:
            return None
        
        required = len(chef_order['order_data']['ingredients'])
        prepared = len(chef_order['prepared_ingredients'])
        
        return {
            'order_name': chef_order['order_data']['name'],
            'prepared': prepared,
            'required': required,
            'plated': chef_order['plated'],
            'ingredients_needed': [
                ing for ing in chef_order['order_data']['ingredients']
                if ing not in chef_order['prepared_ingredients']
            ]
        }
    
    def cancel_chef_order(self, bot_id):
        """Annule la commande d'un chef (debug)"""
        if bot_id in self.chef_orders:
            order = self.chef_orders[bot_id]
            print(f"❌ Annulation commande de {order['chef_name']}")
            del self.chef_orders[bot_id]
    
    def get_status_summary(self):
        """Résumé de l'état du système"""
        return {
            'available_orders': len(self.available_orders),
            'active_orders': len(self.chef_orders),
            'completed_orders': len(self.completed_orders),
            'chefs_working': [
                {
                    'chef': order['chef_name'],
                    'order': order['order_data']['name'],
                    'progress': f"{len(order['prepared_ingredients'])}/{len(order['order_data']['ingredients'])}"
                }
                for order in self.chef_orders.values()
            ]
        }
    
    def reset(self):
        """Réinitialise tout le système de commandes"""
        self.chef_orders.clear()
        self.available_orders.clear()
        self.completed_orders.clear()
        print("🔄 Système de commandes réinitialisé")


class GameLogic:
    def __init__(self):
        self.start_time = time.time()
        self.running = True
        
        # ⭐ Créer le gestionnaire de commandes
        self.order_manager = OrderManager()
        print("✅ OrderManager intégré dans GameLogic")
    
    def update_timer(self):
        """Met à jour le timer du jeu"""
        current_time = time.time()
        game_state.timer = GAME_DURATION - (current_time - self.start_time)
        
        if game_state.timer <= 0:
            self.running = False
    
    def reduce_combo_over_time(self):
        """Réduit le combo s'il n'y a pas d'activité"""
        current_time = time.time()
        if game_state.combo > 0 and current_time % 15 < 0.1:
            game_state.combo = max(0, game_state.combo - 1)
    
    def calculate_final_stats(self):
        """Calcule les statistiques finales"""
        current_time = time.time()
        plates_delivered = len([p for p in game_state.delivered_plates
                              if current_time - p["time"] < GAME_DURATION])
        
        time_used = GAME_DURATION - game_state.timer if game_state.timer < GAME_DURATION else GAME_DURATION
        efficiency = min(100, int(game_state.score / max(1, time_used))) if time_used > 0 else 100
        
        return {
            'plates_delivered': plates_delivered,
            'efficiency': efficiency,
            'time_used': int(time_used),
            'total_orders_completed': len(self.order_manager.completed_orders)
        }
    
    def print_final_stats(self, stats):
        """Affiche les statistiques finales dans la console"""
        print("\n" + "="*40)
        print("MINI OVERCOOKED BOT - STATISTIQUES")
        print("="*40)
        print(f"Score Final: {game_state.score}")
        print(f"Combo Maximum: {game_state.combo}")
        print(f"Plats Livrés: {stats['plates_delivered']}")
        print(f"Commandes Totales: {stats.get('total_orders_completed', 0)}")
        print(f"Efficacité: {stats['efficiency']}%")
        
        # Performance
        if game_state.score > 300:
            performance = "MAÎTRE CHEF LÉGENDAIRE!"
        elif game_state.score > 200:
            performance = "Chef Professionnel!"
        elif game_state.score > 120:
            performance = "Bon Cuisinier!"
        elif game_state.score > 60:
            performance = "Apprenti Chef"
        else:
            performance = "Débutant"
            
        print(f"Performance: {performance}")
        print("="*40)
        
        # Détails des commandes complétées
        if self.order_manager.completed_orders:
            print("\n📋 COMMANDES COMPLÉTÉES:")
            for i, order in enumerate(self.order_manager.completed_orders, 1):
                print(f"  {i}. {order['chef_name']}: {order['order_name']} ({order['prep_time']:.1f}s)")
        
        print("="*40)
        print("Merci d'avoir joué!")
        print("="*40)
    
    def is_running(self):
        """Vérifie si le jeu est encore en cours"""
        return self.running and game_state.timer > 0
    
    def stop(self):
        """Arrête le jeu"""
        self.running = False
    
    def reset(self):
        """Réinitialise la logique du jeu"""
        self.start_time = time.time()
        self.running = True
        self.order_manager.reset()
        print("🔄 GameLogic réinitialisé")