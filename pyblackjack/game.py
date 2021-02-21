from .deck import Deck
from .hand import Hand
from .strategy import DealerStrategy, BasicStrategy

TIE = 0
WIN = 1
LOSS = 2


class Game():
    """Blackjack game
    Args:
        deck: finalized deck to use
        player_strategy: strategy for player to inject
    """

    def __init__(self, deck, player_strategy):
        self.deck = deck
        self.player_strategy = player_strategy
        self.pool = 1000
        self.default_bet = 5.0

    def calculate_result(self, player_hand, dealer_hand):
        """Calculate result of game with specific hands
        """
        #print("player hand: " + str(player_hand.cards))
        #print("dealer hand: " + str(dealer_hand.cards))

        # Initialize strategies
        self.dealer_strategy = DealerStrategy(self.deck)
        self.player_strategy.deck = self.deck

        player_has_blackjack, dealer_has_blackjack = Game.check_inital_blackjack(
            player_hand, dealer_hand)

        if player_has_blackjack or dealer_has_blackjack:
            if player_has_blackjack and dealer_has_blackjack:
                return TIE
            elif player_has_blackjack:
                return WIN
            elif dealer_has_blackjack:
                return LOSS
        self.player_strategy.play(player_hand, dealer_hand)
        # print(self.player_strategy.split_hands)
        # if len(self.player_strategy.split_hands) > 0:
        #     for s_hand in self.player_strategy.split_hands:
        #         self.calculate_result(s_hand, dealer_hand)
        if Game.check_bust(player_hand):
            return LOSS

        self.dealer_strategy.play(dealer_hand)
        if Game.check_bust(dealer_hand):
            return WIN

        if player_hand.get_value() == dealer_hand.get_value():
            return TIE
        elif player_hand.get_value() > dealer_hand.get_value():
            return WIN
        else:
            return LOSS

    def play(self):
        """Play a single game
        Returns outcome of game for player, 0, 1, 2 (DRAW, WIN, LOSS)
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

        result = self.calculate_result(self.player_hand, self.dealer_hand)
        return result

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

    def display_results(self, result):
        """Print results of game
        Args:
            result: result value to display
        """
        if result == TIE:
            print("Tie!")
        elif result == WIN:
            print("Player wins!")
        elif result == LOSS:
            print("Dealer wins!")

        print("Final Results")
        print("Player's hand:", self.player_hand.get_value())
        print("Player's cards: ", str(self.player_hand.cards))
        print("Player's bet: ", str(self.player_hand.bet))
        print("Dealer's hand:", self.dealer_hand.get_value())
        print("Dealer's cards: ", str(self.dealer_hand.cards))
