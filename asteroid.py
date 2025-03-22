import random
import pygame
import circleshape
from constants import *


class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius, kind):
        super().__init__(x, y, radius)
        self.edges = self.generate_edges(15)
        self.kind = kind
        self.health = int(kind * 1.5)

    def generate_edges(self, n):
        rand_angles = random.sample(range(0, 360, max((360 // n) - (n // 2), 1)), n)
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

        pygame.draw.polygon(screen, color=(128, 128, 128), points=edge_update)
        pygame.draw.polygon(screen, color=(144, 12, 63), points=edge_update, width=3)

    def update(self, dt):
        super().update(dt)

        self.position += self.velocity * dt

        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH

        if self.position.y < -self.radius * 3 or self.position.y > SCREEN_HEIGHT + self.radius * 3:
            self.kill()

    def split(self, other: circleshape.CircleShape, effect_manager):
        effect_manager.add_effect(self.position, self.radius, 0.5, "explosion", target=self)
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Base direction should be random, not strictly bullet-based
        base_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if base_direction.length() == 0:
            base_direction = pygame.Vector2(1, 0)  # Prevent division by zero
        base_direction = base_direction.normalize()

        # Ensure `other.velocity` is not zero (add a small random velocity if needed)
        base_velocity = other.velocity if other.velocity.length() > 0 else pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * 50

        # Scale velocity for smaller asteroids
        velocity_scale = 1 + (ASTEROID_KINDS - self.kind) * 0.2
        new_velocity_magnitude = base_velocity.length() * velocity_scale

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
            delta_pos = pygame.Vector2(
                random.uniform(-1, 1), random.uniform(-1, 1)
            ).normalize()
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

    def take_damage(self, other, effect_manager, score_system):
        if self.health <= 0:
            self.split(other, effect_manager)
            score_system.add_score(self)
        self.health = max(0, self.health - 1)
