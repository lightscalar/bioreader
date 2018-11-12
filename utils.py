"""Utilities for BIOREADER."""
from datetime import datetime
from glob import glob
from ipdb import set_trace as debug
import re


# Datetime regular expression.
REGEX = r"(\d+)-(\d+)-(\d+)_(\d+).(\d+).(\d+)"


def valid_date_time_folder(path_to_folder):
    """Verify that folder name matches proper date/time format."""
    return re.search(REGEX, path_to_folder) is not None


def find_all_collections(path_to_card):
    """Find all collections given a path to an SD card."""
    contents_of_card = glob(f"{path_to_card}/*")

    # Find all datetime folders.
    collections = []
    for content in contents_of_card:
        if valid_date_time_folder(content):
            collections.append(content)
    return collections


class Collection:
    """Defines a single time aligned collection."""

    def __init__(self, path_to_collection):
        """Find all files present in dated folder."""
        self.errors = []
        valid_folder = valid_date_time_folder(path_to_collection)
        if not valid_folder:
            self.errors.append("Folder name is not in the specified date/time format.")
        else:
            self.path_to_collection = path_to_collection
            self.create_datetime()
            self.collect_data()

    def create_datetime(self):
        """Create a datetime object from collection path."""
        dt = re.search(REGEX, self.path_to_collection)
        self.datetime = datetime(
            int(dt[3]), int(dt[1]), int(dt[2]), int(dt[4]), int(dt[5]), int(dt[6])
        )

    def collect_data(self):
        """Let's find all .DAT files in collection path."""
        self.datafiles = glob(f"{self.path_to_collection}/*/*.dat")


if __name__ == "__main__":

    path_to_sd_card = "./sd_card"
