from filters import *

from glob import glob
import numpy as np
import pandas as pd
import pylab as plt
import seaborn as sns


dirs = glob("today_card/ARXIV/*")
pzt = pd.read_csv(f"{dirs[0]}/PZT.csv")
t = pzt["Corrected Timestamps (seconds)"]
v = pzt["Low-pass Filtered Signal (10 Hz)"]
# v_ = np.array(pzt["Raw Signal"])

v_ = (v - np.median(v)) / v.std()
v_[np.abs(v_) > 5 * v.std()] = 0
v_ *= -1

plt.ion()
plt.close("all")
plt.plot((t - t[0]) / 60, v_)
