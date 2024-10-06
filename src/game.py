import pygame
import random
from player import Player
from celestial import Celestial
from UI import draw_board, draw_hand, draw_deck, draw_mana, draw_end_turn_button, draw_held

encounter_list = [
    [Celestial("Angel"), Celestial("Angel")]
]
# Basic settings
MAX_HAND_SIZE = 10
MAX_MANA = 10
CARD_DRAW = 1
START_MANA = 3
ANIMATION_SPEED = 1

class Game:
    def __init__(self):
        self.state = "battle"
        self.player = Player(30, START_MANA)
        self.enemies = []  # List of Celestial enemies in the current battle
        self.turn = 3  # 1 for player, 2 for enemies, 3 for begin player turn
        self.round_count = 0
        self.dragging_card = None  # Track if a card is being dragged
        self.dragged_index = None  # Track the index of the dragged card
        self.end_turn_button = None
        self.board = None
        self.attacking_card = None
        self.attacking_target = None
        self.is_animating = False
        self.card_start_pos = None
        self.card_end_pos = None
        self.card_current_pos = None
        self.background = pygame.image.load(f'assets/heaven.jpg')

    def start_turn(self):
        self.turn = 1
        # Gain mana
        self.player.mana = min(START_MANA+self.round_count, MAX_MANA)
        # Draw cards, up to the hand size limit
        self.draw_cards(CARD_DRAW)

    def end_player_turn(self):
        for celestial in self.enemies:
            celestial.choose_action(self.player.board)
            self.resolve_deaths()
        
        self.round_count += 1
        self.turn = 3

    def resolve_deaths(self):
        # Remove dead demons and celestials from their respective lists
        self.player.board = [d for d in self.player.board if d.alive]
        self.enemies = [c for c in self.enemies if c.alive]

    def draw_cards(self, amount):
        for _ in range(amount):
            if len(self.player.hand) < MAX_HAND_SIZE:
                card = random.choice(self.player.deck)  # Simplified card draw
                self.player.hand.append(card)
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicking on a card in hand
            for idx, card in enumerate(self.player.hand):
                if card.rect.collidepoint(event.pos):
                    self.dragging_card = card
                    self.dragged_index = idx
                    break
            if self.end_turn_button.collidepoint(event.pos):
                self.end_player_turn()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_card:
                if self.board.collidepoint(event.pos) and self.player.mana >= self.dragging_card.cost:
                    self.player.board.append(self.dragging_card)
                    self.player.hand.pop(self.dragged_index)
                    self.player.mana -= self.dragging_card.cost
                self.dragging_card = None  # Stop dragging the card after drop

    def generate_encounter(self):
        self.enemies = encounter_list[random.randint(0, len(encounter_list) - 1)]

    def animate_attack(self, attacking_card, target_card):
        self.is_animating = True
        self.attacking_card = attacking_card
        self.attacking_target = target_card
        self.card_start_pos = pygame.Vector2(attacking_card.rect.x, attacking_card.rect.y)
        self.card_end_pos = pygame.Vector2(target_card.rect.x, target_card.rect.y)
        self.card_current_pos = self.card_start_pos

    def update_animation(self):
        if self.is_animating and self.attacking_card and self.attacking_target:
            direction = (self.card_end_pos - self.card_current_pos).normalize()  # Calculate direction to target
            distance_to_target = self.card_current_pos.distance_to(self.card_end_pos)

            if distance_to_target > 10:  # Continue moving toward target
                self.card_current_pos += direction * ANIMATION_SPEED
                self.attacking_card.rect.topleft = (int(self.card_current_pos.x), int(self.card_current_pos.y))
            else:
                # Move back to start position
                direction_back = (self.card_start_pos - self.card_current_pos).normalize()
                distance_to_start = self.card_current_pos.distance_to(self.card_start_pos)

                if distance_to_start > 10:  # Continue moving back
                    self.card_current_pos += direction_back * ANIMATION_SPEED
                    self.attacking_card.rect.topleft = (int(self.card_current_pos.x), int(self.card_current_pos.y))
                else:
                    self.is_animating = False  # Animation finished
    def run(self):
        
        pygame.init()  # Initialize Pygame
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Heavenfall")  # Set window title
        clock = pygame.time.Clock()
        self.board = pygame.Rect(100, 400, screen.get_width() - 200, 250)
        self.generate_encounter()
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the game loop if the window is closed
                self.handle_input(event)
            if self.state == "battle":
                draw_board(screen, self.player, self.enemies, self.board, self.background)
                self.end_turn_button = draw_end_turn_button(screen)
                draw_deck(screen)
                draw_hand(screen, self.player.hand, self.dragging_card, self.dragged_index)
                draw_mana(screen, self.player.mana, min(START_MANA+self.round_count, MAX_MANA))
                if(self.dragging_card):
                    mouse_position = pygame.mouse.get_pos()
                    draw_held(screen, self.player.hand[self.dragged_index], mouse_position)
                pygame.display.update()
                if(self.turn == 3):
                    self.start_turn()

            # Add other game state handling here (e.g., reward phase)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()  # Clean up
