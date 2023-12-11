import logging
import re
from aoc_2023.python.utilities import process_day


class Hand:

    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)

    @classmethod
    def from_string(cls, handstring: str):
        bits = [x.strip().split() for x in handstring.split(",")]
        classdict = {
            key: value for value, key in bits
        }
        return Hand(**classdict)


class Game:

    def __init__(
        self,
        game_id: int,
        hands: list,
        limit_red: int = 12,
        limit_green: int = 13,
        limit_blue: int = 14
    ):
        self.id = int(game_id)
        self.limit_red = limit_red
        self.limit_green = limit_green
        self.limit_blue = limit_blue
        self.hands = hands
        self.power = self.get_power()

    @classmethod
    def from_row(cls, row: str):
        id_chunk, hand_chunk = row.split(":")
        id_pattern = r"Game (\d+)"
        game_id = re.match(id_pattern, id_chunk).group(1)

        handstrings = hand_chunk.split(";")
        hands = [Hand.from_string(handstring) for handstring in handstrings]
        return Game(game_id=game_id, hands=hands)

    def is_legit(self):
        return all(
            [
                max([hand.red for hand in self.hands]) <= self.limit_red,
                max([hand.blue for hand in self.hands]) <= self.limit_blue,
                max([hand.green for hand in self.hands]) <= self.limit_green
            ]
        )

    def get_power(self):
        # get minimal colors for game - the max shown in any one hand
        max_red = max([hand.red for hand in self.hands])
        max_green = max([hand.green for hand in self.hands])
        max_blue = max([hand.blue for hand in self.hands])
        game_power = max_red * max_green * max_blue
        return game_power


def day2(data: list[str]):
    all_games = [Game.from_row(row) for row in data]
    legit_games = [x for x in all_games if x.is_legit()]
    part_a = sum([x.id for x in legit_games])
    part_b = sum([x.power for x in all_games])
    logging.info(f"Sum of legit IDs: {part_a}")
    logging.info(f"Sum of powers: {part_b}")
    return part_a, part_b


if __name__ == "__main__":
    process_day(2, callback=day2)
