"""
Point d'entrée principal pour Mini Overcooked avec ARCHITECTURE BDI
VERSION COMPLÈTE CORRIGÉE - INTERFACE AMÉLIORÉE
✅ Système d'accidents ACTIVÉ ET FONCTIONNEL
❌ Mode panique DÉSACTIVÉ (pour garder le rendu)
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
    print("✅ CORRECTION DU BLOCAGE AUX BACS")
    print("✅ STRESS ÉQUILIBRÉ ET STABLE")
    print("✅ INTERFACE CORRIGÉE")
    print("✅ ACCIDENTS ACTIVÉS ET FONCTIONNELS")
    print("❌ MODE PANIQUE DÉSACTIVÉ")
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
            
            # ✅ STRESS INITIAL MODÉRÉ - ACCIDENTS ACTIVÉS
            kitchen_renderer.kitchen_stress_level = 10
            # ACTIVER le système d'accidents
            kitchen_renderer.accident_cooldown = 30  # Cooldown entre accidents
            kitchen_renderer.total_accidents_count = 0
            kitchen_renderer.panic_mode = False  # ❌ DÉSACTIVER le mode panique
            kitchen_renderer.kitchen_accidents = []  # Liste pour les accidents actifs
            print("✓ Renderer de cuisine initialisé (accidents ACTIVÉS, mode panique DÉSACTIVÉ)")
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
        print("🧠 INITIALISATION AGENTS BDI - BLOCAGE CORRIGÉ")
        print("=" * 60)
        
        try:
            bot_manager = BotManager()
            game_state.bot_manager = bot_manager
            
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
            
            # Synchroniser les zones
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
            print("✅ ACCIDENTS ACTIVÉS")
            print("❌ MODE PANIQUE DÉSACTIVÉ")
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
        print("✅ ACCIDENTS ACTIVÉS ET FONCTIONNELS")
        print("❌ MODE PANIQUE DÉSACTIVÉ")
        print("🎮" * 30)
        print("\n📝 Commandes disponibles:")
        for recipe in game_state.available_ingredients.keys():
            print(f"  - {recipe}")
        
        print("\n⌨️ Raccourcis:")
        print("  F1  - Ajouter 5 commandes (test)")
        print("  F2  - Réinitialiser système")
        print("  F5  - 🎯 DEBUG POSITIONS BOTS")
        print("  F6  - 🚨 FORCER UN ACCIDENT (test)")
        print("  F7  - 🧠 État mental des agents")
        print("  F8  - 🧠 Toggle logs BDI")
        print("  F9  - 😊 État émotionnel des chefs")
        print("  F10 - 📊 État du stress de la cuisine")
        print("  ESC - Quitter")
        print("\n⚠️  Les accidents sont ACTIVÉS - Les steaks peuvent brûler!")
        print("📌 Mode panique désactivé pour garder le rendu stable")
        
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
                            # Réinitialiser les accidents
                            if hasattr(kitchen_renderer, 'kitchen_accidents'):
                                kitchen_renderer.kitchen_accidents = []
                            kitchen_renderer.panic_mode = False  # ❌ Garder désactivé
                            kitchen_renderer.total_accidents_count = 0
                            kitchen_renderer.accident_cooldown = 30
                        print("🔧 Système BDI réinitialisé (mode panique désactivé)")
                    
                    elif event.key == pygame.K_F5:
                        print("\n🎯 DEBUG POSITIONS BOTS:")
                        for bot in bot_manager.bots:
                            print(f"  {bot.chef_name}: ({bot.x:.1f}, {bot.y:.1f}) - {bot.get_state_text()}")
                    
                    elif event.key == pygame.K_F6:
                        # 🚨 FORCER UN ACCIDENT
                        print("\n🚨 FORCING ACCIDENT (TEST)...")
                        if kitchen_renderer:
                            # Appeler la méthode create_accident si elle existe
                            if hasattr(kitchen_renderer, 'create_accident'):
                                accident_info = kitchen_renderer.create_accident(bot_manager)
                                if accident_info:
                                    print(f"🚨 ACCIDENT CRÉÉ! {accident_info['message']}")
                                    kitchen_renderer.total_accidents_count += 1
                                    # Augmenter le stress
                                    kitchen_renderer.kitchen_stress_level = min(100, 
                                        kitchen_renderer.kitchen_stress_level + 20)
                            else:
                                # Créer un accident manuellement
                                accidents = [
                                    "Le steak brûle sur la cuisinière!",
                                    "Un ingrédient tombe par terre!",
                                    "Un chef trébuche et renverse des aliments!",
                                    "Feu de friteuse! (simulé)",
                                    "Panne de l'équipement de cuisson!"
                                ]
                                accident_message = random.choice(accidents)
                                
                                # Créer un effet visuel
                                accident_effect = {
                                    'message': accident_message,
                                    'position': (random.randint(100, 900), random.randint(150, 550)),
                                    'timer': 180,  # 3 secondes à 60 FPS
                                    'type': random.choice(['fire', 'spill', 'smoke'])
                                }
                                
                                # Ajouter à la liste des accidents
                                if not hasattr(kitchen_renderer, 'kitchen_accidents'):
                                    kitchen_renderer.kitchen_accidents = []
                                kitchen_renderer.kitchen_accidents.append(accident_effect)
                                kitchen_renderer.total_accidents_count += 1
                                
                                print(f"🚨 ACCIDENT FORCÉ! {accident_message}")
                                kitchen_renderer.kitchen_stress_level = min(100, 
                                    kitchen_renderer.kitchen_stress_level + 20)
                        else:
                            print("❌ KitchenRenderer non disponible")
                    
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
                            accidents_count = kitchen_renderer.total_accidents_count
                            
                            active_orders_count = len(order_manager.active_orders) if hasattr(order_manager, 'active_orders') else 0
                            
                            print(f"\n📊 Niveau de stress: {stress_level}%")
                            print(f"🚨 Mode panique: {'DÉSACTIVÉ'}")
                            print(f"📈 Commandes actives: {active_orders_count}")
                            print(f"🔥 Accidents: {accidents_count}")
                        else:
                            print("❌ KitchenRenderer non disponible")
                    
                    else:
                        # ✅ CORRECTION: Limiter la longueur du texte de saisie
                        if event.unicode.isprintable() and len(game_state.user_input) < 25:
                            game_state.user_input += event.unicode

            # Logique du jeu
            game_logic.update_timer()
            game_logic.reduce_combo_over_time()
            
            # Mise à jour BDI
            try:
                bot_manager.update()
                
                if kitchen_renderer:
                    current_time = time.time()
                    
                    # ✅ GESTION DU COOLDOWN DES ACCIDENTS
                    # Réduire le cooldown
                    if hasattr(kitchen_renderer, 'accident_cooldown'):
                        kitchen_renderer.accident_cooldown -= dt
                        
                        # Si le cooldown est écoulé, tenter de créer un accident
                        if kitchen_renderer.accident_cooldown <= 0:
                            # Réinitialiser le cooldown
                            kitchen_renderer.accident_cooldown = random.randint(20, 60)  # 20-60 secondes
                            
                            # Plus le stress est élevé, plus la chance d'accident est grande
                            if kitchen_renderer.kitchen_stress_level > 40:
                                # Probabilité basée sur le stress (0-15%)
                                chance = (kitchen_renderer.kitchen_stress_level - 40) / 400  # 15% max à 100% stress
                                
                                # Augmenter la chance avec le nombre d'accidents déjà survenus
                                if hasattr(kitchen_renderer, 'total_accidents_count'):
                                    chance += kitchen_renderer.total_accidents_count / 100
                                
                                # Augmenter la chance avec le nombre de commandes actives
                                active_orders = len(order_manager.active_orders) if hasattr(order_manager, 'active_orders') else 0
                                chance += active_orders / 200
                                
                                if random.random() < chance:
                                    # Créer un accident
                                    if hasattr(kitchen_renderer, 'create_accident'):
                                        accident_info = kitchen_renderer.create_accident(bot_manager)
                                    else:
                                        # Créer un accident manuellement
                                        accidents = [
                                            "Le steak brûle sur la cuisinière!",
                                            "Un ingrédient tombe par terre!",
                                            "Un chef trébuche et renverse des aliments!",
                                            "Feu de friteuse! (simulé)",
                                            "Panne de l'équipement de cuisson!"
                                        ]
                                        accident_message = random.choice(accidents)
                                        
                                        # Créer un effet visuel
                                        accident_effect = {
                                            'message': accident_message,
                                            'position': (random.randint(100, 900), random.randint(150, 550)),
                                            'timer': 180,  # 3 secondes à 60 FPS
                                            'type': random.choice(['fire', 'spill', 'smoke'])
                                        }
                                        
                                        # Ajouter à la liste des accidents
                                        if not hasattr(kitchen_renderer, 'kitchen_accidents'):
                                            kitchen_renderer.kitchen_accidents = []
                                        kitchen_renderer.kitchen_accidents.append(accident_effect)
                                        accident_info = accident_effect
                                    
                                    if accident_info:
                                        print(f"🚨 ACCIDENT! {accident_info['message']}")
                                        kitchen_renderer.total_accidents_count += 1
                                        
                                        # Augmenter le stress de la cuisine
                                        kitchen_renderer.kitchen_stress_level = min(100, 
                                            kitchen_renderer.kitchen_stress_level + 15)
                    
                    # ✅ MISE À JOUR DES ACCIDENTS EXISTANTS
                    if hasattr(kitchen_renderer, 'kitchen_accidents'):
                        for accident in kitchen_renderer.kitchen_accidents[:]:
                            # Réduire le timer
                            if 'timer' in accident:
                                accident['timer'] -= 1
                                if accident['timer'] <= 0:
                                    kitchen_renderer.kitchen_accidents.remove(accident)
                    
                    # Stress équilibré avec accidents
                    active_orders_count = len(order_manager.active_orders) if hasattr(order_manager, 'active_orders') else 0
                    
                    base_stress = active_orders_count * 5
                    busy_chefs = sum(1 for bot in bot_manager.bots 
                                   if bot.state not in ["idle", "thinking", "observing"])
                    base_stress += busy_chefs * 3
                    
                    # ✅ INCLURE LES ACCIDENTS DANS LE CALCUL DU STRESS
                    if hasattr(kitchen_renderer, 'total_accidents_count'):
                        base_stress += kitchen_renderer.total_accidents_count * 10  # +10% par accident
                    
                    if base_stress > kitchen_renderer.kitchen_stress_level:
                        kitchen_renderer.kitchen_stress_level = min(90, kitchen_renderer.kitchen_stress_level + 1)
                    else:
                        kitchen_renderer.kitchen_stress_level = max(0, kitchen_renderer.kitchen_stress_level - 0.3)
                    
                    # ✅ Mise à jour du système de stress sans mode panique
                    if hasattr(kitchen_renderer, 'update_stress_system'):
                        # Forcer le mode panique à False
                        kitchen_renderer.panic_mode = False
                        kitchen_renderer.update_stress_system(bot_manager, order_manager)
                    
                    # ✅ Mise à jour des accidents
                    if hasattr(kitchen_renderer, 'update_accidents'):
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
                        accidents_count = kitchen_renderer.total_accidents_count
                        
                        active_orders_count = len(order_manager.active_orders) if hasattr(order_manager, 'active_orders') else 0
                        
                        print(f"  ⚡ Stress cuisine: {stress_level:.0f}%")
                        print(f"  🚨 Mode panique: DÉSACTIVÉ")
                        print(f"  📈 Commandes actives: {active_orders_count}")
                        print(f"  🔥 Accidents: {accidents_count}")
                    
                    last_debug_time = current_time
                    
            except Exception as e:
                print(f"⚠ Erreur mise à jour: {e}")
                import traceback
                traceback.print_exc()
                continue

            # RENDU PRINCIPAL
            screen.fill((50, 60, 70))
            
            try:
                if kitchen_renderer:
                    # ✅ Rendu avec accidents mais SANS mode panique
                    kitchen_renderer.render_full_kitchen(
                        bot_manager, 
                        asset_manager, 
                        game_state.timer, 
                        order_manager
                    )
                    
                    # ✅ RENDRE LES ACCIDENTS VISIBLES
                    if hasattr(kitchen_renderer, 'kitchen_accidents'):
                        for accident in kitchen_renderer.kitchen_accidents:
                            # Dessiner l'effet visuel
                            if accident['type'] == 'fire':
                                # Feu orange/rouge
                                pygame.draw.circle(screen, (255, 100, 0), accident['position'], 20)
                                pygame.draw.circle(screen, (255, 200, 0), accident['position'], 15)
                                pygame.draw.circle(screen, (255, 255, 150), accident['position'], 8)
                            elif accident['type'] == 'smoke':
                                # Fumée grise
                                pygame.draw.circle(screen, (100, 100, 100), accident['position'], 25)
                                pygame.draw.circle(screen, (150, 150, 150), accident['position'], 18)
                                pygame.draw.circle(screen, (200, 200, 200), accident['position'], 10)
                            elif accident['type'] == 'spill':
                                # Débordement liquide
                                pygame.draw.circle(screen, (100, 150, 255), accident['position'], 22)
                                pygame.draw.circle(screen, (150, 200, 255), accident['position'], 16)
                                pygame.draw.circle(screen, (200, 230, 255), accident['position'], 10)
                            
                            # Afficher un texte d'avertissement
                            font = pygame.font.Font(None, 20)
                            warning_text = font.render("!", True, (255, 0, 0))
                            screen.blit(warning_text, (accident['position'][0] - 5, accident['position'][1] - 10))
                else:
                    draw_basic_kitchen(screen)
                    for bot in bot_manager.bots:
                        bot.draw_chef(screen)
                        
            except Exception as e:
                print(f"⚠ Erreur rendu: {e}")
                import traceback
                traceback.print_exc()
                draw_basic_kitchen(screen)
            
            # ⭐ INTERFACE CORRIGÉE
            try:
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
                
                # ✅ CORRECTION: Limiter l'affichage du texte de saisie
                user_input_display = game_state.user_input + ("_" if int(time.time() * 2) % 2 == 0 else " ")
                # Limiter à 22 caractères affichés
                if len(user_input_display) > 22:
                    user_input_display = user_input_display[-22:]
                input_text = font_medium.render(user_input_display, True, (255, 255, 150))
                screen.blit(input_text, (20, 35))
                
                # ✅ BARRE DE STRESS - ARRONDIE
                if kitchen_renderer:
                    stress_level = int(kitchen_renderer.kitchen_stress_level)  # ✅ ARRONDI
                    
                    stress_x = 370
                    stress_y = 15
                    
                    if stress_level < 40:
                        stress_color = (100, 255, 100)
                    elif stress_level < 70:
                        stress_color = (255, 200, 50)
                    else:
                        stress_color = (255, 80, 80)
                    
                    stress_bg = pygame.Rect(stress_x, stress_y, 200, 25)
                    pygame.draw.rect(screen, (50, 50, 50), stress_bg, border_radius=5)
                    
                    stress_fill_width = int(200 * (stress_level / 100))
                    stress_fill = pygame.Rect(stress_x, stress_y, stress_fill_width, 25)
                    pygame.draw.rect(screen, stress_color, stress_fill, border_radius=5)
                    
                    # ✅ TEXTE SANS DÉCIMALES
                    stress_text = font_small.render(f"Stress: {stress_level}%", True, (255, 255, 255))
                    screen.blit(stress_text, (stress_x + 5, stress_y + 4))
                    
                    # ✅ AFFICHER LE NOMBRE D'ACCIDENTS
                    accidents_count = kitchen_renderer.total_accidents_count
                    if accidents_count > 0:
                        accident_text = font_small.render(f"🔥 {accidents_count}", True, (255, 100, 100))
                        screen.blit(accident_text, (stress_x + 180, stress_y + 4))
                
                # TIMER
                timer_x = stress_x + 210
                timer_y = stress_y + 2
                timer_text = font_large.render(f"⏱️ {game_state.timer:.1f}s", True, (255, 255, 255))
                screen.blit(timer_text, (timer_x, timer_y))
                
            except Exception as e:
                print(f"⚠ Erreur UI: {e}")
                import traceback
                traceback.print_exc()
            
            pygame.display.flip()
        
        # Fin de partie
        game_logic.stop()
        stats = game_logic.calculate_final_stats()
        stats['total_chefs'] = len(bot_manager.bots)
        stats['leaderboard'] = bot_manager.get_leaderboard()
        
        if kitchen_renderer:
            stats['max_stress'] = int(kitchen_renderer.kitchen_stress_level)  # ✅ ARRONDI
            stats['panic_mode'] = False  # Toujours désactivé
            stats['accidents_count'] = kitchen_renderer.total_accidents_count
        
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
        
        pygame.draw.rect(screen, (200, 200, 255), (50, 120, 300, 350))
        pygame.draw.rect(screen, (160, 120, 80), (400, 120, 250, 120))
        pygame.draw.rect(screen, (240, 230, 220), (400, 280, 250, 100))
        pygame.draw.rect(screen, (255, 200, 100), (700, 120, 120, 300))
        
    except Exception:
        screen.fill((50, 50, 50))


def show_game_over_screen(screen, stats, bot_manager, kitchen_renderer=None):
    """✅ ÉCRAN DE FIN CORRIGÉ - AVEC ACCIDENTS, SANS PANIQUE"""
    try:
        import game_state
        import config
        
        # Fond avec effet de flou
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((10, 15, 30))
        screen.blit(overlay, (0, 0))
        
        # Effet d'étoiles
        for i in range(50):
            x = random.randint(0, config.WIDTH)
            y = random.randint(0, config.HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
        
        # Polices améliorées
        font_title = pygame.font.Font(None, 64)
        font_large = pygame.font.Font(None, 40)
        font_medium = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 22)
        
        # Titre avec effet
        title = font_title.render("PARTIE TERMINÉE!", True, (255, 215, 0))
        title_shadow = font_title.render("PARTIE TERMINÉE!", True, (180, 140, 0))
        screen.blit(title_shadow, title_shadow.get_rect(center=(config.WIDTH//2 + 3, 53)))
        screen.blit(title, title.get_rect(center=(config.WIDTH//2, 50)))
        
        # Ligne décorative
        pygame.draw.line(screen, (255, 215, 0), (100, 90), (config.WIDTH-100, 90), 3)
        
        y_offset = 115
        
        # Score avec effet
        score_bg = pygame.Rect(config.WIDTH//2 - 180, y_offset - 8, 360, 55)
        pygame.draw.rect(screen, (30, 40, 60), score_bg, border_radius=12)
        pygame.draw.rect(screen, (255, 215, 0), score_bg, 3, border_radius=12)
        
        score_text = font_large.render(f"🎯 Score Final: {game_state.score}", True, (255, 255, 255))
        screen.blit(score_text, score_text.get_rect(center=(config.WIDTH//2, y_offset + 15)))
        y_offset += 70
        
        # ✅ STATISTIQUES AVEC ACCIDENTS
        if kitchen_renderer:
            stats_bg = pygame.Rect(config.WIDTH//2 - 240, y_offset - 8, 480, 85)
            pygame.draw.rect(screen, (40, 50, 70, 200), stats_bg, border_radius=12)
            pygame.draw.rect(screen, (100, 150, 255), stats_bg, 2, border_radius=12)
            
            # ✅ STRESS ET ACCIDENTS
            max_stress = int(stats.get('max_stress', 0))
            accidents_count = stats.get('accidents_count', 0)
            
            stress_text = font_medium.render(f"📈 Stress maximum: {max_stress}%", True, (255, 200, 100))
            accidents_text = font_medium.render(f"🔥 Accidents: {accidents_count}", True, (255, 100, 100))
            
            screen.blit(stress_text, stress_text.get_rect(center=(config.WIDTH//2, y_offset + 20)))
            screen.blit(accidents_text, accidents_text.get_rect(center=(config.WIDTH//2, y_offset + 50)))
        
        y_offset += 90
        
        # Classement avec effets
        classement_title = font_large.render("🏆 CLASSEMENT FINAL 🏆", True, (255, 215, 0))
        screen.blit(classement_title, classement_title.get_rect(center=(config.WIDTH//2, y_offset)))
        y_offset += 50
        
        leaderboard = bot_manager.get_leaderboard()
        winner_name = ""
        
        for i, entry in enumerate(leaderboard):
            # Cadre pour chaque chef
            chef_bg = pygame.Rect(config.WIDTH//2 - 280, y_offset - 10, 560, 75)
            bg_color = (50, 70, 100) if i % 2 == 0 else (60, 80, 110)
            pygame.draw.rect(screen, bg_color, chef_bg, border_radius=10)
            
            # Bordure colorée selon le rang
            if i == 0:
                border_color = (255, 215, 0)
                medal = "🥇"
            elif i == 1:
                border_color = (192, 192, 192)
                medal = "🥈"
            elif i == 2:
                border_color = (205, 127, 50)
                medal = "🥉"
            else:
                border_color = (100, 120, 150)
                medal = f"{i+1}."
            
            pygame.draw.rect(screen, border_color, chef_bg, 2, border_radius=10)
            
            if i == 0:
                winner_name = entry['name']
            
            # ✅ NOM DU CHEF À GAUCHE
            chef_text = f"{medal} {entry['name']}"
            chef_surf = font_medium.render(chef_text, True, (255, 255, 255))
            screen.blit(chef_surf, (config.WIDTH//2 - 265, y_offset + 5))
            
            # ✅ SCORE À DROITE - BIEN ALIGNÉ
            score_surf = font_medium.render(f"{entry['score']} points", True, (200, 255, 200))
            score_rect = score_surf.get_rect(right=config.WIDTH//2 + 265, centery=y_offset + 15)
            screen.blit(score_surf, score_rect)
            
            # ✅ STATISTIQUES EN BAS
            dishes = entry['stats']['dishes_delivered']
            stats_text = f"Plats livrés: {dishes}"
            stats_surf = font_small.render(stats_text, True, (180, 200, 220))
            screen.blit(stats_surf, (config.WIDTH//2 - 265, y_offset + 35))
            
            y_offset += 85
        
        # ✅ MESSAGE DE FÉLICITATIONS AU GAGNANT
        if winner_name:
            y_offset += 15
            congrats_bg = pygame.Rect(config.WIDTH//2 - 320, y_offset - 8, 640, 55)
            pygame.draw.rect(screen, (30, 60, 100), congrats_bg, border_radius=12)
            pygame.draw.rect(screen, (255, 215, 0), congrats_bg, 3, border_radius=12)
            
            # ✅ MESSAGE COMPLET
            congrats_text = font_large.render(f"🎉 Félicitations au gagnant {winner_name} ! 🎉", True, (255, 255, 200))
            screen.blit(congrats_text, congrats_text.get_rect(center=(config.WIDTH//2, y_offset + 20)))
            y_offset += 70
        
        # Message de fin avec effet de clignotement
        blink = int(time.time() * 2) % 2 == 0
        if blink:
            continue_text = font_small.render("Appuyez sur une touche pour quitter...", True, (150, 200, 255))
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