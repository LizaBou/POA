import pygame, time, math

pygame.init()

# ----- CONFIGURATION -----
WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Overcooked Bot")

# Images
player_img = pygame.transform.scale(pygame.image.load("images/player1.png"), (50,50))
knife_img = pygame.transform.scale(pygame.image.load("images/couteau.png"), (40,40))

ingredient_imgs = {
    "T": pygame.transform.scale(pygame.image.load("images/tomate.png"), (40,40)),
    "L": pygame.transform.scale(pygame.image.load("images/salade.png"), (40,40)),
    "B": pygame.transform.scale(pygame.image.load("images/pain.png"), (40,40)),
    "C": pygame.transform.scale(pygame.image.load("images/fromage.png"), (40,40)),
    "H": pygame.transform.scale(pygame.image.load("images/steak.png"), (40,40))
}

cutting_img = pygame.transform.scale(pygame.image.load("images/planche.png"), (400,150))
delivery_img = pygame.transform.scale(pygame.image.load("images/livraison.png"), (64,64))
sol_img = pygame.transform.scale(pygame.image.load("images/sol.png"), (64,64))

# ----- BOT -----
bot = {"x":50, "y":HEIGHT//2, "img":player_img, "inv":None, "preparing":None, "prep_time":0, "prep_position":(0,0)}

# Zones fixes
fridge = {"x":50, "y":50}
cutting_board = {"x":WIDTH//2-200, "y":50, "w":400, "h":150}
delivery = {"x":cutting_board["x"] + cutting_board["w"] + 20, "y":cutting_board["y"]}

# Recettes
recipes = {
    "salade": ["L", "T"],
    "steak": ["H"],
    "burger": ["B", "T", "L", "C", "H"]
}

# Ingrédients à couper
to_cut = ["L","T","B","C"]

# Tranches
slices_count = {"T":4, "L":3, "B":2, "C":3, "H":1}

# Ingrédients dans le frigo
ingredients = [{"x":fridge["x"], "y":fridge["y"], "type":t, "taken":False} for t in ["T","L","B","C","H"] for _ in range(3)]

# Commande
current_order_name = None
current_order = []
assembled_plate = []
board_contents = []

# Livraisons visibles
delivered_plates = []

# Score et timer
score = 0
timer = 120
user_input = ""
PREP_DURATION = 2.5

# Fonction pour dessiner une planche à découper stylée
def draw_cutting_board(screen, x, y, w, h):
    # Cadre extérieur en bois foncé
    pygame.draw.rect(screen, (101, 67, 33), (x-5, y-5, w+10, h+10))  # Brun foncé
    
    # Surface de la planche en bois clair
    pygame.draw.rect(screen, (205, 133, 63), (x, y, w, h))  # Brun clair
    
    # Texture bois - lignes horizontales
    for i in range(5, h-5, 15):
        pygame.draw.line(screen, (180, 120, 50), (x+10, y+i), (x+w-10, y+i), 1)
    
    # Bordure interne décorative
    pygame.draw.rect(screen, (139, 90, 43), (x+10, y+10, w-20, h-20), 3)
    
    # Zone de découpe centrale
    center_x, center_y = x + w//2 - 100, y + h//2 - 40
    pygame.draw.rect(screen, (160, 110, 60), (center_x, center_y, 200, 80))
    pygame.draw.rect(screen, (120, 80, 40), (center_x, center_y, 200, 80), 2)

def draw_kitchen_counter():
    # Comptoir de cuisine avec tiroirs
    counter_x, counter_y = cutting_board["x"] - 50, cutting_board["y"] + cutting_board["h"] + 10
    counter_w, counter_h = cutting_board["w"] + 100, 80
    
    # Base du comptoir
    pygame.draw.rect(SCREEN, (139, 126, 102), (counter_x, counter_y, counter_w, counter_h))
    
    # Tiroirs
    drawer_w = counter_w // 3 - 10
    for i in range(3):
        drawer_x = counter_x + 10 + i * (drawer_w + 5)
        pygame.draw.rect(SCREEN, (160, 145, 120), (drawer_x, counter_y + 15, drawer_w, counter_h - 30))
        pygame.draw.rect(SCREEN, (100, 90, 70), (drawer_x, counter_y + 15, drawer_w, counter_h - 30), 2)
        
        # Poignées
        handle_x = drawer_x + drawer_w // 2 - 8
        handle_y = counter_y + counter_h // 2 - 3
        pygame.draw.ellipse(SCREEN, (80, 70, 50), (handle_x, handle_y, 16, 6))

# Fonctions
def distance(a,b):
    return ((a["x"]-b["x"])**2 + (a["y"]-b["y"])**2)**0.5

def clamp_player(p):
    p["x"] = max(0, min(WIDTH - p["img"].get_width(), p["x"]))
    p["y"] = max(0, min(HEIGHT - p["img"].get_height(), p["y"]))

# Horloge
clock = pygame.time.Clock()
start_time = time.time()

# ----- BOUCLE -----
running = True
while running and timer>0:
    SCREEN.fill((45, 45, 45))  # Fond gris foncé pour une ambiance cuisine
    
    # Dessiner sol avec motif carrelage
    tile_size = 64
    for i in range(0, WIDTH, tile_size):
        for j in range(0, HEIGHT, tile_size):
            # Alternance de couleurs pour effet carrelage
            if (i//tile_size + j//tile_size) % 2 == 0:
                pygame.draw.rect(SCREEN, (240, 240, 240), (i, j, tile_size, tile_size))
            else:
                pygame.draw.rect(SCREEN, (220, 220, 220), (i, j, tile_size, tile_size))
            # Joints de carrelage
            pygame.draw.rect(SCREEN, (180, 180, 180), (i, j, tile_size, tile_size), 1)
    
    # Dessiner le comptoir de cuisine
    draw_kitchen_counter()
    
    # Dessiner la planche à découper améliorée
    draw_cutting_board(SCREEN, cutting_board["x"], cutting_board["y"], cutting_board["w"], cutting_board["h"])
    
    # Zone de livraison avec style
    pygame.draw.rect(SCREEN, (200, 150, 100), (delivery["x"]-10, delivery["y"]-10, 84, 84))
    pygame.draw.rect(SCREEN, (150, 100, 50), (delivery["x"]-10, delivery["y"]-10, 84, 84), 3)
    SCREEN.blit(delivery_img,(delivery["x"],delivery["y"]))
    
    # Zone frigo avec style
    pygame.draw.rect(SCREEN, (200, 220, 255), (fridge["x"]-15, fridge["y"]-15, 80, 80))
    pygame.draw.rect(SCREEN, (150, 180, 220), (fridge["x"]-15, fridge["y"]-15, 80, 80), 3)
    
    # Ingrédients disponibles
    for ing in ingredients:
        if not ing["taken"]:
            SCREEN.blit(ingredient_imgs[ing["type"]],(ing["x"],ing["y"]))
    
    # Ingrédients sur la planche (dans la zone de découpe)
    for idx, ing_type in enumerate(board_contents):
        offset_x = (idx % 4) * 45
        offset_y = (idx // 4) * 45
        pos_x = cutting_board["x"] + cutting_board["w"]//2 - 80 + offset_x
        pos_y = cutting_board["y"] + cutting_board["h"]//2 - 30 + offset_y
        SCREEN.blit(ingredient_imgs[ing_type], (pos_x, pos_y))
    
    # Bot avec ombre
    pygame.draw.ellipse(SCREEN, (50, 50, 50, 100), (bot["x"]+5, bot["y"]+45, 40, 15))  # Ombre
    SCREEN.blit(bot["img"],(bot["x"],bot["y"]))
    
    # Découpe animée
    if bot["preparing"]:
        elapsed = time.time() - bot["prep_time"]
        total_slices = slices_count[bot["preparing"]]
        slices_done = int(total_slices * min(elapsed / PREP_DURATION,1))
        
        # Effet de découpe avec particules
        for i in range(slices_done):
            slice_x = bot["prep_position"][0] + i * 8 + math.sin(time.time() * 3 + i) * 3
            slice_y = bot["prep_position"][1] + i * 8 + math.cos(time.time() * 3 + i) * 3
            SCREEN.blit(ingredient_imgs[bot["preparing"]], (slice_x, slice_y))
        
        # Animation du couteau plus fluide
        knife_offset_x = 25 * math.sin(time.time() * 8)
        knife_offset_y = 15 * math.cos(time.time() * 8)
        knife_angle = math.sin(time.time() * 8) * 30
        
        # Rotation du couteau
        rotated_knife = pygame.transform.rotate(knife_img, knife_angle)
        knife_rect = rotated_knife.get_rect(center=(bot["prep_position"][0] + 20 + knife_offset_x, 
                                                   bot["prep_position"][1] + 20 + knife_offset_y))
        SCREEN.blit(rotated_knife, knife_rect)
        
        # Effet de brillance sur le couteau
        if int(time.time() * 10) % 3 == 0:
            pygame.draw.circle(SCREEN, (255, 255, 255), 
                             (int(knife_rect.centerx + 10), int(knife_rect.centery - 10)), 3)
    elif bot["inv"]:
        # Ingrédient porté avec légère oscillation
        carry_offset_y = math.sin(time.time() * 4) * 3
        SCREEN.blit(ingredient_imgs[bot["inv"]], (bot["x"], bot["y"] - 45 + carry_offset_y))
    
    # Affichage plats livrés avec animation
    for plate in delivered_plates:
        alpha = max(0, 255 - int((time.time() - plate["time"]) * 255))
        for i, ing_type in enumerate(plate["plate"]):
            img = ingredient_imgs[ing_type].copy()
            img.set_alpha(alpha)
            pos_y = plate["y"] - (time.time() - plate["time"]) * 30  # Animation montante
            SCREEN.blit(img, (plate["x"] + i * 20, pos_y))
    delivered_plates = [p for p in delivered_plates if time.time()-p["time"]<1.5]
    
    # Interface utilisateur améliorée - déplacée en bas
    font = pygame.font.SysFont('Arial', 24, bold=True)
    font_small = pygame.font.SysFont('Arial', 20)
    
    # Fond pour le texte en bas de l'écran
    ui_y = HEIGHT - 75
    pygame.draw.rect(SCREEN, (0, 0, 0, 200), (5, ui_y, WIDTH-10, 70))
    pygame.draw.rect(SCREEN, (100, 100, 100), (5, ui_y, WIDTH-10, 70), 2)
    
    # Texte principal
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = font.render(f"Temps: {int(timer)}s", True, (255, 255, 255))
    order_text = font.render(f"Commande: {current_order_name if current_order_name else 'Aucune'}", True, (255, 215, 0))
    
    SCREEN.blit(score_text, (15, ui_y + 5))
    SCREEN.blit(time_text, (150, ui_y + 5))
    SCREEN.blit(order_text, (280, ui_y + 5))
    
    # Zone de saisie stylée en bas
    input_bg = pygame.Rect(15, ui_y + 35, 400, 30)
    pygame.draw.rect(SCREEN, (50, 50, 50), input_bg)
    pygame.draw.rect(SCREEN, (200, 200, 200), input_bg, 2)
    
    input_text = font_small.render("Tapez la commande: " + user_input + "|", True, (255, 255, 0))
    SCREEN.blit(input_text, (20, ui_y + 40))
    
    pygame.display.flip()
    
    # Événements
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                if user_input.lower() in recipes:
                    current_order_name = user_input.lower()
                    current_order = recipes[current_order_name].copy()
                    assembled_plate.clear()
                    board_contents.clear()
                user_input=""
            elif event.key==pygame.K_BACKSPACE:
                user_input=user_input[:-1]
            else:
                user_input+=event.unicode
    
    # --- LOGIQUE BOT ---
    target = None
    # Prochain ingrédient exact de la recette restant
    if bot["inv"] is None and bot["preparing"] is None and current_order:
        next_ing = current_order[0]
        for ing in ingredients:
            if ing["type"]==next_ing and not ing["taken"]:
                target = ing
                break
    elif bot["inv"]:
        target = cutting_board
    elif current_order_name and len(assembled_plate)==len(recipes[current_order_name]):
        target = delivery

    # Déplacement
    speed = 3
    if target:
        if abs(bot["x"]-target["x"])>speed: bot["x"] += speed if bot["x"]<target["x"] else -speed
        if abs(bot["y"]-target["y"])>speed: bot["y"] += speed if bot["y"]<target["y"] else -speed

    clamp_player(bot)
    
    # Prendre ingrédient
    if bot["inv"] is None and bot["preparing"] is None and current_order:
        for ing in ingredients:
            if not ing["taken"] and ing["type"]==current_order[0] and distance(bot, ing)<50:
                bot["inv"] = ing["type"]
                ing["taken"] = True
                current_order.pop(0)  # Retirer seulement l'ingrédient pris
                break

    # Découpe si nécessaire
    if bot["inv"] and distance(bot,cutting_board)<64:
        if bot["inv"] in to_cut:
            bot["preparing"] = bot["inv"]
            bot["prep_time"] = time.time()
            idx = len(board_contents)
            # Position centrée dans la zone de découpe
            bot["prep_position"] = (cutting_board["x"] + cutting_board["w"]//2 - 80 + (idx%4)*45, 
                                  cutting_board["y"] + cutting_board["h"]//2 - 30 + (idx//4)*45)
        else:
            assembled_plate.append(bot["inv"])
            board_contents.append(bot["inv"])
        bot["inv"] = None

    # Terminer découpe
    if bot["preparing"] and time.time()-bot["prep_time"]>=PREP_DURATION:
        assembled_plate.append(bot["preparing"])
        board_contents.append(bot["preparing"])
        bot["preparing"] = None

    # Livraison
    if current_order_name and len(assembled_plate)==len(recipes[current_order_name]) and distance(bot,delivery)<50:
        delivered_plates.append({
            "plate": assembled_plate.copy(),
            "x": delivery["x"],
            "y": delivery["y"],
            "time": time.time()
        })
        score += 10
        assembled_plate.clear()
        board_contents.clear()
        current_order_name=None
        current_order=[]

    timer = 120 - (time.time()-start_time)
    clock.tick(30)

pygame.quit()
print(f"Fin de la partie! Score final: {score}")