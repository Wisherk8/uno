from card import Card
import random

class Coloda:
    cards = []
    colors = [] # 1-red 2-orange 3-green 4-blue 5-black
    values = [] #10 - skip, 11 - reverse, 12 - +2, 13 - change color, 14 black +4

    for color in range(1, 6):
        colors.append(color)

    for value in range(0, 15):
        values.append(value)

    for value in range(1, 13):
        for color in range(1, 5):
            cards.append(Card(color, value))
            cards.append(Card(color, value))

    for color in range(1, 5):
        cards.append(Card(color, 0))

    for smth in range(1, 5):
        cards.append(Card(5, 13))
        cards.append(Card(5, 14))

    def get_card(self):
        chislo = random.randint(0, len(self.cards) - 1)
        card = self.cards[chislo]
        self.cards.pop(chislo)
        print(f"Осталось карт в колоде {len(self.cards) + 1}")
        return card

