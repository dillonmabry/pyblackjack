from unittest import TestCase
from pyblackjack.card import Card


class TestCard(TestCase):
    """Test cards
    """

    def test_card_init(self):
        c = Card("Spades", "2")
        self.assertEquals(c.suit, "Spades")
        self.assertEquals(c.value, "2")
