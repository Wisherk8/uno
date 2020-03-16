import random
from coloda import Coloda



class Game:
    def __init__(self, players):
        self.players = []
        for player in range(players):
            self.players.append(Player())


        self.coloda = Coloda()
        self.card_on_table = None
        self.turn = 0
        self.direct = True
        self.has_get_card = False
        self.gameover = False

        for player in self.players:
            for count in range(0, 7):
                self.get_card(player)

        self.card_on_table = self.coloda.get_card()

    def get_card(self, player):
        card = self.coloda.get_card()
        player.cards.append(card)

    def put_card(self, player, card, new_color):
        if card.color == 5:
            if new_color not in range(1,5):
                return False
            self.card_on_table.color = new_color
            self.card_on_table.value = card.value
            player.cards.remove(card)
            if card.value == 14: # +4

                print("Следующий игрок берет 4 карты и пропускает ход")
                self.next_turn()
                print(len(self.players[self.turn].cards))
                self.get_card(game.players[self.turn])
                self.get_card(game.players[self.turn])
                self.get_card(game.players[self.turn])
                self.get_card(game.players[self.turn])
                print(len(self.players[self.turn].cards))
        elif card.value == self.card_on_table.value or card.color == self.card_on_table.color:
            self.card_on_table = card
            player.cards.remove(card)
            if card.value == 11: # проверка и логика реверса
                print("Reverse!!!")
                self.direct = not self.direct
            elif card.value == 10: # проверка и логика пропуска хода
                print(f"Пропуск хода для игрока {game.turn}")
                self.next_turn()
            elif card.value == 12: # проверка +2 цветной
                print("Следующий игрок берет 2 карты и пропускает ход")
                self.next_turn()
                print(len(self.players[self.turn].cards))
                self.get_card(self.players[game.turn])
                self.get_card(self.players[game.turn])
                print(len(self.players[self.turn].cards))
        else:
            return False
        return True

    def skip(self, player):
        if self.players.index(player) == self.turn:
            self.turn += 1

    def next_turn(self):
        if self.direct == False:
            self.turn -=1
        elif self.direct == True:
            self.turn +=1

        if self.turn == len(self.players):
            self.turn = 0
        elif self.turn == -1:
            self.turn = len(self.players) - 1


class Player:
    def __init__(self):
       # print(1)
        self.cards = []

    def get_card(self, card):
        self.cards.append(card)


    def put_card(self, card):
        return card

    def skip(self):
        print(2)


game = Game(3)

while game.gameover != True:
    print(f"Ходит {game.turn}")
    print(f"осталось карт в колоде {len(game.coloda.cards)}")
    print(f"Карта на столе {game.card_on_table.color, game.card_on_table.value}")
    print("Ваши карты")
    index = 0
    for card in game.players[game.turn].cards:
        accept = ""
        if card.value == game.card_on_table.value or card.color == game.card_on_table.color or card.color == 5:
            accept = "+"
        print(index, card.color, card.value, accept)
        index += 1
    a = input()
    cmd = a.split(" ")
    if cmd[0] == "skip" and game.has_get_card == True:
        print(f"Игрок {game.turn}  пропускает ход")
        game.next_turn()
        game.has_get_card = False
    elif cmd[0] == "get":
        game.get_card(game.players[game.turn])
        game.has_get_card = True
    elif cmd[0] == "put":

        cardindex = int(cmd[1])
        if cardindex not in range(0, len(game.players[game.turn].cards)):
            print("Неравильно выбрана карта")
            continue
        if len(cmd) < 3 and (game.players[game.turn].cards[cardindex].value == 14 or game.players[game.turn].cards[cardindex].value == 13):
            print("Не указан новый цвет")
            continue
        if len(cmd) > 2:
            new_color = int(cmd[2])
        if len(cmd) < 3:
            new_color = "none"
        if game.put_card(game.players[game.turn], game.players[game.turn].cards[cardindex], new_color):
            game.next_turn()
    else:
        print('Давай заного')
    print(game.turn)
    if len(game.players[game.turn].cards) == 0:
        game.gameover = True


