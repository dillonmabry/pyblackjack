from unittest import TestCase
from pyblackjack.hand import Hand
from pyblackjack.card import Card
from pyblackjack.deck import Deck


class TestGame(TestCase):
    """Test game
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.deck.shuffle()
        self.deck.cut()

    #def test_game_ends_21(self):