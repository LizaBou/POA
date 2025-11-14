"""
Point d'entrée principal pour Mini Overcooked avec ARCHITECTURE BDI
VERSION CORRIGÉE - Affichage cuisine continu pendant assemblage
"""
import sys
import os
import pygame
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("🧠 MINI OVERCOOKED - ARCHITECTURE BDI MULTI-AGENTS")
    print("=" * 60)
    print("✅ Agents BDI (Belief-Desire-Intention)")
    print("✅ Planification STRIPS automatique")
    print("✅ Délibération rationnelle")
    print("=" * 60)
    
    try:
        import game_state
        from game.logic import GameLogic
        from graphics.kitchen import KitchenRenderer
        from graphics import ui, assets
        from entities.bot_bdi import BDIBot
        from entities.bot import BotManager
        from entities.order_manager import OrderManager
        import config
        
        print("✓ Modules BDI chargés")
        
        # Initialiser pygame
        pygame.init()
        screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Mini Overcooked - Architecture BDI")
        clock = pygame.time.Clock()
        
        print("✓ Interface graphique initialisée")
        
        # Initialiser le jeu
        game_state.initialize_ingredients()
        game_logic = GameLogic()
        
        # Initialiser le renderer
        try:
            kitchen_renderer = KitchenRenderer(screen)
            game_state.kitchen_renderer = kitchen_renderer
            print("✓ Renderer de cuisine initialisé")
        except Exception as e:
            print(f"❌ Erreur renderer: {e}")
            kitchen_renderer = None
            return
        
        # Initialiser OrderManager
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
        
        # Initialiser les assets
        try:
            asset_manager = assets.AssetManager()
            print("✓ Assets chargés")
        except Exception as e:
            print(f"⚠ Erreur assets: {e}")
            asset_manager = None
        
        # ⭐ INITIALISATION AGENTS BDI
        print("\n" + "=" * 60)
        print("🧠 INITIALISATION AGENTS BDI")
        print("=" * 60)
        
        try:
            bot_manager = BotManager()
            game_state.bot_manager = bot_manager
            
            print("\n🤖 Création Chef 1...")
            chef1 = BDIBot(x=300, y=400, chef_name="Chef Marcel", color_variant=0)
            print(f"  ✓ {chef1.chef_name} créé")
            
            print("\n🤖 Création Chef 2...")
            chef2 = BDIBot(x=500, y=400, chef_name="Chef Sophie", color_variant=1)
            print(f"  ✓ {chef2.chef_name} créé")
            
            bot_manager.add_bot(chef1)
            bot_manager.add_bot(chef2)
            
            # Synchroniser les zones
            if kitchen_renderer:
                zones = kitchen_renderer.get_interaction_zones()
                bins = getattr(kitchen_renderer, 'ingredient_positions', {})
                
                for bot in bot_manager.bots:
                    bot.update_interaction_zones(zones)
                    if bins:
                        bot.update_ingredient_bins(bins)
                
                print("\n✅ Zones d'interaction synchronisées")
            
            print("\n" + "=" * 60)
            print("✅ SYSTÈME BDI MULTI-AGENTS PRÊT!")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Erreur initialisation BDI: {e}")
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
        
        print("\n" + "🎮" * 30)
        print("🧠 MODE BDI ACTIVÉ")
        print("🎮" * 30)
        print("\n📝 Commandes disponibles:")
        for recipe in game_state.available_ingredients.keys():
            print(f"  - {recipe}")
        
        print("\n⌨️ Raccourcis:")
        print("  F1  - Ajouter 5 commandes (test)")
        print("  F2  - Réinitialiser système")
        print("  F7  - 🧠 État mental des agents")
        print("  F8  - 🧠 Toggle logs BDI")
        print("  ESC - Quitter")
        
        running = True
        frame_count = 0
        last_debug_time = 0
        show_bdi_logs = True
        last_bdi_log_time = 0
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
                        order_name = game_state.user_input.lower().strip()
                        print(f"\n🍽️ AJOUT COMMANDE: '{order_name}'")
                        
                        if order_name in game_state.available_ingredients:
                            ingredients = game_state.available_ingredients[order_name]
                            order_manager.add_order(order_name, ingredients)
                            print(f"✅ Commande '{order_name}' ajoutée")
                        else:
                            print(f"❌ Recette inconnue: {order_name}")
                        
                        game_state.user_input = ""
                    
                    elif event.key == pygame.K_F1:
                        import random
                        print("\n🎲 AJOUT DE 5 COMMANDES RANDOM:")
                        for i in range(5):
                            recipe = random.choice(recipe_names)
                            ingredients = game_state.available_ingredients[recipe]
                            order_manager.add_order(recipe, ingredients)
                            print(f"  {i+1}. {recipe}")
                        print("✅ Agents BDI vont délibérer!")
                    
                    elif event.key == pygame.K_F2:
                        order_manager.reset()
                        for bot in bot_manager.bots:
                            bot.beliefs.clear()
                            bot.desires.clear()
                            bot.current_intention = None
                            bot.inv = None
                            bot._is_preparing = None
                            bot._is_plating = False
                        print("🔧 Système BDI réinitialisé")
                    
                    elif event.key == pygame.K_F7:
                        print("\n" + "🧠" * 30)
                        print("ÉTAT MENTAL DES AGENTS BDI")
                        print("🧠" * 30)
                        
                        for bot in bot_manager.bots:
                            print(f"\n{'='*50}")
                            print(f"👨‍🍳 {bot.chef_name}")
                            print(f"{'='*50}")
                            
                            print("\n📚 BELIEFS (Croyances):")
                            if bot.beliefs:
                                for key, belief in list(bot.beliefs.items())[:10]:
                                    print(f"  • {key}: {belief.content}")
                                    print(f"    ↳ Confiance: {belief.confidence:.2f}")
                            else:
                                print("  (aucune croyance)")
                            
                            print("\n💭 DESIRES (Désirs):")
                            if bot.desires:
                                for desire in bot.desires[:5]:
                                    print(f"  • {desire.goal}")
                                    print(f"    ↳ Priorité: {desire.priority:.2f}")
                            else:
                                print("  (aucun désir)")
                            
                            print("\n🎯 INTENTION ACTUELLE:")
                            if bot.current_intention:
                                intention = bot.current_intention
                                print(f"  • But: {intention.desire.goal}")
                                print(f"  • Engagé: {intention.committed}")
                                print(f"  • Étapes restantes: {len(intention.plan)}")
                                
                                if intention.plan:
                                    print("\n  📋 Plan d'actions:")
                                    for i, action in enumerate(intention.plan[:5], 1):
                                        print(f"    {i}. {action.name}")
                                        if action.parameters:
                                            print(f"       Params: {action.parameters}")
                            else:
                                print("  (pas d'intention - en délibération)")
                    
                    elif event.key == pygame.K_F8:
                        show_bdi_logs = not show_bdi_logs
                        status = "ACTIVÉS" if show_bdi_logs else "DÉSACTIVÉS"
                        print(f"\n🔔 Logs BDI temps réel: {status}")
                    
                    else:
                        if event.unicode.isprintable():
                            game_state.user_input += event.unicode

            # Logique du jeu
            game_logic.update_timer()
            game_logic.reduce_combo_over_time()
            
            # Mise à jour BDI
            try:
                bot_manager.update()
                
                if show_bdi_logs and (current_time - last_bdi_log_time >= 3.0):
                    print("\n" + "─" * 60)
                    print(f"🧠 CYCLE BDI (t={game_state.timer:.1f}s)")
                    print("─" * 60)
                    
                    for bot in bot_manager.bots:
                        beliefs_count = len(bot.beliefs)
                        desires_count = len(bot.desires)
                        
                        status = f"{bot.chef_name}: "
                        
                        if bot.current_intention:
                            status += f"🎯 {bot.current_intention.desire.goal}"
                            status += f" ({len(bot.current_intention.plan)} actions)"
                        elif bot.desires:
                            status += f"💭 {desires_count} options"
                        else:
                            status += "🤔 Observation..."
                        
                        status += f" | {beliefs_count} beliefs"
                        print(status)
                    
                    last_bdi_log_time = current_time
                
                if current_time - last_debug_time >= 10.0:
                    status = order_manager.get_status_summary()
                    print(f"\n📊 STATUS (t={game_state.timer:.1f}s):")
                    print(f"  Commandes: {status['available_orders']} dispo | {status['active_orders']} actives | {status['completed_orders']} complétées")
                    last_debug_time = current_time
                    
            except Exception as e:
                print(f"⚠ Erreur mise à jour: {e}")
                import traceback
                traceback.print_exc()

            # ⭐⭐⭐ CORRECTION PRINCIPALE: TOUJOURS DESSINER LA CUISINE ⭐⭐⭐
            screen.fill((40, 40, 40))
            
            try:
                if kitchen_renderer:
                    # ⭐ Dessiner TOUT le temps avec les NOUVEAUX VISUELS
                    kitchen_renderer.draw_floor()
                    
                    # ⭐ NOUVEAUX : Éléments décoratifs
                    kitchen_renderer.draw_overhead_lamps()
                    kitchen_renderer.draw_wall_decorations()
                    
                    kitchen_renderer.draw_individual_ingredient_stations(asset_manager)
                    kitchen_renderer.draw_work_station(asset_manager)
                    kitchen_renderer.draw_plating_station(asset_manager)
                    kitchen_renderer.draw_service_station()
                    
                    # ⭐ NOUVEAU : Vapeur de cuisson
                    kitchen_renderer.update_steam_particles()
                    kitchen_renderer.draw_steam_particles()
                    
                    # Dessiner tous les chefs avec leur animation
                    for bot in bot_manager.bots:
                        # ⭐ Vérifier livraison pour animation
                        kitchen_renderer.check_delivery_trigger(bot)
                        
                        # ⭐ Dessiner le chef avec toutes ses animations
                        kitchen_renderer.draw_chef_enhanced(bot, asset_manager)
                        kitchen_renderer.draw_chef_status(bot)
                    
                    # ⭐ Animation de découpe si active
                    if kitchen_renderer.cutting_animation.active:
                        kitchen_renderer.cutting_animation.update()
                        kitchen_renderer.cutting_animation.draw()
                        
                else:
                    # Fallback basique
                    draw_basic_kitchen(screen)
                    for bot in bot_manager.bots:
                        bot.draw_chef(screen)
                        
            except Exception as e:
                print(f"⚠ Erreur rendu: {e}")
                import traceback
                traceback.print_exc()
                draw_basic_kitchen(screen)
            
            # UI en overlay
            try:
                font_small = pygame.font.Font(None, 24)
                
                # Timer et score
                timer_text = font_small.render(f"⏱️ {game_state.timer:.1f}s", True, (255, 255, 255))
                screen.blit(timer_text, (config.WIDTH - 100, 10))
                
                score_text = font_small.render(f"💰 {game_state.score}", True, (255, 215, 0))
                screen.blit(score_text, (config.WIDTH - 100, 35))
                
                bdi_status = "🧠 BDI ACTIF" if show_bdi_logs else "🧠 BDI (logs off)"
                bdi_text = font_small.render(bdi_status, True, (100, 255, 100))
                screen.blit(bdi_text, (config.WIDTH - 150, 60))
                
                # Zone de saisie
                input_font = pygame.font.Font(None, 28)
                
                input_bg_rect = pygame.Rect(10, 10, 450, 45)
                input_bg_surf = pygame.Surface((450, 45), pygame.SRCALPHA)
                input_bg_surf.fill((0, 0, 0, 200))
                screen.blit(input_bg_surf, input_bg_rect)
                pygame.draw.rect(screen, (255, 215, 0), input_bg_rect, 3)
                
                label_text = input_font.render("Tapez une recette:", True, (255, 255, 255))
                screen.blit(label_text, (18, 16))
                
                user_input_display = game_state.user_input + ("_" if int(time.time() * 2) % 2 == 0 else " ")
                input_text = input_font.render(user_input_display, True, (255, 255, 100))
                screen.blit(input_text, (18, 35))
                
            except Exception as e:
                print(f"⚠ Erreur UI: {e}")
            
            pygame.display.flip()
        
        # Fin de partie
        game_logic.stop()
        stats = game_logic.calculate_final_stats()
        stats['total_chefs'] = len(bot_manager.bots)
        stats['leaderboard'] = bot_manager.get_leaderboard()
        
        show_game_over_screen(screen, stats, bot_manager)
        time.sleep(3)
    
    except ImportError as e:
        print(f"❌ Module manquant: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("\n👋 Au revoir !")


def draw_basic_kitchen(screen):
    """Rendu basique de secours"""
    try:
        import config
        screen.fill((120, 140, 120))
        
        pygame.draw.rect(screen, (200, 200, 255), (50, 120, 300, 350))
        pygame.draw.rect(screen, (160, 120, 80), (400, 120, 250, 120))
        pygame.draw.rect(screen, (240, 230, 220), (400, 280, 250, 100))
        pygame.draw.rect(screen, (255, 200, 100), (700, 120, 120, 300))
        
    except Exception as e:
        screen.fill((50, 50, 50))


def show_game_over_screen(screen, stats, bot_manager):
    """Écran de fin avec classement BDI"""
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
        screen.blit(title, title.get_rect(center=(config.WIDTH//2, 80)))
        
        subtitle = font_medium.render("🧠 Architecture BDI Multi-Agents", True, (100, 255, 100))
        screen.blit(subtitle, subtitle.get_rect(center=(config.WIDTH//2, 130)))
        
        y_offset = 180
        score_text = f"Score Total: {game_state.score}"
        rendered = font_medium.render(score_text, True, (255, 255, 255))
        screen.blit(rendered, rendered.get_rect(center=(config.WIDTH//2, y_offset)))
        y_offset += 60
        
        winner_title = font_large.render("🏆 CLASSEMENT", True, (255, 215, 0))
        screen.blit(winner_title, winner_title.get_rect(center=(config.WIDTH//2, y_offset)))
        y_offset += 50
        
        leaderboard = bot_manager.get_leaderboard()
        for i, entry in enumerate(leaderboard):
            medal = "🥇" if i == 0 else "🥈"
            color = (255, 215, 0) if i == 0 else (192, 192, 192)
            
            chef_text = f"{medal} {entry['name']}: {entry['score']} points"
            chef_surf = font_medium.render(chef_text, True, color)
            screen.blit(chef_surf, chef_surf.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 35
            
            stats_text = f"Plats: {entry['stats']['dishes_delivered']}"
            stats_surf = font_small.render(stats_text, True, (200, 200, 200))
            screen.blit(stats_surf, stats_surf.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 30
        
        pygame.display.flip()
        
    except Exception as e:
        print(f"Erreur game over: {e}")


if __name__ == "__main__":
    main()