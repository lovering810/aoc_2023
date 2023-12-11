import argparse
import python.utilities as u
import importlib.util
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("day")
parser.add_argument("language")
args = parser.parse_args()


def import_day_callback(day: int):
    day = str(day)


def load_module(
    dayname: str, language: str = "python"
):
    """
    Given day and language of AOC try to retrieve and load a module from file.

    Args:
    day (int): day of AoC whose code we want
    language (str): programming language whose day we want

    Raises:
    FileNotFoundError: if the module cannot be found on the path;
    messaging specific to filepath components
    ImportError: if the module is found on the path, but suffers 
    some kind of import error due to malformation.

    Returns:
    module: if a module exists for this field, returns it.
    """

    language = language.lower()
    lang_dir = Path(__file__).parent / language
    if not lang_dir.exists():
        raise FileNotFoundError(
            f"No directory for language {language} exists at {lang_dir})"
        )

    module_filepath = lang_dir / f"{dayname}.py"
    if not module_filepath.exists():
        raise FileNotFoundError(
            f"No module for {dayname} found for language {language} at {module_filepath})"
        )
    try:
        module_spec = importlib.util.spec_from_file_location(
            dayname, module_filepath
        )
        module = importlib.util.module_from_spec(spec=module_spec)
        sys.modules[dayname] = module
        module_spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(
            f"Could not import {dayname} module from {module_filepath}: {e}"
        )
    return module


def get_callback(day: int, language: str = "python"):

    dayname = f"day{day}"
    module = load_module(dayname=dayname, language=language)
    callback = getattr(module, dayname)
    return callback


def main():

    callback = get_callback(args.day, args.language)
    return u.process_day(args.day, callback)


if __name__ == "__main__":
    main()
