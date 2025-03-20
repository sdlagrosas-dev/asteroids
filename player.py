import pygame
from constants import *
import circleshape
import shot


class Player(circleshape.CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.shoot_timer = 0

    def triangle(self):
        front_vector = pygame.Vector2(0, -1).rotate(self.rotation)
        side_vector = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius
        a = self.position + front_vector * self.radius
        b = self.position - front_vector * self.radius - side_vector
        c = self.position - front_vector * self.radius + side_vector
        return [a, b, c]

    def draw(self, screen):
        super().draw(screen)

        pygame.draw.polygon(screen, color="white", points=self.triangle(), width=2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            forward = pygame.Vector2(0, -1).rotate(self.rotation)
            self.position += forward * PLAYER_SPEED * dt
        if keys[pygame.K_s]:
            backward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.position += backward * PLAYER_SPEED * dt
        if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER]:
            if self.shoot_timer <= 0:
                self.shoot()
                self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            else:
                # Shoot Cooldown
                self.shoot_timer -= dt

    def shoot(self):
        front_pos = self.triangle()[0]
        shot_projectile = shot.Shot(
            front_pos[0], front_pos[1], PLAYER_SHOT_RADIUS
        )
        shot_projectile.velocity = (
            pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        )
