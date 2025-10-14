"""
UI Renderer - Interface utilisateur simplifiée
"""
import pygame
from config import COLORS


class UIRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)

    def render_full_ui(self, score, timer, combo, bot, user_input, current_order_name, prepared_ingredients):
        """Affiche l'interface complète"""
        width = self.screen.get_width()
        height = self.screen.get_height()

        # Panneau principal (score, timer, combo, commande, input) sur une ligne en haut
        self.draw_main_panel(score, timer, combo, current_order_name, user_input, width)

        # Panneau ingrédients préparés
        self.draw_prepared_ingredients_panel(prepared_ingredients)

        # Panneau statut du bot
        self.draw_bot_status_panel(bot)

    def draw_main_panel(self, score, timer, combo, current_order_name, user_input, width):
        """Panneau principal avec score, timer, input sur la même ligne en haut"""
        panel_height = 60

        # Fond semi-transparent du panneau en haut
        overlay = pygame.Surface((width, panel_height), pygame.SRCALPHA)
        overlay.fill((240, 240, 245, 220))
        self.screen.blit(overlay, (0, 0))
        pygame.draw.rect(self.screen, COLORS['gold'], (0, 0, width, panel_height), 3)

        # Score à gauche
        score_text = self.font_medium.render(f"💰 {score}", True, (0, 0, 0))
        self.screen.blit(score_text, (20, 15))

        # Timer à droite du score
        timer_color = COLORS['red'] if timer < 30 else (0, 0, 0)
        timer_text = self.font_medium.render(f"⏱️ {timer:.1f}s", True, timer_color)
        timer_pos_x = 20 + score_text.get_width() + 40
        self.screen.blit(timer_text, (timer_pos_x, 15))

        # Combo à droite du timer
        combo_color = COLORS['gold'] if combo > 0 else (0, 0, 0)
        combo_text = self.font_medium.render(f"🔥 x{combo}", True, combo_color)
        combo_pos_x = timer_pos_x + timer_text.get_width() + 40
        self.screen.blit(combo_text, (combo_pos_x, 15))

        # Commande actuelle à droite du combo (optionnel)
        if current_order_name:
            order_text = self.font_medium.render(f"📋 {current_order_name}", True, COLORS['orange'])
            order_pos_x = combo_pos_x + combo_text.get_width() + 40
            self.screen.blit(order_text, (order_pos_x, 15))

        # Zone de saisie (user_input) alignée à droite sur la même ligne
        input_width = 300
        input_height = 40
        input_x = width - input_width - 20
        input_y = (panel_height - input_height) // 2

        input_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        pygame.draw.rect(self.screen, (245, 245, 250), input_rect)
        pygame.draw.rect(self.screen, COLORS['white'], input_rect, 2)

        input_text = self.font_medium.render(user_input, True, (0, 0, 0))
        self.screen.blit(input_text, (input_rect.x + 10, input_rect.y + 8))

        # Curseur clignotant à la fin du texte saisi
        if int(pygame.time.get_ticks() / 500) % 2:
            cursor_x = input_rect.x + 10 + input_text.get_width()
            pygame.draw.line(self.screen, (0, 0, 0),
                             (cursor_x, input_rect.y + 5),
                             (cursor_x, input_rect.y + input_height - 5), 2)

    def draw_prepared_ingredients_panel(self, prepared_ingredients):
        """Liste des ingrédients préparés"""
        panel_x, panel_y = 10, 90
        panel_width, panel_height = 180, 200

        # Fond
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((230, 245, 230, 200))
        self.screen.blit(panel_surf, (panel_x, panel_y))
        pygame.draw.rect(self.screen, COLORS['green'],
                         (panel_x, panel_y, panel_width, panel_height), 2)

        # Titre
        title = self.font_small.render("🥗 INGRÉDIENTS", True, COLORS['green'])
        self.screen.blit(title, (panel_x + 10, panel_y + 10))

        # Liste des ingrédients
        if prepared_ingredients:
            for idx, ing_type in enumerate(prepared_ingredients):
                y_pos = panel_y + 40 + idx * 25
                # Point vert
                pygame.draw.circle(self.screen, COLORS['green'],
                                   (panel_x + 20, y_pos + 10), 6)
                # Nom de l'ingrédient
                ing_text = self.font_tiny.render(ing_type[:15], True, (0, 0, 0))
                self.screen.blit(ing_text, (panel_x + 35, y_pos + 2))
        else:
            empty = self.font_tiny.render("Aucun", True, (150, 150, 150))
            self.screen.blit(empty, (panel_x + 20, panel_y + 50))

    def draw_bot_status_panel(self, bot):
        """Statut du bot"""
        panel_width, panel_height = 200, 120
        panel_x = self.screen.get_width() - panel_width - 10
        panel_y = 90

        # Fond
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((235, 235, 250, 200))
        self.screen.blit(panel_surf, (panel_x, panel_y))

        state_color = bot.get_state_color() if bot else (0, 0, 0)
        pygame.draw.rect(self.screen, state_color,
                         (panel_x, panel_y, panel_width, panel_height), 3)

        # Titre
        title = self.font_small.render("🤖 BOT", True, state_color)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))

        if bot:
            # État
            state = self.font_tiny.render(bot.get_state_text(), True, (0, 0, 0))
            self.screen.blit(state, (panel_x + 10, panel_y + 40))

            # Inventaire
            if bot.inv:
                inv = self.font_tiny.render(f"Porte: {bot.inv}", True, COLORS['gold'])
                self.screen.blit(inv, (panel_x + 10, panel_y + 60))

            # En préparation
            if bot.preparing:
                prep = self.font_tiny.render(f"Prépare: {bot.preparing}", True, COLORS['orange'])
                self.screen.blit(prep, (panel_x + 10, panel_y + 80))
