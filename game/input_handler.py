"""
Input handling - Gère les entrées clavier et événements
"""
import pygame
from config import recipes
import game_state

class InputHandler:
    def __init__(self):
        self.user_input = ""

    def handle_events(self, events, bot, particle_system):
        """Gère tous les événements pygame"""
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._handle_command_input(bot, particle_system)
                
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                
                elif event.key == pygame.K_ESCAPE:
                    self._cancel_current_order()
                
                elif len(self.user_input) < 15 and event.unicode.isprintable():
                    self.user_input += event.unicode
        
        return True

    def _handle_command_input(self, bot, particle_system):
        """Gère la saisie d'une commande"""
        command = self.user_input.lower().strip()
        
        if command in recipes:
            # Nouvelle commande (remplace l'ancienne)
            if game_state.start_new_order(command):
                bot.happiness = min(100, bot.happiness + 10)
                print(f"Nouvelle commande: {command}")
                particle_system.add_sparkle_particles(bot.x + 25, bot.y + 25)
        else:
            print(f"Commande inconnue: {command}")
            bot.happiness = max(50, bot.happiness - 5)
        
        self.user_input = ""

    def _cancel_current_order(self):
        """Annule la commande actuelle"""
        game_state.reset_order()
        self.user_input = ""
        print("Commande annulée")

    def wait_for_exit_input(self):
        """Attend l'input pour quitter (écran de fin)"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or 
                   (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    waiting = False

    def get_user_input(self):
        """Retourne la saisie utilisateur actuelle"""
        return self.user_input