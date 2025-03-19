import pygame
from constants import get_font


class ScoreSystem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(*self.containers)
        self.destroyed_count = 0
        self.score = 0

    def draw(self, screen):
        label = get_font(16).render(f"Score:{self.score}", True, (255, 255, 255))
        screen.blit(label, (10, 20))

        destroyed_count_label = get_font(16).render(
            f"Destroyed:{self.destroyed_count}",
            True,
            (255, 255, 255),
        )
        screen.blit(destroyed_count_label, (10, 40))

    def update(self, dt):
        pass

    def add_score(self, asteroid):
        kind = asteroid.kind
        add_score = {
            1: 10,
            2: 20,
            3: 50,
        }.get(kind, 0)
        self.score += add_score
        self.destroyed_count += 1
