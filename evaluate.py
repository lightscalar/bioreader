from filters import *

from glob import glob
import numpy as np
import pandas as pd
import pylab as plt
import seaborn as sns

plot_raw_signal = False
dirs = glob("today_card/ARXIV/*")
dirs = glob("/Volumes/GARNET/ARXIV/*")
pzt = pd.read_csv(f"{dirs[0]}/PZT.csv")
t = pzt["Corrected Timestamps (seconds)"]
if plot_raw_signal:
    v_ = np.array(pzt["Raw Signal"])
else:
    v_ = pzt["Low-pass Filtered Signal (10 Hz)"]

plt.ion()
plt.close("all")
plt.plot((t - t[0]) / 60, v_, '.')
plt.xlabel("Time (minutes)")
plt.ylabel("Signal")
