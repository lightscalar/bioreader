import numpy as np
from ipdb import set_trace as debug


def lowpass(t, y, transition_band=5, freq_cutoff=10):
    """Low-pass sinc filter."""

    # Determine the sampling rate of the supplied data.
    fs = 1 / np.median(np.diff(t))
    nyquist = 0.5 * fs
    fc = freq_cutoff / nyquist
    b = transition_band / nyquist

    N = int(np.ceil(4 / b))
    if not N % 2:
        N -= 1

    n = np.arange(N)
    fs = 1 / np.median(np.diff(t))
    nyquist = 0.5 * fs
    f_low = freq_cutoff / nyquist

    # Compute sinc filter.
    h = np.sinc(2 * fc * (n - (N - 1) / 2.))

    # Compute Blackman window.
    w = (
        0.42
        - 0.5 * np.cos(2 * np.pi * n / (N - 1))
        + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    )

    # Multiply sinc filter with window.
    h = h * w

    # Normalize to get unity gain.
    h = h / np.sum(h)

    # Filter the signal.
    y_filt = np.convolve(y, h)
    lag = int((len(h) - 1) / 2)
    y_filt = y_filt[lag:-lag]

    # Keep output consistent with scipy-based filter.
    return y_filt, h


if __name__ == "__main__":
    from pylab import *

    t = np.linspace(0, 10, 2000)
    y = np.sin(2 * np.pi * t / 5) + 0.05 * np.random.randn(len(t))

    y_filt, h = lowpass(t, y, 15, freq_cutoff=5)
    # y_filt_2, _ = lowpass(t, y, 5, freq_cutoff=5)

    ion()
    close("all")
    plot(t, y)
    plot(t, y_filt)
    # plot(t, y_filt_2)
