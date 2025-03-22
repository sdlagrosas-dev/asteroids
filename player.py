import pygame
from constants import *
import circleshape
import shot

# Load and scale heart image once (not every frame)
HEART_IMG = pygame.image.load("assets/Heart.png")
# Scale the heart image to a reasonable size (adjusted for screen dimensions)
HEART_SCALE_FACTOR = 0.025  # Adjust this to fit properly
HEART_SIZE = (int(HEART_IMG.get_width() * HEART_SCALE_FACTOR), int(HEART_IMG.get_height() * HEART_SCALE_FACTOR))

HEART_IMG = pygame.transform.scale(HEART_IMG, HEART_SIZE)  # Scale once


class Player(circleshape.CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.shoot_timer = 0
        self.health = 3
        self.immunity_timer = 0

    def triangle(self):
        """Returns the three vertices of the player's triangle (ship)."""
        front_vector = pygame.Vector2(0, -1).rotate(self.rotation)
        side_vector = pygame.Vector2(0, 1).rotate(self.rotation + 90) * (self.radius / 1.5)
        a = self.position + front_vector * self.radius
        b = self.position - front_vector * self.radius - side_vector
        c = self.position - front_vector * self.radius + side_vector
        return [a, b, c]

    def draw(self, screen):
        """Draws the player and health UI."""
        super().draw(screen)
        pygame.draw.polygon(screen, color="white", points=self.triangle(), width=2)

        # Draw health UI (hearts)
        for i in range(self.health):
            screen.blit(HEART_IMG, (SCREEN_WIDTH - (HEART_SIZE[0] * (i + 1)), 10))

    def rotate(self, dt):
        """Rotates the player based on turn speed."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        """Handles movement, shooting cooldown, and screen wrapping."""
        if self.immunity_timer > 0:
            self.immunity_timer -= dt  # Reduce immunity timer
        
        # Player movement and shooting logic
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        movement_vector = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            movement_vector += pygame.Vector2(0, -1).rotate(self.rotation)
        if keys[pygame.K_s]:
            movement_vector += pygame.Vector2(0, 1).rotate(self.rotation)

        # Apply movement
        self.position += movement_vector * PLAYER_SPEED * dt

        # Shooting logic
        if keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER]:
            if self.shoot_timer <= 0:
                self.shoot()
                self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            else:
                self.shoot_timer -= dt

        # Screen Wrapping (Toroidal Space)
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

    def shoot(self):
        """Shoots a projectile from the front of the player's ship."""
        front_pos = self.triangle()[0]
        shot_projectile = shot.Shot(front_pos.x, front_pos.y, PLAYER_SHOT_RADIUS)
        shot_projectile.velocity = (
            pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        )

    def take_damage(self, effect_manager):
        """Reduces player health and grants temporary immunity"""
        if self.immunity_timer > 0:
            return  # Player is still immune, ignore damage

        self.health -= 1
        self.immunity_timer = 5.0  # Start immunity

        # Attach immunity effect to player (so it follows the player)
        effect_manager.add_effect(self.position, self.radius, 5.0, "immunity", target=self)
