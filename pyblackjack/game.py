from .deck import Deck
from .hand import Hand
from .strategy import DealerStrategy, BasicStrategy

class Game():
    """Blackjack game
    Args:
        deck: finalized deck to use
        player_strategy: strategy for player to inject
    """

    def __init__(self, deck, player_strategy):
        self.deck = deck
        self.player_strategy = player_strategy
        self.earnings = 0.0
        self.default_bet = 5.0
        self.ties = 0
        self.wins = 0
        self.losses = 0
        self.game_info = {"wins": 0, "ties": 0, "losses": 0, "earnings": 0}
        self.has_split = False

    def calculate_results(self, player_hand, dealer_hand):
        """Calculate result of game with specific hands
        Args:
            player_hand: initial player hand
            dealer_hand: dealer_hand (visible)
        Play game and calculate results
        """

        # Initialize strategies
        self.dealer_strategy = DealerStrategy(self.deck)
        self.player_strategy.deck = self.deck

        player_has_blackjack, dealer_has_blackjack = Game.check_inital_blackjack(
            player_hand, dealer_hand)

        if player_has_blackjack or dealer_has_blackjack:
            if player_has_blackjack and dealer_has_blackjack:
                self.ties += 1
                return
            elif player_has_blackjack:
                self.wins += 1
                self.earnings += player_hand.bet
                return
            elif dealer_has_blackjack:
                self.losses += 1
                self.earnings -= player_hand.bet
                return
        self.player_strategy.play(player_hand, dealer_hand)

        # Allow split once, cannot split after first split house rules
        if len(self.player_strategy.split_hands) > 0 and not self.has_split:
            self.has_split = True
            for s_hand in self.player_strategy.split_hands:
                # Reset game info and continue splitting
                self.ties = 0
                self.wins = 0
                self.losses = 0
                self.earnings = 0
                self.calculate_results(s_hand, dealer_hand)
        if Game.check_bust(player_hand):
            self.losses += 1
            self.earnings -= player_hand.bet
            return

        self.dealer_strategy.play(dealer_hand)
        if Game.check_bust(dealer_hand):
            self.wins += 1
            self.earnings += player_hand.bet
            return

        if player_hand.get_value() == dealer_hand.get_value():
            self.ties += 1
            return
        elif player_hand.get_value() > dealer_hand.get_value():
            self.wins += 1
            self.earnings += player_hand.bet
            return
        else:
            self.losses += 1
            self.earnings -= player_hand.bet
            return

    def play(self):
        """Play a game
        Returns game obj with stats
        """
        # Initialize hands
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        # Deal initial cards
        for i in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

        # Intialize default bets
        self.player_hand.add_bet(self.default_bet)

        self.calculate_results(self.player_hand, self.dealer_hand)

    @staticmethod
    def check_blackjack(hand):
        """Check hand for blackjack
        Args:
            hand: hand to check
        """
        if hand.get_value() == 21:
            return True
        else:
            return False

    @staticmethod
    def check_inital_blackjack(player_hand, dealer_hand):
        """Check if player or dealer has blackjack
        Args:
            player_hand: hand of player
            dealer_hand hand of dealer
        Returns if player_has_blackjack, dealer_has_blackjack
        """
        player_has_blackjack, dealer_has_blackjack = False, False
        if Game.check_blackjack(player_hand):
            player_has_blackjack = True
        if Game.check_blackjack(dealer_hand):
            dealer_has_blackjack = True
        return player_has_blackjack, dealer_has_blackjack

    @staticmethod
    def check_bust(hand):
        """Check for bust
        Args:
            hand: hand to check
        """
        if hand.get_value() > 21:
            return True
        else:
            return False

    def display_results(self):
        """Print results of game
        """
        print("Total wins: {0}".format(str(self.wins)))
        print("Total ties: {0}".format(str(self.ties)))
        print("Total losses: {0}".format(str(self.losses)))
        print("Total earnings: {0}".format(str(self.earnings)))
