from datetime import datetime
from utils import *

import argparse
from glob import glob
import json
import pandas as pd
import shutil


def pretty_time(timestamp):
    """Create a pretty date timestamp based on unix time."""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%b-%d %H:%M:%S.%f")


def extract_annotations(path_to_annotations, destination_path):
    """Extract annotations from the target USB drive."""
    text_files = glob(f"{path_to_annotations}/*.txt")
    notes = []
    master_note_list = []
    for tf in text_files:
        with open(tf, "r") as f:
            text = f.read()
        text_dict = json.loads(text)
        notes.append(text_dict)
    for note in notes:
        board_id = list(note.keys())[0]
        for item in note[board_id]:
            item["board_id"] = board_id
            item["datetime"] = pretty_time(item["date"])
            item["timestamp"] = item["date"]
            del item["date"]
            master_note_list.append(item)

    master_note_list = sorted(master_note_list, key=lambda x: x["timestamp"])
    first_datetime = master_note_list[0]["datetime"].replace(" ", "_").replace(":", ".")
    note_frame = pd.DataFrame(master_note_list)
    csv_filename = f"ANNOTATIONS_{first_datetime}.csv"
    note_frame.to_csv(csv_filename)
    shutil.move(csv_filename, destination_path)
    return master_note_list


class Struct:
    pass


if __name__ == "__main__":

    # Check for arguments.
    parser = argparse.ArgumentParser(
        description="Extract annotations from USB drive and generate CSV file."
    )

    # Define possible arguments to the script.
    parser.add_argument(
        "path",
        nargs="+",
        default="/Volumes/ANNOTATIONS",
        type=str,
        help="The location of the target SD card",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default="/Volumes/ANNOTATIONS",
        type=str,
        help="Where should we store the extracted CSV files?",
    )

    config = Struct()
    args = parser.parse_args()
    config.path_to_card = args.path[0]
    config.destination = args.destination

    notes = extract_annotations(config.path_to_card, config.destination)
