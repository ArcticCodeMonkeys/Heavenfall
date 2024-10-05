class Artifact:
    def __init__(self, name, card_type, cost, effect=None):
        self.name = name
        self.cost = cost
        self.effect = effect
