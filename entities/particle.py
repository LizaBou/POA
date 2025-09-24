"""
Particle system - Gère les effets visuels de particules
"""
import random
import pygame
from config import COLORS, PARTICLE_COUNT

class Particle:
    def __init__(self, x, y, color, velocity, life):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.life = life
        self.max_life = life
        self.size = random.randint(2, 6)
    
    def update(self):
        """Met à jour la position et la vie de la particule"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravité
        self.life -= 1
        self.vx *= 0.98  # Friction
    
    def draw(self, screen):
        """Dessine la particule sur l'écran"""
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 255)
            size = max(1, int(self.size * (self.life / self.max_life)))
            color = (*self.color[:3], min(255, alpha))
            
            temp_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, color, (size, size), size)
            screen.blit(temp_surf, (int(self.x-size), int(self.y-size)))

    def is_alive(self):
        """Vérifie si la particule est encore vivante"""
        return self.life > 0

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_cutting_particles(self, x, y, ingredient_type):
        """Ajoute des particules lors de la découpe"""
        from entities.ingredient import IngredientManager
        ingredient_manager = IngredientManager()
        colors = ingredient_manager.get_ingredient_colors(ingredient_type)
        
        for _ in range(PARTICLE_COUNT):
            color = random.choice(colors)
            velocity = (random.uniform(-2, 2), random.uniform(-3, -1))
            particle = Particle(
                x + random.randint(-8, 8), 
                y + random.randint(-8, 8),
                color, velocity, random.randint(15, 30)
            )
            self.particles.append(particle)

    def add_sparkle_particles(self, x, y):
        """Ajoute des particules dorées (succès)"""
        for _ in range(4):
            velocity = (random.uniform(-1.5, 1.5), random.uniform(-3, -1))
            particle = Particle(
                x + random.randint(-4, 4), 
                y + random.randint(-4, 4),
                COLORS['gold'], velocity, random.randint(12, 25)
            )
            self.particles.append(particle)

    def add_delivery_particles(self, x, y):
        """Ajoute des particules lors de la livraison"""
        for _ in range(12):
            velocity = (random.uniform(-3, 3), random.uniform(-5, -2))
            particle = Particle(
                x + random.randint(-10, 10),
                y + random.randint(-10, 10),
                COLORS['gold'], velocity, random.randint(25, 50)
            )
            self.particles.append(particle)

    def update(self):
        """Met à jour toutes les particules"""
        # Mettre à jour les particules existantes
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, screen):
        """Dessine toutes les particules"""
        for particle in self.particles:
            particle.draw(screen)

    def clear(self):
        """Supprime toutes les particules"""
        self.particles.clear()

    def get_count(self):
        """Retourne le nombre de particules actives"""
        return len(self.particles)