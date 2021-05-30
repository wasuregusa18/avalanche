from random import shuffle
from typing import List, Tuple
from Card import Card


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for val in range(13):
                self.cards.append(Card(suit, val))
        self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def partion(self, n: int) -> Tuple[List[Card], List[Card]]:
        return self.cards[:n], self.cards[n:]

    def deal(self, n: int) -> List[Card]:
        # alternate is to use a pointer - this means not 52 in deck
        cards = []
        for _ in range(n):
            cards.append(self.cards.pop())
        return cards

    def __str__(self):
        return "".join(map(str, self.cards))
