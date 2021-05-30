class Card:
    symbols = ["♧", "♢", "♡", "♤"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(
        self,
        suit: int,
        rank: int = None,
    ):
        # initatlize from integer 0-51
        if not rank:
            self.suit = suit // 13
            self.rank = suit // 4
        else:
            self.suit = suit
            self.rank = rank
        assert 0 <= self.suit <= 3, "invalid suit"
        assert 0 <= self.rank <= 12, "invalid rank"

        self.val = self.rank if self.rank <= 10 else 10
        self.alt_val = 0 if self.rank != 1 else 11

    def __str__(self):
        suit_str, val_str = self.symbols[self.suit], self.ranks[self.rank]
        return f"{suit_str}{val_str}"

    def __eq__(self, other) -> bool:
        return self.suit == other.suit and self.rank == other.rank

    def __repr__(self) -> str:
        return str(self)

    def __lt__(self, other) -> bool:
        return self.suit < other.suit or (
            self.suit == other.suit and self.rank < other.rank
        )
