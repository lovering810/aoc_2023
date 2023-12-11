import logging
import re
from collections import defaultdict
from itertools import chain
from .utilities import process_day


def get_loc_dict(data: list[str], symbol_pattern: str = r"[^\.\d]") -> dict:
    # 2D matrix adjacency
    # process for symbol locations
    symbol_locs = defaultdict(list)
    # get spans w re.finditer()
    for i in range(len(data)):
        row_key = str(i)
        row_entry = symbol_locs[row_key]
        row = data[i]
        for match in re.finditer(symbol_pattern, row):
            if match:
                row_entry.append(match)

    return symbol_locs


def is_adjacent(candidate_position: int, target_position: int):
    return abs(candidate_position - target_position) < 2


def is_overlap(candidate, target) -> bool:
    result = False
    if any(
        [
            candidate.start() <= target.start() <= candidate.end(),
            candidate.start() <= target.end() <= candidate.end()
        ]
    ):
        # logging.debug(f"Candidate {candidate} overlaps target {target}")
        result = True
    return result


def spans_adjacent(
    target_match: re.Match,
    candidate_match: re.Match,
    ends: bool = True
) -> bool:

    # if the target (fixed point) overlaps the candidate, we're good! 
    overlap = is_overlap(candidate_match, target_match)
    
    # if the target's start is within 1 after the candidate end
    # or start, also good.
    # if (
    #     target_match.start() - candidate_match.end()
    # ) == 1 or (candidate_match.start() - target_match.end()) == 1:
    #     # logging.debug(f"{candidate_match} starts in range of {target_match}")
    #     return True
    # # if the target's end is within 1 space of the candidate start,
    # # okay!
    # if ends and (target_match.end() - candidate_match.start()) == 1:
    #     # logging.debug(f"{target_match} ends in range of {candidate_match}")
    #     return True
    return any([overlap])


def meets_adjacency_criteria(
    row_number: int,
    item_match: re.Match,
    comparison_dict: dict[list[re.Match]],
    match_threshold: int = 1
):
    ends = match_threshold == 1
    # get all adjacent rows in which we are looking
    adjacent_rows = comparison_dict[str(row_number)] + comparison_dict[str(row_number - 1)] + comparison_dict[str(row_number + 1)]

    # we're only looking at the comps for these rows
    # accumulate matches based on match_func
    legits = [comp for comp in adjacent_rows if spans_adjacent(
        target_match=item_match, candidate_match=comp, ends=ends)
    ]
    # logging.debug(f"{item_match} legits after comparison: {legits}")
    # if we have enough matches for this target, send them back as results
    if len(legits) >= match_threshold:
        return legits
    else:
        return None


def day3(data: list[str]) -> int:
    # part A
    symbol_locs = get_loc_dict(data)
    # part B
    number_locs = get_loc_dict(data, symbol_pattern=r"\d+")
    part_a_legits = []
    part_b_pairs = []
    for row in data:
        row_number = data.index(row)
        # part A
        for a in re.finditer(r"\d+", row):
            if _ := meets_adjacency_criteria(
                row_number=row_number,
                item_match=a,
                comparison_dict=symbol_locs
            ):
                part_a_legits.append(a)

        for b in re.finditer(r"\*", row):
            if pair := meets_adjacency_criteria(
                row_number=row_number,
                item_match=b,
                comparison_dict=number_locs,
                match_threshold=2
            ):
                part_b_pairs.append(tuple([int(x.group(0)) for x in pair]))
                
    # logging.debug(f"part_a_legits after loop-through: {part_a_legits}")
    # logging.debug(f"part_b_pairs after loop-through: {part_b_pairs}")
    result_a = sum([int(x.group(0)) for x in part_a_legits])
    result_b = sum([a*b for a, b in part_b_pairs])
    logging.info(f"Part A: {result_a}, Part B: {result_b}")

    return result_a, result_b


if __name__ == "__main__":
    process_day(3, day3)
