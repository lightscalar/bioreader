# Bioreader

 The `bioreader.py` script is for configuring the Biomonitor SD cards as well
 script for extracting stored data.

# Requirements

The `bioreader.py` script was written and tested in Python 3.7.1, though should
be compatible with Python 3.6+. The script relies on a number of third party libraries. 
To ensure these are available, run,

```unix
pip install -r requirements.txt
```

# Configuring an SD card

Before use in a Biomontor device, the SD card must be configured. At the command line one 
simply calls the script and passes in the 

```unix
python bioreader.py /path/to/sd/card --config
```

Please note that this will *erase all data on the SD card*, and is not reversible. You will
be asked if you really want to do this to prevent accidental data loss.

By default, the Biomonitor will record four channels of data — PZT Ring (0),
PPG (1), Bioimpedance (2), and ECG (3). In many cases, researchers will want to
collect only a subset of the channels. To do this, simply specify the channels
using the `--channels` flag:

```unix
python bioreader.py /path/to/sd/card --config --channels 0 1
```

In this example, the SD card will be configured so that only the PZT ring and
the PPG channel will be recorded.

# Extracting data

After data has been collected, you'll want to access to it. This is
accomplished using the `--extract` command. For example,

```unix
python bioreader.py /path/to/sd/card --extract
```

This will convert data from the Biomonitor's format into CSV files. By default,
the script will extract the data into CSV files stored on the SD card in a
root-level folder called `/ARXIV`. To specify an alternate location, you may
specify the file destination:

```unix
python bioreader.py /path/to/sd/card --extract --destination /path/to/files
```
