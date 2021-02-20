from unittest import TestCase
from pyblackjack.hand import Hand
from pyblackjack.card import Card


class TestHand(TestCase):
    """Test hands
    """

    def test_hand_init(self):
        player_hand = Hand()
        dealer_hand = Hand()
        self.assertEqual(player_hand.value, 0)
        self.assertEqual(player_hand.cards, [])
        self.assertEqual(dealer_hand.value, 0)
        self.assertEqual(dealer_hand.cards, [])

    def test_hand_add_cards(self):
        """Test adding cards
        """
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.assertEqual(len(player_hand.cards), 1)
        self.assertEqual(len(dealer_hand.cards), 1)
        self.assertEqual(player_hand.get_value(), 2)
        self.assertEqual(dealer_hand.get_value(), 11)

    def test_hand_ace_case(self):
        """Test ace bust case
        """
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "A"))
        player_hand.add_card(Card("Hearts", "2"))
        dealer_hand.add_card(Card("Clubs", "J"))

        self.assertEqual(len(player_hand.cards), 2)
        self.assertEqual(len(dealer_hand.cards), 2)
        self.assertEqual(player_hand.get_value(), 4)
        self.assertEqual(dealer_hand.get_value(), 21)

        # Switch Ace from 11 to 1 to avoid bust
        dealer_hand.add_card(Card("Clubs", "2"))
        self.assertEqual(dealer_hand.get_value(), 13)

    def test_hand_add_bet(self):
        """Test adding bet
        """
        h = Hand()
        h.add_bet(10)
        self.assertEqual(h.bet, 10)
        payout_ratio = 0.5
        h.add_bet(10 + (10 * payout_ratio))
        self.assertEqual(h.bet, 15)
