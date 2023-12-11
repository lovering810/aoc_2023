import logging
import re
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Card:

    card_id: str
    winners: list
    candidates: list
    wins_in_hand: field()
    value: field()
    cards: field()

    def __init__(self, card_id: str, winners: list, candidates: list):
        self.card_id = card_id
        self.winners = winners
        self.candidates = candidates
        self.wins_in_hand = [
            winner for winner in self.winners
            if winner in self.candidates
        ]
        self.value = self.calculate_points()
        self.cards = self.calculate_cards()

    @classmethod
    def from_row(cls, row: str):
        id_string, number_lists = row.strip().split(":")
        id_pattern = r"Card\s+(\d+)"
        card_id = re.match(id_pattern, id_string).group(1)
        winners, in_hand = number_lists.strip().split("|")
        winners = winners.split()
        candidates = in_hand.split()
        return Card(card_id=card_id, winners=winners, candidates=candidates)

    def calculate_points(self):
        if self.wins_in_hand:
            return 2**(len(self.wins_in_hand)-1)
        else:
            return 0

    def calculate_cards(self):
        cards = []
        # for each win, we gain another line's card, starting from our own ID
        if self.wins_in_hand:
            cards = [
                str(int(self.card_id) + added + 1)
                for added in range(len(self.wins_in_hand))
            ]
        return cards


def get_children(
    card: Card, deckt: dict[Card],
    family: list = [], depth: int = 0
):
    family.append(card.card_id)
    logging.debug(f"card {card.card_id} lvl {depth} has kids {card.cards}")
    for c_id in card.cards:
        child = deckt[c_id]
        return get_children(child, deckt, family, depth+1)
    logging.info(f"Total family: {Counter(family)}")
    return family


def expand_deck(deckt: dict[Card]):
    card_counts = {key: 1 for key in deckt.keys()}
    for card in deckt.values():
        # logging.info(f"Processing card {card.card_id}")
        # logging.debug(f"Card count to process: {range(card_counts[card.card_id])}")
        for _ in range(card_counts[card.card_id]):
            for copy_id in card.cards:
                # logging.debug(f"Adding card {copy_id} from parent {card.card_id}")
                card_counts[copy_id] += 1

    return card_counts


def day4(data: list[str]):
    original_deck = [Card.from_row(row) for row in data]
    part_a = sum([x.value for x in original_deck])
    deckt = {c.card_id: c for c in original_deck}
    expanded_deck = expand_deck(deckt)
    part_b = sum(expanded_deck.values())
    return part_a, part_b
