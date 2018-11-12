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
be prompted 

By default, the Biomonitor will record four channels of data — PZT Ring (0),
PPG (1), Bioimpedance (2), and ECG (3). In many cases, researchers will want to
collect only a subset of the channels. To do this, we simply specify the
channels using the `--channel` flag:

```unix
python bioreader.py /path/to/sd/card --config --channels 0 1




