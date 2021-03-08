"""Module for games"""
import logging
from .hand import Hand
from .strategy import DealerStrategy

WIN = 1
LOSS = 0


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
        self.game_info = {"wins": 0, "ties": 0, "losses": 0, "earnings": 0.0}
        self.has_split = False

    def calculate_earnings(self, player_hand, result, dealer_bust):
        """Return earnings
        Payouts are 3-2 for standard casino rules if player has an "natural" win
        Args:
            player_hand: player hand
            result: result of hand
            dealer_bust: did dealer bust
        Returns earnings payout
        """
        if any(c.value in ['A', 'J', 'Q', 'K'] for c in player_hand.cards) \
                and result == WIN \
                and dealer_bust is False:
            return player_hand.bet * 1.5
        return player_hand.bet

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
        logging.debug("Player initial hand: %s", str(player_hand.cards))
        logging.debug("Dealer initial hand: %s", str(dealer_hand.cards))

        player_has_blackjack, dealer_has_blackjack = Game.check_inital_blackjack(
            player_hand, dealer_hand)

        if player_has_blackjack or dealer_has_blackjack:
            if player_has_blackjack and dealer_has_blackjack:
                self.game_info["ties"] += 1
                return
            if player_has_blackjack:
                self.game_info["wins"] += 1
                self.game_info["earnings"] += self.calculate_earnings(
                    player_hand, WIN, False)
                return
            if dealer_has_blackjack:
                self.game_info["losses"] += 1
                self.game_info["earnings"] -= self.calculate_earnings(
                    player_hand, LOSS, False)
                return
        self.player_strategy.play(player_hand, dealer_hand)
        logging.debug("Player post-strat hand: %s", str(player_hand.cards))
        # Allow split once, cannot split after first split house rules
        if len(self.player_strategy.split_hands) > 0 and not self.has_split:
            self.has_split = True
            for s_hand in self.player_strategy.split_hands:
                logging.debug("Player post-strat split hand: %s",
                              str(s_hand.cards))
                # Reset game info and continue splitting
                self.game_info["ties"] = 0
                self.game_info["wins"] = 0
                self.game_info["losses"] = 0
                self.game_info["earnings"] = 0
                self.calculate_results(s_hand, dealer_hand)
        if Game.check_bust(player_hand):
            self.game_info["losses"] += 1
            self.game_info["earnings"] -= self.calculate_earnings(
                player_hand, LOSS, False)
            return

        self.dealer_strategy.play(dealer_hand)
        logging.debug("Dealer post-strat hand: %s", str(dealer_hand.cards))
        if Game.check_bust(dealer_hand):
            self.game_info["wins"] += 1
            self.game_info["earnings"] += self.calculate_earnings(
                player_hand, WIN, True)
            return

        if player_hand.get_value() == dealer_hand.get_value():
            self.game_info["ties"] += 1
            return
        if player_hand.get_value() > dealer_hand.get_value():
            self.game_info["wins"] += 1
            self.game_info["earnings"] += self.calculate_earnings(
                player_hand, WIN, False)
            return

        self.game_info["losses"] += 1
        self.game_info["earnings"] -= self.calculate_earnings(
            player_hand, LOSS, False)
        return

    def play(self):
        """Play a game
        Returns game obj with stats
        """
        # Initialize hands
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        # Deal initial cards
        for _ in range(2):
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
        return bool(hand.get_value() == 21)

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
        return bool(hand.get_value() > 21)

    def display_results(self):
        """Print results of game
        """
        logging.debug("Total wins: %s", str(self.game_info["wins"]))
        logging.debug("Total ties: %s", str(self.game_info["ties"]))
        logging.debug("Total losses: %s", str(self.game_info["losses"]))
        logging.debug("Total earnings: %s", str(self.game_info["earnings"]))
