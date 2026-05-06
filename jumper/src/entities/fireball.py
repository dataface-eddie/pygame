import pygame

class Fireball:
    def __init__(self, x, y, direction, is_player=False):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.speed = 6 * direction
        self.lifetime = 180
        self.is_player = is_player

    def update(self):
        self.rect.x += self.speed
        self.lifetime -= 1

    def draw(self, surface, camera_x, camera_y):
        offset_rect = pygame.Rect(
            self.rect.x - camera_x,
            self.rect.y - camera_y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.circle(surface, (255, 100, 0), offset_rect.center, 8)
