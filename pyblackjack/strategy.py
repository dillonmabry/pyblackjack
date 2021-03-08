"""Module for strategies"""

import json
import pkg_resources as pkg
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
        self.split_hands = []

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

    def __init__(self, deck, **kwargs):
        self.deck = deck
        self.split_hands = []
        self.cont_split = True
        strat_file = kwargs.get('strat_file', None)
        strategy_path = 'resources/strategies/{0}.json'.format(
            strat_file) if strat_file is not None else 'resources/strategies/basic_strategy.json'
        try:
            with open(pkg.resource_filename('pyblackjack', strategy_path), 'r') as resource:
                self.lookup_table = json.load(resource)
        except Exception as ex:
            raise ex

    @classmethod
    def lookup(cls, dict_lookup, dealer_card):
        """Lookup strat based on scenario
        Args:
            dict_lookup: original dict lookup
            dealer_card: known card of dealer to compare
        Returns strat to use (Hit, Stand, Split, Double-Down)
        """
        if isinstance(dict_lookup, str):
            return dict_lookup
        for i in dict_lookup.keys():
            if dealer_card.get_value() == int(i):
                return dict_lookup[i]

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
        if strat == HIT:  # Hit
            hand.add_card(self.deck.deal())
            return True
        if strat == SPLIT:  # Split
            if len(self.split_hands) > 0:  # Cannot split further after single split
                return False
            if hand.cards[0].value == "A" and hand.cards[1].value == "A":
                self.cont_split = False
            hand_1 = Hand()
            hand_2 = Hand()
            hand_1.add_card(hand.cards[0])
            hand_2.add_card(hand.cards[1])

            hand_1.add_card(self.deck.deal())
            hand_2.add_card(self.deck.deal())

            hand_1.bet = hand.bet
            hand_2.bet = hand.bet

            self.split_hands.append(hand_1)
            self.split_hands.append(hand_2)

            return True
        if strat == DOUBLE:  # Double Down (if first hand)
            if len(hand.cards) == 2:
                if hand.bet:
                    hand.bet = hand.bet * 2
                hand.add_card(self.deck.deal())
                return False

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
        while is_playing and hand.get_value() <= 21 and self.cont_split:
            # Two same cards
            if len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
                tbl = self.lookup_table['BasicStrategy']['Pairs']
                strat = BasicStrategy.lookup(
                    tbl[str(hand.cards[0].get_value())], dealer_hand.cards[1])
                is_playing = self.play_hand(strat, hand, dealer_hand)
            # Has Ace
            elif len(hand.cards) == 2 \
                and (hand.cards[0].value == "A"
                     or hand.cards[1].value == "A"):
                tbl = self.lookup_table['BasicStrategy']['Ace']
                non_ace = hand.cards[0]
                if hand.cards[0].value == "A":
                    non_ace = hand.cards[1]
                strat = BasicStrategy.lookup(
                    tbl[str(non_ace.get_value())], dealer_hand.cards[1])
                is_playing = self.play_hand(strat, hand, dealer_hand)
            # Normal lookup
            else:
                tbl = self.lookup_table['BasicStrategy']['Other']
                hand_value = str(hand.get_value())
                strat = BasicStrategy.lookup(tbl[hand_value], dealer_hand.cards[1])
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
