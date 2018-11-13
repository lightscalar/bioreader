"""Utilities for BIOREADER."""
from sinc_filters import *

from datetime import datetime
from glob import glob
from ipdb import set_trace as debug
import numpy as np
import pandas as pd
import os
import re
from tqdm import tqdm


# Useful constants
REGEX = r"(\d+)-(\d+)-(\d+)_(\d+).(\d+).(\d+)"
MAXVAL = 2 ** 24 - 1
MAXVAL_BIOZ = 2 ** 20 - 1
MAXREF = 1.0
COVFAC = MAXREF * (1 / MAXVAL)
COVFAC_BIOZ = MAXREF * (1 / MAXVAL_BIOZ)
FACTORS = [COVFAC / 512, COVFAC, COVFAC_BIOZ, COVFAC]


class Struct:
    pass


def translate_line(line):
    """Translate a line from the Biomonitor device."""
    biomonitor_regex = r"(B1)\s*(\d*)\s*(\w*)\s*(\w*)"
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
                value = (int(out.group(3), 16)) * FACTORS[channel_number]
            except:
                pass
            try:  # timestamp present?
                timestamp = int(out.group(4), 16)
            except:
                pass
    return channel_number, value, timestamp


def read_datafile(data_file, data):
    """Read the data from specified file."""

    # Read content from the file.
    with open(data_file, "r", encoding="latin-1") as f:
        content = f.readlines()

    # Extract data line by line.
    for line in content:
        c, v, t = translate_line(line)
        if (c is not None) and (t is not None) and (v is not None):
            data[c]["Raw Timestamps (seconds)"].append(t)
            data[c]["Raw Signal"].append(v)
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

    def __init__(self, path_to_card, path_to_collection, path_to_csv_files):
        """Find all files present in dated folder."""
        self.errors = []
        valid_folder = valid_date_time_folder(path_to_collection)
        self.channels = [0, 1, 2, 3]
        self.channel_names = ["PZT", "PPG", "BIOZ", "ECG"]
        self.path_to_card = path_to_card
        if path_to_csv_files == "__SD_LOCAL__":
            self.path_to_csv_files = f"{path_to_card}/ARXIV"
        else:
            self.path_to_csv_files = path_to_csv_files
        if not valid_folder:
            self.errors.append("Folder name is not in the specified date/time format.")
        else:
            self.path_to_collection = path_to_collection
            self.create_datetime()
            self.collect_data()
            self.generate_csv_files()

    def pretty_time(self, timestamp):
        """Create a pretty date timestamp based on unix time."""
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%b-%d %H:%M:%S.%f")

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
        self.datafiles = sorted(self.datafiles)
        data = {}
        fields = [
            "Raw Timestamps (seconds)",
            "Corrected Timestamps (seconds)",
            "Date/Time",
            "Raw Signal",
            "Low-pass Filtered Signal (10 Hz)",
        ]
        for c in self.channels:
            data[c] = {}
            for f in fields:
                data[c][f] = []
        self.data = data
        print("> Extracting data...")
        for datafile in tqdm(self.datafiles):
            self.data = read_datafile(datafile, self.data)

        # Shift time and filter signals
        print("> Processing and filtering data.")
        self.data_frames = {}
        for c in tqdm(self.channels):
            if len(self.data[c][fields[0]])==0:
                continue
            # Create a dictionary to hold all the data.
            for f in fields:
                self.data[c][f] = np.array(self.data[c][f])
            # Correct timestamps.
            self.data[c][fields[1]] = (
                self.data[c][fields[0]] - self.data[c][fields[0]][0]
            ) * 1e-6 + self.time_offset
            if c == 0:  # scale into appropriate range
                self.data[c][fields[3]] = (
                    self.data[c][fields[3]] - np.median(self.data[c][fields[3]])
                ) / (self.data[c][fields[3]].std())
            # Filter raw signal data.
            self.data[c][fields[4]], _ = lowpass(
                self.data[c][fields[1]], self.data[c][fields[3]], freq_cutoff=10
            )
            # Generate pretty date/time stamps for data.
            self.data[c][fields[2]] = np.array(
                [self.pretty_time(t) for t in self.data[c][fields[1]]]
            )
            # Generate pandas dataframes.
            self.data_frames[c] = pd.DataFrame(self.data[c])

    def generate_csv_files(self):
        """Generate CSV files from the data frames."""
        print("> Generating CSV files.")
        datetime_folder = self.datetime.strftime("%Y-%b-%d_%H.%M.%S")
        location = f"{self.path_to_csv_files}/{datetime_folder}"
        if not os.path.isdir(location):
            os.makedirs(location)
        for c in tqdm(self.channels):
            if c not in self.data_frames.keys():
                continue # channel not collected
            else:
                filename = f"{location}/{self.channel_names[c]}.csv"
                self.data_frames[c].to_csv(filename)
