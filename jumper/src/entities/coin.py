import pygame

class Coin:
    def __init__(self, x, y, size=20):
        self.rect = pygame.Rect(x, y, size, size)
        self.collected = False

    def draw(self, surface, camera_x, camera_y):
        if not self.collected:
            pygame.draw.circle(surface, (255, 215, 0),
                               (self.rect.centerx - camera_x, self.rect.centery - camera_y), 10)
