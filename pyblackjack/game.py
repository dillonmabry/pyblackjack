from .deck import Deck
from .hand import Hand
from .strategy import DealerStrategy, BasicStrategy, SimpleStrategy

class Game():
    """Blackjack game
    Args:
        deck: finalized deck to use
        player_strategy: strategy for player to inject, "basic", "basic_alt", or "simple"
    """

    def __init__(self, deck, player_strategy):
        self.deck = deck
        self.player_strategy = player_strategy
        self.dealer_strategy = DealerStrategy(self.deck)
        self.default_bet = 5.0
        self.game_info = {"wins": 0, "ties": 0, "losses": 0, "earnings": 0}
        self.has_split = False

    def calculate_results(self, player_hand, dealer_hand):
        """Calculate result of game with specific hands
        Args:
            player_hand: initial player hand
            dealer_hand: dealer_hand (visible)
        Play game and calculate results
        """

        # Re-calculate decks to ensure latest
        self.dealer_strategy.deck = self.deck
        self.player_strategy.deck = self.deck
        # print("player initial hand: " + str(player_hand.cards))
        # print("dealer initial hand: " + str(dealer_hand.cards))

        player_has_blackjack, dealer_has_blackjack = Game.check_inital_blackjack(
            player_hand, dealer_hand)

        if player_has_blackjack or dealer_has_blackjack:
            if player_has_blackjack and dealer_has_blackjack:
                self.game_info["ties"] += 1
                return
            elif player_has_blackjack:
                self.game_info["wins"] += 1
                self.game_info["earnings"] += player_hand.bet
                return
            elif dealer_has_blackjack:
                self.game_info["losses"] += 1
                self.game_info["earnings"] -= player_hand.bet
                return
        self.player_strategy.play(player_hand, dealer_hand)
        # print("player post-strat hand: " + str(player_hand.cards))
        # print("player post-strat split hands: ", self.player_strategy.split_hands)
        # Allow split once, cannot split after first split house rules
        if len(self.player_strategy.split_hands) > 0 and not self.has_split:
            self.has_split = True
            for s_hand in self.player_strategy.split_hands:
                # Reset game info and continue splitting
                self.game_info["ties"] = 0
                self.game_info["wins"] = 0
                self.game_info["losses"] = 0
                self.game_info["earnings"] = 0
                self.calculate_results(s_hand, dealer_hand)
        if Game.check_bust(player_hand):
            self.game_info["losses"] += 1
            self.game_info["earnings"] -= player_hand.bet
            return

        self.dealer_strategy.play(dealer_hand)
        # print("dealer post-strat hand: " + str(dealer_hand.cards))
        if Game.check_bust(dealer_hand):
            self.game_info["wins"] += 1
            self.game_info["earnings"] += player_hand.bet
            return

        if player_hand.get_value() == dealer_hand.get_value():
            self.game_info["ties"] += 1
            return
        elif player_hand.get_value() > dealer_hand.get_value():
            self.game_info["wins"] += 1
            self.game_info["earnings"] += player_hand.bet
            return
        else:
            self.game_info["losses"] += 1
            self.game_info["earnings"] -= player_hand.bet
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
        print("Total wins: {0}".format(str(self.game_info["wins"])))
        print("Total ties: {0}".format(str(self.game_info["ties"])))
        print("Total losses: {0}".format(str(self.game_info["losses"])))
        print("Total earnings: {0}".format(str(self.game_info["earnings"])))
