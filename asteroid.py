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
        rand_angles = random.sample(range(0, 360, max((360//n)-(n//2), 1)), n)
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

        # Base direction should be random, not strictly bullet-based
        base_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if base_direction.length() == 0:
            base_direction = pygame.Vector2(1, 0)  # Prevent division by zero
        base_direction = base_direction.normalize()

        # Scale velocity for smaller asteroids (make them faster)
        velocity_scale = 1 + (ASTEROID_KINDS - self.kind) * 0.2
        new_velocity_magnitude = bullet.velocity.length() * velocity_scale

        # Generate **opposing** directions with significant separation
        angle_offset = random.uniform(30, 100)
        velocity_1 = base_direction.rotate(angle_offset) * new_velocity_magnitude
        velocity_2 = base_direction.rotate(-angle_offset) * new_velocity_magnitude

        # New asteroid radius and kind
        new_radius = self.radius // 2
        new_kind = self.kind - 1

        # Ensure safe spawn distance using both radius and an additional margin
        margin = new_radius * 1.2  # Increase separation factor
        position_1 = self.position + velocity_1.normalize() * (new_radius + margin)
        position_2 = self.position + velocity_2.normalize() * (new_radius + margin)

        # Spawn two smaller asteroids at offset positions
        asteroid_spawn_1 = Asteroid(position_1.x, position_1.y, new_radius, new_kind)
        asteroid_spawn_1.velocity = velocity_1

        asteroid_spawn_2 = Asteroid(position_2.x, position_2.y, new_radius, new_kind)
        asteroid_spawn_2.velocity = velocity_2

    def handle_collision(self, other):
        """Handles collision between two asteroids by adjusting their velocities and resolving overlaps."""
        if not isinstance(other, Asteroid):
            return  # Only handle asteroid-asteroid collisions

        # Compute the difference in position
        delta_pos = self.position - other.position
        distance = delta_pos.length()

        # Prevent division by zero or redundant checks
        if distance == 0:
            delta_pos = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            distance = self.radius + other.radius

        # Calculate overlap and resolve it
        overlap = (self.radius + other.radius) - distance
        if overlap > 0:
            # Move each asteroid away from each other proportionally
            correction = delta_pos.normalize() * (overlap / 2)
            self.position += correction
            other.position -= correction

        # Compute unit normal and tangent vectors
        normal = delta_pos.normalize()
        tangent = pygame.Vector2(-normal.y, normal.x)

        # Project velocities onto normal and tangent
        v1n = normal.dot(self.velocity)
        v1t = tangent.dot(self.velocity)
        v2n = normal.dot(other.velocity)
        v2t = tangent.dot(other.velocity)

        # Swap the normal velocity components (elastic collision)
        v1n, v2n = v2n, v1n

        # Reconstruct velocities
        self.velocity = (normal * v1n) + (tangent * v1t)
        other.velocity = (normal * v2n) + (tangent * v2t)
