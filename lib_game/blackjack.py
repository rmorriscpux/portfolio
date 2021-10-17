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

    # Hand is a blackjack: Ace and 10-value on the first two cards.
    @property
    def blackjack(self):
        return self.soft_value == 21 and len(self.cards) == 2

    # Value string for display.
    def print_value(self):
        return f"{self.hard_value}" if self.hard_value == self.soft_value else f"{self.hard_value}/{self.soft_value}"

class Player_Hand(BJ_Hand):
    # Constructor
    def __init__(self, bet=0):
        self.bet = bet
        Hand.__init__(self)

    def rebuild(self, hand_dict):
        self.bet = hand_dict['bet']
        Hand.rebuild(self, hand_dict)
        return self

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

    # Dealer Blackjack
    @property
    def blackjack(self):
        if self.facedown_card == None:
            return self.soft_value == 21 and len(self.cards) == 2
        else:
            if len(self.cards) == 1:
                return self.cards[0].value + self.facedown_card.value == 21

    # Rebuild from a JSON formatted dictionary.
    def rebuild(self, hand_dict):
        self.facedown_card = hand_dict['facedown_card']
        Hand.rebuild(self, hand_dict)
        return self

    def reveal(self):
        if self.facedown_card != None:
            self.cards.insert(0, self.facedown_card)
            self.facedown_card = None
        return self

    def discard_all(self, game_shoe):
        self.reveal()
        Hand.discard_all(self, game_shoe)
        return self

class BJ_Table:
    # Constructor
    def __init__(self):
        self.shoe = Shoe(6)
        self.player = []
        self.dealer = Dealer_Hand()
        self.side_bets = {}
        self.wins = {}
        self.state = "init"
        self.active_hand = -1

    # Total Bet
    @property
    def total_bet(self):
        total = 0
        for p_hand in self.player:
            total += p_hand.bet
        for b in self.side_bets:
            total += b.value()
        return total

    # Player actions.
    @property
    def actions(self):
        # Default all actions to False.
        action_dict = {
            'hit' : False,
            'stand' : False,
            'double down' : False,
            'split' : False
        }
        if self.state == "player turn" and self.active_hand >= 0 and self.active_hand < len(self.player):
            cur_hand = self.player[self.active_hand]
            # Hit - Current hand is less than 21, and it is not the result of a split ace.
            action_dict['hit'] = cur_hand.value < 21 and not (cur_hand.cards[0]['rank'] == "Ace" and self.active_hand > 0)
            # Stand - Always true on player turn.
            action_dict['stand'] = True
            if len(cur_hand.cards) == 2:
            # Double Down - Current hand is 2 cards valued at 9, 10, or 11.
                action_dict['double_down'] = cur_hand.value >= 9 and cur_hand.value <= 11
            # Split - Current hand is 2 cards of the same rank.
                action_dict['split'] = cur_hand.cards[0].rank == cur_hand.cards[1].rank
        
        return action_dict