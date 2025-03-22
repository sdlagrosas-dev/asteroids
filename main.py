import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from scoresystem import ScoreSystem
from button import Button
from shot import Shot
from effects import EffectManager


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
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9)
    asteroid_field = AsteroidField()
    score_system = ScoreSystem()
    effect_manager = EffectManager()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over(score_system)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        SCREEN.fill(color="black")

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroid_group:
            if asteroid.is_in_collision(player):
                asteroid.split(player, effect_manager)

                if player.immunity_timer <= 0:
                    player.take_damage(effect_manager)
                
                    if player.health <= 0:
                        game_over(score_system)

            for asteroid_2 in asteroid_group:
                if asteroid != asteroid_2 and asteroid.is_in_collision(asteroid_2):
                    asteroid.handle_collision(asteroid_2)

            for bullet in shot_group:
                if asteroid.is_in_collision(bullet):
                    asteroid.take_damage(bullet, effect_manager, score_system)
                    bullet.kill()

        effect_manager.update(dt)
        effect_manager.draw(SCREEN)

        for obj in drawable:
            obj.draw(SCREEN)

        pygame.display.flip()

        dt = GAME_CLOCK.tick(60) / 1000
        pygame.display.update()


def pause():

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(
        (0, 0, 0, 196)
    )  # Custom background: light gray with about 50% transparency
    SCREEN.blit(overlay, (0, 0))

    while True:
        GAME_CLOCK.tick(60)
        menu_mouse_pos = pygame.mouse.get_pos()

        pause_text = get_font(80).render("Paused", True, (186, 174, 165))
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        # The main button
        resume_button = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, 300),
            text_input="Resume",
            font=get_font(55),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        retry_button = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, 450),
            text_input="Retry",
            font=get_font(55),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        quit_button = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, 600),
            text_input="Quit",
            font=get_font(55),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        # Put the text on top of everything
        SCREEN.blit(pause_text, pause_rect)

        for button in [resume_button, retry_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(menu_mouse_pos):
                    return
                if retry_button.checkForInput(menu_mouse_pos):
                    play()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def game_over(score_system: ScoreSystem):

    final_score = score_system.score

    while True:
        SCREEN.blit(BG_MENU, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        game_over_text = get_font(80).render("Game Over!", True, "#b68f40")
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        score_text = get_font(30).render(f"Score:{final_score}", True, "White")
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))

        SCREEN.blit(game_over_text, game_over_rect)
        SCREEN.blit(score_text, score_rect)

        retry_button = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, 400),
            text_input="Retry",
            font=get_font(55),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        quit_button = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, 550),
            text_input="Quit",
            font=get_font(55),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        for button in [quit_button, retry_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.checkForInput(menu_mouse_pos):
                    play()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main():

    pygame.init()
    pygame.display.set_caption("Asteroids")

    while True:
        SCREEN.blit(BG_MENU, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Asteroids", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        play_button = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, 250),
            text_input="PLAY",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        options_button = Button(
            image=pygame.image.load("assets/Options Rect.png"),
            pos=(SCREEN_WIDTH // 2, 400),
            text_input="OPTIONS",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        quit_button = Button(
            image=pygame.image.load("assets/Quit Rect.png"),
            pos=(SCREEN_WIDTH // 2, 550),
            text_input="QUIT",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    pass
                    # options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
