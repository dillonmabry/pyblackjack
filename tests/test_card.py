from unittest import TestCase
from pyblackjack.card import Card


class TestCard(TestCase):
    """Test cards
    """

    def test_card_init(self):
        c = Card("Spades", "2")
        self.assertEqual(c.suit, "Spades")
        self.assertEqual(c.value, "2")

    def test_card_value(self):
        c = Card("Clubs", "A")
        self.assertEqual(c.get_value(), 11)
        c2 = Card("Aces", "J")
        self.assertEqual(c2.get_value(), 10)
        c3 = Card("Aces", "2")
        self.assertEqual(c3.get_value(), 2)
