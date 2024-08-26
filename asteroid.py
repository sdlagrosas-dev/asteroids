import pygame
import circleshape


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
