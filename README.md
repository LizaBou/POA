# Mini Overcooked - Simulation Multi-Agents avec Architecture BDI

## 📋 Description

**Mini Overcooked** est une simulation multi-agents en 2D développée avec Python et Pygame. Inspiré du jeu *Overcooked*, ce projet met en scène des **agents autonomes (chefs)** dotés d'une **architecture BDI (Belief-Desire-Intention)** qui travaillent de manière **compétitive** pour préparer et livrer des plats.

### Architecture BDI

Chaque agent implémente le modèle BDI complet :
- **Beliefs (Croyances)** : Perception et représentation de l'environnement
- **Desires (Désirs)** : Génération d'options d'action selon les objectifs
- **Intentions (Intentions)** : Engagement envers un plan d'action
- **Planning STRIPS** : Raisonnement means-ends pour la génération de plans
- **Système émotionnel** : Gestion du stress et des émotions (😌 Calme, 🎯 Concentré, 😰 Stressé, 😱 Paniqué)

## 🎮 Fonctionnalités

### Système Multi-Agents BDI

- **2 agents BDI autonomes** : Chef Marcel et Chef Sophie
- **Cycle BDI complet** :
  1. **PERCEIVE** : Observation de l'environnement
  2. **DELIBERATE** : Génération et filtrage des désirs
  3. **MEANS-ENDS REASONING** : Planification STRIPS
  4. **EXECUTE** : Exécution des intentions
- **Système émotionnel dynamique** :
  - Niveau de stress adaptatif (0-100%)
  - 6 émotions : Calme, Concentré, Stressé, Paniqué, Heureux, Frustré
  - Impact sur la vitesse et les temps de préparation
- **Gestion des accidents** : Système de stress de la cuisine avec événements aléatoires

### Gameplay

- **5 recettes** : Salade, Burger, Sandwich, Salade complète, Burger deluxe
- **6 ingrédients** : Laitue, Tomate, Pain, Fromage, Steak, Oignon
- **Système de cuisson réaliste** : 
  - États de cuisson (Cru → Saignant → À point → Bien cuit → **BRÛLÉ**)
  - Gestion du timing critique
- **5 zones d'interaction** : Stockage, Préparation, Cuisson, Assemblage, Service
- **Système de scoring** : Points selon la complexité + bonus de rapidité
- **Compte à rebours** : 180 secondes de jeu
- **Classement en temps réel** : Compétition entre agents

### Interface

- Rendu graphique fluide (60 FPS)
- Affichage des statistiques (score, timer, stress)
- Visualisation des états émotionnels des agents
- Barres de stress individuelles et globale
- Système de commandes par saisie textuelle

## 🛠️ Prérequis

- **Python** : version 3.8+
- **Pygame** : version 2.x

## 📦 Installation

```bash
# 1. Clone le dépôt
git clone https://github.com/LizaBou/POA.git
cd POA

# 2. Bascule sur la branche BDI
git checkout feature/bdi-architecture

# 3. Installe les dépendances
pip install pygame

# 4. Lance le jeu
python main.py
```

## 🎯 Utilisation

### Démarrage

Le jeu démarre automatiquement avec 2 agents BDI (Marcel et Sophie).

### Ajouter une commande

Tapez le nom d'une recette dans la zone de saisie et appuyez sur **Entrée** :
- `salade`
- `burger`
- `sandwich`
- `salade_complete`
- `burger_deluxe`

### Touches de fonction

- **F1** : Ajouter 5 commandes aléatoires (test)
- **F2** : Réinitialiser le système
- **F3** : Forcer un accident (test)
- **F4** : Augmenter le stress +15%
- **F5** : Debug positions des bots
- **F7** : Afficher l'état mental des agents (Beliefs, Desires, Intentions)
- **F8** : Toggle logs BDI temps réel
- **F9** : Afficher l'état émotionnel des chefs
- **F10** : Afficher l'état du stress de la cuisine
- **ESC** : Quitter le jeu


**Système de cuisson** :
- Steak : 3s de cuisson optimale (risque de brûler après 3.6s)

## 🏗️ Architecture

```
POA/
├── main.py                 # Point d'entrée avec intégration BDI
├── config.py               # Configuration globale
├── game_state.py           # État partagé du jeu
├── entities/
│   ├── bot_bdi.py          # Agent BDI complet (⭐ NOUVEAU)
│   ├── bot.py              # Agent de base (legacy)
│   └── order_manager.py    # Gestion des commandes
├── game/
│   ├── logic.py            # Logique du jeu
│   └── input_handler.py    # Gestion des entrées
└── graphics/
    ├── kitchen.py          # Rendu de la cuisine + système de stress
    ├── ui.py               # Interface utilisateur
    └── assets.py           # Chargement des ressources
```

### Classes principales

#### Architecture BDI (`bot_bdi.py`)

- **BDIBot** : Agent complet avec cycle BDI
  - `Belief` : Croyances avec types (environment, self, other_agents, capability)
  - `Desire` : Désirs avec priorités et préconditions
  - `Intention` : Plans d'action avec engagement
  - `Action` : Actions atomiques STRIPS (préconditions, effets, durée)
  
- **Système émotionnel** :
  - `EmotionType` : Enum des 6 émotions
  - Calcul du stress dynamique selon la situation
  - Impact sur les performances (vitesse, temps de préparation)
  - Animations visuelles (tremblements en cas de stress)



#### Gestion du jeu

- **BotManager** : Coordination multi-agents et classement
- **OrderManager** : File d'attente des commandes (FIFO)
- **KitchenRenderer** : Rendu visuel + système de stress et accidents
- **UIRenderer** : Interface utilisateur étendue

## 🧠 Détails de l'Architecture BDI

### Cycle BDI

1. **PERCEIVE** : L'agent observe son environnement et met à jour ses croyances
   - Position, inventaire, commandes disponibles, état des autres agents
   - Filtrage des croyances périmées (> 10s)

2. **DELIBERATE** : Génération des options d'action (désirs)
   - Déblocage (priorité maximale si bloqué)
   - Prise de commande
   - Obtention d'ingrédients
   - Cuisson/Préparation
   - Assemblage du plat
   - Livraison

3. **MEANS-ENDS REASONING** : Planification STRIPS
   - Génération d'un plan d'actions pour atteindre le désir
   - Actions avec préconditions et effets
   - Durées adaptatives selon le stress

4. **EXECUTE** : Exécution du plan
   - Exécution séquentielle des actions
   - Gestion des échecs et timeouts adaptatifs
   - Abandon et récupération en cas de blocage

### Système émotionnel

Le stress est calculé dynamiquement selon :
- Progression de la commande (ingrédients restants)
- Échecs consécutifs
- Temps depuis le dernier succès
- Durée de l'intention courante
- Blocage physique

Les émotions influencent :
- **Vitesse de déplacement** : -40% en panique, +10% concentré
- **Temps de préparation** : +50% si stress > 100%
- **Affichage visuel** : Couleurs, tremblements, emojis

## 🌿 Branches

- **`main`** : Version stable avec agents réactifs de base
- **`feature/bdi-architecture`** : Version avec architecture BDI complète ⭐

## 👤 Auteur

**Liza BOUROUINA**  
Master 1 Informatique – Génie Logiciel  
Université de Montpellier  
Année 2025-2026

## 📄 Licence

Projet académique - Université de Montpellier

