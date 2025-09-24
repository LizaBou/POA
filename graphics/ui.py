"""
UI Renderer - Interface utilisateur pour la cuisine en angle carré
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

    def render_full_ui(self, score, timer, combo, bot, user_input, current_order_name, prepared_ingredients, asset_manager):
        """Affiche l'interface complète adaptée à la cuisine en angle"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        # === PANNEAU PRINCIPAL (en haut) ===
        self.draw_main_panel(score, timer, combo, current_order_name, width)
        
        # === PANNEAU INGRÉDIENTS PRÉPARÉS (côté gauche) ===
        self.draw_prepared_ingredients_panel(prepared_ingredients, asset_manager)
        
        # === PANNEAU BOT STATUS (côté droit) ===
        self.draw_bot_status_panel(bot, height)
        
        # === ZONE DE SAISIE (en bas) ===
        self.draw_input_area(user_input, width, height)
        
        # === AIDE VISUELLE ===
        self.draw_help_overlay()

    def draw_main_panel(self, score, timer, combo, current_order_name, width):
        """Panneau principal avec score, timer, combo"""
        # Fond semi-transparent
        panel_height = 80
        overlay = pygame.Surface((width, panel_height), pygame.SRCALPHA)
        overlay.fill((40, 40, 50, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Bordure dorée
        pygame.draw.rect(self.screen, COLORS['gold'], (0, 0, width, panel_height), 3)
        
        # Score avec icône
        score_text = self.font_large.render(f"💰 {score}", True, COLORS['gold'])
        self.screen.blit(score_text, (20, 15))
        
        # Timer avec couleur conditionnelle
        timer_color = COLORS['red'] if timer < 30 else COLORS['white']
        timer_text = self.font_medium.render(f"⏱️ {timer:.1f}s", True, timer_color)
        self.screen.blit(timer_text, (200, 20))
        
        # Combo avec effet
        combo_color = COLORS['gold'] if combo > 0 else COLORS['white']
        combo_text = self.font_medium.render(f"🔥 Combo x{combo}", True, combo_color)
        self.screen.blit(combo_text, (380, 20))
        
        # Commande actuelle avec cadre
        if current_order_name:
            order_x = 580
            order_width = width - order_x - 20
            
            # Cadre de la commande
            order_rect = pygame.Rect(order_x, 10, order_width, 60)
            pygame.draw.rect(self.screen, (80, 60, 40), order_rect)
            pygame.draw.rect(self.screen, COLORS['orange'], order_rect, 2)
            
            # Texte de la commande
            order_text = self.font_medium.render("📋 COMMANDE", True, COLORS['orange'])
            self.screen.blit(order_text, (order_x + 10, 15))
            
            name_text = self.font_small.render(current_order_name, True, COLORS['white'])
            self.screen.blit(name_text, (order_x + 10, 40))

    def draw_prepared_ingredients_panel(self, prepared_ingredients, asset_manager):
        """Panneau des ingrédients préparés (côté gauche)"""
        panel_x = 10
        panel_y = 90
        panel_width = 180
        panel_height = 200
        
        # Fond du panneau
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((50, 70, 50, 180))
        self.screen.blit(panel_surf, (panel_x, panel_y))
        
        # Bordure
        pygame.draw.rect(self.screen, COLORS['green'], 
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Titre
        title_text = self.font_small.render("🥗 INGRÉDIENTS PRÊTS", True, COLORS['green'])
        self.screen.blit(title_text, (panel_x + 10, panel_y + 10))
        
        # Liste des ingrédients préparés
        if prepared_ingredients:
            for idx, ing_type in enumerate(prepared_ingredients):
                y_pos = panel_y + 35 + idx * 25
                
                # Icône de l'ingrédient
                try:
                    if asset_manager:
                        img = asset_manager.get_ingredient_image(ing_type)
                        if img:
                            scaled_img = pygame.transform.scale(img, (20, 20))
                            self.screen.blit(scaled_img, (panel_x + 15, y_pos))
                        else:
                            pygame.draw.circle(self.screen, (100, 200, 100), 
                                             (panel_x + 25, y_pos + 10), 8)
                    else:
                        pygame.draw.circle(self.screen, (100, 200, 100), 
                                         (panel_x + 25, y_pos + 10), 8)
                except:
                    pygame.draw.circle(self.screen, (100, 200, 100), 
                                     (panel_x + 25, y_pos + 10), 8)
                
                # Nom de l'ingrédient
                ing_text = self.font_tiny.render(ing_type[:12], True, COLORS['white'])
                self.screen.blit(ing_text, (panel_x + 45, y_pos + 2))
                
                # Check mark
                pygame.draw.circle(self.screen, COLORS['green'], 
                                 (panel_x + 160, y_pos + 10), 6)
                pygame.draw.line(self.screen, COLORS['white'],
                               (panel_x + 157, y_pos + 10), (panel_x + 159, y_pos + 12), 2)
                pygame.draw.line(self.screen, COLORS['white'],
                               (panel_x + 159, y_pos + 12), (panel_x + 163, y_pos + 8), 2)
        else:
            # Aucun ingrédient préparé
            empty_text = self.font_tiny.render("Aucun ingrédient", True, (150, 150, 150))
            self.screen.blit(empty_text, (panel_x + 20, panel_y + 50))
            empty_text2 = self.font_tiny.render("préparé", True, (150, 150, 150))
            self.screen.blit(empty_text2, (panel_x + 20, panel_y + 70))

    def draw_bot_status_panel(self, bot, height):
        """Panneau de statut du bot (côté droit)"""
        panel_width = 200
        panel_height = 150
        panel_x = self.screen.get_width() - panel_width - 10
        panel_y = 90
        
        # Fond du panneau
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((50, 50, 70, 180))
        self.screen.blit(panel_surf, (panel_x, panel_y))
        
        # Bordure avec couleur d'état
        state_color = bot.get_state_color()
        pygame.draw.rect(self.screen, state_color, 
                        (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Titre
        title_text = self.font_small.render("🤖 STATUS BOT", True, state_color)
        self.screen.blit(title_text, (panel_x + 10, panel_y + 10))
        
        # État actuel
        state_text = self.font_small.render(f"État: {bot.get_state_text()}", True, COLORS['white'])
        self.screen.blit(state_text, (panel_x + 10, panel_y + 35))
        
        # Position
        pos_text = self.font_tiny.render(f"Position: ({int(bot.x)}, {int(bot.y)})", True, (180, 180, 180))
        self.screen.blit(pos_text, (panel_x + 10, panel_y + 55))
        
        # Inventaire
        if bot.inv:
            inv_text = self.font_tiny.render(f"Porte: {bot.inv}", True, COLORS['gold'])
            self.screen.blit(inv_text, (panel_x + 10, panel_y + 75))
        
        # En cours de préparation
        if bot.preparing:
            prep_text = self.font_tiny.render(f"Prépare: {bot.preparing}", True, COLORS['orange'])
            self.screen.blit(prep_text, (panel_x + 10, panel_y + 95))
        
        # Indicateur visuel d'état
        indicator_x = panel_x + panel_width - 30
        indicator_y = panel_y + 20
        pygame.draw.circle(self.screen, state_color, (indicator_x, indicator_y), 12)
        pygame.draw.circle(self.screen, COLORS['white'], (indicator_x, indicator_y), 12, 2)

    def draw_input_area(self, user_input, width, height):
        """Zone de saisie de commande en bas"""
        input_height = 40
        input_y = height - input_height - 10
        
        # Fond
        input_rect = pygame.Rect(10, input_y, width - 20, input_height)
        pygame.draw.rect(self.screen, (30, 30, 40), input_rect)
        pygame.draw.rect(self.screen, COLORS['white'], input_rect, 2)
        
        # Label
        label_text = self.font_small.render("💬 Tapez votre commande:", True, COLORS['white'])
        self.screen.blit(label_text, (15, input_y - 25))
        
        # Texte saisi
        input_text = self.font_medium.render(user_input, True, COLORS['white'])
        self.screen.blit(input_text, (input_rect.x + 10, input_rect.y + 8))
        
        # Curseur clignotant
        if int(pygame.time.get_ticks() / 500) % 2:
            cursor_x = input_rect.x + 10 + input_text.get_width()
            pygame.draw.line(self.screen, COLORS['white'], 
                           (cursor_x, input_rect.y + 5), 
                           (cursor_x, input_rect.y + input_height - 5), 2)

    def draw_help_overlay(self):
        """Affiche l'aide visuelle"""
        help_y = self.screen.get_height() - 80
        
        # Fond semi-transparent
        help_surf = pygame.Surface((self.screen.get_width(), 30), pygame.SRCALPHA)
        help_surf.fill((0, 0, 0, 100))
        self.screen.blit(help_surf, (0, help_y))
        
        # Texte d'aide
        help_text = "💡 Tapez le nom d'un plat pour commander (ex: 'salade', 'sandwich') | ESC pour quitter"
        help_render = self.font_tiny.render(help_text, True, (200, 200, 200))
        help_rect = help_render.get_rect(center=(self.screen.get_width()//2, help_y + 15))
        self.screen.blit(help_render, help_rect)

    def get_input_rect(self):
        """Retourne le rectangle de la zone de saisie"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        input_height = 40
        input_y = height - input_height - 10
        return pygame.Rect(10, input_y, width - 20, input_height)

    def draw_debug_info(self, bot):
        """Affiche les informations de debug (optionnel)"""
        debug_info = bot.get_debug_info()
        debug_y = 300
        
        debug_surf = pygame.Surface((200, 120), pygame.SRCALPHA)
        debug_surf.fill((0, 0, 0, 150))
        self.screen.blit(debug_surf, (10, debug_y))
        
        y_offset = 0
        for key, value in debug_info.items():
            debug_text = f"{key}: {value}"
            text_surf = self.font_tiny.render(debug_text, True, (255, 255, 0))
            self.screen.blit(text_surf, (15, debug_y + 5 + y_offset))
            y_offset += 15