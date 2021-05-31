from Errors import GameOverError, RuleError
from collections import deque
from typing import Deque, List
from Card import Card
from Pile import Pile
from random import shuffle


# redrawing hand?
class Player:
    def __init__(self, cards: List[Card], id, hand_size=7, shuffle=False):
        self.id = id
        self.hand: List[Card] = cards[:hand_size]
        self.hand.sort()
        self.deck: Deque[Card] = deque(cards[hand_size:])
        self.shuffle = shuffle
        self.hand_size = hand_size

    def play(self, card: Card, pile: Pile):
        # was_successful, is_turn_over, was_squeezed
        self.check_in_hand(card)
        pile.add(card, self.id)
        self.hand.remove(card)
        self.maybe_draw_new_hand()

    def check_in_hand(self, card: Card) -> bool:
        if card not in self.hand:
            raise RuleError(f"Player {self.id+1} does not hold {card}")

    def take_pile(self, cards: List[Card]):
        self.deck.extend(cards)
        if self.shuffle:
            # apparently faster to convert to list
            temp = list(self.deck)
            shuffle(temp)
            self.deck = deque(temp)

    def discard(self, card: Card):
        self.check_in_hand(card)
        self.hand.remove(card)
        self.maybe_draw_new_hand()

    def forced_discard(self, type: int):
        if type == 4:
            self.hand = []
        else:
            for card in self.hand:
                if card.suit == type:
                    self.discard(card)
        self.maybe_draw_new_hand()

    def maybe_draw_new_hand(self) -> bool:
        # game over check is here
        if len(self.hand) == 0:
            for _ in range(self.hand_size):
                self.hand.append(self.deck.popleft())
        self.hand.sort()
        # empty after pickup - means no cards left
        if len(self.hand) == 0:
            raise GameOverError(f"Player {self.id+1} has no more cards. Game Over")
