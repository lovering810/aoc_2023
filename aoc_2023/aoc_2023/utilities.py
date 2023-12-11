from pathlib import Path
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)


# ingest file
def ingest_daily_data(day_number: int):
    input_dir = Path(__file__).parent / "inputs"
    assert input_dir.exists()

    input_file = input_dir / f"day{day_number}.txt"
    with open(input_file, "r+") as fyle:
        data = [line.strip() for line in fyle.readlines()]

    return data


def process_day(day_number: int, callback: callable):

    data = ingest_daily_data(day_number)
    return callback(data)
