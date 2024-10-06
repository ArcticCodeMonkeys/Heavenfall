import random
import pygame
from UI import ENEMY_WIDTH, ENEMY_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT
class Celestial:
    def __init__(self, name, rect=None):
        stats = {
            "Angel": [10, ["3x1", "1x2"]],
            "deck":[0, ["1x1","1x1"]]
        }
        self.actions = stats[name][1]
        self.name = name
        self.hp = stats[name][0]
        self.hpMax = stats[name][0]
        self.dmg_modifier = 1
        self.alive = True
        self.rect = rect
        if(self.name == 'deck'):
            self.boardImg = pygame.transform.smoothscale(pygame.image.load(f'assets/{self.name}.jpg'), (UNIT_WIDTH, UNIT_HEIGHT))
        else:
            self.boardImg = pygame.transform.smoothscale(pygame.image.load(f'assets/{self.name}.jpg'), (ENEMY_WIDTH, ENEMY_HEIGHT))

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False

    def choose_action(self, demons, player):
        if not self.alive:
            return
        
        action = random.choice(self.actions)
        target_count, damage = self.parse_action(action)
        
        if target_count == "a":  # "a" for all
            if(len(demons) == 0):
                player.health -= damage
            for demon in demons:
                demon.take_damage(damage)
        else:
            targets = []
            for _ in range(target_count):
                if(len(demons) == 0):
                    player.health -= damage
                if demons:
                    target = random.choice(demons)
                    target.take_damage(damage, self, demons)
                    targets.append(target)
            return targets

    def parse_action(self, action):
        # Example: "3x12" -> target_count = 3, damage = 12
        targets, damage = action.split("x")
        if targets == "a":
            return "a", int(damage)
        return int(targets), int(damage)
