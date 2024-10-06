import random
import pygame
UNIT_WIDTH = 180
UNIT_HEIGHT = 256
class Celestial:
    def __init__(self, name):
        stats = {
            "Angel": [40, ["3x1", "1x3"]]
        }
        self.actions = stats[name][1]
        self.name = name
        self.hp = stats[name][0]
        self.hpMax = stats[name][0]
        self.dmg_modifier = 1
        self.alive = True
        self.boardImg = pygame.transform.smoothscale(pygame.image.load(f'assets/{self.name}.jpg'), (UNIT_WIDTH, UNIT_HEIGHT))

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False

    def choose_action(self, demons):
        if not self.alive:
            return
        
        action = random.choice(self.actions)
        target_count, damage = self.parse_action(action)
        
        if target_count == "a":  # "a" for all
            for demon in demons:
                demon.take_damage(damage)
        else:
            for _ in range(target_count):
                if demons:
                    target = random.choice(demons)
                    target.take_damage(damage)

    def parse_action(self, action):
        # Example: "3x12" -> target_count = 3, damage = 12
        targets, damage = action.split("x")
        if targets == "a":
            return "a", int(damage)
        return int(targets), int(damage)
