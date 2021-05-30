"""This python module contains loss functions for comparing waveforms."""

import numpy as np

from sklearn.metrics import mean_squared_error
from numpy.fft import fft
from tslearn.metrics import dtw


def _fft_amplitude(waveform, fft_cutoff):
    return np.abs(fft(waveform)[0:fft_cutoff])


def mse_loss(predicted_waveform, actual_waveform, fft_cutoff):
    """Given 2 waveforms, return the MSE of their FFTs.

    The FFTs will be truncated at fft_cutoff (ie. highest freq).
    """
    predicted_fft = _fft_amplitude(predicted_waveform, fft_cutoff)
    actual_fft = _fft_amplitude(actual_waveform, fft_cutoff)
    return mean_squared_error(predicted_fft, actual_fft)


def dtw_loss(predicted_waveform, actual_waveform, fft_cutoff):
    """Given 2 waveforms, return the DTW alignment loss of their FFTs.

    The FFTs will be truncated at fft_cutoff (ie. highest freq).
    """
    predicted_fft = _fft_amplitude(predicted_waveform, fft_cutoff)
    actual_fft = _fft_amplitude(actual_waveform, fft_cutoff)

    # TODO: Do we want to find the peaks first, and just compare via a
    #       {0, 1} thing? This would remove all kinds of amplitude effects.
    #       If we do so, use this: `from scipy.signal import find_peaks`
    return dtw(predicted_fft, actual_fft)
