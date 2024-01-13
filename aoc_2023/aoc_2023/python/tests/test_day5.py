from ..day5 import Seed, Maption, MappyBoi, process_input, get_ordered_maps, part_a
import pytest
input_string = """seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4"""


@pytest.fixture
def input_data():

    return process_input(input_string)


def test_ingest(input_data):

    seeds, map_set = input_data
    assert len(seeds) == 4
    assert len(map_set) == 7


def test_seed(input_data):

    seeds, map_set = input_data
    firstseed = seeds[0]
    assert firstseed.seed_id == 79


def test_sort(input_data):

    seeds, map_set = input_data
    map_dict = {m.source: m for m in map_set}
    result = get_ordered_maps(map_dict)
    assert result == [
        "seed",
        "soil",
        "fertilizer",
        "water",
        "light",
        "temperature",
        "humidity"
    ]


def test_update_seed(input_data):

    seeds, map_set = input_data
    map_dict = {m.source: m for m in map_set}
    soilmap = map_dict["seed"]
    assert soilmap.maptions[0]
    result = soilmap.update_seed(seeds[0])
    assert result.soil == 81

    result = soilmap.update_seed(seeds[1])
    assert result.soil == 14


def test_fake(input_data):

    seeds = part_a(input_string)
    assert seeds
    seedlocs = [s.location for s in seeds]
    assert min(seedlocs) == 35


def test_real():

    seeds = part_a()
    assert seeds
    seedlocs = [s.location for s in seeds]
    assert min(seedlocs) == 600279879
