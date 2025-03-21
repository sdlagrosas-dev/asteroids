import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        super().__init__(self.containers)
        self.spawn_timer = 0.0
        self.spawn_rate = ASTEROID_BASE_SPAWN_RATE

    def spawn(self, radius, position, velocity, kind):
        asteroid = Asteroid(position.x, position.y, radius, kind)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0

            # Spawn at a random edge
            edge = random.choice(self.edges)
            position = edge[1](random.uniform(0, 1))

            # Set a random speed within range
            speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.uniform(-30, 30))

            # Ensure the asteroid moves toward the screen
            screen_center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            to_center = (screen_center - position).normalize()

            if velocity.dot(to_center) < 0:  # If velocity moves away, flip it
                velocity = -velocity

            # Random asteroid size (kind)
            kind = random.randint(1, ASTEROID_KINDS)

            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, kind)