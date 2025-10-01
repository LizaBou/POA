"""
Point d'entrée principal pour Mini Overcooked avec SYSTÈME MULTI-AGENTS COMPÉTITIF
Deux chefs en compétition pour marquer le plus de points!
"""
import sys
import os
import pygame
import time

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=== MINI OVERCOOKED - SYSTÈME MULTI-AGENTS COMPÉTITIF ===")
    print("🏆 Deux chefs en compétition!")
    print("Initialisation de l'interface graphique...")
    
    try:
        import game_state
        from game.logic import GameLogic
        from graphics.kitchen import KitchenRenderer
        from graphics import ui, assets
        from entities.bot import Bot, BotManager
        import config
        
        print("✓ Tous les modules chargés")
        
        # Initialiser pygame
        pygame.init()
        screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Mini Overcooked - Multi-Agents Compétitif")
        clock = pygame.time.Clock()
        
        print("✓ Interface graphique initialisée")
        print(f"✓ Résolution: {config.WIDTH}x{config.HEIGHT}")
        
        # Initialiser le jeu
        game_state.initialize_ingredients()
        game_logic = GameLogic()
        
        # Initialiser le renderer AVANT les bots
        try:
            kitchen_renderer = KitchenRenderer(screen)
            print("✓ Renderer de cuisine initialisé")
        except Exception as e:
            print(f"❌ Erreur renderer: {e}")
            kitchen_renderer = None
            return
        
        # VÉRIFICATION ET INITIALISATION DES VARIABLES GAME_STATE
        print("\n=== VÉRIFICATION GAME_STATE ===")
        
        if not hasattr(game_state, 'current_order_name'):
            game_state.current_order_name = None
        if not hasattr(game_state, 'prepared_ingredients'):
            game_state.prepared_ingredients = []
        if not hasattr(game_state, 'user_input'):
            game_state.user_input = ""
        if not hasattr(game_state, 'plated_dish'):
            game_state.plated_dish = None
        
        # Recettes disponibles
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
            """Démarre une nouvelle commande"""
            if order_name in game_state.available_ingredients:
                if game_state.current_order_name:
                    print(f"⚠ Commande en cours annulée: {game_state.current_order_name}")
                
                game_state.current_order_name = order_name
                game_state.prepared_ingredients.clear()
                game_state.plated_dish = None
                
                # Nettoyer les attributs de compétition
                if hasattr(game_state, 'order_claimed_by'):
                    delattr(game_state, 'order_claimed_by')
                if hasattr(game_state, 'order_claimer_name'):
                    delattr(game_state, 'order_claimer_name')
                
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
        
        # ⭐ INITIALISER LE SYSTÈME MULTI-AGENTS COMPÉTITIF ⭐
        print("\n=== INITIALISATION MULTI-AGENTS COMPÉTITIF ===")
        
        try:
            # Créer le gestionnaire de bots
            bot_manager = BotManager()
            game_state.bot_manager = bot_manager  # ⭐ IMPORTANT: Lien avec game_state
            
            # Créer deux chefs avec positions et apparences différentes
            chef1 = Bot(x=300, y=400, chef_name="Chef Marcel", color_variant=0)
            chef2 = Bot(x=500, y=400, chef_name="Chef Sophie", color_variant=1)
            
            # Ajouter les chefs au manager
            
            bot_manager.add_bot(chef1)
            bot_manager.add_bot(chef2)
            
            print(f"✓ Chef 1: {chef1.chef_name} créé à {chef1.get_position()}")
            print(f"   - bot_id: {chef1.bot_id}")
            print(f"   - Vitesse: {chef1.BOT_SPEED}")
            print(f"✓ Chef 2: {chef2.chef_name} créé à {chef2.get_position()}")
            print(f"   - bot_id: {chef2.bot_id}")
            print(f"   - Vitesse: {chef2.BOT_SPEED}")
            
            # Synchroniser les zones d'interaction avec le renderer
            if kitchen_renderer:
                zones = kitchen_renderer.get_interaction_zones()
                for bot in bot_manager.bots:
                    bot.update_interaction_zones(zones)
                print("✅ Zones d'interaction synchronisées pour tous les chefs")
                print(f"Zone de livraison: {zones.get('delivery')}")
            
            print("✅ Système multi-agents compétitif prêt!")
            
        except Exception as e:
            print(f"❌ Erreur initialisation multi-agents: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Initialiser l'UI
        try:
            ui_renderer = ui.UIRenderer(screen)
            print("✓ Interface utilisateur prête")
        except Exception as e:
            print(f"⚠ Erreur UI: {e}")
            ui_renderer = None
        
        print("\n🎮 LANCEMENT DU JEU EN MODE COMPÉTITION 🎮")
        print("🏆 Les chefs vont se battre pour chaque commande!")
        print("Le plus rapide réclame la commande et marque les points!")
        print("\nRecettes disponibles:")
        for recipe, ingredients in game_state.available_ingredients.items():
            print(f"  - {recipe}: {', '.join(ingredients)}")
        print("\n📝 Tapez une commande et appuyez sur Entrée")
        print("\nRaccourcis:")
        print("  F1 - Debug: Préparer tous les ingrédients instantanément")
        print("  F2 - Debug: Réinitialiser l'état")
        print("  F3 - Debug: Afficher les zones d'interaction")
        print("  F4 - Debug: Info détaillée sur les chefs")
        print("  F5 - Debug: Classement des chefs")
        print("  ESC - Quitter")
        
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
                            print(f"🏁 COURSE! Les chefs vont se battre pour cette commande!")
                        else:
                            print(f"❌ Commande refusée: {order_name}")
                        
                        game_state.user_input = ""
                    elif event.key == pygame.K_F1:
                        # Debug: forcer l'achèvement
                        if game_state.current_order_name:
                            recipe = game_state.available_ingredients[game_state.current_order_name]
                            game_state.prepared_ingredients = recipe.copy()
                            print("🔧 DEBUG: Tous les ingrédients préparés")
                    elif event.key == pygame.K_F2:
                        # Debug: Réinitialiser
                        game_state.current_order_name = None
                        game_state.prepared_ingredients.clear()
                        game_state.plated_dish = None
                        # Nettoyer les attributs de compétition
                        if hasattr(game_state, 'order_claimed_by'):
                            delattr(game_state, 'order_claimed_by')
                        if hasattr(game_state, 'order_claimer_name'):
                            delattr(game_state, 'order_claimer_name')
                        for bot in bot_manager.bots:
                            bot.state = "idle"
                            bot.inv = None
                            bot.preparing = None
                            bot.plating = False
                        print("🔧 DEBUG: État réinitialisé pour tous les chefs")
                    elif event.key == pygame.K_F3:
                        # Debug: Zones
                        print("\n🗺️ ZONES D'INTERACTION:")
                        if bot_manager.bots:
                            for name, coords in bot_manager.bots[0].interaction_zones.items():
                                print(f"   - {name}: {coords}")
                    elif event.key == pygame.K_F4:
                        # Debug: Info chefs
                        print("\n👨‍🍳 INFO DÉTAILLÉE DES CHEFS:")
                        for i, bot in enumerate(bot_manager.bots, 1):
                            info = bot.get_debug_info()
                            print(f"\nChef {i} - {info['name']}:")
                            print(f"  Position: {info['position']}")
                            print(f"  État: {bot.get_state_text()}")
                            print(f"  Inventaire: {info['inventory']}")
                            print(f"  En préparation: {info['preparing']}")
                            print(f"  Peut travailler: {info['can_work']}")
                            print(f"  Motivation: {info['motivation']}")
                            print(f"  bot_id: {bot.bot_id}")
                    elif event.key == pygame.K_F5:
                        # Debug: Classement
                        print("\n🏆 CLASSEMENT DES CHEFS:")
                        leaderboard = bot_manager.get_leaderboard()
                        for i, entry in enumerate(leaderboard, 1):
                            print(f"{i}. {entry['name']}: {entry['score']} points")
                            print(f"   - Plats livrés: {entry['stats']['dishes_delivered']}")
                    else:
                        # Ajouter le caractère
                        if event.unicode.isprintable():
                            game_state.user_input += event.unicode

            # Logique du jeu
            game_logic.update_timer()
            game_logic.reduce_combo_over_time()
            
            # ⭐ MISE À JOUR DU SYSTÈME MULTI-AGENTS ⭐
            try:
                bot_manager.update()
                
                # Debug périodique (toutes les 5 secondes)
                if current_time - last_debug_time >= 5.0:
                    print(f"\n🤖 ÉTAT COMPÉTITION (temps: {game_state.timer:.1f}s):")
                    print(f"  Commande: {game_state.current_order_name}")
                    print(f"  Réclamée par: {getattr(game_state, 'order_claimer_name', 'personne')}")
                    print(f"  Ingrédients prêts: {game_state.prepared_ingredients}")
                    print(f"  Plat assemblé: {game_state.plated_dish}")
                    
                    for i, bot in enumerate(bot_manager.bots, 1):
                        state_text = bot.get_state_text()
                        can_work = "✅ TRAVAILLE" if bot.can_work_on_order() else "⏸️ ATTEND"
                        score = bot_manager.bot_scores.get(bot.bot_id, 0)
                        print(f"  Chef {i} ({bot.chef_name}) - {score} pts: {state_text} [{can_work}]")
                        if bot.inv:
                            print(f"    → Porte: {bot.inv}")
                    
                    last_debug_time = current_time
                    
            except Exception as e:
                print(f"⚠ Erreur mise à jour multi-agents: {e}")
                import traceback
                traceback.print_exc()

            # Rendu
            screen.fill((40, 40, 40))
            
            # Rendu de la cuisine
            try:
                if kitchen_renderer:
                    # Utiliser le premier bot pour les infos générales du rendu
                    primary_bot = bot_manager.bots[0] if bot_manager.bots else None
                    if primary_bot:
                        kitchen_renderer.render_full_kitchen(
                            primary_bot, 
                            asset_manager, 
                            game_state.timer
                        )
                        
                        # Dessiner tous les chefs
                        for bot in bot_manager.bots:
                            bot.draw_chef(screen)
                else:
                    draw_basic_kitchen(screen)
                    # Dessiner les chefs en mode basique
                    for bot in bot_manager.bots:
                        bot.draw_chef(screen)
            except Exception as e:
                print(f"⚠ Erreur rendu cuisine: {e}")
                draw_basic_kitchen(screen)
            
            # Rendu de l'UI
            try:
                if ui_renderer:
                    # Utiliser le premier bot pour l'UI
                    primary_bot = bot_manager.bots[0] if bot_manager.bots else None
                    ui_renderer.render_full_ui(
                        game_state.score,
                        game_state.timer,
                        game_state.combo,
                        primary_bot,
                        game_state.user_input,
                        game_state.current_order_name,
                        game_state.prepared_ingredients,
                        asset_manager,
                        plated_dish=getattr(game_state, 'plated_dish', None)
                    )
                    
                    # Afficher le classement en temps réel
                    font = pygame.font.Font(None, 20)
                    y_offset = 50
                    
                    leaderboard = bot_manager.get_leaderboard()
                    for i, entry in enumerate(leaderboard):
                        color = (255, 215, 0) if i == 0 else (200, 200, 200)
                        text = f"{'🥇' if i == 0 else '🥈'} {entry['name']}: {entry['score']}"
                        score_surf = font.render(text, True, color)
                        screen.blit(score_surf, (config.WIDTH - 220, y_offset + i * 25))
                    
                else:
                    draw_basic_ui(screen, game_state.score, game_state.timer)
            except Exception as e:
                print(f"⚠ Erreur rendu UI: {e}")
                draw_basic_ui(screen, game_state.score, game_state.timer)
            
            pygame.display.flip()
        
        # Fin de partie
        game_logic.stop()
        stats = game_logic.calculate_final_stats()
        
        # Ajouter stats multi-agents
        stats['total_chefs'] = len(bot_manager.bots)
        stats['leaderboard'] = bot_manager.get_leaderboard()
        
        show_game_over_screen(screen, stats, bot_manager)
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
        print("Au revoir !")


def draw_basic_kitchen(screen):
    """Rendu basique si le renderer échoue"""
    try:
        import config
        
        screen.fill((120, 140, 120))
        
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
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        timer_text = font.render(f"Temps: {timer:.1f}s", True, (255, 255, 255))
        screen.blit(timer_text, (10, 50))
        
        import game_state
        if hasattr(game_state, 'current_order_name') and game_state.current_order_name:
            order_text = font.render(f"Commande: {game_state.current_order_name}", True, (255, 215, 0))
            screen.blit(order_text, (10, 90))
        
        if hasattr(game_state, 'user_input'):
            input_text = font.render(f"Tapez: {game_state.user_input}_", True, (200, 200, 200))
            screen.blit(input_text, (10, config.HEIGHT - 40))
            
    except Exception as e:
        print(f"Erreur draw_basic_ui: {e}")


def show_game_over_screen(screen, stats, bot_manager):
    """Écran de fin de partie avec classement compétitif"""
    try:
        import game_state
        import config
        
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        title = font_large.render("PARTIE TERMINÉE!", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(config.WIDTH//2, 100)))
        
        y_offset = 160
        texts = [
            f"Score Total: {game_state.score}",
            f"Combo Maximum: {game_state.combo}",
        ]
        
        for text in texts:
            rendered = font_medium.render(text, True, (255, 255, 255))
            screen.blit(rendered, rendered.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 40
        
        # Classement compétitif
        y_offset += 20
        winner_title = font_large.render("🏆 CLASSEMENT FINAL 🏆", True, (255, 215, 0))
        screen.blit(winner_title, winner_title.get_rect(center=(config.WIDTH//2, y_offset)))
        y_offset += 50
        
        leaderboard = bot_manager.get_leaderboard()
        for i, entry in enumerate(leaderboard):
            if i == 0:
                medal = "🥇"
                color = (255, 215, 0)
                prefix = "GAGNANT: "
            elif i == 1:
                medal = "🥈"
                color = (192, 192, 192)
                prefix = ""
            else:
                medal = "🥉"
                color = (205, 127, 50)
                prefix = ""
            
            chef_text = f"{medal} {prefix}{entry['name']}: {entry['score']} points"
            chef_surf = font_medium.render(chef_text, True, color)
            screen.blit(chef_surf, chef_surf.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 35
            
            stats_text = f"Plats livrés: {entry['stats']['dishes_delivered']}"
            stats_surf = font_small.render(stats_text, True, (200, 200, 200))
            screen.blit(stats_surf, stats_surf.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 30
        
        special_msg = font_medium.render("Merci d'avoir testé le mode compétition!", True, (100, 255, 100))
        screen.blit(special_msg, special_msg.get_rect(center=(config.WIDTH//2, y_offset + 20)))
        
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
            
            time.sleep(0.1)
            
            if game_state.timer > 60:
                break
        
        stats = game_logic.calculate_final_stats()
        print(f"\nJeu terminé!")
        print(f"Score final: {game_state.score}")
        
    except Exception as e:
        print(f"Erreur mode console: {e}")


if __name__ == "__main__":
    main()