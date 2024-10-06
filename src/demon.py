import pygame
UNIT_WIDTH = 120
UNIT_HEIGHT = 172
HAND_WIDTH = 80
HAND_HEIGHT = 120
class Demon:
    def __init__(self, name, attack, health, cost, passive=None, deathrattle=None):
        self.name = name
        self.attack = attack
        self.hp = health
        self.hpMax = health
        self.cost = cost
        self.dmg_modifier = 1
        self.alive = True
        self.passive = passive  # A function for passive effects
        self.deathrattle = deathrattle  # A function for deathrattle effects
        self.can_attack = True  # Track if the demon can attack this turn
        self.rect = None
        self.img = pygame.transform.smoothscale(pygame.image.load(f'assets/{self.name}.jpg'), (HAND_WIDTH, HAND_HEIGHT))
        self.boardImg = pygame.transform.smoothscale(pygame.image.load(f'assets/{self.name}.jpg'), (UNIT_WIDTH, UNIT_HEIGHT))
     

    def attack_celestial(self, target):
        if self.can_attack and self.alive:
            # Deal damage to the celestial
            damage = self.attack * self.dmg_modifier
            target.take_damage(damage)
            self.can_attack = False  # Mark as unable to attack after attacking
            return True  # Return True to indicate attack happened
        return False  # No attack if demon already attacked or is dead

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False
