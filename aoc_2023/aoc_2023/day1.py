import re
import logging
from functools import partial
from aoc_2023.utilities import process_day

numstrings = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0}


def get_firstlast_digits(line: str):
    line = line.lower()
    # get all digits in line
    digits = re.findall(r"\d", line)
    # use first and last only
    rel_digits = []
    first = digits[0]
    rel_digits.append(first)
    if len(digits) > 1:
        last = digits[-1]
    else:
        last = first
    rel_digits.append(last)

    rel_no = int(''.join(rel_digits))
    logging.debug(f"line: {line}, digits: {rel_digits}, num: {rel_no}")
    return rel_no


def day1(data: list[str], part: str = "a"):
    total_numbers = []
    if part == "b":
        joined_data = ' '.join(data)
        data = (
            joined_data.replace("one", "one1one")
            .replace("two", "two2two")
            .replace("three", "three3three")
            .replace("four", "four4four")
            .replace("five", "five5five")
            .replace("six", "six6six")
            .replace("seven", "seven7seven")
            .replace("eight", "eight8eight")
            .replace("nine", "nine9nine")
        ).split(' ')
    for line in data:
        rel_no = get_firstlast_digits(line)
        total_numbers.append(rel_no)

    final_sum = sum(total_numbers)
    logging.info(f"Total sum of {len(total_numbers)} numbers: {final_sum}")
    return final_sum


if __name__ == "__main__":
    part_a = process_day(day_number=1, callback=partial(day1, part="a"))
    part_b = process_day(day_number=1, callback=partial(day1, part="b"))
    logging.info(f"1st part: {part_a}; 2nd part: {part_b}")
