from .cards import Shoe, Hand
import json

class Bacc_Hand(Hand):
    # Baccarat hand value - Total of all card values in hand modulo 10.
    @property
    def value(self):
        total = 0
        for card in self.cards:
            total += card.rank['bacc_val']
        return total % 10

    # Natural - 8 or 9 on the first 2 cards.
    @property
    def natural(self):
        return self.value >= 8 and len(self.cards) == 2

class Bacc_Table:
    def __init__(self):
        self.shoe = Shoe(8)
        self.player = Bacc_Hand()
        self.banker = Bacc_Hand()
        self.bets = {}
        self.wins = {}
        self.state = 'start'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def from_json(self, json_str):
        build_dict = json.loads(json_str)
        # Shoe
        self.shoe.rebuild(build_dict['shoe'])
        # Hands
        self.player.rebuild(build_dict['player'])
        self.banker.rebuild(build_dict['banker'])
        # Status
        self.bets = build_dict['bets']
        self.wins = build_dict['wins']
        self.state = build_dict['state']

        return self

    def print_table(self):
        if os.name == "posix": # Mac/Linux
            os.system("clear")
        else: # Windows
            os.system("cls")

        print(str(self.banker))
        print(self.banker.value)
        print("")
        print(str(self.player))
        print(self.player.value)
        if self.state == "end": # Print Result
            if self.player.value > self.banker.value:
                if self.player.natural:
                    print("Player wins with a natural!")
                else:
                    print("Player wins!")
            elif self.player.value < self.banker.value:
                if self.banker.natural:
                    print("Banker wins with a natural!")
                else:
                    print("Banker wins!")
            else:
                print("Player and Banker Tie!")

        return

if __name__ == "__main__":
    import os, time
    def print_table(player, banker, end=False):
        if os.name == "posix": # Mac/Linux
            os.system("clear")
        else: # Windows
            os.system("cls")

        print(str(banker))
        print(banker.value)
        print("")
        print(str(player))
        print(player.value)
        if end: # Print Result
            if player.value > banker.value:
                if player.natural:
                    print("Player wins with a natural!")
                else:
                    print("Player wins!")
            elif player.value < banker.value:
                if banker.natural:
                    print("Banker wins with a natural!")
                else:
                    print("Banker wins!")
            else:
                print("Player and Banker Tie!")

        return

    player = Bacc_Hand()
    banker = Bacc_Hand()
    game_shoe = Shoe(8)
    game_shoe.shuffle()

    # Burn
    burn_first = game_shoe.draw()

    for i in range(0, burn_first.rank['bj_val']):
        game_shoe.draw()

    # Coup
    player.draw_card(game_shoe)
    banker.draw_card(game_shoe)
    player.draw_card(game_shoe)
    banker.draw_card(game_shoe)

    print_table(player, banker)

    # Natural check
    if not (player.natural or banker.natural):
        # Player Turn. Player draws third card if their total is 5 or less.
        if player.value <= 5:
            time.sleep(1)
            player.draw_card(game_shoe)
            print_table(player, banker)
        
        # Banker Turn
        banker_draw = False
        # When player stands with 2 cards, banker draws third card if their total is 5 or less.
        if len(player.cards) == 2: 
            if banker.value <= 5:
                banker_draw = True
        else:
            player_draw_card = player.cards[2].rank['bacc_val']
            # Banker current total and Player Third Card Conditions
            banker_draw = ((banker.value <= 2) or
                (banker.value == 3 and player_draw_card != 8) or
                (banker.value == 4 and player_draw_card >= 2 and player_draw_card <= 7) or
                (banker.value == 5 and player_draw_card >= 4 and player_draw_card <= 7) or
                (banker.value == 6 and player_draw_card >= 6 and player_draw_card <= 7))
        if banker_draw:
            time.sleep(1)
            banker.draw_card(game_shoe)
    
    print_table(player, banker, True)