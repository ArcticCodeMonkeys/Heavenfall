class Player:
    def __init__(self, health=30, mana=3):
        from demon import Demon
        self.health = health
        self.mana = mana
        self.deck = []  # A list of Demon objects
        self.hand = [Demon('Quasit', 1, 3, 1)]  # Cards drawn into hand
        self.board = []  # Summoned demons on the board
        self.summon_demon(self.hand[0])

    def draw_card(self):
        if len(self.deck) > 0:
            card = self.deck.pop()
            self.hand.append(card)
    
    def summon_demon(self, demon):
        from demon import Demon
        if self.mana >= demon.cost and len(self.board) < 6:  # Max 6 demons on board
            self.board.append(demon)
            self.hand.remove(demon)
            self.mana -= demon.cost
