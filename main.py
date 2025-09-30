"""
Point d'entrée principal pour Mini Overcooked avec interface graphique - VERSION ADAPTÉE
Compatible avec Bot entity et KitchenRenderer avec système d'assiettes
"""
import sys
import os
import pygame
import time

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=== MINI OVERCOOKED - VERSION ASSIETTES ===")
    print("Initialisation de l'interface graphique...")
    
    try:
        import game_state
        from game.logic import GameLogic
        from graphics.kitchen import KitchenRenderer  # Utilise le nouveau renderer
        from graphics import ui, assets
        from entities.bot import Bot  # Utilise la nouvelle classe Bot
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
        kitchen_renderer = KitchenRenderer(screen)  # Nouveau renderer
        
        # VÉRIFICATION ET INITIALISATION DES VARIABLES GAME_STATE
        print("\n=== VÉRIFICATION GAME_STATE ===")
        
        # Variables essentielles pour le système d'assiettes
        if not hasattr(game_state, 'current_order_name'):
            game_state.current_order_name = None
        if not hasattr(game_state, 'prepared_ingredients'):
            game_state.prepared_ingredients = []
        if not hasattr(game_state, 'user_input'):
            game_state.user_input = ""
        if not hasattr(game_state, 'plated_dish'):
            game_state.plated_dish = None  # NOUVEAU: plat assemblé sur assiette
        
        # Recettes disponibles (compatible avec le bot)
        if not hasattr(game_state, 'available_ingredients'):
            game_state.available_ingredients = {
                "salade": ["laitue", "tomate"],
                "burger": ["pain", "steak", "laitue", "tomate"],
                "sandwich": ["pain", "fromage", "tomate"],
                "salade_complete": ["laitue", "tomate", "fromage"],
                "burger_deluxe": ["pain", "steak", "laitue", "tomate", "fromage"]
            }
        
        print(f"current_order_name: {game_state.current_order_name}")
        print(f"prepared_ingredients: {game_state.prepared_ingredients}")
        print(f"plated_dish: {getattr(game_state, 'plated_dish', None)}")
        print(f"available_recipes: {list(game_state.available_ingredients.keys())}")
        
        # Fonction pour démarrer une nouvelle commande
        def start_new_order(order_name):
            """Démarre une nouvelle commande avec le système d'assiettes"""
            if order_name in game_state.available_ingredients:
                if game_state.current_order_name:
                    print(f"⚠ Commande en cours annulée: {game_state.current_order_name}")
                
                game_state.current_order_name = order_name
                game_state.prepared_ingredients.clear()
                game_state.plated_dish = None  # Réinitialiser le plat assemblé
                print(f"✓ Nouvelle commande: {order_name}")
                print(f"Ingrédients requis: {game_state.available_ingredients[order_name]}")
                return True
            else:
                print(f"❌ Recette inconnue: {order_name}")
                print(f"Recettes disponibles: {list(game_state.available_ingredients.keys())}")
                return False
        
        game_state.start_new_order = start_new_order
        
        # Initialiser les assets
        try:
            asset_manager = assets.AssetManager()
            print("✓ Assets chargés")
        except Exception as e:
            print(f"⚠ Erreur assets: {e}")
            asset_manager = None
        
        # Initialiser le bot avec le nouveau système
        try:
            game_bot = Bot(x=400, y=400)  # Position centrale
            print("✓ Bot initialisé avec système d'assiettes")
            print(f"Bot position initiale: {game_bot.get_position()}")
            print(f"Bot états disponibles: {list(game_bot.get_debug_info().keys())}")
        except Exception as e:
            print(f"❌ Erreur bot: {e}")
            import traceback
            traceback.print_exc()
            game_bot = None
            return
        
        # Initialiser l'UI
        try:
            ui_renderer = ui.UIRenderer(screen)
            print("✓ Interface utilisateur prête")
        except Exception as e:
            print(f"⚠ Erreur UI: {e}")
            ui_renderer = None
        
        print("\n🎮 LANCEMENT DU JEU AVEC SYSTÈME D'ASSIETTES 🎮")
        print("Recettes disponibles:")
        for recipe, ingredients in game_state.available_ingredients.items():
            print(f"  - {recipe}: {', '.join(ingredients)}")
        print("\nTapez une commande et appuyez sur Entrée pour la lancer")
        print("Le bot va maintenant assembler les plats sur des assiettes!")
        print("Appuyez sur ESC ou fermez la fenêtre pour quitter")
        
        running = True
        frame_count = 0
        last_debug_time = 0
        
        while running and game_logic.is_running():
            dt = clock.tick(60) / 1000.0
            frame_count += 1
            current_time = time.time()
            
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
                        print(f"\n🍽️ NOUVELLE COMMANDE: '{order_name}'")
                        
                        success = start_new_order(order_name)
                        if success:
                            print(f"✅ Commande acceptée: {order_name}")
                            print(f"🤖 Le bot va commencer à travailler...")
                        else:
                            print(f"❌ Commande refusée: {order_name}")
                        
                        game_state.user_input = ""
                    elif event.key == pygame.K_F1:
                        # Debug: forcer l'achèvement d'une commande
                        if game_state.current_order_name:
                            recipe = game_state.available_ingredients[game_state.current_order_name]
                            game_state.prepared_ingredients = recipe.copy()
                            print("🔧 DEBUG: Tous les ingrédients préparés instantanément")
                    elif event.key == pygame.K_F2:
                        # Debug: Réinitialiser l'état
                        game_state.current_order_name = None
                        game_state.prepared_ingredients.clear()
                        game_state.plated_dish = None
                        game_bot.state = "idle"
                        game_bot.inv = None
                        game_bot.preparing = None
                        game_bot.plating = False
                        print("🔧 DEBUG: État réinitialisé")
                    else:
                        # Ajouter le caractère tapé
                        if event.unicode.isprintable():
                            game_state.user_input += event.unicode

            # Logique du jeu
            game_logic.update_timer()
            game_logic.reduce_combo_over_time()
            
            # Mise à jour du bot avec le nouveau système
            if game_bot:
                try:
                    game_bot.update(dt)
                    
                    # Debug détaillé toutes les 2 secondes
                    if current_time - last_debug_time >= 2.0:
                        debug_info = game_bot.get_debug_info()
                        print(f"\n🤖 DEBUG BOT (temps: {game_state.timer:.1f}s):")
                        print(f"  État: {game_bot.get_state_text()}")
                        print(f"  Position: {debug_info['position']}")
                        print(f"  Cible: {debug_info['target']}")
                        print(f"  Distance: {debug_info['distance_to_target']}")
                        print(f"  Inventaire: {debug_info['inventory']}")
                        print(f"  En préparation: {debug_info['preparing']}")
                        print(f"  Assemblage: {debug_info['plating']}")
                        print(f"  Commande: {game_state.current_order_name}")
                        print(f"  Ingrédients prêts: {game_state.prepared_ingredients}")
                        print(f"  Plat assemblé: {debug_info['plated_dish']}")
                        print(f"  Prochain besoin: {debug_info['next_needed']}")
                        print(f"  Tous prêts: {debug_info['all_ingredients_ready']}")
                        last_debug_time = current_time
                except Exception as e:
                    print(f"⚠ Erreur mise à jour bot: {e}")
                    import traceback
                    traceback.print_exc()

            # Rendu avec le nouveau système
            screen.fill((40, 40, 40))
            
            try:
                if kitchen_renderer and game_bot:
                    # Utilise le nouveau renderer avec support des assiettes
                    kitchen_renderer.render_full_kitchen(game_bot, asset_manager, game_state.timer)
                else:
                    draw_basic_kitchen(screen)
            except Exception as e:
                print(f"⚠ Erreur rendu cuisine: {e}")
                draw_basic_kitchen(screen)
            
            try:
                if ui_renderer:
                    # Interface utilisateur adaptée
                    ui_renderer.render_full_ui(
                        game_state.score,
                        game_state.timer,
                        game_state.combo,
                        game_bot,
                        game_state.user_input,
                        game_state.current_order_name,
                        game_state.prepared_ingredients,
                        asset_manager,
                        plated_dish=getattr(game_state, 'plated_dish', None)
                    )
                else:
                    draw_basic_ui(screen, game_state.score, game_state.timer)
            except Exception as e:
                print(f"⚠ Erreur rendu UI: {e}")
                draw_basic_ui(screen, game_state.score, game_state.timer)
            
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
        
        # Sol de base
        screen.fill((120, 140, 120))
        
        # Zones simplifiées
        # Zone de stockage (gauche)
        pygame.draw.rect(screen, (200, 200, 255), (50, 120, 300, 350))
        pygame.draw.rect(screen, (100, 100, 200), (50, 120, 300, 350), 3)
        
        # Plan de travail (centre-haut)
        pygame.draw.rect(screen, (160, 120, 80), (400, 120, 250, 120))
        pygame.draw.rect(screen, (120, 80, 40), (400, 120, 250, 120), 3)
        
        # Station d'assemblage (centre-bas)
        pygame.draw.rect(screen, (240, 230, 220), (400, 280, 250, 100))
        pygame.draw.rect(screen, (180, 150, 120), (400, 280, 250, 100), 3)
        
        # Zone de service (droite)
        pygame.draw.rect(screen, (255, 200, 100), (700, 120, 120, 300))
        pygame.draw.rect(screen, (200, 150, 50), (700, 120, 120, 300), 3)
        
        # Étiquettes
        font = pygame.font.Font(None, 24)
        
        labels = [
            ("STOCKAGE", (150, 100)),
            ("PRÉPARATION", (450, 100)),
            ("ASSEMBLAGE", (450, 260)),
            ("SERVICE", (720, 100))
        ]
        
        for text, pos in labels:
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, pos)
            
    except Exception as e:
        screen.fill((50, 50, 50))
        print(f"Erreur draw_basic_kitchen: {e}")


def draw_basic_ui(screen, score, timer):
    """Interface basique si l'UI échoue"""
    try:
        import config
        font = pygame.font.Font(None, 36)
        
        # Score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Timer
        timer_text = font.render(f"Temps: {timer:.1f}s", True, (255, 255, 255))
        screen.blit(timer_text, (10, 50))
        
        # Commande actuelle
        import game_state
        if hasattr(game_state, 'current_order_name') and game_state.current_order_name:
            order_text = font.render(f"Commande: {game_state.current_order_name}", True, (255, 215, 0))
            screen.blit(order_text, (10, 90))
        
        # Input
        if hasattr(game_state, 'user_input'):
            input_text = font.render(f"Tapez: {game_state.user_input}_", True, (200, 200, 200))
            screen.blit(input_text, (10, config.HEIGHT - 40))
            
    except Exception as e:
        print(f"Erreur draw_basic_ui: {e}")


def show_game_over_screen(screen, stats):
    """Écran de fin de partie"""
    try:
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
            f"Plats Livrés: {stats.get('plates_delivered', 0)}",
            f"Efficacité: {stats.get('efficiency', 0)}%"
        ]
        
        for text in texts:
            rendered = font_medium.render(text, True, (255, 255, 255))
            screen.blit(rendered, rendered.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 40
        
        # Message spécial pour le système d'assiettes
        special_msg = font_medium.render("Merci d'avoir testé le système d'assiettes!", True, (100, 255, 100))
        screen.blit(special_msg, special_msg.get_rect(center=(config.WIDTH//2, y_offset + 40)))
        
        pygame.display.flip()
        
    except Exception as e:
        print(f"Erreur show_game_over_screen: {e}")


def run_console_fallback():
    """Mode console si pygame échoue"""
    try:
        import game_state
        from game.logic import GameLogic
        
        print("Mode console de secours...")
        game_state.initialize_ingredients()
        game_logic = GameLogic()
        
        print("Tapez 'quit' pour arrêter")
        
        while game_logic.is_running():
            game_logic.update_timer()
            print(f"\rScore: {game_state.score} | Temps: {game_state.timer:.1f}s", end="")
            
            # Simulation d'input non-bloquant (simplifié)
            time.sleep(0.1)
            
            if game_state.timer > 60:  # Fin après 1 minute
                break
        
        stats = game_logic.calculate_final_stats()
        print(f"\nJeu terminé!")
        print(f"Score final: {game_state.score}")
        
    except Exception as e:
        print(f"Erreur mode console: {e}")


if __name__ == "__main__":
    main()