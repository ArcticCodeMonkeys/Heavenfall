import pygame

def draw_unit(screen, demon, x, y, w, h):
    demon_image = pygame.image.load(f'assets/{demon.name}.jpg')
    demon_image = pygame.transform.smoothscale(demon_image, (w, h))
    screen.blit(demon_image, (x, y))

def draw_board(screen, player, enemies):
    screen.fill((0, 0, 0))  # Clear screen with black background
    background = pygame.image.load(f'assets/heaven.jpg')
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    # Dimensions for drawing
    unit_width = 188
    unit_height = 262
    padding = 10  # Space between units

    # Calculate total width of player's demons
    total_player_width = len(player.board) * unit_width + (len(player.board) - 1) * padding
    player_start_x = (screen.get_width() - total_player_width) // 2  # Center horizontally

    # Draw player demons on board
    for idx, demon in enumerate(player.board):
        draw_unit(screen, demon, player_start_x + idx * (unit_width + padding), 500, unit_width, unit_height)

    # Calculate total width of enemies
    total_enemy_width = len(enemies) * unit_width + (len(enemies) - 1) * padding
    enemy_start_x = (screen.get_width() - total_enemy_width) // 2  # Center horizontally

    # Draw enemy celestials on the other side
    for idx, enemy in enumerate(enemies):
        draw_unit(screen, enemy, enemy_start_x + idx * (unit_width + padding), 100, unit_width, unit_height)

    pygame.display.update()

