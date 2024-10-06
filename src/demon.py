import pygame
import random
UNIT_WIDTH = 120
UNIT_HEIGHT = 172
HAND_WIDTH = 80
HAND_HEIGHT = 120
class Demon:
    def __init__(self, name):
        stats = {
            "Quasit": [1, 3, 1],
            "Hellhound":[1, 4, 2],
            "Succubus":[2, 5, 3],
            "Rakshasa":[3, 3, 2],
            "Pit Fiend":[4, 4, 3],
            "Orcus":[2, 5, 3],
            "Yeenoghu":[2, 3, 2],
            "Zariel":[1, 7, 3],
            "Imp":[2, 1, 1],
            "The Devil":[0, 6, 6]
        }
        self.name = name
        self.attack = stats[name][0]
        self.hp = stats[name][1]
        self.hpMax = stats[name][1]
        self.cost = stats[name][2]
        self.has_battlecry = False
        if(self.name in ["Yeenoghu"]):
            self.has_battlecry = True
        self.has_deathrattle = False
        if(self.name in ["Imp","Orcus"]):
            self.has_deathrattle = True
        self.alive = True
        self.can_attack = True  # Track if the demon can attack this turn
        self.rect = None
        self.img = pygame.transform.smoothscale(pygame.image.load(f'assets/{self.name}.jpg'), (HAND_WIDTH, HAND_HEIGHT))
        self.boardImg = pygame.transform.smoothscale(pygame.image.load(f'assets/{self.name}.jpg'), (UNIT_WIDTH, UNIT_HEIGHT))
     

    def attack_celestial(self, target):
        if self.can_attack and self.alive:
            # Deal damage to the celestial
            damage = self.attack + self.attack_bonus
            target.take_damage(damage)
            self.can_attack = False  # Mark as unable to attack after attacking
            return True  # Return True to indicate attack happened
        return False  # No attack if demon already attacked or is dead

    def take_damage(self, dmg, attacker, allies):
        self.hp -= dmg
        if(self.name == "Succubus"):
            attacker.dmg_modifier *= 0.5
        if(self.name == "Rakshasa"):
            if(dmg < 2):
                self.hp += dmg
        if self.hp <= 0:
            self.die(allies)

    def passive(self, allies, enemies, status):
        match self.name:
            case "Hellhound":
                if(status == "Summon"):
                    count = 0
                    for h in allies:
                        if h.name == "Hellhound":
                            h.attack += 1
                            count += 1
                    self.attack = 1 + count
            case "Rakshasa":
                self.attack = 3
            case "Yeenoghu":
                if(status == "Summon"):
                    if(len(allies) > 1):
                        consume = random.choice(allies)
                        allies.remove(consume)
                        consume.die(allies)
                        target = random.choice(allies)
                        target.hp += consume.hpMax
                        target.hpMax += consume.hpMax
                        target.attack += consume.attack
            case "The Devil":
                if(status == "Summon"):
                    for ally in allies:
                        if(ally != self):
                            ally.attack += 6
            case _:
                return
                



    def die(self, allies):
        self.alive = False
        if(self in allies):
            allies.remove(self)
        for ally in allies:
            if self.name == "Hellhound" and ally.name == "Hellhound":
                ally.attack -= 1
            if ally.name == "Zariel":
                ally.attack += 2
            if self.name == "Imp":
                target = random.choice(allies)
                target.hp = min(target.hp + self.attack, target.hpMax) 
            if self.name == "The Devil":
                ally.attack -= 6

