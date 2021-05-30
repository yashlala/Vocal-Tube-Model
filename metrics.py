"""This python module contains loss functions for comparing waveforms."""

import numpy as np

from sklearn.metrics import mean_squared_error
from numpy.fft import fft
from tslearn.metrics import dtw


def _fft_amplitude(waveform, fft_cutoff):
    return np.abs(fft(waveform)[0:fft_cutoff])


def mse_loss(target_waveform, model_waveform, fft_cutoff):
    """Given 2 waveforms, return the MSE of their FFTs.

    The FFTs will be truncated at fft_cutoff (ie. highest freq).
    """
    target_fft = _fft_amplitude(target_waveform, fft_cutoff)
    model_fft = _fft_amplitude(model_waveform, fft_cutoff)
    return mean_squared_error(target_fft, model_fft)


def dtw_loss(target_waveform, model_waveform, fft_cutoff):
    """Given 2 waveforms, return the DTW alignment loss of their FFTs.

    The FFTs will be truncated at fft_cutoff (ie. highest freq).
    """
    target_fft = _fft_amplitude(target_waveform, fft_cutoff)
    model_fft = _fft_amplitude(model_waveform, fft_cutoff)

    # TODO: Do we want to find the peaks first, and just compare via a
    #       {0, 1} thing? This would remove all kinds of amplitude effects.
    #       If we do so, use this: `from scipy.signal import find_peaks`
    return dtw(target_fft, model_fft)


if __name__ == "__main__":
    a = [1, -1, 1, -1, 1, -1]
    b = [-1, 101, -1, -99, -1, 101]
    print(f"MSE Loss: {mse_loss(a, b, 100)}")
    print(f"DTW Loss: {dtw_loss(a, b, 100)}")
