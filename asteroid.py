import random
import pygame
import circleshape
from constants import *


class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.edges = self.generate_edges(15)

    def generate_edges(self, n):
        rand_angles = random.sample(range(0, 360, 10), n)
        rand_angles.sort()
        rand_points = []

        for angle in rand_angles:
            vector = pygame.Vector2(0, 1).rotate(angle)
            point_pos = vector * self.radius
            rand_points.append(point_pos)

        return rand_points

    def draw(self, screen):
        super().draw(screen)

        # pygame.draw.circle(
        #     screen, color="red", center=self.position, radius=self.radius, width=2
        # )
        edge_update = [self.position + edge for edge in self.edges]

        pygame.draw.polygon(
            screen,
            color="red",
            points=edge_update,
            width=2
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
