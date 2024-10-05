import random
class Demon:
    def __init__(self, name, attack, health, cost, passive=None, deathrattle=None):
        
        self.name = name
        self.attack = attack
        self.health = health
        self.cost = cost
        self.passive = passive  # A function for passive effects
        self.deathrattle = deathrattle  # A function for deathrattle effects

    def act(self, enemies, allies):
        from celestial import Celestial
        action = self.actions[random.randint(0, len(self.actions))]
        if("x" in action):
            # Attack
            targets = action[:action.find("x")]
            damage = int(action[action.find('x')+1:])
            if(targets == 'a'):
                for enemy in enemies:
                    enemy.take_damage(damage*self.dmg_modifier)
                    self.take_damage(enemy.attack)
                    self.onHit()
            else:
                for _ in range(int(targets)):
                    target = random.randint(0, len(enemies))
                    enemies[target].take_damage(damage*self.dmg_modifier)
        if("+" in action):
            if("[" in action):
                # Heal Ally
                allies[int(action[3])].heal(int(action[5:]))
            else:
                # Heal Self
                self.heal(int(action[1:]))
        if("*" in action):
            if("/" in action):
                # Debuff
                target = random.randint(0, len(enemies))
                enemies[target].dmg_modifer *= action[1]/action[3]
            else:
                # Buff
                target = random.randint(0, len(allies))
                allies[target].dmg_modifier
    
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.die()

    def die(self, p):
        from player import Player
        p.board.remove(self)
        p.deck.append(self)