import random
import pygame
import circleshape
from shot import Shot
from constants import *


class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius, kind):
        super().__init__(x, y, radius)
        self.edges = self.generate_edges(15)
        self.kind = kind

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

        edge_update = [self.position + edge for edge in self.edges]

        pygame.draw.polygon(screen, color="red", points=edge_update, width=2)

    def update(self, dt):
        super().update(dt)

        self.position += self.velocity * dt

    def split(self, bullet: Shot):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Use bullet's velocity as base direction
        base_velocity = bullet.velocity
        if base_velocity.length() == 0:
            base_velocity = pygame.Vector2(1, 0)  # Prevent division by zero

        # Scale velocity for smaller asteroids (make them faster)
        velocity_scale = 1 + (ASTEROID_KINDS - self.kind) * 0.5
        new_velocity_magnitude = (
            base_velocity.length() * velocity_scale
            + ASTEROID_SPLIT_SPEED_MULTIPLIER * 3
        )

        # Generate random angles within ±120° of bullet's trajectory
        angle_offset_1 = random.uniform(-120, 120)
        angle_offset_2 = random.uniform(-120, 120)

        # Calculate new velocities
        velocity_1 = (
            base_velocity.normalize().rotate(angle_offset_1) * new_velocity_magnitude
        )
        velocity_2 = (
            base_velocity.normalize().rotate(angle_offset_2) * new_velocity_magnitude
        )

        # New asteroid radius and kind
        new_radius = self.radius // 2
        new_kind = self.kind - 1

        # Spawn two smaller asteroids
        asteroid_spawn_1 = Asteroid(
            self.position.x, self.position.y, new_radius, new_kind
        )
        asteroid_spawn_1.velocity = velocity_1

        asteroid_spawn_2 = Asteroid(
            self.position.x, self.position.y, new_radius, new_kind
        )
        asteroid_spawn_2.velocity = velocity_2
