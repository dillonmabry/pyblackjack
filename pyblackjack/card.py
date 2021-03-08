"""Module for cards"""


class Card():
    """Basic unit of card
    Args:
        suit: suit of card
        value: number value of card
    """

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        """Gets numeric value of card
        Returns card value
        """
        if self.value == "A":
            return 11
        if self.value == "J" or self.value == "Q" or self.value == "K":
            return 10
        return int(self.value)

    def __repr__(self):
        """Repr of card"""
        return " of ".join((self.value, self.suit))
