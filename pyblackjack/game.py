from .deck import Deck
from .hand import Hand
from .strategy import DealerStrategy


class Game():
    """Blackjack game
    Args:
        num_decks: number of decks to use in the game
        shuffle_perc: percentage at which deck should be shuffled
        player_strategy: strategy for player to inject
    """

    def __init__(self, num_decks, shuffle_perc, player_strategy):
        self.num_decks = num_decks
        self.shuffle_perc = shuffle_perc
        self.player_strategy = player_strategy

    def play(self):
        """Play a single game
        Returns outcome of game for player, 0, 1, 2 (DRAW, WIN, LOSS)
        """
        #print()
        #print("----New game----")

        # Initialize deck
        self.deck = Deck(num_decks=self.num_decks)
        self.deck.shuffle()

        # Initialize strategies
        self.dealer_strategy = DealerStrategy(self.deck)
        self.player_strategy.deck = self.deck

        # Initialize hands
        self.player_hand = Hand()
        self.dealer_hand = Hand(is_dealer=True)

        # Deal initial cards
        for i in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

        #print("Your hand is:")
        #self.player_hand.display()
        #print()
        #print("Dealer's hand is:")
        #self.dealer_hand.display()

        game_result = 0
        player_has_blackjack, dealer_has_blackjack = self.check_blackjack(
            self.player_hand, self.dealer_hand)

        if player_has_blackjack or dealer_has_blackjack:
            if player_has_blackjack and dealer_has_blackjack:
                #print("Tie!")
                game_result = 0
            elif player_has_blackjack:
                #print("You Win!")
                game_result = 1
            elif dealer_has_blackjack:
                #print("Dealer Wins!")
                game_result = 2
            return game_result

        self.player_strategy.play(self.player_hand, self.dealer_hand.cards[1])
        if self.check_bust(self.player_hand):
            game_result = 2
            #self.display_results(self.dealer_hand, self.player_hand)
            return game_result
        
        self.dealer_strategy.play(self.dealer_hand)
        if self.check_bust(self.dealer_hand):
            game_result = 1
            #self.display_results(self.dealer_hand, self.player_hand)
            return game_result

        if self.player_hand.get_value() > self.dealer_hand.get_value():
            #print("You Win!")
            game_result = 1
        elif self.player_hand.get_value() == self.dealer_hand.get_value():
            #print("Tie!")
            game_result = 0
        else:
            #print("Dealer Wins!")
            game_result = 2
        #print()
        #self.display_results(self.dealer_hand, self.player_hand)
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

    def display_results(self, dealer_hand, player_hand):
        print("Final Results")
        print("Player's hand:", player_hand.get_value())
        print("Player's cards: ", str(player_hand.cards))
        print("Dealer's hand:", dealer_hand.get_value())
        print("Dealer's cards: ", str(dealer_hand.cards))
