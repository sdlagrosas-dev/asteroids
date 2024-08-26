import random
import pygame
import circleshape
from constants import *


class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        super().draw(screen)

        pygame.draw.circle(
            screen, color="red", center=self.position, radius=self.radius, width=2
        )

    def update(self, dt):
        super().update(dt)

        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        rand_angle = random.uniform(20, 50)
        spawn_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_spawn_1 = Asteroid(self.position.x, self.position.y, spawn_radius)
        asteroid_spawn_1.velocity = (
            asteroid_spawn_1.position.rotate(rand_angle) * ASTEROID_SPLIT_VELOCITY
        )

        asteroid_spawn_2 = Asteroid(self.position.x, self.position.y, spawn_radius)
        asteroid_spawn_2.velocity = (
            asteroid_spawn_2.position.rotate(-rand_angle) * ASTEROID_SPLIT_VELOCITY
        )
