# import pytest
from aoc_2023.day1 import day1


def test_ingest():
    first_lines = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet"
    ]
    result = day1(data=first_lines)
    assert result == 142


def test_words():

    test_lines = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen"
    ]
    result = day1(data=test_lines, part="b")
    assert result == 281


def test_mixed():

    inputs = [
        "sdxd22",
        "n7"
    ]
    result = day1(data=inputs, part="b")
    assert result == 99