from ..day4 import Card, day4
from ..utilities import process_day
import pytest


@pytest.fixture
def test_input():
    input_string = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    return input_string.split("\n")


def test_card(test_input):
    card1 = Card.from_row(test_input[0])
    assert card1.card_id == "1"
    assert card1.winners == ["41", "48", "83", "86", "17"]
    assert card1.candidates == ["83", "86",  "6", "31", "17", "9", "48", "53"]
    assert card1.value == 8
    assert card1.cards == ["2", "3", "4", "5"]


def test_fake(test_input):

    result_a, result_b = day4(test_input)
    assert result_a == 13
    assert result_b == 30


def test_real():

    part_a, part_b = process_day(4, day4)
    assert part_a == 22488
