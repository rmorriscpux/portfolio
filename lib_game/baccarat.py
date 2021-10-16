from .cards import Shoe, Hand
import os, json

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
    def __init__(self, **bets):
        self.shoe = Shoe(8)
        self.player = Bacc_Hand()
        self.banker = Bacc_Hand()
        self.bets = bets
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

    # Reset to a full draw shoe. This can be done after every play (continuous shuffle) or once a shoe is exhausted.
    def reset(self):
        self.player.discard_all(self.shoe)
        self.banker.discard_all(self.shoe)
        self.shoe.shuffle()
        self.state = "start"
        return self

    # Burn cards before the game begins.
    def burn(self):
        if self.state == "burn":
            # Burn first card.
            first_burn = self.shoe.draw()
            burn_cards = [first_burn]

            # Burn additional cards
            for i in range(0, first_burn.rank['bj_val']):
                if len(self.shoe.draw_stack) <= 7: # End of shoe.
                    break

                burn_cards.append(self.shoe.draw())

            # Put burn cards in the discard stack.
            self.shoe.discard(*burn_cards)

            self.state = "coup"
        
        return self

    def coup(self):
        if self.state == "coup":
            self.player.draw_card(self.shoe)
            self.banker.draw_card(self.shoe)
            self.player.draw_card(self.shoe)
            self.banker.draw_card(self.shoe)

            # Natural check.
            if self.player.natural or self.banker.natural:
                self.state = "end"
            elif self.player.value <= 5: # No natural, player acts if hand value is 5 or less.
                self.state = "player_turn"
            else: # No natural, player has 6 or 7, stands and go to banker turn.
                self.state = "banker_turn"

        return self

    def player_action(self):
        if self.state == "player_turn" and self.player.value <= 5:
            self.player.draw_card(self.shoe)
            self.state = "banker_turn"

        return self

    def banker_action(self):
        if self.state == "banker_turn":
            banker_draw = False
            if len(self.player.cards) == 2:
                # Player did not draw. Banker draws based on banker hand value.
                if self.banker.value <= 5:
                    banker_draw = True
            else: # Player did draw. Banker draws based on player third card and banker hand value.
                player_draw_card = self.player.cards[2].rank['bacc_val']
                # Banker current total and Player Third Card Conditions
                banker_draw = ((self.banker.value <= 2) or
                    (self.banker.value == 3 and player_draw_card != 8) or
                    (self.banker.value == 4 and player_draw_card >= 2 and player_draw_card <= 7) or
                    (self.banker.value == 5 and player_draw_card >= 4 and player_draw_card <= 7) or
                    (self.banker.value == 6 and player_draw_card >= 6 and player_draw_card <= 7))

            if banker_draw:
                self.banker.draw_card(self.shoe)

            self.state = "end"
        
        return self

    def eval_wins(self):
        if self.state == "end":
            # Banker wins, pay banker bet 1 to 1
            # TODO: Add commission option.
            if self.banker.value > self.player.value and 'banker' in self.bets:
                self.wins['banker'] = self.bets['banker'] * 2

            # Player wins, pay player bet 1 to 1
            if self.player.value > self.banker.value and 'player' in self.bets:
                self.wins['player'] = self.bets['player'] * 2

            # Tie, pay tie bet 8 to 1, return player or banker bets.
            if self.player.value == self.banker.value:
                if 'tie' in self.bets:
                    self.wins['tie'] = self.bets['tie'] * 9
                if 'banker' in self.bets:
                    self.wins['banker'] = self.bets['banker']
                if 'player' in self.bets:
                    self.wins['player'] = self.bets['player']

        return self

if __name__ == "__main__":
    import time
    
    bacc_game = Bacc_Table().reset()

    # Bets placed.
    bacc_game.state = "burn"
    bacc_game.burn().coup()

    if bacc_game.state == "player_turn":
        bacc_game.print_table()
        bacc_game.player_action()
        time.sleep(1)

    if bacc_game.state == "banker_turn":
        bacc_game.print_table()
        bacc_game.banker_action()
        if len(bacc_game.banker.cards) == 3:
            time.sleep(1)
        
    bacc_game.print_table()