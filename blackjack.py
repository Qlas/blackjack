from random import shuffle
from subprocess import call

class Croupier:
    def __init__(self):
        self.hand = []
        self.count = 0
        self.hid = 0

    def draw(self, deck):
        card = deck.draw_card()
        self.hand.append(card)
        try:
            self.count += int(card.card_value())
        except ValueError:
            self.count += 11

    def show_hand_hidden(self):
        print("\nCroupier hand is:")
        lines = [self.hand[0].show(),
                 ['┌─────────┐',
                  '│░░░░░░░░░│',
                  '│░░░░░░░░░│',
                  '│░░░░░░░░░│',
                  '│░░░░░░░░░│',
                  '│░░░░░░░░░│',
                  '└─────────┘']]

        for i in range(7):
            a = ""
            for j in range(len(lines)):
                a += lines[j][i]
            print(a)

    def show_hand(self):
        print("\nCroupier hand is:")
        lines = []
        for card in self.hand:
            lines.append(card.show())

        for i in range(7):                                                              #print card in one line
            a = ""
            for j in range(len(lines)):
                a += lines[j][i]
            print(a)
        print(f"Sum: {self.count}")

    def end_game(self, deck, player):
        self.hid = 1
        while self.count < 16 and self.count < player.count:
            self.draw(deck)

    def clear(self):
        self.hand = []
        self.count = 0
        self.hid = 0


class Player:
    def __init__(self):
        self.wallet = 1_000
        self.hand = []
        self.bet = 0
        self.count = 0

    def draw(self, deck):
        card = deck.draw_card()
        self.hand.append(card)
        try:
            self.count += int(card.card_value())
        except ValueError:
            print(f"Your card count is {self.count}")
            x = input("Would you like use Ace like 1 or 11 (wrong type == 1)\n")
            if x == "11":
                self.count += 11
            else:
                self.count += 1

    def show_hand(self):
        print("\nYour hand is:")
        lines = []
        for c in self.hand:
            lines.append(c.show())
        for i in range(7):
            a = ""
            for j in range(len(lines)):
                a += lines[j][i]
            print(a)
        print(f"Sum: {self.count}")

    def clear(self):
        self.hand = []
        self.bet = 0
        self.count = 0


class Card:
    def __init__(self, suit, values):
        self.suit = suit
        self.values = values
    def show(self):
        ranks = {"Jack": "J", "Queen": "Q", "King": "K", "Ace": "A"}
        try:
            rank = ranks[self.values]
        except KeyError:
            rank = self.values
        suit = {"Spades": '♠', "Clubs": '♦', "Diamonds": '♥', "Hearts": '♣'}
        if rank == 10:
            space = ''
        else:
            space = ' '
        lines= ['┌─────────┐',
                '│{}{}       │'.format(rank, space),
                '│         │',
                '│    {}    │'.format(suit[self.suit]),
                '│         │',
                '│       {}{}│'.format(space, rank),
                '└─────────┘']
        return lines

    def card_value(self):
        value = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
                 "Jack": 10, "Queen": 10, "King": 10, "Ace": "A"}
        return value[self.values]


class Deck:
    def __init__(self):
        self.cards = []
        self.decks = 6
        self.build()
        self.deck_shuffle()

    def build(self):
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        suit = ["Spades", "Clubs", "Diamonds", "Hearts"]
        self.cards = [Card(s, v) for v in values for s in suit for _ in range(self.decks)]  #create deck

    def show(self):
        [print(a) for c in self.cards for a in c.show()]                                    #print every cards in deck

    def deck_shuffle(self):
        shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


def check_bet(player):
    bet = 0
    print(f"Your wallet is {player.wallet}")
    while True:
        try:
            bet = int(input("Your bet is?\n"))
        except ValueError:
            print("Wrong number")
            continue
        if bet > player.wallet or bet <= 0:
            print("your bet must be lower than your wallet and greater than 0")
        else:
            break
    player.wallet -= bet
    player.bet = bet


def show(player, croupier):
    call('cls', shell=True)
    print(f"Wallet: {player.wallet}\nbet: {player.bet}")
    if len(player.hand) > 0:
        player.show_hand()
    if len(croupier.hand) > 0:
        if croupier.hid == 0:
            croupier.show_hand_hidden()
        else:
            croupier.show_hand()


def decision(player, dec):
    while True:
        if len(player.hand) == 2:
            deci = input("\nWhat do you want to do?\nh - hit\ns - stand\nd - double down\n").lower()
            if deci == 'd':
                if player.wallet >= player.bet:
                    player.draw(dec)
                    player.wallet -= player.bet
                    player.bet *= 2
                    return True
                else:
                    print("You don't have enough money")
                    continue
        else:
            deci = input("\nWhat do you want to do?\nh - hit\ns - stand\n").lower()
        if deci == 'h':
            player.draw(dec)
            break
        elif deci == 's':
            return True
        print("Wrong symbol")


def new_game(player, dec, croupier):
    if len(dec.cards) < 200:
        dec.build()
    check_bet(player)
    player.draw(dec)
    player.draw(dec)
    croupier.draw(dec)
    croupier.draw(dec)
    dec.deck_shuffle()


def end_game(player, croupier, dec):
    call('cls', shell=True)
    player1.show_hand()
    croupier1.show_hand()
    print()

    if player.count > 21 or player.count < croupier.count <= 21:
        print("You lose :(")
    elif player.count == croupier.count:
        print("Draw")
        player.wallet += player.bet
    else:
        print("You Won")
        player.wallet += player.bet * 2

    if player1.wallet == 0 or input("Again?\n(n - no, any other - yes)").lower() == 'n':
        print(f"Your wallet is:{player.wallet}")
        return True
    else:
        player.clear()
        croupier.clear()
        new_game(player, dec, croupier)


def game(player, dec, croupier):                                                       # main game loop
    new_game(player, dec, croupier)
    while True:
        show(player, croupier)
        if decision(player, dec) or player.count > 21:
            croupier.end_game(dec, player)
            show(player, croupier)
            if end_game(player, croupier, dec):
                break

call('cls', shell=True)
player1 = Player()
dec1 = Deck()
croupier1 = Croupier()
print("Lets the game begin.")
game(player1, dec1, croupier1)


