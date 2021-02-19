from unittest import TestCase
from pyblackjack.hand import Hand
from pyblackjack.card import Card
from pyblackjack.deck import Deck
from pyblackjack.strategy import DealerStrategy, BasicStrategy


class TestDealerStrategy(TestCase):
    """Test dealer strat
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.strategy = DealerStrategy(self.deck)

    def test_dealer_strategy_with_ace(self):
        dealer_hand = Hand(is_dealer=True)
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.strategy.play(dealer_hand)
        self.assertGreaterEqual(len(dealer_hand.cards), 3)

    def test_dealer_strategy_with_ace_stand(self):
        dealer_hand = Hand(is_dealer=True)
        dealer_hand.add_card(Card("Spades", "8"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.strategy.play(dealer_hand)
        self.assertEquals(len(dealer_hand.cards), 2)

    def test_dealer_strategy_generic(self):
        dealer_hand = Hand(is_dealer=True)
        dealer_hand.add_card(Card("Spades", "J"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.strategy.play(dealer_hand)
        self.assertEquals(len(dealer_hand.cards), 2)

class TestBasicStrategy(TestCase):
    """Test basic strat
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.strategy = BasicStrategy(self.deck)