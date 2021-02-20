from unittest import TestCase
from pyblackjack.deck import Deck
from pyblackjack.card import Card


class TestDeck(TestCase):
    """Test decks
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.std_deck = Deck(4)

    def test_deck_init(self):
        self.assertEqual(len(self.deck.cards), 52)
        self.assertEqual(len(self.std_deck.cards), 208)

    def test_deck_shuffle(self):
        """Test shuffle deck
        """
        self.assertEqual(str(self.deck.cards[0]), "A of Spades")
        self.deck.shuffle()
        self.assertTrue(str(self.deck.cards[0]) != "A of Spades")

    def test_deck_cut(self):
        """Test cut deck at random point
        """
        d = Deck(1)
        l = len(d.cards)
        d.cut()
        self.assertGreater(l, len(d.cards))

    def test_deck_deal(self):
        """Test deck deal card
        """
        d = Deck(1)
        c = d.deal()
        self.assertEqual(c.value, "A")
