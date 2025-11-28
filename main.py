"""
Point d'entrée principal pour Mini Overcooked avec ARCHITECTURE BDI
VERSION COMPLÈTE CORRIGÉE - SANS STRESS INDIVIDUEL DES CHEFS
"""
import sys
import os
import pygame
import time
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("🧠 MINI OVERCOOKED - ARCHITECTURE BDI MULTI-AGENTS")
    print("=" * 60)
    print("✅ Agents BDI (Belief-Desire-Intention)")
    print("✅ Planification STRIPS automatique") 
    print("✅ Système de cuisson réaliste")
    print("✅ Système émotionnel (stress/émotions)")
    print("✅ SYSTÈME DE STRESS ET ACCIDENTS ACTIVÉ")
    print("✅ CORRECTION DU BLOCAGE AUX BACS")
    print("✅ STRESS ÉQUILIBRÉ ET STABLE")
    print("✅ COMPTAGE ACCIDENTS CORRECT")
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
            
            # ✅ STRESS INITIAL MODÉRÉ
            kitchen_renderer.kitchen_stress_level = 10
            kitchen_renderer.accident_cooldown = 0
            kitchen_renderer.total_accidents_count = 0  # ✅ COMPTEUR TOTAL DES ACCIDENTS
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
        
        # ⭐ INITIALISATION AGENTS BDI - VERSION CORRIGÉE
        print("\n" + "=" * 60)
        print("🧠 INITIALISATION AGENTS BDI - BLOCAGE CORRIGÉ")
        print("=" * 60)
        
        try:
            bot_manager = BotManager()
            game_state.bot_manager = bot_manager
            
            # ✅ CORRECTION MAJEURE : Positions initiales DANS la cuisine
            print("\n🤖 Création Chef 1...")
            chef1 = BDIBot(x=250, y=300, chef_name="Chef Marcel", color_variant=0)
            print(f"  ✓ {chef1.chef_name} créé à ({chef1.x}, {chef1.y})")
            
            print("\n🤖 Création Chef 2...")
            chef2 = BDIBot(x=650, y=300, chef_name="Chef Sophie", color_variant=1)
            print(f"  ✓ {chef2.chef_name} créé à ({chef2.x}, {chef2.y})")
            
            bot_manager.add_bot(chef1)
            bot_manager.add_bot(chef2)
            
            # Configurer les références pour les bots BDI
            for bot in bot_manager.bots:
                if hasattr(bot, 'set_order_manager'):
                    bot.set_order_manager(order_manager)
                if hasattr(bot, 'set_bot_manager'):
                    bot.set_bot_manager(bot_manager)
            
            # Synchroniser les zones AVEC POSITIONS CORRIGÉES
            if kitchen_renderer:
                zones = kitchen_renderer.get_interaction_zones()
                bins = getattr(kitchen_renderer, 'ingredient_positions', {})
                
                for bot in bot_manager.bots:
                    bot.update_interaction_zones(zones)
                    if bins:
                        bot.update_ingredient_bins(bins)
                
                print("\n" + "="*60)
                print("✅ Zones d'interaction synchronisées")
                print("="*60)
            
            print("\n" + "=" * 60)
            print("✅ SYSTÈME BDI MULTI-AGENTS PRÊT!")
            print("🎯 BLOCAGE AUX BACS CORRIGÉ")
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
        print("🧠 MODE BDI ACTIVÉ - STRESS ÉQUILIBRÉ")
        print("⚡ ACCIDENTS MODÉRÉS")
        print("🎮" * 30)
        print("\n📝 Commandes disponibles:")
        for recipe in game_state.available_ingredients.keys():
            print(f"  - {recipe}")
        
        print("\n⌨️ Raccourcis:")
        print("  F1  - Ajouter 5 commandes (test)")
        print("  F2  - Réinitialiser système")
        print("  F3  - ⚡ FORCER UN ACCIDENT (test)")
        print("  F4  - 📈 AUGMENTER STRESS +15%")
        print("  F5  - 🎯 DEBUG POSITIONS BOTS")
        print("  F7  - 🧠 État mental des agents")
        print("  F8  - 🧠 Toggle logs BDI")
        print("  F9  - 😊 État émotionnel des chefs")
        print("  F10 - 📊 État du stress de la cuisine")
        print("  ESC - Quitter")
        
        running = True
        frame_count = 0
        last_debug_time = 0
        show_bdi_logs = True
        last_bdi_log_time = 0
        last_accident_check = time.time()
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
                        
                        # ✅ STRESS MODÉRÉ POUR 5 COMMANDES
                        if kitchen_renderer:
                            kitchen_renderer.kitchen_stress_level = min(70, kitchen_renderer.kitchen_stress_level + 15)
                            print(f"⚡ Stress augmenté à {kitchen_renderer.kitchen_stress_level}%")
                        print("✅ Agents BDI vont délibérer!")
                    
                    elif event.key == pygame.K_F2:
                        order_manager.reset()
                        for bot in bot_manager.bots:
                            bot.beliefs.clear()
                            bot.desires.clear()
                            bot.current_intention = None
                            bot.inv = None
                            bot._is_preparing = None
                            bot._is_cooking = None
                            bot._is_plating = False
                            bot.cooking_progress = 0.0
                            bot.action_attempts = 0
                        if kitchen_renderer:
                            kitchen_renderer.kitchen_stress_level = 10
                            kitchen_renderer.kitchen_accidents = []
                            kitchen_renderer.panic_mode = False
                            kitchen_renderer.total_accidents_count = 0  # ✅ RÉINITIALISER LE COMPTEUR
                        print("🔧 Système BDI réinitialisé")
                    
                    elif event.key == pygame.K_F3:
                        print("\n💥 FORÇAGE D'UN ACCIDENT VISIBLE!")
                        if bot_manager and hasattr(bot_manager, 'bots') and kitchen_renderer:
                            bot = random.choice(bot_manager.bots)
                            accident_type = random.choice(["drop_plate", "slip_fall", "ingredient_spill"])
                            kitchen_renderer.trigger_accident(bot, accident_type)
                            print(f"💥 Accident forcé: {accident_type} pour {bot.chef_name}")
                            # ✅ INCRÉMENTER LE COMPTEUR TOTAL
                            kitchen_renderer.total_accidents_count += 1
                            print(f"📊 Total accidents: {kitchen_renderer.total_accidents_count}")
                            # Stress modéré
                            kitchen_renderer.kitchen_stress_level = min(80, kitchen_renderer.kitchen_stress_level + 10)
                    
                    elif event.key == pygame.K_F4:
                        print("\n📈 AUGMENTATION FORCÉE DU STRESS!")
                        if kitchen_renderer:
                            current_stress = kitchen_renderer.kitchen_stress_level
                            new_stress = min(85, current_stress + 15)  # Limité à 85%
                            kitchen_renderer.kitchen_stress_level = new_stress
                            print(f"⚡ Stress augmenté: {current_stress}% → {new_stress}%")
                            
                            if new_stress >= 70 and not kitchen_renderer.panic_mode:
                                kitchen_renderer.trigger_panic_mode()
                    
                    elif event.key == pygame.K_F5:
                        print("\n🎯 DEBUG POSITIONS BOTS:")
                        for bot in bot_manager.bots:
                            print(f"  {bot.chef_name}: ({bot.x:.1f}, {bot.y:.1f}) - {bot.get_state_text()}")
                    
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
                                for key, belief in list(bot.beliefs.items())[:5]:
                                    print(f"  • {key}: {belief.content}")
                            else:
                                print("  (aucune croyance)")
                            
                            print("\n🎯 INTENTION ACTUELLE:")
                            if bot.current_intention:
                                intention = bot.current_intention
                                print(f"  • But: {intention.desire.goal}")
                                print(f"  • Étapes restantes: {len(intention.plan)}")
                            else:
                                print("  (pas d'intention)")
                    
                    elif event.key == pygame.K_F8:
                        show_bdi_logs = not show_bdi_logs
                        status = "ACTIVÉS" if show_bdi_logs else "DÉSACTIVÉS"
                        print(f"\n🔔 Logs BDI temps réel: {status}")
                    
                    elif event.key == pygame.K_F9:
                        print("\n" + "😊" * 30)
                        print("ÉTAT ÉMOTIONNEL DES CHEFS")
                        print("😊" * 30)
                        
                        for bot in bot_manager.bots:
                            emoji = bot.get_emotion_emoji()
                            print(f"\n{emoji} {bot.chef_name}:")
                            print(f"  Émotion: {bot.current_emotion.value}")
                            print(f"  Stress: {bot.stress_level:.1%}")
                    
                    elif event.key == pygame.K_F10:
                        print("\n" + "⚡" * 30)
                        print("ÉTAT DU STRESS DE LA CUISINE")
                        print("⚡" * 30)
                        
                        if kitchen_renderer:
                            stress_level = kitchen_renderer.kitchen_stress_level
                            panic_mode = kitchen_renderer.panic_mode
                            accidents_count = len(kitchen_renderer.kitchen_accidents)
                            total_accidents = kitchen_renderer.total_accidents_count
                            
                            # ✅ CORRECTION : Utiliser active_orders au lieu de pending_orders
                            active_orders_count = len(order_manager.active_orders) if hasattr(order_manager, 'active_orders') else 0
                            
                            print(f"\n📊 Niveau de stress: {stress_level}%")
                            print(f"🚨 Mode panique: {'ACTIF' if panic_mode else 'inactif'}")
                            print(f"💥 Accidents en cours: {accidents_count}")
                            print(f"📈 Total accidents: {total_accidents}")
                            print(f"📈 Commandes actives: {active_orders_count}")
                        else:
                            print("❌ KitchenRenderer non disponible")
                    
                    else:
                        if event.unicode.isprintable():
                            game_state.user_input += event.unicode

            # Logique du jeu
            game_logic.update_timer()
            game_logic.reduce_combo_over_time()
            
            # Mise à jour BDI
            try:
                bot_manager.update()
                
                if kitchen_renderer:
                    # ✅ SYSTÈME DE STRESS ÉQUILIBRÉ
                    current_time = time.time()
                    
                    # Vérifier les accidents modérément
                    if current_time - last_accident_check > 3.0:  # Toutes les 3 secondes
                        last_accident_check = current_time
                        
                        # ✅ ACCIDENTS MODÉRÉS
                        accident_chance = kitchen_renderer.kitchen_stress_level / 100  # Seuil normal
                        
                        if random.random() < accident_chance and bot_manager and hasattr(bot_manager, 'bots'):
                            eligible_bots = [bot for bot in bot_manager.bots if bot.inv or random.random() < 0.2]
                            if eligible_bots:
                                bot = random.choice(eligible_bots)
                                accident_types = ["drop_plate", "slip_fall", "ingredient_spill"]
                                accident_type = random.choice(accident_types)
                                kitchen_renderer.trigger_accident(bot, accident_type)
                                # ✅ INCRÉMENTER LE COMPTEUR TOTAL
                                kitchen_renderer.total_accidents_count += 1
                                print(f"💥 Accident naturel: {accident_type} pour {bot.chef_name}")
                                print(f"📊 Total accidents: {kitchen_renderer.total_accidents_count}")
                    
                    # ✅ STRESS ÉQUILIBRÉ
                    # ✅ CORRECTION : Utiliser active_orders au lieu de pending_orders
                    active_orders_count = len(order_manager.active_orders) if hasattr(order_manager, 'active_orders') else 0
                    
                    # Stress de base basé sur les commandes (MODÉRÉ)
                    base_stress = active_orders_count * 5  # Réduit de 8 à 5
                    
                    # Stress additionnel pour les chefs occupés (MODÉRÉ)
                    busy_chefs = sum(1 for bot in bot_manager.bots 
                                   if bot.state not in ["idle", "thinking", "observing"])
                    base_stress += busy_chefs * 3  # Réduit de 5 à 3
                    
                    # Stress des accidents (MODÉRÉ)
                    base_stress += len(kitchen_renderer.kitchen_accidents) * 8  # Réduit de 15 à 8
                    
                    # Appliquer le stress (MODÉRÉ)
                    if base_stress > kitchen_renderer.kitchen_stress_level:
                        kitchen_renderer.kitchen_stress_level = min(90, kitchen_renderer.kitchen_stress_level + 1)  # Réduit de 2 à 1
                    else:
                        # Réduction du stress
                        kitchen_renderer.kitchen_stress_level = max(0, kitchen_renderer.kitchen_stress_level - 0.3)  # Réduction augmentée
                    
                    kitchen_renderer.update_stress_system(bot_manager, order_manager)
                    kitchen_renderer.update_accidents()
                
                if show_bdi_logs and (current_time - last_bdi_log_time >= 3.0):
                    print("\n" + "─" * 60)
                    print(f"🧠 CYCLE BDI (t={game_state.timer:.1f}s)")
                    print("─" * 60)
                    
                    for bot in bot_manager.bots:
                        emoji = bot.get_emotion_emoji()
                        status = f"{emoji} {bot.chef_name}: "
                        
                        if bot.current_intention:
                            status += f"🎯 {bot.current_intention.desire.goal}"
                            status += f" ({len(bot.current_intention.plan)} actions)"
                        else:
                            status += "🤔 Observation..."
                        
                        status += f" | Stress: {bot.stress_level:.0%}"
                        print(status)
                    
                    last_bdi_log_time = current_time
                
                if current_time - last_debug_time >= 8.0:
                    status = order_manager.get_status_summary()
                    print(f"\n📊 STATUS (t={game_state.timer:.1f}s):")
                    print(f"  Commandes actives: {status['active_orders']}")
                    print(f"  Commandes complétées: {status['completed_orders']}")
                    
                    if kitchen_renderer:
                        stress_level = kitchen_renderer.kitchen_stress_level
                        accidents_count = len(kitchen_renderer.kitchen_accidents)
                        total_accidents = kitchen_renderer.total_accidents_count
                        panic_mode = kitchen_renderer.panic_mode
                        
                        # ✅ CORRECTION : Utiliser active_orders
                        active_orders_count = len(order_manager.active_orders) if hasattr(order_manager, 'active_orders') else 0
                        
                        print(f"  ⚡ Stress cuisine: {stress_level}% | Accidents en cours: {accidents_count}")
                        print(f"  📊 Total accidents: {total_accidents} | Panique: {'OUI' if panic_mode else 'non'}")
                        print(f"  📈 Commandes actives: {active_orders_count}")
                    
                    last_debug_time = current_time
                    
            except Exception as e:
                print(f"⚠ Erreur mise à jour: {e}")
                # Éviter de bloquer le jeu en cas d'erreur
                continue

            # RENDU PRINCIPAL
            screen.fill((50, 60, 70))  # Fond bleu-gris clair
            
            try:
                if kitchen_renderer:
                    kitchen_renderer.render_full_kitchen(
                        bot_manager, 
                        asset_manager, 
                        game_state.timer, 
                        order_manager
                    )
                else:
                    draw_basic_kitchen(screen)
                    for bot in bot_manager.bots:
                        bot.draw_chef(screen)
                        
            except Exception as e:
                print(f"⚠ Erreur rendu: {e}")
                draw_basic_kitchen(screen)
            
            # ⭐ INTERFACE AVEC UNE SEULE BARRE DE STRESS À CÔTÉ DE LA ZONE DE SAISIE
            try:
                # Polices
                font_large = pygame.font.Font(None, 36)
                font_medium = pygame.font.Font(None, 28)
                font_small = pygame.font.Font(None, 22)
                
                # ZONE DE SAISIE EN HAUT À GAUCHE
                input_bg = pygame.Rect(10, 10, 350, 50)
                pygame.draw.rect(screen, (20, 20, 30), input_bg, border_radius=8)
                pygame.draw.rect(screen, (255, 215, 0), input_bg, 3, border_radius=8)
                
                # Label
                label_text = font_medium.render("Commande:", True, (255, 255, 255))
                screen.blit(label_text, (20, 15))
                
                # Texte de saisie
                user_input_display = game_state.user_input + ("_" if int(time.time() * 2) % 2 == 0 else " ")
                input_text = font_medium.render(user_input_display, True, (255, 255, 150))
                screen.blit(input_text, (20, 35))
                
                # ✅ UNE SEULE BARRE DE STRESS - À DROITE DE LA ZONE DE SAISIE
                if kitchen_renderer:
                    stress_level = kitchen_renderer.kitchen_stress_level
                    
                    # Position à droite de la zone de saisie
                    stress_x = 370  # À droite de la zone de saisie (350 + 20 de marge)
                    stress_y = 15
                    
                    # Couleurs plus douces
                    if stress_level < 40:
                        stress_color = (100, 255, 100)  # Vert
                    elif stress_level < 70:
                        stress_color = (255, 200, 50)   # Orange
                    else:
                        stress_color = (255, 80, 80)    # Rouge plus doux
                    
                    # Barre de stress UNIQUE
                    stress_bg = pygame.Rect(stress_x, stress_y, 200, 25)
                    pygame.draw.rect(screen, (50, 50, 50), stress_bg, border_radius=5)
                    
                    stress_fill_width = int(200 * (stress_level / 100))
                    stress_fill = pygame.Rect(stress_x, stress_y, stress_fill_width, 25)
                    pygame.draw.rect(screen, stress_color, stress_fill, border_radius=5)
                    
                    # Texte du stress
                    stress_text = font_small.render(f"Stress: {stress_level:.0f}%", True, (255, 255, 255))
                    screen.blit(stress_text, (stress_x + 5, stress_y + 4))
                    
                    # Mode panique seulement si vraiment élevé
                    if kitchen_renderer.panic_mode:
                        panic_text = font_small.render("🚨", True, (255, 50, 50))
                        screen.blit(panic_text, (stress_x + 180, stress_y + 4))
                
                # ✅ TIMER - JUSTE À CÔTÉ DE LA BARRE DE STRESS
                timer_x = stress_x + 210  # À droite de la barre de stress
                timer_y = stress_y + 2
                timer_text = font_large.render(f"⏱️ {game_state.timer:.1f}s", True, (255, 255, 255))
                screen.blit(timer_text, (timer_x, timer_y))
                
            except Exception as e:
                print(f"⚠ Erreur UI: {e}")
            
            pygame.display.flip()
        
        # Fin de partie
        game_logic.stop()
        stats = game_logic.calculate_final_stats()
        stats['total_chefs'] = len(bot_manager.bots)
        stats['leaderboard'] = bot_manager.get_leaderboard()
        
        if kitchen_renderer:
            stats['max_stress'] = kitchen_renderer.kitchen_stress_level
            stats['panic_mode'] = kitchen_renderer.panic_mode
            # ✅ UTILISER LE COMPTEUR TOTAL DES ACCIDENTS
            stats['total_accidents'] = kitchen_renderer.total_accidents_count
        
        show_game_over_screen(screen, stats, bot_manager, kitchen_renderer)
    
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
        
        # Zones de la cuisine
        pygame.draw.rect(screen, (200, 200, 255), (50, 120, 300, 350))  # Préparation
        pygame.draw.rect(screen, (160, 120, 80), (400, 120, 250, 120))  # Cuisson
        pygame.draw.rect(screen, (240, 230, 220), (400, 280, 250, 100)) # Assemblage
        pygame.draw.rect(screen, (255, 200, 100), (700, 120, 120, 300)) # Service
        
    except Exception:
        screen.fill((50, 50, 50))


def show_game_over_screen(screen, stats, bot_manager, kitchen_renderer=None):
    """Écran de fin SANS stress individuel des chefs"""
    try:
        import game_state
        import config
        
        # Fond semi-transparent
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Polices
        font_title = pygame.font.Font(None, 64)
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        # Titre
        title = font_title.render("PARTIE TERMINÉE!", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(config.WIDTH//2, 80)))
        
        y_offset = 150
        
        # Score
        score_text = font_large.render(f"Score Final: {game_state.score}", True, (255, 255, 255))
        screen.blit(score_text, score_text.get_rect(center=(config.WIDTH//2, y_offset)))
        y_offset += 60
        
        # Statistiques de stress et accidents
        if kitchen_renderer:
            stress_text = font_medium.render(f"📈 Stress maximum: {stats.get('max_stress', 0)}%", True, (255, 100, 100))
            screen.blit(stress_text, stress_text.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 40
            
            # ✅ AFFICHER LE TOTAL CORRECT DES ACCIDENTS
            accidents_count = stats.get('total_accidents', 0)
            accidents_text = font_medium.render(f"💥 Accidents: {accidents_count}", True, (255, 150, 50))
            screen.blit(accidents_text, accidents_text.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 60
        
        # Classement
        classement_title = font_large.render("🏆 CLASSEMENT", True, (255, 215, 0))
        screen.blit(classement_title, classement_title.get_rect(center=(config.WIDTH//2, y_offset)))
        y_offset += 60
        
        leaderboard = bot_manager.get_leaderboard()
        winner_name = ""
        
        for i, entry in enumerate(leaderboard):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
            color = (255, 215, 0) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50)
            
            if i == 0:
                winner_name = entry['name']
            
            chef_text = f"{medal} {entry['name']}: {entry['score']} points"
            chef_surf = font_medium.render(chef_text, True, color)
            screen.blit(chef_surf, chef_surf.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 40
            
            # ✅ SUPPRIMER LE STRESS INDIVIDUEL - Afficher seulement les plats
            stats_text = f"Plats: {entry['stats']['dishes_delivered']}"
            stats_surf = font_small.render(stats_text, True, (200, 200, 200))
            screen.blit(stats_surf, stats_surf.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 30
        
        # ✅ MESSAGE DE FÉLICITATIONS POUR LE GAGNANT
        y_offset += 40
        if winner_name:
            congrats_text = font_large.render(f"🎉 Félicitations à {winner_name} ! 🎉", True, (255, 215, 0))
            screen.blit(congrats_text, congrats_text.get_rect(center=(config.WIDTH//2, y_offset)))
            y_offset += 50
        
        # Message de fin
        continue_text = font_small.render("Appuyez sur une touche pour quitter...", True, (150, 150, 150))
        screen.blit(continue_text, continue_text.get_rect(center=(config.WIDTH//2, y_offset)))
        
        pygame.display.flip()
        
        # Attendre une touche
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
        
    except Exception as e:
        print(f"Erreur game over: {e}")


if __name__ == "__main__":
    main()