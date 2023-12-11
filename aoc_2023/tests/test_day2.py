from aoc_2023 import day2, utilities
import pytest


@pytest.fixture
def game_class():
    return day2.Game


@pytest.fixture
def hand_class():
    return day2.Hand


@pytest.mark.parametrize(
    "row,firstblue,firstred,firstgreen,legit,power",
    [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
            3, 4, 0, True, 48),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
            1, 0, 2, True, 12),
        ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
            6, 20, 8, False, 1560),
        ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
            6, 3, 1, False, 630),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
            1, 6, 3, True, 36)
    ]
)
def test_game_class(row, firstblue, firstred, firstgreen, legit, power):
    game = day2.Game.from_row(row)
    assert game.hands[0].blue == firstblue
    assert game.hands[0].green == firstgreen
    assert game.hands[0].red == firstred
    assert game.is_legit() == legit
    assert game.power == power


def test_full_day2():
    part_a, part_b = utilities.process_day(2, day2.day2)
    assert part_b > 15279
