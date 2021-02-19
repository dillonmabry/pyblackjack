from .deck import Deck
from .hand import Hand
from .strategy import DealerStrategy


class Game():
    """Blackjack game
    Args:
        deck: finalized deck to use
        player_strategy: strategy for player to inject
        pool: pool size
    """

    def __init__(self, deck, player_strategy, pool):
        self.deck = deck
        self.player_strategy = player_strategy
        self.pool = pool

    def play(self):
        """Play a single game
        Returns outcome of game for player, 0, 1, 2 (DRAW, WIN, LOSS)
        """

        # Initialize strategies
        self.dealer_strategy = DealerStrategy(self.deck)
        self.player_strategy.deck = self.deck

        # Initialize hands
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        # Deal initial cards
        for i in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())
        
        game_result = 0
        player_has_blackjack, dealer_has_blackjack = self.check_blackjack(
            self.player_hand, self.dealer_hand)

        if player_has_blackjack or dealer_has_blackjack:
            if player_has_blackjack and dealer_has_blackjack:
                game_result = 0
            elif player_has_blackjack:
                game_result = 1
            elif dealer_has_blackjack:
                game_result = 2
            return game_result

        self.player_strategy.play(self.player_hand, self.dealer_hand.cards[1])
        if self.check_bust(self.player_hand):
            game_result = 2
            return game_result

        self.dealer_strategy.play(self.dealer_hand)
        if self.check_bust(self.dealer_hand):
            game_result = 1
            return game_result

        if self.player_hand.get_value() == self.dealer_hand.get_value():
            game_result = 0
        elif self.player_hand.get_value() > self.dealer_hand.get_value():
            game_result = 1
        else:
            game_result = 2

        return game_result

    def check_blackjack(self, player_hand, dealer_hand):
        """Check if player or dealer has blackjack
        Args:
            player_hand: hand of player
            dealer_hand hand of dealer
        Returns if player_has_blackjack, dealer_has_blackjack
        """
        player_has_blackjack, dealer_has_blackjack = False, False
        if player_hand.get_value() == 21:
            player_has_blackjack = True
        if dealer_hand.get_value() == 21:
            dealer_has_blackjack = True
        return player_has_blackjack, dealer_has_blackjack

    def check_bust(self, hand):
        """Check for bust
        Args:
            hand: hand to check
        """
        if hand.get_value() > 21:
            return True
        else:
            return False

    def display_results(self, result):
        """Print results of game
        Args:
            result: result value to display
        """
        if result == 0:
            print("Tie!")
        elif result == 1:
            print("Player wins!")
        elif result == 2:
            print("Dealer wins!")

        print("Final Results")
        print("Player's hand:", self.player_hand.get_value())
        print("Player's cards: ", str(self.player_hand.cards))
        print("Dealer's hand:", self.dealer_hand.get_value())
        print("Dealer's cards: ", str(self.dealer_hand.cards))
