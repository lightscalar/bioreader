"""Utilities for BIOREADER."""
from datetime import datetime
from glob import glob
from ipdb import set_trace as debug
import re
from tqdm import tqdm


# Datetime regular expression.
REGEX = r"(\d+)-(\d+)-(\d+)_(\d+).(\d+).(\d+)"


class Struct:
    pass


def translate_line(line):
    """Translate a line from the Biomonitor device."""
    biomonitor_regex = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"
    out = re.search(biomonitor_regex, line)
    channel_number, value, timestamp = None, None, None
    if out:
        # We caught something!
        if out.group(1) == "B1":
            # Looks like we have some BioMonitor output.
            try:  # channel number there?
                channel_number = int(out.group(2), 16)
            except:
                pass
            try:  # value present?
                value = (int(out.group(3), 16)) * COVFAC
            except:
                pass
            try:  # timestamp present?
                timestamp = int(out.group(4), 16)
            except:
                pass
    return channel_number, value, timestamp


def read_data_file(data_file, data):
    """Read the data from specified file."""

    # Read content from the file.
    with open(data_file, "r", encoding="latin-1") as f:
        content = f.readlines()

    # Extract data line by line.
    for line in content:
        c, v, t = translate_line(line)
        if (c is not None) and (t is not None) and (v is not None):
            data["t_raw"][c].append(t)
            data["v_raw"][c].append(v)
    return data


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
        self.channels = [0, 1, 2, 3]
        self.channel_names = ["PZT", "PPG", "BIOZ", "ECG"]
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
        self.time_offset = self.datetime.timestamp()

    def collect_data(self):
        """Let's find all .DAT files in collection path."""
        self.datafiles = glob(f"{self.path_to_collection}/*/*.dat")
        data = {}
        fields = ["t_raw", "t_shift", "v_raw", "v_filt"]
        for f in fields:
            data[f] = {}
            for channel in self.channels:
                data[f][channel] = []
        self.data = data
        for datafile in tqdm(self.datafiles):
            self.data = read_data_file(datafile, self.data)


if __name__ == "__main__":

    path_to_sd_card = "./sd_card"
