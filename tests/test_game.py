from unittest import TestCase
from pyblackjack.hand import Hand
from pyblackjack.card import Card
from pyblackjack.deck import Deck
from pyblackjack.game import Game, WIN, LOSS
from pyblackjack.strategy import BasicStrategy


class TestGame(TestCase):
    """Test game
    """

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
        d = Deck(4)
        d.shuffle()
        d.cut()

        player_hand = Hand()
        player_hand.add_card(Card("Spades", "Q"))
        player_hand.add_card(Card("Clubs", "2"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "5"))

        strategy = BasicStrategy(d)

        game = Game(d, strategy)
        game.calculate_results(player_hand, dealer_hand)
        self.assertEqual(len(player_hand.cards), 2)

    def test_calculate_result_hit(self):
        """Test result for normal stand
        """
        d = Deck(4)
        d.shuffle()
        d.cut()

        player_hand = Hand()
        player_hand.add_card(Card("Spades", "Q"))
        player_hand.add_card(Card("Clubs", "2"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "7"))

        strategy = BasicStrategy(d)

        game = Game(d, strategy)
        game.calculate_results(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)

    def test_calculate_result_double(self):
        """Test result for normal stand
        """
        d = Deck(4)
        d.shuffle()
        d.cut()

        player_hand = Hand()
        player_hand.add_card(Card("Spades", "Q"))
        player_hand.add_card(Card("Clubs", "1"))
        player_hand.add_bet(5.0)

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "3"))

        strategy = BasicStrategy(d)

        game = Game(d, strategy)
        game.calculate_results(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)
        self.assertEqual(player_hand.bet, 10.0)

    def test_calculate_result_split_ace(self):
        """Test result for split
        """
        d = Deck(4)
        d.shuffle()
        d.cut()

        player_hand = Hand()
        player_hand.add_card(Card("Spades", "A"))
        player_hand.add_card(Card("Clubs", "A"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "3"))

        strategy = BasicStrategy(d)

        game = Game(d, strategy)
        game.calculate_results(player_hand, dealer_hand)
        game.display_results()
        self.assertGreaterEqual(len(strategy.split_hands), 2)
        self.assertEqual(len(strategy.split_hands[0].cards), 2)
        self.assertEqual(len(strategy.split_hands[1].cards), 2)

    def test_calculate_result_split_noneace(self):
        """Test result for split without aces
        """
        d = Deck(4)
        d.shuffle()
        d.cut()

        player_hand = Hand()
        player_hand.add_card(Card("Spades", "2"))
        player_hand.add_card(Card("Clubs", "2"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "10"))
        dealer_hand.add_card(Card("Hearts", "3"))

        strategy = BasicStrategy(d)

        game = Game(d, strategy)
        game.calculate_results(player_hand, dealer_hand)
        game.display_results()
        self.assertGreaterEqual(len(strategy.split_hands), 2)
        self.assertEqual(
            game.game_info["losses"] + game.game_info["wins"] + game.game_info["ties"], 2)

    def test_calculate_earnings(self):
        d = Deck(4)
        d.shuffle()
        d.cut()

        h1 = Hand()
        h1.add_card(Card("Spades", "2"))
        h1.add_card(Card("Clubs", "2"))
        h1.add_bet(5.0)

        h2 = Hand()
        h2.add_card(Card("Spades", "2"))
        h2.add_card(Card("Clubs", "A"))
        h2.add_bet(5.0)

        h3 = Hand()
        h3.add_card(Card("Spades", "2"))
        h3.add_card(Card("Clubs", "J"))
        h3.add_bet(5.0)

        h4 = Hand()
        h4.add_card(Card("Spades", "2"))
        h4.add_card(Card("Clubs", "Q"))
        h4.add_bet(5.0)

        h5 = Hand()
        h5.add_card(Card("Spades", "2"))
        h5.add_card(Card("Clubs", "K"))
        h5.add_bet(5.0)

        strategy = BasicStrategy(d)

        game = Game(d, strategy)
        earnings = game.calculate_earnings(h1, WIN, False)
        self.assertEqual(earnings, 5.0)

        game = Game(d, strategy)
        earnings = game.calculate_earnings(h1, LOSS, False)
        self.assertEqual(earnings, 5.0)

        game = Game(d, strategy)
        earnings = game.calculate_earnings(h1, WIN, True)
        self.assertEqual(earnings, 5.0)

        game = Game(d, strategy)
        earnings = game.calculate_earnings(h2, WIN, False)
        self.assertEqual(earnings, 7.5)

        game = Game(d, strategy)
        earnings = game.calculate_earnings(h3, WIN, False)
        self.assertEqual(earnings, 7.5)

        game = Game(d, strategy)
        earnings = game.calculate_earnings(h4, WIN, False)
        self.assertEqual(earnings, 7.5)

        game = Game(d, strategy)
        earnings = game.calculate_earnings(h5, WIN, False)
        self.assertEqual(earnings, 7.5)
