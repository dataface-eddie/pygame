import pygame
import sys
import os
import random
import pygame.mixer
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.world import place_coins_on_platforms

# Init
pygame.init()
#menu fonts
menu_font = pygame.font.SysFont("Arial", 64)
menu_option_font = pygame.font.SysFont("Arial", 48)
#fonts
font_small = pygame.font.SysFont("Arial", 32)
font_large = pygame.font.SysFont("Arial", 72, bold=True)
# Screen
WIDTH, HEIGHT = 1600, 800 #800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")
# World dimensions
WORLD_WIDTH = 10000
WORLD_HEIGHT = 5000

fireballs = []

# Initialize the mixer
pygame.mixer.init()

# Centralized asset loading
from src.assets import AssetManager
am = AssetManager()

# Images
am.load_image('background', 'images/background.png')
background_image = am.get_image('background')
if background_image:
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Sounds (moved into assets/audio/)
coin_sound = am.load_sound('coin', 'audio/coin_collect.mp3')
death_by_fire_ball_sound = am.load_sound('death', 'audio/death_by_fire_ball.mp3')
monster_roar_sound = am.load_sound('monster_roar', 'audio/monster_roar.mp3')
dramatic_synth_echo_sound = am.load_sound('dramatic_echo', 'audio/dramatic_synth_echo.mp3')
game_over_music = am.load_sound('game_over', 'audio/game_over_music.mp3')
jump_sound = am.load_sound('jump', 'audio/jump_sound.mp3')
fireball_sound_1 = am.load_sound('fireball1', 'audio/fireball_sound_1.mp3')
fireball_sound_2 = am.load_sound('fireball2', 'audio/fireball_sound_2.mp3')
fireball_hit_enemy_sound = am.load_sound('fireball_hit', 'audio/steam_hissing.mp3')

def main_menu():
    selected = 0
    options = ["Play", "Quit"]

    while True:
        screen.fill((0, 0, 0))

        title_text = menu_font.render("Jumper", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            option_text = menu_option_font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 250 + i * 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Play":
                        # Go to character selection and return the chosen frames
                        return character_select()
                    elif options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()

def pause_menu():
    paused = True
    selected = 0
    options = ["Resume", "Quit to Main Menu"]

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)  # Semi-transparent
    overlay.fill((0, 0, 0))  # Black overlay

    while paused:
        screen.blit(overlay, (0, 0))  # Transparent overlay

        pause_text = menu_font.render("Paused", True, (255, 255, 255))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            option_text = menu_option_font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 250 + i * 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Resume":
                        return
                    elif options[selected] == "Quit to Main Menu":
                        main_menu()
                        return

def load_enemy_images():
    images = []
    for i in range(6):
        key = f'enemy_{i}'
        am.load_image(key, f'images/enemy_frames/enemy_{i}.png')
        img = am.get_image(key)
        if img:
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
        key = f'charles_walk_{i}'
        am.load_image(key, f'images/charles/charles_walk_{i}.png')
        img = am.get_image(key)
        if img:
            img = pygame.transform.scale(img, (50, 50))
            images.append(img)
    return images

def load_images_for_character(folder, frame_count=None, size=(50,50)):
    """Load PNG frames from `assets/images/<folder>/`.

    This is tolerant to different naming schemes (e.g. `car_car_1.png`).
    If `frame_count` is None, load all PNGs found.
    """
    images = []
    rel_dir = f'images/{folder}'
    full_dir = am._full_path(rel_dir)
    if not os.path.isdir(full_dir):
        return []
    # Collect png files sorted alphabetically (preserves numeric order if named that way)
    files = sorted([f for f in os.listdir(full_dir) if f.lower().endswith('.png')])
    if not files:
        return []
    if frame_count is None:
        frame_count = len(files)
    for fname in files[:frame_count]:
        key = f'{folder}_{fname}'
        rel_path = f'{rel_dir}/{fname}'
        try:
            am.load_image(key, rel_path)
        except Exception:
            continue
        img = am.get_image(key)
        if img:
            img = pygame.transform.scale(img, size)
            images.append(img)
    return images

def character_select():
    selected = 0
    options = ["Charles", "Carlisle"]

    while True:
        screen.fill((0, 0, 0))
        title_text = menu_font.render("Choose Character", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            option_text = menu_option_font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 250 + i * 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    choice = options[selected].lower()
                    # Attempt to load character frames; fall back to Charles if none found
                    imgs = load_images_for_character(choice)
                    if not imgs:
                        imgs = load_images_for_character('charles')
                    return imgs

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
        # Draw HUD background bar (top of screen)
        hud_height = 60
        pygame.draw.rect(screen, (0, 0, 0, 128), (0, 0, WIDTH, hud_height))  # semi-transparent black
        pygame.display.update()
        clock.tick(60)



# Place platforms with absolute Y values in the tall world
base = WORLD_HEIGHT - 40  # ground level
platforms = [
    pygame.Rect(0, WORLD_HEIGHT - 40, 700, 40),       # Ground 1
    pygame.Rect(800, WORLD_HEIGHT - 100, 200, 20),    # Platform 1
    pygame.Rect(1100, WORLD_HEIGHT - 200, 200, 20),   # Platform 2
    pygame.Rect(1400, WORLD_HEIGHT - 300, 200, 20),   # Platform 3
    pygame.Rect(1700, WORLD_HEIGHT - 400, 200, 20),   # Platform 4
    pygame.Rect(2000, WORLD_HEIGHT - 500, 200, 20),   # Platform 5
    pygame.Rect(2300, WORLD_HEIGHT - 600, 200, 20),
    pygame.Rect(2600, WORLD_HEIGHT - 40, 8000, 40),   # Ground 2
]

def regenerate_enemies():
    return [
        create_enemy_on_platform(platforms[1], enemy_images),
        create_enemy_on_platform(platforms[2], enemy_images),
        create_enemy_on_platform(platforms[3], enemy_images),
        create_enemy_on_platform(platforms[4], enemy_images),
        create_enemy_on_platform(platforms[5], enemy_images),
        create_enemy_on_platform(platforms[6], enemy_images),
        create_enemy_on_platform(platforms[7], enemy_images),
        create_enemy_on_platform(platforms[7], enemy_images),
    ]
enemies = regenerate_enemies()

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  # Size of the coin
        self.collected = False

    def draw(self, surface, camera_x, camera_y):
        if not self.collected:
            pygame.draw.circle(surface, (255, 215, 0),  # Gold color
                               (self.rect.centerx - camera_x, self.rect.centery - camera_y), 10)

coins = []

coins = place_coins_on_platforms(platforms, random)

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

# Prepare for player creation after character selection
player_fireballs = []

# Show main menu and get selected character frames
walk_images = main_menu()
player = Player(100, WORLD_HEIGHT - 150, images=walk_images)
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
    # Draw HUD background bar (top of screen)
    hud_height = 60
    pygame.draw.rect(screen, (0, 0, 0, 128), (0, 0, WIDTH, hud_height))  # semi-transparent black

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu()

    # Handle continuous key input (shooting)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        # Respect player's internal cooldown
        if getattr(player, 'fire_cooldown', 0) <= 0:
            fb = player.shoot()
            if fb:
                player_fireballs.append(fb)
                player.fire_cooldown = 20
                try:
                    fireball_sound_1.play()
                except Exception:
                    pass

    # Update player
    # Update player
    prev_lives = player.lives
    constants = {
        'SPEED': SPEED,
        'JUMP_STRENGTH': JUMP_STRENGTH,
        'GRAVITY': GRAVITY,
        'WORLD_HEIGHT': WORLD_HEIGHT,
    }
    sounds = {'coin': coin_sound, 'death': death_by_fire_ball_sound}
    player.update(platforms, enemies, player_fireballs, coins, constants, sounds=sounds)
    if player.lives < prev_lives:
        # Player lost a life — handle respawn or game over
        if player.lives <= 0:
            fade_screen(screen, camera_x, camera_y, message="GAME OVER")
            wait_for_restart()
            player.lives = 3
            player.respawn((100, WORLD_HEIGHT - 150))
            # Reset enemies and coins on respawn
            for e in enemies:
                try:
                    e.fireballs.clear()
                except Exception:
                    pass
            enemies = regenerate_enemies()
            coins = place_coins_on_platforms(platforms, random)
            fade_screen(screen, camera_x, camera_y, fade_in=True)
        else:
            fade_screen(screen, camera_x, camera_y, message="YOU DIED")
            pygame.time.delay(500)
            player.respawn((100, WORLD_HEIGHT - 150))
            for e in enemies:
                try:
                    e.fireballs.clear()
                except Exception:
                    pass
            enemies = regenerate_enemies()
            coins = place_coins_on_platforms(platforms, random)
            fade_screen(screen, camera_x, camera_y, fade_in=True)

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
                    fireball_hit_enemy_sound.play()
                    enemies.remove(enemy)
                    if fb in player_fireballs:
                        player_fireballs.remove(fb)
                    break
                    
    # Draw player fireballs
    for fb in player_fireballs:
        fb.draw(screen, camera_x, camera_y)
    # Draw coins
    for coin in coins:
        coin.draw(screen, camera_x, camera_y)

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