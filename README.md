# Mini Overcooked - Simulation Multi-Agents Compétitive

##  Description

**Mini Overcooked** est une simulation multi-agents en 2D développée avec Python et Pygame. Inspiré du jeu *Overcooked*, ce projet met en scène des **agents autonomes (chefs)** qui travaillent de manière **compétitive** pour préparer et livrer des plats.

Chaque agent :
- Perçoit son environnement
- Prend des décisions autonomes
- Gère sa propre commande
- Rivalise pour obtenir le meilleur score

## 🎮 Fonctionnalités

### Système Multi-Agents
- **2 agents autonomes** : Chef Marcel et Chef Sophie
- **Machine à états** : Gestion du comportement (idle, moving, preparing, plating)
- **Prise de décision** : Combinaison d'agents réactifs et déductifs
- **Gestion de la concurrence** : Exclusion mutuelle sur les ressources partagées

### Gameplay
- **5 recettes** : Salade, Burger, Sandwich, Salade complète, Burger deluxe
- **5 ingrédients** : Laitue (L), Tomate (T), Pain (B), Fromage (C), Steak (H)
- **4 zones d'interaction** : Stockage, Préparation, Assemblage, Service
- **Système de scoring** : Points selon la complexité + bonus de rapidité
- **Compte à rebours** : 60 secondes de jeu
- **Classement en temps réel** : Compétition entre agents

### Interface
- Rendu graphique fluide (60 FPS)
- Affichage des statistiques (score, timer, combo)
- Visualisation des états des agents
- Système de commandes par saisie textuelle

## 🛠️ Prérequis

- **Python** : version 3.8+
- **Pygame** : version 2.x

## 📦 Installation

```bash
# 1. Clone le dépôt
git clone https://github.com/LizaBou/POA.git
cd POA

# 2. Installe les dépendances
pip install pygame

# 3. Lance le jeu
python main.py
```

## 🎯 Utilisation

### Démarrage
Le jeu démarre automatiquement avec 2 agents (Marcel et Sophie).

### Ajouter une commande
Tapez le nom d'une recette dans la zone de saisie et appuyez sur **Entrée** :
- `salade`
- `burger`
- `sandwich`
- `salade complete`
- `burger deluxe`

### Touches de fonction
- **F1-F6** : Fonctions de debug
- **ESC** : Quitter le jeu

## 📊 Recettes et Points

| Recette | Ingrédients | Temps | Points |
|---------|-------------|-------|--------|
| Salade | Laitue, Tomate | ~2.5s | 10 |
| Sandwich | Pain, Fromage, Tomate | ~4.2s | 15 |
| Salade complète | Laitue, Tomate, Fromage | ~3.7s | 20 |
| Burger | Pain, Steak, Laitue, Tomate, Fromage | ~8.2s | 25 |
| Burger deluxe | Pain, Steak, Laitue, Tomate, Fromage | ~8.2s | 35 |

**Bonus de rapidité** :
- +10 points si livré en < 10s
- +5 points si livré en < 15s

## 🏗️ Architecture

```
POA/
├── main.py                 # Point d'entrée
├── config.py               # Configuration globale
├── game_state.py           # État partagé
├── entities/
│   ├── bot.py              # Agent autonome
│   └── order_manager.py    # Gestion des commandes
├── game/
│   ├── logic.py            # Logique du jeu
│   └── input_handler.py    # Gestion des entrées
└── graphics/
    ├── kitchen.py          # Rendu de la cuisine
    ├── ui.py               # Interface utilisateur
    └── assets.py           # Chargement des ressources
```

### Classes principales
- **Bot** : Agent chef avec machine à états
- **BotManager** : Coordination multi-agents
- **OrderManager** : File d'attente des commandes (FIFO)
- **KitchenRenderer** : Rendu visuel de la cuisine
- **UIRenderer** : Interface utilisateur



## 👤 Auteur

**Liza BOUROUINA**  
Master 1 Informatique – Génie Logiciel  
Université de Montpellier  
Année 2025-2026

## 📄 Licence

Projet académique - Université de Montpellier