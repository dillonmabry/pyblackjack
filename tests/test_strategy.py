from unittest import TestCase
from pyblackjack.hand import Hand
from pyblackjack.card import Card
from pyblackjack.deck import Deck
from pyblackjack.strategy import DealerStrategy, BasicStrategy, SimpleStrategy, SPLIT


class TestDealerStrategy(TestCase):
    """Test dealer strat
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.deck.shuffle()
        self.deck.cut()
        self.strategy = DealerStrategy(self.deck)

    def test_dealer_strategy_with_ace(self):
        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.strategy.play(dealer_hand)
        self.assertGreaterEqual(len(dealer_hand.cards), 3)

    def test_dealer_strategy_with_ace_stand(self):
        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "8"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.strategy.play(dealer_hand)
        self.assertEqual(len(dealer_hand.cards), 2)

    def test_dealer_strategy_generic(self):
        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "J"))
        dealer_hand.add_card(Card("Clubs", "A"))
        self.strategy.play(dealer_hand)
        self.assertEqual(len(dealer_hand.cards), 2)


class TestSimpleStrategy(TestCase):
    """Test simplest strat
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.deck.shuffle()
        self.deck.cut()
        self.strategy = SimpleStrategy(self.deck)

    def test_simple_strat_stand(self):
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "2"))
        player_hand.add_card(Card("Clubs", "J"))

        self.strategy.play(player_hand, None)
        self.assertEqual(len(player_hand.cards), 2)

    def test_simple_strat_hit(self):
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "2"))
        player_hand.add_card(Card("Clubs", "9"))

        self.strategy.play(player_hand, None)
        self.assertEqual(len(player_hand.cards), 3)


class TestBasicStrategy(TestCase):
    """Test basic strat
    """

    @classmethod
    def setUpClass(self):
        self.deck = Deck(1)
        self.deck.shuffle()
        self.deck.cut()
        self.strategy = BasicStrategy(self.deck)

    def test_basic_strat_normal_hit(self):
        """Test with hit scenario
        """
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "4"))
        player_hand.add_card(Card("Clubs", "4"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "Q"))
        dealer_hand.add_card(Card("Clubs", "10"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)

    def test_basic_strat_normal_hit_two(self):
        """Test with hit scenario 2 (border edge of chart)
        """
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "J"))
        player_hand.add_card(Card("Clubs", "6"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "7"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)

    def test_basic_strat_normal_stand(self):
        """Test with stand scenario (border edge of chart)
        """
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "J"))
        player_hand.add_card(Card("Clubs", "6"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "6"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertEqual(len(player_hand.cards), 2)

    def test_basic_strat_split(self):
        """Test split
        """
        strategy = BasicStrategy(self.deck)
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "A"))
        player_hand.add_card(Card("Clubs", "A"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "9"))

        cont_playing = strategy.play_hand(SPLIT, player_hand, dealer_hand)
        self.assertEqual(len(strategy.split_hands), 2)
        self.assertEqual(cont_playing, True)
        self.assertEqual(strategy.cont_split, False)

    def test_basic_strat_split_nonace(self):
        """Test split non-ace
        """
        strategy = BasicStrategy(self.deck)
        player_hand = Hand()
        player_hand.add_card(Card("Spades", "3"))
        player_hand.add_card(Card("Clubs", "3"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "3"))

        is_playing = strategy.play_hand(SPLIT, player_hand, dealer_hand)
        self.assertEqual(len(strategy.split_hands), 2)
        self.assertEqual(is_playing, True)

    def test_basic_strat_double_1(self):
        """Test double down 1
        """
        player_hand = Hand()
        player_hand.add_bet(2.0)
        player_hand.add_card(Card("Spades", "A"))
        player_hand.add_card(Card("Clubs", "2"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "5"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)
        self.assertEqual(player_hand.bet, 4.0)

    def test_basic_strat_double_2(self):
        """Test double down 2
        """
        player_hand = Hand()
        player_hand.add_bet(2.0)
        player_hand.add_card(Card("Spades", "A"))
        player_hand.add_card(Card("Clubs", "3"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "5"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)
        self.assertEqual(player_hand.bet, 4.0)

    def test_basic_strat_double_hit(self):
        """Test double down 2
        """
        player_hand = Hand()
        player_hand.add_bet(2.0)
        player_hand.add_card(Card("Spades", "A"))
        player_hand.add_card(Card("Clubs", "3"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "2"))
        dealer_hand.add_card(Card("Clubs", "4"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)
        self.assertEqual(player_hand.bet, 2.0)

    def test_basic_strat_scen_1(self):
        """Test basic scenario, A, 3, dealer: 6, 10
        """
        player_hand = Hand()
        player_hand.add_bet(2.0)
        player_hand.add_card(Card("Spades", "A"))
        player_hand.add_card(Card("Clubs", "3"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "6"))
        dealer_hand.add_card(Card("Clubs", "10"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)

    def test_basic_strat_scen_2(self):
        """Test basic scenario, A, 3, dealer: 6, 10
        """
        player_hand = Hand()
        player_hand.add_bet(2.0)
        player_hand.add_card(Card("Spades", "A"))
        player_hand.add_card(Card("Clubs", "7"))

        dealer_hand = Hand()
        dealer_hand.add_card(Card("Spades", "6"))
        dealer_hand.add_card(Card("Clubs", "5"))

        self.strategy.play(player_hand, dealer_hand)
        self.assertGreater(len(player_hand.cards), 2)
        self.assertEqual(player_hand.bet, 4.0)
