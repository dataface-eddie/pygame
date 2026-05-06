import pygame

# UI menu stubs: we'll migrate the actual menu code from jumper.py later.

def main_menu(screen, menu_font, menu_option_font, WIDTH, HEIGHT):
    # Minimal blocking menu: user starts the game by pressing Enter
    running = True
    selected = 0
    options = ["Play", "Quit"]
    while running:
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
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if options[selected] == "Play":
                        return
                    else:
                        pygame.quit()
                        raise SystemExit
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)


def pause_menu():
    # Placeholder; we'll migrate full implementation later
    pass
