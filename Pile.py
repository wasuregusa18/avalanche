from collections import deque
from typing import Deque, List, Tuple, Optional
from Card import Card
from Errors import RuleError


class Pile:
    def __init__(self, starting: List[Card] = []):
        self.pile: Deque[Card] = deque(starting)
        self.count = 0  # this should be the lower
        self.alt_count = 0

        # frozen
        self.is_frozen = -1  # otherwise player number
        self.frozen_rank: Optional[int] = None
        self.frozen_depth = 0

    def add(self, card: Card, player_num: int) -> Tuple[bool, List[Card], bool]:
        """
        returns was_successful, taken_cards, was_squeezed
        """
        self.validate(card, player_num)
        self.pile.append(card)
        self.count += card.val

        # up to one ace as 11 - others must be 1
        temp_alt_count = self.alt_count + card.alt_val
        self.alt_count = (
            temp_alt_count if temp_alt_count <= 21 else self.alt_count + card.val
        )

        # update freeze conditions
        if self.top_card and self.top_card.rank == card.rank:
            self.frozen_depth += 1
            self.is_frozen = player_num
            self.frozen_rank = card.rank
            # if self.frozen_depth == 3:
            # return True, self.empty(), True

        # if self.is_taken():
        # return True, self.empty(), False

        # return True, [], False

    def validate(self, card: Card, player_num: int) -> bool:
        # empty
        if not (top_card := self.top_card):
            return True
        # same suit
        if top_card.suit == card.suit:
            raise RuleError(f"{card} played same suit as {top_card}")
        # too large - count should always be the smaller
        if new_sum := card.val + self.count > 21:
            raise RuleError(
                f"{card} would push pile sum over 21: {card.val} + {self.count} = {new_sum}"
            )
        # frozen - is_frozen by other player and not freeze card
        if (
            self.is_frozen > 0
            and self.is_frozen != player_num
            and card.rank != self.frozen_rank
        ):
            raise RuleError("Pile is frozen by other player")
        return True

    def is_taken(self) -> bool:
        return self.count == 21 or self.alt_count == 21 or self.frozen_depth == 3

    def empty(self) -> List[Card]:
        # reset freeze conditions
        self.is_frozen = -1
        self.frozen_rank = None
        self.frozen_depth = 0

        cards = []
        while self.pile:
            cards.append(self.pile.popleft())
        return cards

    @property
    def top_card(self) -> Optional[Card]:
        if len(self.pile) == 0:
            return None
        else:
            return self.pile[-1]
