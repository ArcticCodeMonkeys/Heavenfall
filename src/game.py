import pygame
import random
import copy
from player import Player
from celestial import Celestial
from UI import draw_board, draw_hand, draw_deck, draw_mana, draw_end_turn_button, draw_held, draw_arrows, draw_unit, draw_health, UNIT_WIDTH, UNIT_HEIGHT, PADDING

encounter_list = [
    [Celestial("Angel"), Celestial("Angel")],
    [Celestial("Angel"), Celestial("Angel")],
    [Celestial("Angel"), Celestial("Angel")],
    [Celestial("Angel"), Celestial("Angel")]
]
# Basic settings
MAX_HAND_SIZE = 10
MAX_MANA = 10
CARD_DRAW = 1
START_MANA = 3
ANIMATION_ACCEL = 2
ANIMATION_MAX_SPEED = 50
MAX_BOARD_SIZE = 7
MAX_HEALTH = 10

class Game:
    def __init__(self):
        self.state = "battle"
        self.player = Player(MAX_HEALTH, START_MANA)
        self.enemies = []  # List of Celestial enemies in the current battle
        self.turn = 1  # 1 for player, 2 for enemies, 3 for begin player turn
        self.round_count = 0
        self.dragging_card = None  # Track if a card is being dragged
        self.dragged_index = None  # Track the index of the dragged card
        self.end_turn_button = None
        self.board = None
        self.attacking_card = None
        self.attacking_target = None
        self.is_animating = False
        self.returning = False
        self.card_start_pos = None
        self.card_end_pos = None
        self.card_current_pos = None
        self.background = pygame.image.load(f'assets/heaven.jpg')
        self.attack_queue = []  # List of (attacker, target) pairs for animation
        self.animation_speed = 5
        self.selected_demon = None
        self.selected_celestial = None
        self.drawn_card = None
        self.hand_pos = None
        self.deck_pos = None
        self.last = self.player.board

    def start_turn(self):
        for d in self.player.board:
            d.passive(self.player.board, self.enemies, "Start Turn")
        if(len(self.player.deck)):
            new_card = random.choice(self.player.deck)
            self.player.deck.remove(new_card)
            self.player.hand.append(new_card)
        self.attack_queue = []
        self.turn = 1
        self.player.mana = min(START_MANA + self.round_count, MAX_MANA)

    def end_player_turn(self):
        from demon import Demon
        for attacker, enemy in self.attack_queue:
            if(type(attacker) == Demon):
                enemy.take_damage(attacker.attack)
                if(attacker.name == "Pit Fiend"):
                    attacker.can_attack = True
                    second_target = random.choice(self.enemies)
                    second_target.take_damage(attacker.attack)
        for celestial in self.enemies:
            targets = celestial.choose_action(self.player.board, self.player)
            for d in self.player.board:
                d.passive(self.player.board, self.enemies, "Attacked")
            if(targets != None and len(targets) != 0):
                for target in targets:
                    self.attack_queue.append((celestial, target))  # Queue attacker-target pairs
                    self.attack_queue.append((celestial, Celestial("Angel", celestial.rect)))
            else:
                self.attack_queue.append((celestial, Celestial("Angel", self.hand_pos)))
                self.attack_queue.append((celestial, Celestial("Angel", celestial.rect)))
        self.draw_cards(CARD_DRAW)
        self.turn = 3  # Switch to animation mode
        self.round_count += 1

    def resolve_deaths(self):
        # Remove dead demons and celestials from their respective lists
        from demon import Demon
        output = ""
        for d in self.last:
            if d not in self.player.board and d.name == 'Orcus':
                self.summon(Demon("Quasit"))
                self.summon(Demon("Quasit"))
                self.summon(Demon("Quasit"))
        print(output)
        self.last = self.player.board
        self.player.board = [d for d in self.player.board if d.alive]
        self.enemies = [c for c in self.enemies if c.alive]

    def draw_cards(self, amount):
        for _ in range(amount):
            if len(self.player.hand) < MAX_HAND_SIZE and len(self.player.deck) > 0:
                self.attack_queue.append((Celestial('deck', pygame.Rect(self.deck_pos)), Celestial("Angel", self.hand_pos)))
                self.attack_queue.append((Celestial('deck', pygame.Rect(10000, 0, 1, 1)), (Celestial('deck', pygame.Rect(10000, 1.6, 1, 1)))))
                
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
            # Check if clicking on a card on board
            for demon in self.player.board:
                if demon.rect.collidepoint(event.pos):
                    self.selected_demon = demon
                    return

            # Check if clicking on a celestial (after selecting a demon)
            if self.selected_demon and all(self.selected_demon not in atk for atk in self.attack_queue):
                for celestial in self.enemies:
                    if celestial.rect.collidepoint(event.pos):
                        self.selected_celestial = celestial
                        self.attack_queue.append((self.selected_demon, self.selected_celestial))
                        self.attack_queue.append((self.selected_demon, Celestial("Angel", self.selected_demon.rect)))
                        self.selected_demon = None  # Reset selection
                        self.selected_celestial = None
                        return

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_card:
                if self.board.collidepoint(event.pos) and self.player.mana >= self.dragging_card.cost:
                    self.player.hand.pop(self.dragged_index)
                    self.player.mana -= self.dragging_card.cost
                    self.summon(self.dragging_card)
                    self.resolve_deaths()
                self.dragging_card = None  # Stop dragging the card after drop

    def summon(self, card):
        if(len(self.player.board) < MAX_BOARD_SIZE):
            self.player.board.append(card)
            card.passive(self.player.board, self.enemies, "Summon")
            for d in self.player.board:
                if d.name == "The Devil":
                    card.attack += 6
            
    def generate_encounter(self):
        self.player.mana = 3
        print(self.player.stored_deck)
        self.player.deck = self.player.stored_deck.copy()
        self.player.hand = []
        self.player.board = []
        if(len(self.player.deck) >= 3):
            for _ in range(3):
                new_card = random.choice(self.player.deck)
                self.player.deck.remove(new_card)
                self.player.hand.append(new_card)
        self.enemies = encounter_list[random.randint(0, len(encounter_list) - 1)]

    def animate_attack(self, attacking_card, target_card):
        """Initiate the attack animation."""
        self.is_animating = True
        if(self.returning):
            self.animation_speed = ANIMATION_MAX_SPEED
        self.attacking_card = attacking_card
        self.attacking_target = target_card
        self.card_start_pos = pygame.Vector2(attacking_card.rect.x, attacking_card.rect.y)
        self.card_end_pos = pygame.Vector2(target_card.rect.x, target_card.rect.y)
        self.card_current_pos = self.card_start_pos

    def update_animation(self, screen):
        self.refresh_screen(screen)
        """Handle the ongoing attack animation and queue the next one."""
        if self.is_animating and self.attacking_card and self.attacking_target:
            self.animation_speed *= ANIMATION_ACCEL
            self.animation_speed = min(self.animation_speed, ANIMATION_MAX_SPEED)
            # Move attacking card towards the target or back to the start
            if self.card_current_pos != self.card_end_pos:
                # Phase 1: Move attacking card towards the target
                direction = (self.card_end_pos - self.card_current_pos).normalize()
                distance_to_target = self.card_current_pos.distance_to(self.card_end_pos)

                if distance_to_target > self.animation_speed:  # Continue moving towards the target
                    self.card_current_pos += direction * self.animation_speed
                    self.attacking_card.rect.topleft = (int(self.card_current_pos.x), int(self.card_current_pos.y))
                else:
                    # Phase 2: Attack reached target, switch to return phase
                    self.card_current_pos = self.card_end_pos  # Snap to target position
            else:
                # Phase 2: Move attacking card back to the start position
                # Calculate the direction only if there's a non-zero distance between the positions
                if self.card_start_pos != self.card_current_pos:
                    direction_back = (self.card_start_pos - self.card_current_pos).normalize()
                else:
                    direction_back = pygame.math.Vector2(0, 0)  # Or handle it accordingly

                distance_to_start = self.card_current_pos.distance_to(self.card_start_pos)

                if distance_to_start > self.animation_speed:  # Continue moving back to the start
                    self.card_current_pos += direction_back * self.animation_speed
                    self.attacking_card.rect.topleft = (int(self.card_end_pos.x), int(self.card_end_pos.y))
                else:
                    # Animation finished, snap back to start position and end animation
                    self.attacking_card.rect.topleft = (int(self.card_end_pos.x), int(self.card_end_pos.y))
                    self.is_animating = False  # End the animation
                    self.animation_speed = 5
                    self.returning = not self.returning

            
    def process_attack_queue(self):
        """Process the attack queue one by one."""
        if not self.is_animating and self.attack_queue:
            attacker, target = self.attack_queue.pop(0)
            self.animate_attack(attacker, target)
        if(len(self.attack_queue) == 0):
            self.is_animating = False
            self.start_turn()

    def refresh_screen(self, screen):
        draw_board(screen, self.player, self.enemies, self.board, self.background, self.is_animating, self.attacking_card)
        self.end_turn_button = draw_end_turn_button(screen)
        if(len(self.player.deck) > 0):
            draw_deck(screen, self.deck_pos)
        draw_hand(screen, self.player.hand, self.dragging_card, self.dragged_index)
        draw_mana(screen, self.player.mana, min(START_MANA+self.round_count, MAX_MANA))
        draw_health(screen, self.player.health, MAX_HEALTH)
        if(self.turn != 3):
            draw_arrows(screen, self.attack_queue)
        if(self.attacking_card):
            draw_unit(screen, self.attacking_card, self.attacking_card.rect.x, self.attacking_card.rect.y, self.attacking_card.rect.w, self.attacking_card.rect.h)
        if self.dragging_card:
            mouse_position = pygame.mouse.get_pos()
            draw_held(screen, self.player.hand[self.dragged_index], mouse_position)
        pygame.display.flip()

    def run(self):
        pygame.init()  # Initialize Pygame
        pygame.mixer.init()
        pygame.mixer.music.load('assets/background_music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Heavenfall")  # Set window title
        clock = pygame.time.Clock()
        self.board = pygame.Rect(100, 400, screen.get_width() - 200, 250)
        self.hand_pos = pygame.Rect(screen.get_width()//2 - UNIT_WIDTH, screen.get_height() - UNIT_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT)
        self.deck_pos = pygame.Rect(screen.get_width() - UNIT_WIDTH - PADDING, screen.get_height()-UNIT_HEIGHT - PADDING, UNIT_WIDTH, UNIT_HEIGHT)
        self.generate_encounter()
        
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the game loop if the window is closed
                if(self.turn != 3):
                    self.handle_input(event)

            if self.state == "battle":
                
                
                # Process the attack queue if we're in animation mode
                if self.turn == 3:
                    self.update_animation(screen)
                    self.process_attack_queue()
                else:
                    self.resolve_deaths()
                    self.refresh_screen(screen)
                    if(len(self.enemies) == 0):
                        self.generate_encounter()
                    if(self.player.health <= 0):
                        pygame.quit()
                    
            clock.tick(60)

        pygame.quit()  # Clean up
