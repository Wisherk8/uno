import random
from coloda import Coloda
from flask import Flask, request, redirect, Response
app = Flask(__name__)

address = "192.168.1.1:5000"


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
        self.has_get_card = False
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

    def digit2word(self, card):
        if card.color == 1:
            color = "Красный"
        elif card.color == 2:
            color = "Желтый"
        elif card.color == 3:
            color = "Зеленый"
        elif card.color == 4:
            color = "Синий"
        elif card.color == 5:
            color = "Черный"
        if card.value == 13:
            value = "Смена цвета"
        elif card.value == 14:
            value = "Смена цвета и +4"
        elif card.value == 12:
            value = "Пропуск хода и +2"
        elif card.value == 11:
            value = "Ревёрс!!!"
        elif card.value == 10:
            value = "Пропуск хода!!!"
        elif card.value in range(0, 10):
            value = card.value
        return f"{color} {value}"

    def digit2color(self, color):
        if color == 1:
            c = "Красный"
        elif color == 2:
            c = "Желтый"
        elif color == 3:
            c = "Зеленый"
        elif color == 4:
            c = "Синий"
        elif color == 5:
            c = "Черный"
        return c



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



@app.route('/uno')
def uno():
    address = f"{request.remote_addr}:5000"

    for player in game.players:
        if  len(player.cards) == 0:
            game.gameover = True
    player = int(request.args.get('player'))
    cmds = request.args.get('cmd')
    out = ""
    if cmds != None:
        cmd = cmds.split("_")
        if cmd[0] == "skip" and game.has_get_card == True:
            print(f"Игрок {game.turn}  пропускает ход")
            game.next_turn()
            game.has_get_card = False
            return redirect(f"http://{address}/uno?player={player}")
        elif cmd[0] == "get":
            game.get_card(game.players[game.turn])
            game.has_get_card = True
            return redirect(f"http://{address}/uno?player={player}")
        elif cmd[0] == "put":
            cardindex = int(cmd[1])
            if cardindex not in range(0, len(game.players[game.turn].cards)):
                out += "Неравильно выбрана карта"
                print("Неравильно выбрана карта")
  #          if len(cmd) < 3 and (game.players[game.turn].cards[cardindex].value == 14 or game.players[game.turn].cards[
  #              cardindex].value == 13):
  #              print("Не указан новый цвет")
            if len(cmd) > 2:
                new_color = int(cmd[2])
            if len(cmd) < 3:
                new_color = "none"
            if game.put_card(game.players[game.turn], game.players[game.turn].cards[cardindex], new_color):
                game.next_turn()
                return redirect(f"http://{address}/uno?player={player}")
    else:
        cmd = None
    if player == None:
        return "Не выбран игрок"
    elif player not in range(0, len(game.players)):
        return "Выбран неправильный игрок"
    index = 0
    ochki = 0
    color = None
    value = None
    nbcolor = None
    for card in game.players[player].cards:
        if game.gameover:
            if card.value in range(0, 10):
                ochki += card.value
                out += f'{card.color}, {card.value} - {card.value} <br>'
            elif card.value in range(10, 13):
                ochki += 20
                out += f'{card.color}, {card.value} - 20 <br>'
            else:
                ochki += 50
                out += f'{card.color}, {card.value} - 50 <br>'
        else:
            accept = ""
            if card.value == game.card_on_table.value or card.color == game.card_on_table.color or card.color == 5:
                accept = "+"
            if game.turn == player and (card.value == 14 or card.value == 13):
                for i in range(1, 5):
                    out += f"<a href='http://{address}/uno?player={player}&cmd=put_{index}_{i}'>{index}, {game.digit2word(card)}, Новый цвет {game.digit2color(i)} {accept}</a> <br>"
            elif game.turn == player:

                out += f"<a href='http://{address}/uno?player={player}&cmd=put_{index}'>{index}, {game.digit2word(card)} {accept}</a> <br>"
            else:
                out += f"{index}, {game.digit2word(card)} {accept}<br>"
            index += 1
    if game.gameover:
        out += f'Итого очков {ochki} <br>'
        out += f'Игра окончена!!!'
        return out
    out += f"<br> Карта на столе {game.digit2word(game.card_on_table)}"
    out += f"<br> Осталось карт в колоде - {len(game.coloda.cards)}"

    if game.turn == player and not game.has_get_card:
        out += "<br>Ваш ход"
        out += f"<br> <a href='http://{address}/uno?player={player}&cmd=get'>Взять карту</a> <br>"
    elif game.turn == player and game.has_get_card:
        out += "<br>Ваш ход"
        out += f"<br> <a href='http://{address}/uno?player={player}&cmd=skip'>Пропустить ход</a> <br>"
    else:
        out += f"<br> Ход игрока {game.turn}"
    print(out)
    resp = Response(out)
    resp.headers['refresh'] = "2"
    return resp


