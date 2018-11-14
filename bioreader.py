from utils import *

import argparse
from glob import glob
from ipdb import set_trace as debug
import os
import shutil


def are_you_sure(override):
    '''Ask the user if they really want to proceed.'''
    if override:
        return True
    ays = input(
        "Are you sure you want to reset this card? All data will be erased? (Y/N) "
    )
    return ays.lower() == "y"


def can_remove(content):
    """Is this content that I can safely remove?"""
    removable = False
    if re.search(r"ARXIV", content):
        removable = True
    elif valid_date_time_folder(content):
        removable = True
    elif re.search(r"config.txt", content):
        removable = True
    return removable


def remove_file_or_dir(content):
    """Removes a file or a directory."""
    if os.path.isfile(content):
        os.remove(content)
    elif os.path.isdir(content):
        shutil.rmtree(content)


def delete_card_contents(config):
    """Delete the contents of the card."""
    path_to_card = config.path_to_card
    contents = glob(f"{path_to_card}/*")
    for content in contents:
        if can_remove(content):
            remove_file_or_dir(content)


def configure_card(config):
    """Write configuration file to the card."""
    filename = f"{config.path_to_card}/config.txt"
    file_object = open(filename, "w")
    starting_channel = config.channels[0]
    recording_minutes = config.recording_duration
    file_object.write(f"BLE Channel: {starting_channel}\n")
    file_object.write(f"Recording Minutes: {recording_minutes}\n")
    channel_names = ["PVDF", "PPG", "BIOZ", "ECG"]
    for channel in [0, 1, 2, 3]:
        file_object.write(
            f"Record {channel_names[channel]}: {int(channel in config.channels)}\n"
        )
    file_object.write("BIOZ Current: 2\n")
    file_object.close()


def reset(config, override=False):
    """Configure an SD card for use in the Biomonitor"""
    if not are_you_sure(override):
        print("Okay. Not doing anything.")
        return
    else:
        # Remove all data from card.
        delete_card_contents(config)
        configure_card(config)


def extract_data(config):
    """Extract data from the SD card."""
    # Find all collections on the SD card.
    collections = find_all_collections(config.path_to_card)
    collection_objects = []
    for path_to_collection in collections:
        collection_objects.append(
            Collection(config.path_to_card, path_to_collection, config.destination)
        )
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
        "-m",
        "--minutes",
        nargs="?",
        default=8 * 60,
        type=int,
        help="Maximum duration of recording session, in minutes",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default="__SD_LOCAL__",
        type=str,
        help="Where should we store the extracted CSV files?",
    )
    parser.add_argument(
        "-c",
        "--channels",
        default=[0, 1, 2, 3],
        nargs="+",
        type=int,
        help="Specify the channels we should record (0—PVDF; 1-PPG; 2—BIOZ; 3—ECG)",
    )
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="Erase all data on the SD card and write a new configuration file.",
    )
    parser.add_argument(
        "-e",
        "--extract",
        action="store_true",
        help="Extract data from the SD card and produce CSV files.",
    )

    # Extract arguments from command line.
    config = Struct()
    args = parser.parse_args()
    config.path_to_card = args.path[0]
    config.destination = args.destination
    config.do_reset = args.reset
    config.channels = args.channels
    config.do_extract = args.extract
    config.recording_duration = args.minutes

    # Take action!
    if config.do_reset:
        reset(config)
    elif config.do_extract:
        collections = extract_data(config)
        c = collections[0]
