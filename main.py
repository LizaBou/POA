import os
import time
import random

# ----- CONFIGURATION -----
WIDTH, HEIGHT = 10, 6  # Taille de la cuisine (grille)
EMPTY = '.'
PLAYER = 'P'
CUTTING_BOARD = 'C'
DELIVERY = 'D'

# Ingrédients possibles
INGREDIENTS = ['T', 'L', 'B']  # T=Tomate, L=Salade, B=Pain

# Position du joueur
player_x, player_y = 1, 1
inventory = None  # ingrédient que le joueur porte

# Ingrédients dans la cuisine (x,y) : type
ingredients = {
    (3, 2): 'T',
    (6, 4): 'L',
    (2, 5): 'B'
}

# Stations
cutting_board = (8, 2)
delivery = (9, 5)

# Score et timer
score = 0
timer = 60  # durée en secondes

# Commande actuelle (liste d'ingrédients à préparer)
current_order = random.sample(INGREDIENTS, 2)

# Plat assemblé sur la planche
assembled_plate = []

# ----- FONCTIONS -----
def draw():
    """Affiche la cuisine et le joueur"""
    os.system('clear')  # sur Linux / Mac, utilisez 'cls' sur Windows
    for y in range(HEIGHT):
        row = ''
        for x in range(WIDTH):
            if (x, y) == (player_x, player_y):
                row += PLAYER
            elif (x, y) in ingredients:
                row += ingredients[(x, y)]
            elif (x, y) == cutting_board:
                row += CUTTING_BOARD
            elif (x, y) == delivery:
                row += DELIVERY
            else:
                row += EMPTY
        print(row)
    print(f"\nInventaire: {inventory if inventory else 'vide'} | Plate: {assembled_plate}")
    print(f"Score: {score} | Temps restant: {timer}")
    print(f"Commande à préparer: {current_order}")

def move_player(direction):
    """Déplace le joueur sur la grille"""
    global player_x, player_y
    if direction == 'z' and player_y > 0:
        player_y -= 1
    elif direction == 's' and player_y < HEIGHT - 1:
        player_y += 1
    elif direction == 'q' and player_x > 0:
        player_x -= 1
    elif direction == 'd' and player_x < WIDTH - 1:
        player_x += 1

def action():
    """Permet de ramasser, poser ou livrer un plat"""
    global inventory, assembled_plate, score, current_order

    # Ramasser un ingrédient
    if (player_x, player_y) in ingredients and inventory is None:
        inventory = ingredients.pop((player_x, player_y))
        print(f"Vous avez ramassé {inventory}")

    # Poser sur la planche pour assembler
    elif (player_x, player_y) == cutting_board and inventory is not None:
        assembled_plate.append(inventory)
        print(f"{inventory} ajouté à la planche")
        inventory = None

    # Livrer un plat
    elif (player_x, player_y) == delivery and assembled_plate:
        if sorted(assembled_plate) == sorted(current_order):
            score += 10
            print("Plat livré avec succès! +10 points")
        else:
            print("Commande incorrecte! Aucun point")
        assembled_plate = []
        # Nouvelle commande aléatoire
        current_order = random.sample(INGREDIENTS, 2)

# ----- BOUCLE DE JEU -----
start_time = time.time()
while timer > 0:
    draw()
    cmd = input("Commande (z=haut, s=bas, q=gauche, d=droite, e=action, x=quitter): ")
    if cmd == 'x':
        break
    elif cmd in ['z', 's', 'q', 'd']:
        move_player(cmd)
    elif cmd == 'e':
        action()

    # Met à jour le timer
    elapsed = int(time.time() - start_time)
    timer = 60 - elapsed

print("\nFin de la partie!")
print(f"Score final: {score}")
