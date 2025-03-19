import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from scoresystem import ScoreSystem
from button import Button
from shot import Shot


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_CLOCK = pygame.time.Clock()
BG = pygame.image.load("assets/Background.png")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    # Delta time
    dt = 0

    # Sprite Groups
    asteroid_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    # Class Containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroid_group)
    AsteroidField.containers = updatable
    Shot.containers = (updatable, drawable, shot_group)
    ScoreSystem.containers = (updatable, drawable)

    # Initialized Instances
    player_1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    score_system = ScoreSystem()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        SCREEN.fill(color="black")

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroid_group:
            if asteroid.is_in_collision(player_1):
                print("Game Over!")
                return

            for bullet in shot_group:
                if asteroid.is_in_collision(bullet):
                    asteroid.split(bullet)
                    score_system.add_score(asteroid)
                    bullet.kill()

        for obj in drawable:
            obj.draw(SCREEN)

        pygame.display.flip()

        dt = GAME_CLOCK.tick(60) / 1000
        pygame.display.update()


def game_over():
    pass


def main():

    pygame.init()
    pygame.display.set_caption("Asteroids")


    while True:
        SCREEN.blit(BG, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Asteroids", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                    play()
                if OPTIONS_BUTTON.checkForInput(menu_mouse_pos):
                    pass
                    # options()
                if QUIT_BUTTON.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main()
