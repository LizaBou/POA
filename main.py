"""
Point d'entrée principal pour Mini Overcooked avec interface graphique - VERSION DEBUG
"""
import sys
import os
import pygame
import time

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=== MINI OVERCOOKED ===")
    print("Initialisation de l'interface graphique...")
    
    try:
        import game_state
        from game.logic import GameLogic
        from graphics.kitchen import KitchenRenderer
        from graphics import ui, assets
        from entities import bot
        import config
        
        print("✓ Tous les modules chargés")
        
        # Initialiser pygame
        pygame.init()
        screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)
        clock = pygame.time.Clock()
        
        print("✓ Interface graphique initialisée")
        print(f"✓ Résolution: {config.WIDTH}x{config.HEIGHT}")
        
        # Initialiser le jeu
        game_state.initialize_ingredients()
        game_logic = GameLogic()
        kitchen_renderer = KitchenRenderer(screen)
        
        # VÉRIFICATION DES VARIABLES GAME_STATE
        print("\n=== VÉRIFICATION GAME_STATE ===")
        print(f"current_order_name: {getattr(game_state, 'current_order_name', 'MANQUANT')}")
        print(f"prepared_ingredients: {getattr(game_state, 'prepared_ingredients', 'MANQUANT')}")
        print(f"available_ingredients: {getattr(game_state, 'available_ingredients', 'MANQUANT')}")
        print(f"user_input: {getattr(game_state, 'user_input', 'MANQUANT')}")
        
        # Initialiser les variables manquantes si nécessaire
        if not hasattr(game_state, 'current_order_name'):
            game_state.current_order_name = None
        if not hasattr(game_state, 'prepared_ingredients'):
            game_state.prepared_ingredients = []
        if not hasattr(game_state, 'user_input'):
            game_state.user_input = ""
        
        # Initialiser les assets
        try:
            asset_manager = assets.AssetManager()
            print("✓ Assets chargés")
        except Exception as e:
            print(f"⚠ Erreur assets: {e}")
            asset_manager = None
        
        # Initialiser le bot
        try:
            game_bot = bot.Bot()
            print("✓ Bot initialisé")
            print(f"Bot position initiale: {game_bot.get_position()}")
        except Exception as e:
            print(f"⚠ Erreur bot: {e}")
            import traceback
            traceback.print_exc()
            game_bot = None
        
        # Initialiser l'UI
        try:
            ui_renderer = ui.UIRenderer(screen)
            print("✓ Interface utilisateur prête")
        except Exception as e:
            print(f"⚠ Erreur UI: {e}")
            ui_renderer = None
        
        print("\n🎮 LANCEMENT DU JEU 🎮")
        print("Tapez une commande (ex: salade, burger...) et appuyez sur Entrée pour la lancer")
        print("Appuyez sur ESC ou fermez la fenêtre pour quitter")
        
        running = True
        frame_count = 0
        
        while running and game_logic.is_running():
            dt = clock.tick(60) / 1000.0
            frame_count += 1
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        game_state.user_input = game_state.user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Valider la commande
                        order_name = game_state.user_input.lower().strip()
                        print(f"\n🍽️ TENTATIVE DE COMMANDE: '{order_name}'")
                        
                        if hasattr(game_state, 'start_new_order'):
                            success = game_state.start_new_order(order_name)
                            print(f"Résultat start_new_order: {success}")
                        else:
                            # Fonction manquante, créer une version simple
                            if hasattr(game_state, 'available_ingredients') and order_name in game_state.available_ingredients:
                                game_state.current_order_name = order_name
                                game_state.prepared_ingredients.clear()
                                print(f"✓ Commande {order_name} démarrée (fonction de secours)")
                                success = True
                            else:
                                print(f"❌ Commande inconnue: {order_name}")
                                success = False
                        
                        if success:
                            print(f"✓ Nouvelle commande lancée: {order_name}")
                            print(f"État après commande: current_order_name={game_state.current_order_name}")
                        else:
                            print(f"❌ Commande échouée: {order_name}")
                        
                        game_state.user_input = ""
                    else:
                        game_state.user_input += event.unicode

            # Logique du jeu
            game_logic.update_timer()
            game_logic.reduce_combo_over_time()
            
            # Mise à jour du bot avec debug
            if game_bot:
                game_bot.update(dt)
                
                # Debug toutes les 60 frames (1 seconde)
                if frame_count % 60 == 0:
                    debug_info = game_bot.get_debug_info()
                    print(f"\n🤖 DEBUG BOT (frame {frame_count}):")
                    for key, value in debug_info.items():
                        print(f"  {key}: {value}")
                    print(f"  Commande active: {game_state.current_order_name}")
                    print(f"  Ingrédients préparés: {game_state.prepared_ingredients}")

            # Rendu
            screen.fill((40, 40, 40))
            
            if kitchen_renderer and asset_manager and game_bot:
                kitchen_renderer.render_full_kitchen(game_bot, asset_manager, game_state.timer)
            else:
                draw_basic_kitchen(screen)
            
            if ui_renderer:
                ui_renderer.render_full_ui(
                    game_state.score,
                    game_state.timer,
                    game_state.combo,
                    game_bot,
                    game_state.user_input,
                    game_state.current_order_name,
                    game_state.prepared_ingredients,
                    asset_manager
                )
            
            pygame.display.flip()
        
        # Fin de partie
        game_logic.stop()
        stats = game_logic.calculate_final_stats()
        show_game_over_screen(screen, stats)
        time.sleep(3)
    
    except ImportError as e:
        print(f"❌ Module manquant: {e}")
        import traceback
        traceback.print_exc()
        run_console_fallback()
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("Au revoir ! 👋")


def draw_basic_kitchen(screen):
    """Rendu basique si le renderer échoue"""
    try:
        import config
        screen.fill((100, 150, 100))
        pygame.draw.rect(screen, (200, 200, 255), 
                         (config.fridge["x"], config.fridge["y"], config.fridge["w"], config.fridge["h"]))
        pygame.draw.rect(screen, (160, 120, 80), 
                         (config.cutting_board["x"], config.cutting_board["y"], config.cutting_board["w"], config.cutting_board["h"]))
        pygame.draw.rect(screen, (255, 200, 100), 
                         (config.delivery_counter["x"], config.delivery_counter["y"], config.delivery_counter["w"], config.delivery_counter["h"]))
    except Exception as e:
        screen.fill((50, 50, 50))
        print(f"Erreur draw_basic_kitchen: {e}")


def show_game_over_screen(screen, stats):
    import game_state
    import config
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 32)
    
    title = font_large.render("PARTIE TERMINÉE!", True, (255, 215, 0))
    screen.blit(title, title.get_rect(center=(config.WIDTH//2, 200)))
    
    y_offset = 280
    texts = [
        f"Score Final: {game_state.score}",
        f"Combo Maximum: {game_state.combo}",
        f"Plats Livrés: {stats['plates_delivered']}",
        f"Efficacité: {stats['efficiency']}%"
    ]
    
    for text in texts:
        rendered = font_medium.render(text, True, (255, 255, 255))
        screen.blit(rendered, rendered.get_rect(center=(config.WIDTH//2, y_offset)))
        y_offset += 40
    
    pygame.display.flip()


def run_console_fallback():
    """Mode console si pygame échoue"""
    import game_state
    from game.logic import GameLogic
    import config
    print("Mode console de secours...")
    game_state.initialize_ingredients()
    game_logic = GameLogic()
    while game_logic.is_running():
        game_logic.update_timer()
        print(f"\rScore: {game_state.score} | Temps: {game_state.timer:.1f}s", end="")
        time.sleep(0.1)
    stats = game_logic.calculate_final_stats()
    game_logic.print_final_stats(stats)


if __name__ == "__main__":
    main()