import random

RANKS = {
    'Ace'   : {'name' : "Ace",   'rank' : 13, 'bj_val' : 1,  'bacc_val' : 1, 'shorthand' : 'A'},
    'King'  : {'name' : "King",  'rank' : 12, 'bj_val' : 10, 'bacc_val' : 0, 'shorthand' : 'K'},
    'Queen' : {'name' : "Queen", 'rank' : 11, 'bj_val' : 10, 'bacc_val' : 0, 'shorthand' : 'Q'},
    'Jack'  : {'name' : "Jack",  'rank' : 10, 'bj_val' : 10, 'bacc_val' : 0, 'shorthand' : 'J'},
    'Ten'   : {'name' : "Ten",   'rank' : 9,  'bj_val' : 10, 'bacc_val' : 0, 'shorthand' : 'T'},
    'Nine'  : {'name' : "Nine",  'rank' : 8,  'bj_val' : 9,  'bacc_val' : 9, 'shorthand' : '9'},
    'Eight' : {'name' : "Eight", 'rank' : 7,  'bj_val' : 8,  'bacc_val' : 8, 'shorthand' : '8'},
    'Seven' : {'name' : "Seven", 'rank' : 6,  'bj_val' : 7,  'bacc_val' : 7, 'shorthand' : '7'},
    'Six'   : {'name' : "Six",   'rank' : 5,  'bj_val' : 6,  'bacc_val' : 6, 'shorthand' : '6'},
    'Five'  : {'name' : "Five",  'rank' : 4,  'bj_val' : 5,  'bacc_val' : 5, 'shorthand' : '5'},
    'Four'  : {'name' : "Four",  'rank' : 3,  'bj_val' : 4,  'bacc_val' : 4, 'shorthand' : '4'},
    'Three' : {'name' : "Three", 'rank' : 2,  'bj_val' : 3,  'bacc_val' : 3, 'shorthand' : '3'},
    'Two'   : {'name' : "Two",   'rank' : 1,  'bj_val' : 2,  'bacc_val' : 2, 'shorthand' : '2'},
}

SUITS = {
    'Spade'   : {'name' : "Spade",   'symbol' : "♠"},
    'Club'    : {'name' : "Club",    'symbol' : "♣"},
    'Heart'   : {'name' : "Heart",   'symbol' : "♥"},
    'Diamond' : {'name' : "Diamond", 'symbol' : "♦"},
}

class Card:
    # Constructor
    def __init__(self, _rank, _suit):
        # Check input
        if _rank not in RANKS.keys():
            raise ValueError(f"{_rank} is not a valid card rank.")
        if _suit not in SUITS.keys():
            raise ValueError(f"{_suit} is not a valid card suit.")
        self.rank = RANKS[_rank]
        self.suit = SUITS[_suit]

    # Print String
    def __str__(self):
        return self.rank['shorthand'] + self.suit['symbol']

    @property
    def color(self):
        if self.suit['name'] == "Spade" or self.suit['name'] == "Club":
            return "Black"
        elif self.suit['name'] == "Heart" or self.suit['name'] == "Diamond":
            return "Red"
        else:
            return "Colorless"

class Shoe:
    # Constructor
    def __init__(self, num_decks=1):
        # Check input
        if not isinstance(num_decks, int):
            raise TypeError("num_decks must be of type <int>")
        if num_decks < 1:
            raise ValueError("Number of decks must be 1 or more.")
        # Put In Values.
        self.draw_stack = []
        self.discard_stack = []
        # Fill draw stack.
        for i in range(0, num_decks):
            for rank in RANKS.keys():
                for suit in SUITS.keys():
                    self.draw_stack.append(Card(rank, suit))

    # Rebuild from JSON formatted dictionary.
    def rebuild(self, shoe_dict):
        self.draw_stack = []
        self.discard_stack = []
        for c in shoe_dict['draw_stack']:
            self.draw_stack.append(Card(c['rank']['name'], c['suit']['name']))
        for c in shoe_dict['discard_stack']:
            self.discard_stack.append(Card(c['rank']['name'], c['suit']['name']))

        return self

    # Shuffle all cards in draw_stack and discard_stack into a new draw_stack.
    def shuffle(self):
        self.draw_stack.extend(self.discard_stack)
        self.discard_stack.clear()

        random.shuffle(self.draw_stack)
        return self

    # Draw a card from the draw_stack
    def draw(self):
        # Add error handling for when draw stack is empty?
        return self.draw_stack.pop(0)

    # Add to discard stack
    def discard(self, *cards):
        if len(cards) == 0:
            return self
        # Check that all the passed variables are of type Card.
        if not all(list(map(lambda c: isinstance(c, Card), cards))):
            raise TypeError("All arguments must be of <class 'Card'>")
        # Add to the discard pile.
        for c in cards:
            self.discard_stack.append(c)
        return self

class Hand:
    # Constructor
    def __init__(self):
        self.cards = []

    # Print String
    def __str__(self):
        out_str = ""
        for card in self.cards:
            out_str = out_str + str(card) + " "
        return out_str.strip()

    # Rebuild from JSON-formatted string.
    def rebuild(self, hand_dict):
        self.cards = []
        for c in hand_dict['cards']:
            self.cards.append(Card(c['rank']['name'], c['suit']['name']))
        return self

    # Draw cards from a game shoe.
    def draw_card(self, game_shoe, num_cards=1):
        if not isinstance(game_shoe, Shoe):
            raise TypeError("Hand draw_card method requires argument of <class 'Shoe'>")
        # TODO: Add value check for num_cards.
        for i in range(0, num_cards):
            self.cards.append(game_shoe.draw())
        return self

    # Discard selected cards to a game shoe, removing them from the hand. (assume card_idx list is pre-sorted for now)
    def discard(self, game_shoe, *card_idx):
        if not isinstance(game_shoe, Shoe):
            raise TypeError("Hand draw_card method requires argument of <class 'Shoe'>")
        if len(card_idx) == 0:
            return self
        # Check that all values in in card_idx are within the size of the hand.
        if not all(list(map(lambda i: i >= 0 and i < len(self.cards), card_idx))):
            raise ValueError("Index values not within size of hand.")
        # Move discarded cards to discard_list.
        discard_list = []
        for index in card_idx:
            discard_list.append(self.cards.pop(index-len(discard_list)))
        # Add to discard pile.
        game_shoe.discard(*discard_list)
        
        return self

    # Discard all cards to a game shoe, removing them from the hand.
    def discard_all(self, game_shoe):
        if not isinstance(game_shoe, Shoe):
            raise TypeError("Hand draw_card method requires argument of <class 'Shoe'>")
        game_shoe.discard(*self.cards)
        self.cards.clear()
        return self