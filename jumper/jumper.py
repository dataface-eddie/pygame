import pygame
import sys
import os
import random

# Init
pygame.init()
#fonts
font_small = pygame.font.SysFont("Arial", 32)
font_large = pygame.font.SysFont("Arial", 72, bold=True)
# Screen
WIDTH, HEIGHT = 1600, 800 #800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")
# World dimensions
WORLD_WIDTH = 2000
WORLD_HEIGHT = 5000
background_image = pygame.image.load("background.png").convert()
background_image = pygame.transform.scale(background_image, (800, 600))
fireballs = []

def load_enemy_images():
    images = []
    for i in range(6):
        img = pygame.image.load(f"enemy_frames/enemy_{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (64, 64))  # Resize to 64x64
        images.append(img)
    return images

enemy_images = load_enemy_images()

def create_enemy_on_platform(plat, images):
    patrol_min_x = plat.x
    patrol_max_x = plat.x + plat.width - 64  # Subtract enemy width
    start_x = (patrol_min_x + patrol_max_x) // 2
    y = plat.y - 64  # On top of platform
    speed = random.choice([-2, 2])
    return Enemy(start_x, y, 64, 64, speed, images, patrol_min_x, patrol_max_x)

def load_player_images():
    images = []
    for i in range(4):  # Assuming 4 walking frames
        img = pygame.image.load(f"sprites/charles/charles_walk_{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (50, 50))
        images.append(img)
    return images

# Fade Screen Function
def fade_screen(surface, camera_x, camera_y, fade_in=False, speed=10, message=None):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 256, speed) if not fade_in else reversed(range(0, 256, speed)):
        fade.set_alpha(alpha)
        surface.fill((0, 0, 0))
        draw_world(surface, camera_x, camera_y)

        if message:
            text_surf = font_large.render(message, True, (200, 0, 0))  # Red
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            surface.blit(text_surf, text_rect)

        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(15)

def draw_parallax_background(surface, camera_x, camera_y, bg_image):
    parallax_speed = 0.2  # smaller = slower movement (farther away)
    bg_x = -camera_x * parallax_speed
    bg_y = -camera_y * parallax_speed

    for x in range(-WIDTH, WORLD_WIDTH, bg_image.get_width()):
        for y in range(-HEIGHT, WORLD_HEIGHT, bg_image.get_height()):
            surface.blit(bg_image, (x + bg_x, y + bg_y))

def draw_world(surface, camera_x, camera_y):
    draw_parallax_background(surface, camera_x, camera_y, background_image)  # <--- Add this first
    player.draw(surface, camera_x, camera_y)
    for plat in platforms:
        offset_rect = pygame.Rect(
            plat.x - camera_x,
            plat.y - camera_y,
            plat.width,
            plat.height
        )
        pygame.draw.rect(surface, GREEN, offset_rect)
    

def wait_for_restart():
    text1 = font_large.render("GAME OVER", True, (200, 0, 0))
    text2 = font_small.render("Press R to Restart", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

        screen.fill(BLACK)
        screen.blit(text1, text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(text2, text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        pygame.display.update()
        clock.tick(60)
    
class Enemy:
    def __init__(self, x, y, width, height, speed, images, patrol_min_x, patrol_max_x):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.start_x = patrol_min_x
        self.end_x = patrol_max_x
        self.images = images
        self.current_frame = 0
        self.frame_timer = 0
        self.facing_right = speed > 0
        self.fireball_timer = random.randint(60, 180)  # Random fire delay
        self.fireballs = []

    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= self.start_x or self.rect.x >= self.end_x:
            self.speed *= -1
            self.facing_right = not self.facing_right

        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_timer = 0

        # Animate
        self.frame_timer += 1
        if self.frame_timer >= 6:  # Adjust to change speed
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_timer = 0
        # Fireball logic
        self.fireball_timer -= 1
        if self.fireball_timer <= 0:
            direction = 1 if self.facing_right else -1
            fireball = Fireball(self.rect.centerx, self.rect.centery, direction)
            self.fireballs.append(fireball)
            self.fireball_timer = random.randint(120, 240)  # Reset timer

        # Update fireballs
        for f in self.fireballs[:]:
            f.update()
            if f.lifetime <= 0:
                self.fireballs.remove(f)

    def draw(self, surface, camera_x, camera_y):
        img = self.images[self.current_frame]
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, (self.rect.x - camera_x, self.rect.y - camera_y))
        # Existing image drawing...
        for f in self.fireballs:
            f.draw(surface, camera_x, camera_y)

# Place platforms with absolute Y values in the tall world
base = WORLD_HEIGHT - 40  # ground level
platforms = [
    pygame.Rect(0, WORLD_HEIGHT - 40, 700, 40),       # Ground
    pygame.Rect(800, WORLD_HEIGHT - 100, 200, 20),    # Platform 1
    pygame.Rect(1100, WORLD_HEIGHT - 200, 200, 20),   # Platform 2
    pygame.Rect(1400, WORLD_HEIGHT - 300, 200, 20),   # Platform 3
    pygame.Rect(1700, WORLD_HEIGHT - 400, 200, 20),   # Platform 4
]

def regenerate_enemies():
    return [
        create_enemy_on_platform(platforms[1], enemy_images),
        create_enemy_on_platform(platforms[2], enemy_images),
        create_enemy_on_platform(platforms[3], enemy_images),
        create_enemy_on_platform(platforms[4], enemy_images),
    ]
enemies = regenerate_enemies()
coins = []

def place_coins_on_platforms():
    for plat in platforms[1:]:  # skip ground
        # Place 1–2 coins randomly on the platform
        for _ in range(random.randint(1, 2)):
            x = random.randint(plat.left + 10, plat.right - 30)
            y = plat.top - 25  # slightly above the platform
            coins.append(Coin(x, y))

place_coins_on_platforms()



walk_images = load_player_images()
# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors in RGB format
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (211, 211, 211)
SLIGHTLY_LIGHTER_GREY = (191, 191, 191)

# Physics
GRAVITY = 0.5
JUMP_STRENGTH = -15
SPEED = 5

player_fireballs = []
class Player:
    def __init__(self, images):
        self.lives = 3
        self.coins = 0 
        self.rect = pygame.Rect(100, WORLD_HEIGHT - 150, 50, 50)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.images = images
        self.current_frame = 0
        self.frame_timer = 0
        self.facing_right = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -SPEED
        if keys[pygame.K_RIGHT]:
            self.vel.x = SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = JUMP_STRENGTH
        if self.vel.x > 0:
            self.facing_right = True
        elif self.vel.x < 0:
            self.facing_right = False

        if keys[pygame.K_f]:
            self.shoot()

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > 10:
            self.vel.y = 10

    def move_and_collide(self, platforms):
        # Horizontal movement
        self.rect.x += self.vel.x
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel.x > 0:
                    self.rect.right = plat.left
                elif self.vel.x < 0:
                    self.rect.left = plat.right

        # Vertical movement
        self.rect.y += self.vel.y
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

        
        # Prevent player from moving beyond world boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide(platforms)

        # Animate if moving
        if self.vel.x != 0:
            self.frame_timer += 1
            if self.frame_timer >= 6:  # Adjust for speed
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.frame_timer = 0
        else:
            self.current_frame = 0  # Idle frame
        if self.rect.top > WORLD_HEIGHT + 200:  # Kill plane
            self.lives -= 1
            print(f"You Died. Lives left: {self.lives}")
            if self.lives <= 0:
                fade_screen(screen, camera_x, camera_y, message="GAME OVER")
                wait_for_restart()
                self.lives = 3
                self.respawn()
                fade_screen(screen, camera_x, camera_y, fade_in=True)
            else:
                fade_screen(screen, camera_x, camera_y, message="YOU DIED")
                pygame.time.delay(500)
                self.respawn()
                fade_screen(screen, camera_x, camera_y, fade_in=True)
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.lives -= 1
                print(f"Hit by enemy! Lives left: {self.lives}")
                if self.lives <= 0:
                    fade_screen(screen, camera_x, camera_y, message="GAME OVER")
                    wait_for_restart()
                    self.lives = 3
                else:
                    fade_screen(screen, camera_x, camera_y, message="YOU DIED")
                self.respawn()
                fade_screen(screen, camera_x, camera_y, fade_in=True)
                break
        for enemy in enemies:
            for fireball in enemy.fireballs:
                if self.rect.colliderect(fireball.rect):
                    self.lives -= 1
                    print(f"Hit by fireball! Lives left: {self.lives}")
                    enemy.fireballs.remove(fireball)
                    if self.lives <= 0:
                        fade_screen(screen, camera_x, camera_y, message="GAME OVER")
                        wait_for_restart()
                        self.lives = 3
                        self.respawn()
                        fade_screen(screen, camera_x, camera_y, fade_in=True)
                    else:
                        fade_screen(screen, camera_x, camera_y, message="YOU DIED")
                        pygame.time.delay(500)
                        self.respawn()
                        fade_screen(screen, camera_x, camera_y, fade_in=True)
                    return  # Prevent multiple hits at once
        if hasattr(self, "fire_cooldown") and self.fire_cooldown > 0:
            self.fire_cooldown -= 1

    def draw(self, surface, camera_x, camera_y):
        img = self.images[self.current_frame]
        # Draw lives counter in top-left
        lives_text = font_small.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(lives_text, (20, 20))
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, (self.rect.x - camera_x, self.rect.y - camera_y))
    
    # Player Respawn
    def respawn(self):
        global enemies
        for enemy in enemies:
            enemy.fireballs.clear()
        enemies = regenerate_enemies()
        self.rect.topleft = (100, WORLD_HEIGHT - 150)
        self.vel = pygame.Vector2(0, 0)

    def shoot(self):
        if not hasattr(self, "fire_cooldown"):
            self.fire_cooldown = 0
        if self.fire_cooldown <= 0:
            direction = 1 if self.facing_right else -1
            fb = Fireball(self.rect.centerx, self.rect.centery, direction, is_player=True)
            player_fireballs.append(fb)
            self.fire_cooldown = 20  # cooldown in frames

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  # Size of the coin
        self.collected = False

    def draw(self, surface, camera_x, camera_y):
        if not self.collected:
            pygame.draw.circle(surface, (255, 215, 0),  # Gold color
                               (self.rect.centerx - camera_x, self.rect.centery - camera_y), 10)

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

player = Player(walk_images)
camera_x = 0
camera_y = 0
# Ensure camera_x and camera_y are within bounds
camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))
camera_y = max(0, min(camera_y, WORLD_HEIGHT - HEIGHT))
# Game loop
while True:
    draw_world(screen, camera_x, camera_y)
    camera_x = player.rect.centerx - WIDTH // 2
    camera_y = player.rect.centery - HEIGHT // 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player
    player.update(platforms)

    # Update and draw enemies
    for enemy in enemies:
        enemy.update()
        enemy.draw(screen, camera_x, camera_y)

    # Update player fireballs
    for fb in player_fireballs[:]:
        fb.update()
        if fb.lifetime <= 0:
            player_fireballs.remove(fb)
        else:
            # Check collision with enemies
            for enemy in enemies[:]:
                if fb.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    if fb in player_fireballs:
                        player_fireballs.remove(fb)
                    break
                    
    # Draw player fireballs
    for fb in player_fireballs:
        fb.draw(screen, camera_x, camera_y)

    # Draw player (after enemies so it appears in front)
    player.draw(screen, camera_x, camera_y)

    for plat in platforms:
        offset_rect = pygame.Rect(
        plat.x - camera_x,
        plat.y - camera_y,
        plat.width,
        plat.height
)
        pygame.draw.rect(screen, GREEN, offset_rect)

    pygame.display.flip()
    clock.tick(FPS)