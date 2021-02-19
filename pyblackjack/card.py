
class Card():
    """Basic unit of card
    Args:
        suit: suit of card
        value: number value of card
    """

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return " of ".join((self.value, self.suit))
