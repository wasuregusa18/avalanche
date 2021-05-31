from Errors import GameOverError, RuleError
from typing import List, Optional, Set, Tuple
from Card import Card
from Deck import Deck
from Pile import Pile
from Player import Player

# WRITE TESTS NEXT
class Game:
    def __init__(self, num_piles=3, hand_size=7, shuffle=False):
        deck = Deck()
        starting_cards = deck.deal(num_piles)
        self.players = [
            Player(
                half,
                id,
                hand_size=hand_size,
                shuffle=shuffle,
            )
            for id, half in enumerate(deck.partion((52 - num_piles) // 2))
        ]
        self.board = [Pile([card]) for card in starting_cards]
        self.discard_pile: List[Card] = []
        self.turn = 0

    @property
    def is_empty_pile(self) -> bool:
        return len(self.empty_piles) > 0

    @property
    def empty_piles(self) -> Set[int]:
        empty_piles = set()
        for i, pile in enumerate(self.board):
            if not pile.top_card:
                empty_piles.add(i)
        return empty_piles

    def step(self, card: Card, pile_num: int):
        # card = Card(card_num)
        current_player = self.players[self.turn]
        other_player = self.players[(self.turn + 1) % 2]

        try:
            if not (-1 <= pile_num < len(self.board)):
                raise RuleError(f"There is no Pile {pile_num+1}")
            if self.is_empty_pile and pile_num not in self.empty_piles:
                raise RuleError(f"Must first play on empty pile")
            if pile_num == -1:
                current_player.discard(card)
                self.discard_pile.append(card)
            else:
                target_pile = self.board[pile_num]
                current_player.play(card, target_pile)
                self.resolve(card, target_pile)
        except RuleError as e:
            print(e)
        except GameOverError as e:
            print(e)

        # no empty pile means turn over
        if not self.is_empty_pile:
            self.turn = (self.turn + 1) % 2
        return self.turn

    def resolve(self, card: Card, pile: Pile):

        is_shiver, shiver_suit, is_squeeze, all_frozen = self.check_for_special(
            card, pile
        )
        current_player = self.players[self.turn]
        other_player = self.players[(self.turn + 1) % 2]

        cards_to_play = 0
        if is_shiver:
            other_player.forced_discard(shiver_suit)
        if is_squeeze:
            other_player.forced_discard(4)  # means whole hand
        if all_frozen:
            self.board.append(Pile())
            # self.cards_to_play += 1
        if pile.is_taken():
            cards = pile.empty()
            current_player.take_pile(cards)
            # self.cards_to_play += 1
        # return cards_to_play

    def check_for_special(self, card: Card, pile: Pile):
        is_shiver, shiver_suit = self.is_shiver()
        is_squeeze = pile.frozen_depth == 3
        all_frozen = self.are_all_frozen()
        if all_frozen and len(self.board) == 5:
            raise GameOverError(f"Avalanche!! Player {self.turn+1} wins")
        return is_shiver, shiver_suit, is_squeeze, all_frozen

    def is_shiver(self) -> Tuple[bool, Optional[int]]:
        suit = None
        for pile in self.board:
            if suit is None:
                suit = pile.top_card.suit
            else:
                if suit != pile.top_card.suit:
                    return False, suit
        return True, suit

    def are_all_frozen(self) -> bool:
        player = None
        for pile in self.board:
            if who := pile.is_frozen < 0:
                return False
            elif player is None:
                player = who
            elif player != who:
                return False
        return True

    def draw(self):
        # draws from persepctive of current player
        pass

    # def step(self, card_num: int, pile_num: int):
    #     # player_turn, state, reward, done

    #     current_player = self.players[self.turn]
    #     other_player = self.players[(self.turn + 1) % 2]
    #     card = Card(card_num)

    #     # pile_num = -1 is discard
    #     if pile_num == -1:
    #         was_successful, game_over = current_player.discard(card)
    #         return was_successful

    #     target_pile = self.board[pile_num]
    #     was_successful, is_turn_over, was_squeezed, game_over = current_player.play(
    #         card, target_pile
    #     )
    #     if not was_successful:
    #         return False

    #     if was_squeezed:
    #         game_over = other_player.forced_discard(4)  # whole hand

    #     # check for shiver
    #     elif self.is_shiver():
    #         game_over = other_player.forced_discard(card.suit)

    #     if is_turn_over:
    #         self.turn = (self.turn + 1) % 2
    #         return True
    #     else:
    #         return True

    def to_state(self) -> List[int]:
        pass


game = Game()
p1, p2 = game.players
pil1, pil2, pil3 = game.board
card = p1.hand[0]
