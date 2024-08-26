
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    dt = 0

    # Sprite Groups    
    asteroid_group = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    # Class Containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroid_group)
    AsteroidField.containers = (updatable)

    # Initialized Instances
    player_1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill(color="black")

        for obj in updatable:
            obj.update(dt)

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = game_clock.tick(60)/1000


if __name__ == '__main__':
    main()
