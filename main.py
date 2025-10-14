"""
Point d'entrée principal pour Mini Overcooked avec VRAIE COMPÉTITION MULTI-AGENTS
✅ Chaque chef prend SA PROPRE commande
✅ Travail simultané - PAS D'ATTENTE
✅ Utilise OrderManager pour gérer les commandes multiples
✅ RENDU CORRIGÉ - Ingrédients bien visibles
"""
import sys
import os
import pygame
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=== MINI OVERCOOKED - VRAIE COMPÉTITION MULTI-AGENTS ===")
    print("🏆 Chaque chef prend SA PROPRE commande!")
    print("✅ TRAVAIL SIMULTANÉ - PAS D'ATTENTE")
    print("Initialisation de l'interface graphique...")
    
    try:
        import game_state
        from game.logic import GameLogic
        from graphics.kitchen import KitchenRenderer
        from graphics import ui, assets
        from entities.bot import Bot, BotManager
        from entities.order_manager import OrderManager
        import config
        
        print("✓ Tous les modules chargés")
        
        # Initialiser pygame
        pygame.init()
        screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Mini Overcooked - Vraie Compétition Multi-Agents")
        clock = pygame.time.Clock()
        
        print("✓ Interface graphique initialisée")
        print(f"✓ Résolution: {config.WIDTH}x{config.HEIGHT}")
        
        # Initialiser le jeu
        game_state.initialize_ingredients()
        game_logic = GameLogic()
        
        # Initialiser le renderer
        try:
            kitchen_renderer = KitchenRenderer(screen)
            print("✓ Renderer de cuisine initialisé")
        except Exception as e:
            print(f"❌ Erreur renderer: {e}")
            kitchen_renderer = None
            return
        
        # ⭐ INITIALISER ORDERMANAGER (système de commandes multiples)
        print("\n=== INITIALISATION ORDERMANAGER ===")
        order_manager = OrderManager()
        game_state.order_manager = order_manager
        
        # Recettes disponibles
        game_state.available_ingredients = {
            "salade": ["laitue", "tomate"],
            "burger": ["pain", "steak", "laitue", "tomate"],
            "sandwich": ["pain", "fromage", "tomate"],
            "salade_complete": ["laitue", "tomate", "fromage"],
            "burger_deluxe": ["pain", "steak", "laitue", "tomate", "fromage"]
        }
        
        game_state.user_input = ""
        game_state.score = 0
        
        print(f"✓ OrderManager prêt")
        print(f"✓ Recettes disponibles: {list(game_state.available_ingredients.keys())}")
        
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
            game_state.bot_manager = bot_manager
            
    
            # Créer deux chefs
            chef1 = Bot(x=300, y=400, chef_name="Chef Marcel", color_variant=0)
            chef2 = Bot(x=500, y=400, chef_name="Chef Sophie", color_variant=1)
            
            # Ajouter les chefs au manager
            bot_manager.add_bot(chef1)
            bot_manager.add_bot(chef2)
            
            print(f"✓ Chef 1: {chef1.chef_name} créé")
            print(f"✓ Chef 2: {chef2.chef_name} créé")
            
            # Synchroniser les zones d'interaction
            if kitchen_renderer:
                zones = kitchen_renderer.get_interaction_zones()
                for bot in bot_manager.bots:
                    bot.update_interaction_zones(zones)
                print("✅ Zones d'interaction synchronisées")
            
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
        
        print("\n🎮 LANCEMENT DU JEU EN MODE COMPÉTITION RÉELLE 🎮")
        print("🏆 Chaque chef peut prendre SA PROPRE commande!")
        print("✅ Travail simultané - Les deux peuvent travailler en même temps!")
        print("\nRecettes disponibles:")
        for recipe, ingredients in game_state.available_ingredients.items():
            print(f"  - {recipe}: {', '.join(ingredients)}")
        print("\n📝 Tapez UNE COMMANDE PAR LIGNE et appuyez sur Entrée")
        print("💡 Ajoutez plusieurs commandes pour voir les chefs se battre!")
        print("\nRaccourcis:")
        print("  F1 - Ajouter 5 commandes random (test rapide)")
        print("  F2 - Debug: Réinitialiser")
        print("  F3 - Debug: Afficher zones d'interaction")
        print("  F4 - Debug: Info détaillée sur les chefs")
        print("  F5 - Debug: Classement des chefs")
        print("  F6 - Debug: Afficher le système de commandes")
        print("  ESC - Quitter")
        
        running = True
        frame_count = 0
        last_debug_time = 0
        
        # Liste des recettes pour F1 (test rapide)
        recipe_names = list(game_state.available_ingredients.keys())
        
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
                        # Ajouter la commande via OrderManager
                        order_name = game_state.user_input.lower().strip()
                        print(f"\n🍽️ AJOUT COMMANDE: '{order_name}'")
                        
                        if order_name in game_state.available_ingredients:
                            ingredients = game_state.available_ingredients[order_name]
                            order_manager.add_order(order_name, ingredients)
                            print(f"✅ Commande '{order_name}' ajoutée à la file")
                        else:
                            print(f"❌ Recette inconnue: {order_name}")
                        
                        game_state.user_input = ""
                    
                    elif event.key == pygame.K_F1:
                        # Ajouter 5 commandes random pour test
                        import random
                        print("\n🎲 AJOUT DE 5 COMMANDES RANDOM:")
                        for i in range(5):
                            recipe = random.choice(recipe_names)
                            ingredients = game_state.available_ingredients[recipe]
                            order_manager.add_order(recipe, ingredients)
                            print(f"  {i+1}. {recipe}")
                        print("✅ 5 commandes ajoutées - Les chefs vont s'affronter!")
                    
                    elif event.key == pygame.K_F2:
                        # Réinitialiser tout
                        order_manager.reset()
                        for bot in bot_manager.bots:
                            bot.state = "idle"
                            bot.inv = None
                            bot.preparing = None
                            bot.plating = False
                        print("🔧 DEBUG: Système complètement réinialisé")
                    
                    elif event.key == pygame.K_F3:
                        # Afficher les zones
                        print("\n🗺️ ZONES D'INTERACTION:")
                        if bot_manager.bots:
                            for name, coords in bot_manager.bots[0].interaction_zones.items():
                                print(f"   - {name}: {coords}")
                    
                    elif event.key == pygame.K_F4:
                        # Info détaillée des chefs
                        print("\n👨‍🍳 INFO DÉTAILLÉE DES CHEFS:")
                        for i, bot in enumerate(bot_manager.bots, 1):
                            info = bot.get_debug_info()
                            print(f"\nChef {i} - {info['name']}:")
                            print(f"  Position: {info['position']}")
                            print(f"  État: {bot.get_state_text()}")
                            print(f"  Inventaire: {info['inventory']}")
                            print(f"  En préparation: {info['preparing']}")
                            print(f"  A une commande: {info['has_order']}")
                            print(f"  Motivation: {info['motivation']}")
                            
                            progress = order_manager.get_chef_progress(bot.bot_id)
                            if progress:
                                print(f"  🍽️ Commande actuelle: {progress['order_name']}")
                                print(f"     Progression: {progress['prepared']}/{progress['required']}")
                                print(f"     Manquants: {progress['ingredients_needed']}")
                    
                    elif event.key == pygame.K_F5:
                        # Classement
                        print("\n🏆 CLASSEMENT DES CHEFS:")
                        leaderboard = bot_manager.get_leaderboard()
                        for i, entry in enumerate(leaderboard, 1):
                            print(f"{i}. {entry['name']}: {entry['score']} points")
                            print(f"   - Plats livrés: {entry['stats']['dishes_delivered']}")
                    
                    elif event.key == pygame.K_F6:
                        # Afficher le système de commandes
                        print("\n📋 SYSTÈME DE COMMANDES:")
                        status = order_manager.get_status_summary()
                        print(f"  Disponibles: {status['available_orders']}")
                        print(f"  Actives: {status['active_orders']}")
                        print(f"  Complétées: {status['completed_orders']}")
                        
                        if status['chefs_working']:
                            print("\n  👨‍🍳 Chefs en action:")
                            for chef_info in status['chefs_working']:
                                print(f"    - {chef_info['chef']}: {chef_info['order']} ({chef_info['progress']})")
                        
                        if order_manager.available_orders:
                            print("\n  📋 File d'attente:")
                            for i, order in enumerate(order_manager.available_orders[:5], 1):
                                print(f"    {i}. {order['name']}")
                    
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
                    status = order_manager.get_status_summary()
                    print(f"\n🤖 ÉTAT COMPÉTITION (temps: {game_state.timer:.1f}s):")
                    print(f"  📋 Disponibles: {status['available_orders']} | Actives: {status['active_orders']} | Complétées: {status['completed_orders']}")
                    
                    for chef_info in status['chefs_working']:
                        print(f"  ✅ {chef_info['chef']}: {chef_info['order']} ({chef_info['progress']})")
                    
                    for bot in bot_manager.bots:
                        if not order_manager.get_chef_order(bot.bot_id):
                            print(f"  ⏳ {bot.chef_name}: Cherche une commande...")
                    
                    last_debug_time = current_time
                    
            except Exception as e:
                print(f"⚠ Erreur mise à jour multi-agents: {e}")
                import traceback
                traceback.print_exc()

            # 🎨 RENDU CORRIGÉ - Ingrédients bien visibles 🎨
            screen.fill((40, 40, 40))
            
            try:
                if kitchen_renderer:
                    # 1️⃣ Dessiner la cuisine UNE SEULE FOIS
                    kitchen_renderer.draw_floor()
                    kitchen_renderer.draw_individual_ingredient_stations(asset_manager)
                    kitchen_renderer.draw_work_station(asset_manager)
                    kitchen_renderer.draw_plating_station(asset_manager)
                    kitchen_renderer.draw_service_station()
                    
                    # 2️⃣ Mettre à jour les zones pour tous les bots
                    zones = kitchen_renderer.get_interaction_zones()
                    for bot in bot_manager.bots:
                        bot.update_interaction_zones(zones)
                    
                    # 3️⃣ Dessiner TOUS les chefs avec leurs ingrédients (PAR-DESSUS)
                    for bot in bot_manager.bots:
                        kitchen_renderer.draw_chef_enhanced(bot, asset_manager)
                    
                    # 4️⃣ Afficher le statut du premier chef seulement
                    if bot_manager.bots:
                        kitchen_renderer.draw_chef_status(bot_manager.bots[0])
                else:
                    draw_basic_kitchen(screen)
                    for bot in bot_manager.bots:
                        bot.draw_chef(screen)
            except Exception as e:
                print(f"⚠ Erreur rendu cuisine: {e}")
                import traceback
                traceback.print_exc()
                draw_basic_kitchen(screen)
                for bot in bot_manager.bots:
                    bot.draw_chef(screen)
            
            # Rendu de l'UI
            try:
                if ui_renderer:
                    primary_bot = bot_manager.bots[0] if bot_manager.bots else None
                    ui_renderer.render_full_ui(
                        game_state.score,
                        game_state.timer,
                        getattr(game_state, 'combo', 0),
                        primary_bot,
                        game_state.user_input,
                        None,  # Plus de current_order_name unique
                        [],    # Plus de prepared_ingredients unique
                        asset_manager,
                       
                    )
                    
                    # ⭐ Afficher le système de compétition à l'écran
                    font = pygame.font.Font(None, 20)
                    y_offset = 50
                    
                    # Classement
                    leaderboard = bot_manager.get_leaderboard()
                    for i, entry in enumerate(leaderboard):
                        color = (255, 215, 0) if i == 0 else (200, 200, 200)
                        medal = "🥇" if i == 0 else "🥈"
                        text = f"{medal} {entry['name']}: {entry['score']}"
                        score_surf = font.render(text, True, color)
                        screen.blit(score_surf, (config.WIDTH - 220, y_offset + i * 25))
                    
                    # Système de commandes
                    y_offset = 150
                    status = order_manager.get_status_summary()
                    
                    queue_title = font.render("📋 SYSTÈME:", True, (255, 255, 255))
                    screen.blit(queue_title, (config.WIDTH - 220, y_offset))
                    y_offset += 25
                    
                    stats_text = f"Dispo: {status['available_orders']} | Actives: {status['active_orders']}"
                    stats_surf = font.render(stats_text, True, (200, 200, 200))
                    screen.blit(stats_surf, (config.WIDTH - 220, y_offset))
                    y_offset += 25
                    
                    completed_text = f"Complétées: {status['completed_orders']}"
                    completed_surf = font.render(completed_text, True, (150, 255, 150))
                    screen.blit(completed_surf, (config.WIDTH - 220, y_offset))
                    y_offset += 30
                    
                    # Commandes actives
                    if status['chefs_working']:
                        active_title = font.render("⚙️ EN COURS:", True, (255, 255, 100))
                        screen.blit(active_title, (config.WIDTH - 220, y_offset))
                        y_offset += 20
                        
                        for chef_info in status['chefs_working']:
                            chef_text = f"• {chef_info['chef'][:8]}:"
                            chef_surf = font.render(chef_text, True, (200, 200, 200))
                            screen.blit(chef_surf, (config.WIDTH - 215, y_offset))
                            y_offset += 18
                            
                            order_text = f"  {chef_info['order']} {chef_info['progress']}"
                            order_surf = font.render(order_text, True, (150, 255, 150))
                            screen.blit(order_surf, (config.WIDTH - 210, y_offset))
                            y_offset += 22
                    
                    y_offset += 10
                    
                    # File d'attente
                    if order_manager.available_orders:
                        queue_title2 = font.render("⏳ FILE:", True, (255, 200, 100))
                        screen.blit(queue_title2, (config.WIDTH - 220, y_offset))
                        y_offset += 20
                        
                        for i, order in enumerate(order_manager.available_orders[:3], 1):
                            order_text = f"{i}. {order['name']}"
                            order_surf = font.render(order_text, True, (200, 200, 150))
                            screen.blit(order_surf, (config.WIDTH - 210, y_offset))
                            y_offset += 18
                        
                        if len(order_manager.available_orders) > 3:
                            more_text = f"... +{len(order_manager.available_orders) - 3}"
                            more_surf = font.render(more_text, True, (150, 150, 150))
                            screen.blit(more_surf, (config.WIDTH - 210, y_offset))
                    
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
        
        pygame.draw.rect(screen, (200, 200, 255), (50, 120, 300, 350))
        pygame.draw.rect(screen, (100, 100, 200), (50, 120, 300, 350), 3)
        
        pygame.draw.rect(screen, (160, 120, 80), (400, 120, 250, 120))
        pygame.draw.rect(screen, (120, 80, 40), (400, 120, 250, 120), 3)
        
        pygame.draw.rect(screen, (240, 230, 220), (400, 280, 250, 100))
        pygame.draw.rect(screen, (180, 150, 120), (400, 280, 250, 100), 3)
        
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
        score_text = f"Score Total: {game_state.score}"
        rendered = font_medium.render(score_text, True, (255, 255, 255))
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
        
        special_msg = font_medium.render("Système Multi-Agents Compétitif!", True, (100, 255, 100))
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