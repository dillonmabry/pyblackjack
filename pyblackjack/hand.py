
class Hand():
    """Basic hand of gameplay
    """

    def __init__(self, is_dealer=False):
        self.cards = []
        self.value = 0
        self.is_dealer = is_dealer

    def __str__(self):
        return "".join([card.__str__() for card in self.cards])

    def add_card(self, card):
        """Add card to given hand
        Args:
            card: card to add
        """
        self.cards.append(card)

    def calculate_value(self):
        """Calculate value of the hand
        """
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

    def display(self):
        if self.is_dealer:
            print("hidden")
            print(self.cards[1])
        else:
            for card in self.cards:
                print(card)
            print("Value:", self.get_value())

    def get_value(self):
        """Calculate value of hand
        Returns numeric value of hand
        """
        self.calculate_value()
        return self.value
