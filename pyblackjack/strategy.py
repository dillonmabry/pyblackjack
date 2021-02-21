import json
import pkg_resources
from .hand import Hand

STAND = "St"
SPLIT = "Sp"
HIT = "H"
DOUBLE = "D"


class SimpleStrategy():
    """Simplest strategy possible
    Stand 12 or over
    Args:
        deck: deck of cards to deal from
    """

    def __init__(self, deck):
        self.deck = deck

    def play(self, hand, dealer_hand):
        """Play strategy
        Adds cards to hand based on strategy
        Args:
            hand: hand to use with strategy
            dealer_hand: shown dealer card to use with strategy
        """
        while hand.get_value() < 13 and hand.get_value() <= 21:
            if hand.get_value() == 12:
                break

            hand.add_card(self.deck.deal())


class BasicStrategy():
    """Basic 21 strategy as noted by experts
    Args:
        deck: deck of cards to deal from
    """

    def __init__(self, deck):
        self.deck = deck
        self.split_hands = []
        try:
            with open(pkg_resources.resource_filename('pyblackjack', 'resources/strategy.json'), 'r') as f:
                self.lookup_table = json.load(f)
        except Exception:
            raise

    def lookup(self, d, dealer_card):
        """Lookup strat based on scenario
        Args:
            d: original key lookup
            dealer_card: known card of dealer to compare
        Returns strat to use (Hit, Stand, Split, Double-Down)
        """
        if type(d) == str:
            return d
        for i in d.keys():
            if dealer_card.get_value() == int(i):
                return d[i]

    def play_hand(self, strat, hand, dealer_hand):
        """Play hand based on strat input
        Args:
            strat: user input decided on strategy
            hand: hand to play/modify
            dealer_hand: dealer hand to utilize
        Returns is_playing to continue
        """
        if strat == STAND:  # Stand
            return False
        elif strat == HIT:  # Hit
            hand.add_card(self.deck.deal())
            return True
        elif strat == SPLIT:  # Split (if cards are identical)
            is_playing = True
            if hand.cards[0].value == "A" and hand.cards[1].value == "A":
                is_playing = False

            h1 = Hand()
            h2 = Hand()
            h1.add_card(hand.cards[0])
            h2.add_card(hand.cards[1])

            h1.add_card(self.deck.deal())
            h2.add_card(self.deck.deal())

            h1.bet = hand.bet
            h2.bet = hand.bet

            self.split_hands.append(h1)
            self.split_hands.append(h2)

            return is_playing
        elif strat == DOUBLE:  # Double Down (if first hand)
            if len(hand.cards) == 2:
                if hand.bet:
                    hand.bet = hand.bet * 2
                hand.add_card(self.deck.deal())
                return False
            else:
                hand.add_card(self.deck.deal())
                return True

    def play(self, hand, dealer_hand):
        """Play strategy
        Adds cards to hand based on strategy
        Args:
            hand: hand to use with strategy
            dealer_hand: shown dealer card to use with strategy
        """
        is_playing = True
        while is_playing and hand.get_value() <= 21:
            # Two same cards
            if len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
                tbl = self.lookup_table['BasicStrategy']['Pairs']
                strat = self.lookup(
                    tbl[str(hand.cards[0].get_value())], dealer_hand.cards[1])
                is_playing = self.play_hand(strat, hand, dealer_hand)
            # Has Ace
            elif len(hand.cards) == 2 and (hand.cards[0].value == "A" or hand.cards[1].value == "A"):
                tbl = self.lookup_table['BasicStrategy']['Ace']
                non_ace = hand.cards[0]
                if hand.cards[0].value == "A":
                    non_ace = hand.cards[1]
                strat = self.lookup(
                    tbl[str(non_ace.get_value())], dealer_hand.cards[1])
                is_playing = self.play_hand(strat, hand, dealer_hand)
            # Normal lookup
            else:
                tbl = self.lookup_table['BasicStrategy']['Other']
                hand_value = str(hand.get_value())
                strat = self.lookup(tbl[hand_value], dealer_hand.cards[1])
                is_playing = self.play_hand(strat, hand, dealer_hand)


class DealerStrategy():
    """Dealer basic casino rules strategy
    If total hand value >= 17, stand
    If total is < 17, must hit
    Continue to take cards until total is >= 17
    If ace would bring total to >= 17, must use as 11

    Args:
        deck: deck of cards to deal from
    """

    def __init__(self, deck):
        self.deck = deck

    def play(self, hand):
        """Play strategy
        Add cards to hand based on strategy
        Args:
            hand: hand to use with strategy
        """
        while hand.get_value() < 18 and hand.get_value() <= 21:
            if hand.get_value() == 17:  # Ace handling strategy already implemented in hand method
                break

            hand.add_card(self.deck.deal())
