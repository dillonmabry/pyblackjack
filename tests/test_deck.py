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
        self.assertEquals(len(self.deck.cards), 52)
        self.assertEquals(len(self.std_deck.cards), 208)

    def test_deck_shuffle(self):
        """Test shuffle deck
        """
        self.assertEquals(str(self.deck.cards[0]), "A of Spades")
        self.deck.shuffle()
        self.assertNotEquals(str(self.deck.cards[0]), "A of Spades")

    def test_deck_deal(self):
        """Test deck deal card
        """
        d = Deck(1)
        c = d.deal()
        self.assertEquals(c.value, "A")
