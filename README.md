# Bioreader

 `bioreader.py` is a script for configuring the Biomonitor SD cards as well as
 extracting stored data.

## Requirements

The `bioreader.py` script was written and tested in Python 3.7.1, though it
should be compatible with Python 3.6+. The script relies on a number of third
party libraries.  To ensure these are available, run,

```unix
pip install -r requirements.txt
```

## Resetting an SD card

Before use in a Biomontor device, the SD card must be configured. This can be
done using the following command:

```unix
python bioreader.py /path/to/sd/card --reset
```

or,

```unix
python bioreader.py /path/to/sd/card -r
```

Please note that this will *erase all data on the SD card*, and is not
reversible. You will be asked to confirm that you **really** want to do this to
avoid accidental data loss.

By default, the Biomonitor will record four channels of data — PZT Ring (0),
PPG (1), Bioimpedance (2), and ECG (3). In many cases, researchers will want to
collect only a subset of the channels. To do this, simply specify the channels
using the `--channels` flag during a card reset:

```unix
python bioreader.py /path/to/sd/card --reset --channels 0 1
```

In this example, the SD card will be configured so that only the PZT ring and
the PPG channel will be recorded.

## Extracting data

After data has been collected, you'll want to access to it. This is
accomplished using the `--extract` command. For example,

```unix
python bioreader.py /path/to/sd/card --extract
```

This will convert data from the Biomonitor's `.dat` format into easily readable
CSV files. The `.dat` files will not be deleted from the card during this
process. Only a reset command will remove data from the SD card.

By default, the script will extract the data into CSV files stored on
the SD card in a root-level folder called `/ARXIV`. To specify an alternate
location, you may specify a file destination on your computer:

```unix
python bioreader.py /path/to/sd/card --extract --destination /path/to/csv/files
```

## Reading Annotations

You can process raw annotation data into a readable CSV file using the
`read_annotations.py` script. Simply call,

```unix
> python read_annotations path/to/annotation/file -d path/to/destination/csv
```

By default, the script will attempt to write the CSV file back to the
`/Volumes/ANNOTATIONS` USB stick. The annotations CSV file records the board
id, annotation text, timestamp, and datetime string. For details on how to 
export the annotations from the iPad to the iXpand drive, please read the tutorial
PDF available [here](export_annotations_documentation.pdf).

## Help

To see all available options, ask for help:

```unix
$~/dev/bioreader> python bioreader.py -h
usage: bioreader.py [-h] [-m [MINUTES]] [-d DESTINATION]
                    [-c CHANNELS [CHANNELS ...]] [-r] [-e]
                    path [path ...]

Extract data from and configure Biomonitor SD cards.

positional arguments:
  path                  The location of the target SD card

optional arguments:
  -h, --help            show this help message and exit
  -m [MINUTES], --minutes [MINUTES]
                        Maximum duration of recording session, in minutes
  -d DESTINATION, --destination DESTINATION
                        Where should we store the extracted CSV files?
  -c CHANNELS [CHANNELS ...], --channels CHANNELS [CHANNELS ...]
                        Specify the channels we should record (0—PVDF; 1-PPG;
                        2—BIOZ; 3—ECG).
  -r, --reset           Erase all data on the SD card and write a new
                        configuration file.
  -e, --extract         Extract data from the SD card and produce CSV files.
  ```
