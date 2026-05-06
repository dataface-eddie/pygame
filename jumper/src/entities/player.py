import pygame
import math


class Player:
    def __init__(self, x, y, images=None):
        self.lives = 3
        self.coins = 0
        self.rect = pygame.Rect(x, y, 50, 50)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.images = images or []
        self.current_frame = 0
        self.frame_timer = 0
        self.facing_right = True
        self.fire_cooldown = 0

    def handle_input(self, keys, speed, jump_strength):
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -speed
        if keys[pygame.K_RIGHT]:
            self.vel.x = speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = jump_strength
        if self.vel.x > 0:
            self.facing_right = True
        elif self.vel.x < 0:
            self.facing_right = False

    def apply_gravity(self, gravity):
        self.vel.y += gravity
        if self.vel.y > 10:
            self.vel.y = 10

    def move_and_collide(self, platforms):
        # Horizontal
        self.rect.x += int(self.vel.x)
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel.x > 0:
                    self.rect.right = plat.left
                elif self.vel.x < 0:
                    self.rect.left = plat.right

        # Vertical
        self.rect.y += int(self.vel.y)
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel.y > 0:
                    self.rect.bottom = plat.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = plat.bottom
                    self.vel.y = 0
        if self.rect.top < 0:
            self.rect.top = 0

        # World bounds are handled by caller

    def update(self, platforms, enemies, player_fireballs, coins, constants, sounds=None):
        # constants: dict with keys SPEED, JUMP_STRENGTH, GRAVITY, WORLD_HEIGHT
        keys = pygame.key.get_pressed()
        self.handle_input(keys, constants.get('SPEED', 5), constants.get('JUMP_STRENGTH', -15))
        self.apply_gravity(constants.get('GRAVITY', 0.5))
        self.move_and_collide(platforms)

        # Animate
        if self.vel.x != 0 and self.images:
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.frame_timer = 0
        else:
            self.current_frame = 0

        # Kill plane
        if self.rect.top > constants.get('WORLD_HEIGHT', 5000) + 200:
            self.lives -= 1
            if self.lives <= 0:
                if sounds and sounds.get('death'):
                    try:
                        sounds.get('death').play()
                    except Exception:
                        pass
                # Caller should handle fade/wait/respawn
            else:
                # non-fatal death handled by caller
                pass

        # Enemy collisions
        for enemy in list(enemies):
            if self.rect.colliderect(enemy.rect):
                self.lives -= 1
                # caller handles respawn/game over
                break

        # Fireball collisions
        for enemy in enemies:
            for fireball in list(enemy.fireballs):
                if self.rect.colliderect(fireball.rect):
                    self.lives -= 1
                    try:
                        enemy.fireballs.remove(fireball)
                    except ValueError:
                        pass
                    if self.lives <= 0:
                        if sounds and sounds.get('death'):
                            try:
                                sounds.get('death').play()
                            except Exception:
                                pass
                    return

        # Fire cooldown decrement
        if hasattr(self, 'fire_cooldown') and self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # Coin collection
        for coin in coins:
            if not coin.collected and self.rect.colliderect(coin.rect):
                coin.collected = True
                self.coins += 1
                if sounds and sounds.get('coin'):
                    try:
                        sounds.get('coin').play()
                    except Exception:
                        pass

    def draw(self, surface, camera_x, camera_y, fonts=None):
        img = None
        if self.images:
            img = self.images[self.current_frame]
            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)
            surface.blit(img, (self.rect.x - camera_x, self.rect.y - camera_y))
        # HUD
        if fonts and 'small' in fonts:
            lives_text = fonts['small'].render(f"Lives: {self.lives}", True, (255, 255, 255))
            coins_text = fonts['small'].render(f"Coins: {self.coins}", True, (255, 255, 255))
            surface.blit(lives_text, (20, 15))
            surface.blit(coins_text, (180, 15))

    def respawn(self, start_pos=(100, 0)):
        self.rect.topleft = start_pos
        self.vel = pygame.Vector2(0, 0)
        self.coins = 0

    def shoot(self):
        # Return a Fireball instance fired from the player
        try:
            from .fireball import Fireball
        except Exception:
            # fallback local definition (shouldn't happen after migration)
            return None
        direction = 1 if self.facing_right else -1
        fb = Fireball(self.rect.centerx, self.rect.centery, direction, is_player=True)
        return fb
