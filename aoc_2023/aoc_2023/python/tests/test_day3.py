from ..day3 import get_loc_dict, meets_adjacency_criteria, day3
from ..utilities import process_day
import pytest
import re


@pytest.fixture
def input_data():

    input_string = """467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598.."""

    return [row.strip() for row in input_string.split("\n")]


def test_id_symbols(input_data):

    result = get_loc_dict(input_data)
    assert isinstance(result, dict)
    assert len(result["1"]) == 1
    assert len(result["8"]) == 2


def test_adjacency(input_data):
    symbol_locs = get_loc_dict(input_data)
    legit_numbers = []
    for row in input_data:
        row_number = input_data.index(row)
        for x in re.finditer(r"\d+", row):
            if meets_adjacency_criteria(
                row_number=row_number,
                item_match=x,
                comparison_dict=symbol_locs
            ):
                legit_numbers.append(x)

    legit_numbers = [int(x.group(0)) for x in legit_numbers]
    assert legit_numbers == [
        467, 35, 633, 617, 592, 755, 664, 598
    ]


def test_fake(input_data):
    part_a, part_b = day3(input_data)
    assert part_a == 4361
    assert part_b == 467835


def test_real():

    result_a, result_b = process_day(3, day3)
    assert result_a == 527364
    assert result_b == 79026871