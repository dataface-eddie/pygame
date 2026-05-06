import pygame
import random


class Enemy:
    def __init__(self, x, y, width, height, speed, images, patrol_min_x, patrol_max_x):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.start_x = patrol_min_x
        self.end_x = patrol_max_x
        self.images = images or []
        self.current_frame = 0
        self.frame_timer = 0
        self.facing_right = speed > 0
        self.fireball_timer = random.randint(60, 180)
        self.fireballs = []

    def update(self):
        # Patrol
        self.rect.x += self.speed
        if self.rect.x <= self.start_x or self.rect.x >= self.end_x:
            self.speed *= -1
            self.facing_right = not self.facing_right

        # Animate
        self.frame_timer += 1
        if self.frame_timer >= 6 and self.images:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_timer = 0

        # Fireball logic
        self.fireball_timer -= 1
        if self.fireball_timer <= 0:
            try:
                from .fireball import Fireball
                direction = 1 if self.facing_right else -1
                fb = Fireball(self.rect.centerx, self.rect.centery, direction)
                self.fireballs.append(fb)
            except Exception:
                pass
            self.fireball_timer = random.randint(120, 240)

        # Update fireballs
        for f in self.fireballs[:]:
            f.update()
            if getattr(f, 'lifetime', 0) <= 0:
                try:
                    self.fireballs.remove(f)
                except ValueError:
                    pass

    def draw(self, surface, camera_x, camera_y):
        if self.images:
            img = self.images[self.current_frame]
            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)
            surface.blit(img, (self.rect.x - camera_x, self.rect.y - camera_y))
        for f in self.fireballs:
            try:
                f.draw(surface, camera_x, camera_y)
            except Exception:
                pass
