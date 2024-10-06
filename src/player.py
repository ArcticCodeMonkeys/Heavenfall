class Player:
    def __init__(self, health=10, mana=3):
        from demon import Demon
        self.health = health
        self.mana = mana
        self.deck = [Demon('Quasit'),Demon('Quasit'),Demon('Quasit'),Demon('Hellhound'),Demon('Hellhound'),Demon('Hellhound'),Demon('Succubus')]  # A list of Demon objects
        self.stored_deck = self.deck
        self.hand = []  # Cards drawn into hand
        self.board = []  # Summoned demons on the board

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
