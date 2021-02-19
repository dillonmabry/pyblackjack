import random
from .card import Card

SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]
CARD_VALUES = ["A", "2", "3", "4", "5",
               "6", "7", "8", "9", "10", "J", "Q", "K"]


class Deck():
    """Basic deck of gameplay
    Args:
        num_decks: number of decks to use
    """

    def __init__(self, num_decks):
        self.cards = [Card(s, v)
                      for s in SUITS for v in CARD_VALUES] * num_decks

    def shuffle(self):
        """
        Shuffles deck
        """
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        """
        Gets first card from deck
        Returns first card from top of deck
        """
        if len(self.cards) > 1:
            return self.cards.pop(0)
