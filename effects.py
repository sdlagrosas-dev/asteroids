import pygame

class Effect:
    def __init__(self, position, radius, duration, effect_type, target=None):
        """Effect class for various effects animations"""
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.duration = duration
        self.effect_type = effect_type
        self.timer = 0
        self.target = target  # If target exists, effect follows it

    def update(self, dt):
        self.timer += dt
        if self.target:
            self.position = self.target.position  # Keep effect following target

    def is_expired(self):
        return self.timer >= self.duration

    def draw(self, screen):
        time_left = max(0, self.duration - self.timer)
        if self.effect_type == "immunity":
            if int(time_left * 10) % 2 == 0:  # Blinking effect
                pygame.draw.circle(screen, (255, 255, 0), self.position, self.radius*1.5, 2)  # Yellow glow

        if self.effect_type == "explosion":
            radius_shrinked = int((self.radius * 0.8) * (time_left / self.duration))
            pygame.draw.circle(screen, (255, 100, 0), self.position, radius_shrinked)
        

class EffectManager:
    def __init__(self):
        self.effects = []

    def add_effect(self, position, radius, duration, effect_type, target=None):
        self.effects.append(Effect(position, radius, duration, effect_type, target))

    def update(self, dt):
        for effect in self.effects:
            effect.update(dt)

        # Remove expired effects
        self.effects = [effect for effect in self.effects if not effect.is_expired()]

    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)
