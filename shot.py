import pygame
import circleshape
from constants import *


class Shot(circleshape.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        super().draw(screen)

        pygame.draw.circle(
            screen, color="blue", center=self.position, radius=self.radius, width=2
        )

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        super().update(dt)

        self.position += self.velocity * dt
