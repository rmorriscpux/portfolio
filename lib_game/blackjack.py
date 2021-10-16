from .cards import Card, Shoe, Hand

class BJ_Hand(Hand):
    # Hard value: Total value of all cards in hand.
    @property
    def hard_value(self):
        total = 0
        for card in self.cards:
            total += card.rank['bj_value']
        return total

    # Soft value: Value of hand if an ace is in it. Doubles as final value.
    @property
    def soft_value(self):
        # Soft value is always the hard value if the hard value is greater than 11.
        if self.hard_value > 11:
            return self.hard_value
        # Check if the hand has an ace.
        for card in self.cards:
            if card.rank['name'] == "Ace":
                return self.hard_value + 10
        # No ace in hand. Return hard value.
        return self.hard_value

    # Value string for display.
    def print_value(self):
        return f"{self.hard_value}" if self.hard_value == self.soft_value else f"{self.hard_value}/{self.soft_value}"

class Dealer_Hand(BJ_Hand):
    # Constructor
    def __init__(self):
        self.facedown_card = None
        Hand.__init__(self)

    # Print String
    def __str__(self):
        out_str = ""
        if self.facedown_card != None:
            out_str = "## "
        out_str = out_str + Hand.__str__(self)
        return out_str

    def rebuild(self, hand_dict):
        self.facedown_card = hand_dict['facedown_card']
        Hand.rebuild(hand_dict)
        return self