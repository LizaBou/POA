"""
Game logic - Gère la logique principale du jeu
"""
import time
from config import GAME_DURATION
import game_state

class GameLogic:
    def __init__(self):
        self.start_time = time.time()
        self.running = True

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
            'time_used': int(time_used)
        }

    def print_final_stats(self, stats):
        """Affiche les statistiques finales dans la console"""
        print("\n" + "="*40)
        print("MINI OVERCOOKED BOT - STATISTIQUES")
        print("="*40)
        print(f"Score Final: {game_state.score}")
        print(f"Combo Maximum: {game_state.combo}")
        print(f"Plats Livrés: {stats['plates_delivered']}")
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
        print("Merci d'avoir joué!")
        print("="*40)

    def is_running(self):
        """Vérifie si le jeu est encore en cours"""
        return self.running and game_state.timer > 0

    def stop(self):
        """Arrête le jeu"""
        self.running = False