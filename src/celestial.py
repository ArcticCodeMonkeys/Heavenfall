import random

class Celestial:
    def __init__(self, name):
        stats = {
            "Angel":[40, ["3x3","1x12","+10"]]
        }
        self.actions = stats[name][1]
        self.name = name
        self.hp = stats[name][0]
        self.hpMax = stats[name][0]
        self.dmg_modifier = 1
    def onHit(self):
        if(self.name == 'Angel'):
            self.heal(2)
    def act(self, enemies, allies):
        from demon import Demon
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
        
    def heal(self, amt):
        self.hp += amt
        self.hp = min(self.hp, self.hpMax)
    
            
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        # Logic to remove from enemy lineup
        pass
