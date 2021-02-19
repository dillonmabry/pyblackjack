
class SimpleStrategy():
    """Simplest strategy possible
    Stand 12 or over
    Args:
        deck: deck of cards to deal from
    """

    def __init__(self, deck):
        self.deck = deck

    def play(self, hand, dealer_card):
        """Play strategy
        Adds cards to hand based on strategy
        Args:
            hand: hand to use with strategy
            dealer_card: shown dealer card to use with strategy
        """
        while hand.get_value() < 13:
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

    def lookup(self, d, dealer_hand):
        """Lookup strat based on scenario
        Args:
            d: original key lookup
            dealer_hand: hand of dealer to compare
        Returns strat to use (Hit, Stand, Split, Double-Down)
        """
        if type(d) == str:
            return d
        for i in d.keys():
            if dealer_hand.get_value() >= i:
                return d[i]

    def play(self, hand, dealer_card):
        """Play strategy
        Adds cards to hand based on strategy
        Args:
            hand: hand to use with strategy
            dealer_card: shown dealer card to use with strategy
        """
        # Two same cards
        
        # Has Ace

        # Normal lookup


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
        while hand.get_value() < 18:
            if hand.get_value() == 17:  # Ace handling strategy already implemented in hand method
                break

            hand.add_card(self.deck.deal())
