from utils import *

import argparse
from glob import glob
from ipdb import set_trace as debug


class Struct:
    pass


def are_you_sure():
    ays = input(
        "Are you sure you want to configure this card? All data will be erased? (Y/N) "
    )
    return ays.lower() == "y"


def configure(config):
    """Configure an SD card for use in the Biomonitor"""
    if not are_you_sure():
        print("Okay. Not doing anything.")
        return
    else:
        # Magic here.
        pass


def extract_data(config):
    """Extract data from the SD card."""

    # Find all collections on the SD card.
    collections = find_all_collections(config.path_to_card)
    collection_objects = []
    for path_to_collection in collections:
        collection_objects.append(Collection(path_to_collection))
    return collection_objects


if __name__ == "__main__":

    # Check for arguments.
    parser = argparse.ArgumentParser(
        description="Extract data from and configure Biomonitor SD cards."
    )

    # Define possible arguments to the script.
    parser.add_argument(
        "path",
        nargs="+",
        default="/path/to/card",
        type=str,
        help="The location of the target SD card",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default="__SD_LOCAL__",
        type=str,
        help="Where should we store the extracted data?",
    )
    parser.add_argument("-ch", "--channels", default=[0, 1, 2, 3], nargs="+", type=int)
    parser.add_argument("-c", "--config", action="store_true")
    parser.add_argument("-e", "--extract", action="store_true")

    # Extract arguments from command line.
    config = Struct()
    args = parser.parse_args()
    config.path_to_card = args.path[0]
    config.destination = args.destination
    config.do_config = args.config
    config.channels = args.channels
    config.extract = args.extract

    # Take action!
    if config.do_config:
        configure(config)
    elif config.extract:
        collections = extract_data(config)
