from unittest import TestCase
from pyblackjack.hand import Hand
from pyblackjack.card import Card


class TestHand(TestCase):
    """Test hands
    """

    def test_hand_init(self):
        player_hand = Hand(is_dealer=False)
        dealer_hand = Hand(is_dealer=True)
        self.assertEquals(player_hand.value, 0)
        self.assertEquals(player_hand.cards, [])
        self.assertEquals(dealer_hand.value, 0)
        self.assertEquals(dealer_hand.cards, [])

    def test_hand_add_cards(self):
        """Test adding cards
        """
        player_hand = Hand(is_dealer=False)
        dealer_hand = Hand(is_dealer=True)
        player_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.assertEquals(len(player_hand.cards), 1)
        self.assertEquals(len(dealer_hand.cards), 1)
        self.assertEquals(player_hand.get_value(), 2)
        self.assertEquals(dealer_hand.get_value(), 11)

    def test_hand_ace_case(self):
        """Test ace bust case
        """
        player_hand = Hand(is_dealer=False)
        dealer_hand = Hand(is_dealer=True)
        player_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "A"))
        player_hand.add_card(Card("Hearts", "2"))
        dealer_hand.add_card(Card("Clubs", "J"))

        self.assertEquals(len(player_hand.cards), 2)
        self.assertEquals(len(dealer_hand.cards), 2)
        self.assertEquals(player_hand.get_value(), 4)
        self.assertEquals(dealer_hand.get_value(), 21)

        # Switch Ace from 11 to 1 to avoid bust
        dealer_hand.add_card(Card("Clubs", "2"))
        self.assertEquals(dealer_hand.get_value(), 13)
