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
    SCREEN.fill((0,0,0))
    
    # Dessiner sol
    for i in range(0, WIDTH, 64):
        for j in range(0, HEIGHT, 64):
            SCREEN.blit(sol_img,(i,j))
    
    # Dessiner planche et comptoir livraison
    SCREEN.blit(cutting_img,(cutting_board["x"],cutting_board["y"]))
    SCREEN.blit(delivery_img,(delivery["x"],delivery["y"]))
    
    # Ingrédients disponibles
    for ing in ingredients:
        if not ing["taken"]:
            SCREEN.blit(ingredient_imgs[ing["type"]],(ing["x"],ing["y"]))
    
    # Ingrédients sur la planche
    for idx, ing_type in enumerate(board_contents):
        offset_x = idx % 8 * 40
        offset_y = idx // 8 * 40
        SCREEN.blit(ingredient_imgs[ing_type], (cutting_board["x"]+10+offset_x, cutting_board["y"]+10+offset_y))
    
    # Bot
    SCREEN.blit(bot["img"],(bot["x"],bot["y"]))
    
    # Découpe animée
    if bot["preparing"]:
        elapsed = time.time() - bot["prep_time"]
        total_slices = slices_count[bot["preparing"]]
        slices_done = int(total_slices * min(elapsed / PREP_DURATION,1))
        for i in range(slices_done):
            SCREEN.blit(ingredient_imgs[bot["preparing"]],
                        (bot["prep_position"][0]+i*5, bot["prep_position"][1]+i*5))
        knife_offset_x = 20*math.sin(time.time()*5)
        knife_offset_y = 20*math.cos(time.time()*5)
        SCREEN.blit(knife_img,(bot["prep_position"][0]+knife_offset_x, bot["prep_position"][1]+knife_offset_y))
    elif bot["inv"]:
        SCREEN.blit(ingredient_imgs[bot["inv"]],(bot["x"],bot["y"]-40))
    
    # Affichage plats livrés
    for plate in delivered_plates:
        for i, ing_type in enumerate(plate["plate"]):
            SCREEN.blit(ingredient_imgs[ing_type],
                        (plate["x"] + i*20, plate["y"]))
    delivered_plates = [p for p in delivered_plates if time.time()-p["time"]<1]
    
    # Texte
    font = pygame.font.SysFont(None,28)
    SCREEN.blit(font.render(f"Score: {score} | Temps: {int(timer)} | Commande: {current_order_name}", True, (255,255,255)),(10,10))
    SCREEN.blit(font.render("Tapez la commande: " + user_input, True, (255,255,0)),(10,40))
    
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
            bot["prep_position"] = (cutting_board["x"]+10+idx%8*40, cutting_board["y"]+10+idx//8*40)
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
