from unittest import TestCase
from pyblackjack.hand import Hand
from pyblackjack.card import Card
from pyblackjack.deck import Deck
from pyblackjack.game import Game, WIN, LOSS, TIE
from pyblackjack.strategy import BasicStrategy


class TestGame(TestCase):
    """Test game
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.deck.shuffle()
        self.deck.cut()

    def test_check_blackjack(self):
        """Test blackjack
        """
        h = Hand()
        h.add_card(Card("Spades", "10"))
        h.add_card(Card("Clubs", "A"))
        result = Game.check_blackjack(h)
        self.assertTrue(result)

        h = Hand()
        h.add_card(Card("Spades", "9"))
        h.add_card(Card("Clubs", "A"))
        result = Game.check_blackjack(h)
        self.assertFalse(result)

    def test_bust(self):
        """Test busted
        """
        h = Hand()
        h.add_card(Card("Spades", "11"))
        h.add_card(Card("Clubs", "10"))
        h.add_card(Card("Hearts", "2"))
        result = Game.check_bust(h)
        self.assertTrue(result)

        h = Hand()
        h.add_card(Card("Spades", "11"))
        h.add_card(Card("Clubs", "10"))
        result = Game.check_bust(h)
        self.assertFalse(result)

    def test_initial_blackjack(self):
        """Test initial blackjack
        """
        h1 = Hand()
        h1.add_card(Card("Spades", "11"))
        h1.add_card(Card("Clubs", "10"))

        h2 = Hand()
        h2.add_card(Card("Spades", "11"))
        h2.add_card(Card("Clubs", "8"))


        h1_blackjack, h2_blackjack = Game.check_inital_blackjack(h1, h2)
        self.assertTrue(h1_blackjack)
        self.assertFalse(h2_blackjack)

    def test_calculate_result_stand(self):
        """Test result for normal stand
        """
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "Q"))
        player_hand.add_card(Card("Clubs", "2"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "5"))

        strategy = BasicStrategy([])

        game = Game(self.deck, strategy)
        game.calculate_result(player_hand, dealer_hand)
        self.assertEqual(len(player_hand.cards), 2)

    def test_calculate_result_hit(self):
        """Test result for normal stand
        """
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "Q"))
        player_hand.add_card(Card("Clubs", "2"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "7"))

        strategy = BasicStrategy([])

        game = Game(self.deck, strategy)
        game.calculate_result(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)

    def test_calculate_result_double(self):
        """Test result for normal stand
        """
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "Q"))
        player_hand.add_card(Card("Clubs", "1"))
        player_hand.add_bet(5.0)

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "3"))

        strategy = BasicStrategy([])

        game = Game(self.deck, strategy)
        game.calculate_result(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)
        self.assertEqual(player_hand.bet, 10.0)

    # def test_calculate_result_split(self):
    #     """Test result for split
    #     """
    #     player_hand = Hand()
    #     player_hand.add_card(Card("Spades", "A"))
    #     player_hand.add_card(Card("Clubs", "A"))

    #     dealer_hand = Hand()
    #     dealer_hand.add_card(Card("Spades", "10"))
    #     dealer_hand.add_card(Card("Hearts", "3"))

    #     strategy = BasicStrategy([])

    #     game = Game(self.deck, strategy)
    #     result = game.calculate_result(player_hand, dealer_hand)
    #     self.assertGreaterEqual(len(strategy.split_hands), 2)
