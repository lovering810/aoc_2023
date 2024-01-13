import logging
import re
from dataclasses import dataclass, field, asdict
from graphlib import TopologicalSorter
from pathlib import Path


@dataclass
class Seed:

    seed_id: int
    soil: int = None
    fertilizer: int = None
    water: int = None
    light: int = None
    temperature: int = None
    humidity: int = None
    location: int = None


@dataclass
class Maption:

    target_start: int
    source_start: int
    range_len: int

    @classmethod
    def from_row(cls, row: str):
        t, s, r = [int(x.strip()) for x in row.split()]
        return Maption(t, s, r)

    def is_in_range(self, input_id: int):

        return self.source_start < input_id <= (
            self.source_start + self.range_len
            )


class MappyBoi:

    def __init__(self, source, target, maption_input: list[str]):
        self.source = source
        self.target = target
        self.maptions = self.make_maptions(maption_input)

    @staticmethod
    def make_maptions(maption_input: list[str]):
        maptions = [Maption.from_row(row.strip()) for row in maption_input if row!='']
        return maptions

    @classmethod
    def from_stanza(cls, stanza: str):
        title_pattern = r"^(\D+ ?\w+)\:"
        title_match = re.match(title_pattern, stanza)
        title = title_match.group(1)
        if title.endswith("map"):
            direct, _ = title.split()
            source, _, target = direct.split("-")
            maption_input = stanza.split("\n")[1:]
            result = MappyBoi(source, target, maption_input)
            return result
        else:
            return None

    def update_seed(self, seed: Seed):
        input_attr = "seed_id" if self.source == "seed" else self.source
        if not hasattr(seed, input_attr):
            raise AttributeError(
                f"No attribute exists/is populated for {self.source}"
            )
        if _ := getattr(seed, self.target):
            raise AttributeError(f"Already set {self.target}!")

        input_id = getattr(seed, input_attr)
        lookups = [
            maption for maption in self.maptions
            if maption.is_in_range(input_id)
        ]
        if len(lookups) == 0:
            new_val = input_id
        else:
            assert len(lookups) < 2, f"Too many qualified maptions! {lookups}"
            lookup = lookups[0]
            distance = input_id - lookup.source_start
            new_val = lookup.target_start + distance

        setattr(seed, self.target, new_val)

        return seed


def get_input():
    # go to input folder
    input_dir = Path(__file__).parents[1] / "inputs"
    assert input_dir.exists(), f"No input dir at {input_dir}"
    # get the file contents
    input_file = input_dir / "day5.txt"
    with open(input_file, "r+") as fyle:
        input_string = fyle.read()
    return input_string


def parse_seeds(seed_stanza: str, part: str = "a"):
    bits = [int(x.strip()) for x in seed_stanza.split()]
    if part == "a":
        return [Seed(bit) for bit in bits]
    # for part B, we need to create ranges based on pairs
    # get pairwise
    seedranges = []
    for i in range(0, len(bits), step=2):
        start, span = bits[i:i+1]
        new_seeds = [Seed(s) for s in range(start, span)]
        seedranges.extend(new_seeds)
    return seedranges


def process_input(input_string: str, part: str = "a"):
    map_set = []
    seeds = []
    chunks = input_string.split("\n\n")
    for chunk in chunks:
        if chunk == '':
            continue
        if chunk.startswith("seeds:"):
            seeds = parse_seeds(seed_stanza=chunk[7:])
        elif result := MappyBoi.from_stanza(chunk):
            map_set.append(result)

    return seeds, map_set


def get_ordered_maps(map_dict):

    map_deps = {key: map_dict[key].target for key in map_dict.keys()}
    dep_graph = [
        x for x in TopologicalSorter(map_deps).static_order()
        if len(x) > 1]
    return dep_graph


def process_part(input_string: str = None, part: str = "a"):
    if not input_string:
        input_string = get_input()
    seeds, map_set = process_input(input_string, part)
    map_dict = {m.source: m for m in map_set}
    dep_graph = get_ordered_maps(map_dict)
    for step in dep_graph:
        # logging.debug(f"Processing step {step}, with seeds {seeds}")
        stepmap = map_dict[step]
        seeds = [stepmap.update_seed(s) for s in seeds]

    return seeds


def part_a(input_string: str = None):
    return process_part(input_string, "a")


def part_b(input_string: str = None):
    return process_part(input_string, "b")
