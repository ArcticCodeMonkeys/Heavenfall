import pygame
import math

UNIT_WIDTH = 120
UNIT_HEIGHT = 172
ENEMY_WIDTH = 180
ENEMY_HEIGHT = 256
PADDING = 10
ANIMATION_SPEED = 15  # Adjust this for faster/slower animation
ARROW_COLOUR = (255, 0, 0)
ARROW_WIDTH = 10

def draw_unit(screen, unit, x, y, w, h):
    from demon import Demon
    from celestial import Celestial
    screen.blit(unit.boardImg, (x, y))
    if type(unit) is Demon or unit.name != 'deck':
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"{unit.hp}/{str(unit.hpMax)}", True, (255, 0, 0))
        if type(unit) is Demon:
            screen.blit(hp_text, (x + w - PADDING - 24, y + h - 34))
        else:
            screen.blit(hp_text, (x + w - PADDING - 44, y + h - 34))
    if type(unit) is Demon:
        atk_text = font.render(f"{unit.attack}", True, (0, 0, 255))
        screen.blit(atk_text, (x + PADDING, y + h - 34))


def draw_hand(screen, hand, holding, held_idx):
    # Dimensions for cards in hand
    card_width = 80
    card_height = 120
    padding = 10  # Space between cards in the hand

    # Calculate total width of the hand
    total_hand_width = len(hand) * card_width + (len(hand) - 1) * padding
    hand_start_x = (screen.get_width() - total_hand_width) // 2  # Center horizontally

    # Draw the player's hand at the bottom of the screen
    for idx, card in enumerate(hand):
        if(held_idx != idx or not holding):
            card.rect = pygame.Rect(hand_start_x + idx * (card_width + padding), screen.get_height() - card_height - PADDING, card_width, card_height)
            screen.blit(card.img, card.rect)

def draw_held(screen, held, mouse_pos):
    card_width = 80
    card_height = 120
    padding = 10
    screen.blit(held.img, (mouse_pos[0] - card_width // 2, mouse_pos[1] - card_height // 2))
    
def draw_deck(screen, deck_pos):
    # Draw deck icon in the bottom right corner
    deck_image = pygame.image.load('assets/deck.jpg')
    deck_image = pygame.transform.smoothscale(deck_image, (deck_pos.w, deck_pos.h))
    screen.blit(deck_image, deck_pos.topleft)


def draw_mana(screen, mana, max_mana):
    font = pygame.font.Font(None, 36)
    mana_text = font.render(f'Mana: {mana}/{max_mana}', True, (255, 255, 255))
    screen.blit(mana_text, (10, 10))

def draw_end_turn_button(screen):
    button_rect = pygame.Rect(PADDING, screen.get_height() - 60, 100, 40)  # Position in the bottom left corner
    pygame.draw.rect(screen, (0, 0, 255), button_rect)  # Blue button
    font = pygame.font.Font(None, 36)
    text = font.render("End Turn", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

def draw_arrows(screen, pairings):
    """Draw arrows between units"""
    for pair in pairings:
        start_pos = pair[0].rect.center
        end_pos = pair[1].rect.center
        # Draw the line part of the arrow
        pygame.draw.line(screen, ARROW_COLOUR, start_pos, end_pos, ARROW_WIDTH)

        # Calculate the angle of the arrow for the arrowhead
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        
        # Define the length and angle of the arrowhead
        arrowhead_length = 15
        arrowhead_angle = math.pi / 6  # 30 degrees for the arrowhead

        # Calculate the two points for the arrowhead lines
        left_x = end_pos[0] - arrowhead_length * math.cos(angle - arrowhead_angle)
        left_y = end_pos[1] - arrowhead_length * math.sin(angle - arrowhead_angle)
        right_x = end_pos[0] - arrowhead_length * math.cos(angle + arrowhead_angle)
        right_y = end_pos[1] - arrowhead_length * math.sin(angle + arrowhead_angle)

        # Draw the arrowhead lines
        pygame.draw.line(screen, ARROW_COLOUR, end_pos, (left_x, left_y), ARROW_WIDTH)
        pygame.draw.line(screen, ARROW_COLOUR, end_pos, (right_x, right_y), ARROW_WIDTH)


def draw_board(screen, player, enemies, board, background, animating, attacking_card):
    screen.fill((0, 0, 0))  # Clear screen with black background
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), board)
 
    # Calculate total width of player's demons
    total_player_width = len(player.board) * UNIT_WIDTH + (len(player.board) - 1) * PADDING
    player_start_x = (screen.get_width() - total_player_width) // 2  # Center horizontally

    # Draw player demons on board
    for idx, demon in enumerate(player.board):
        if(not animating):
            demon.rect = pygame.Rect(player_start_x + idx * (UNIT_WIDTH + PADDING), board.h//2 + board.y - UNIT_HEIGHT//2, UNIT_WIDTH, UNIT_HEIGHT)
        if(demon != attacking_card):
            draw_unit(screen, demon, demon.rect.x, demon.rect.y, demon.rect.w, demon.rect.h)

    # Calculate total width of enemies
    total_enemy_width = len(enemies) * ENEMY_WIDTH + (len(enemies) - 1) * PADDING
    enemy_start_x = (screen.get_width() - total_enemy_width) // 2  # Center horizontally

    # Draw enemy celestials on the other side
    for idx, enemy in enumerate(enemies):
        if(not animating):
            enemy.rect = pygame.Rect(enemy_start_x + idx * (ENEMY_WIDTH + PADDING), 100, ENEMY_WIDTH, ENEMY_HEIGHT)
        if(enemy != attacking_card):
            draw_unit(screen, enemy, enemy.rect.x, enemy.rect.y, enemy.rect.w, enemy.rect.h)


