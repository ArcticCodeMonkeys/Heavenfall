from player import Player
from demon import Demon
from celestial import Celestial
from artifact import Artifact
from UI import draw_board
import random
import pygame

encounter_list = [
    [Celestial("Angel"), Celestial("Angel")]
]

class Game:
    def __init__(self):
        self.state = "battle"
        self.player = Player()
        self.enemies = []  # List of Celestial enemies in the current battle
        self.turn = 1  # 1 for player, 2 for enemies

    def start_battle(self):
        # Populate enemy list
        encounter_index = random.randint(0, len(encounter_list) - 1)  # Changed to avoid IndexError
        self.enemies = encounter_list[encounter_index]
        self.state = "battle"

    def battle_turn(self):
        if self.turn == 1:
            # Player's turn logic
            self.turn = 2
        else:
            # Enemy's turn logic
            self.turn = 1

    def run(self):
        
        pygame.init()  # Initialize Pygame
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Heaven's Fall")  # Set window title
        
        self.start_battle()  # Call to start the battle at the beginning

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the game loop if the window is closed
            
            if self.state == "battle":
                draw_board(screen, self.player, self.enemies)
                self.battle_turn()

            # Add other game state handling here (e.g., reward phase)
            
        pygame.quit()  # Clean up
