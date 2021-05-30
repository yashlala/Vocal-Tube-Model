# two tube model, draw frequency response and waveform, considering glottal
# voice source and mouth radiation save generated waveform as a wav file
# Length & Area value, from problems 3.8 in "Digital Processing of Speech
# Signals" by L.R.Rabiner and R.W.Schafer

import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write as wavwrite
import scipy.optimize

from n_tube_filter import NTubeFilter
from glottal_source import Glottal
from high_pass_filter import HPF
from metrics import mse_loss, dtw_loss


def _save_wav(waveform, file_path, sampling_rate):
    """Save the input waveform to the given file path as a .wav file.

    The waveform is looped, for ease of listening.
    """
    waveform_data = (waveform * 2 ** 15).astype(np.int16)
    wavwrite(file_path, sampling_rate, waveform_data)


def generate_waveform(tube_parameters):
    """Generate a sonic waveform, then pass it through arbitrary tubes.

    Some model parameters are fixed -- they are hardcoded into this method.
    The arguments to this method are designed to be optimized over.

    Arguments:
        - tube_parameters: A list of "tubes". Each tube is a 2-tuple of the
               form (tube_length (cm), tube_cross_sectional_area (cm^2)).

    Returns:
        - An output waveform.
        - The sampling rate of the output waveform.
    """
    # Some fixed hyperparameters for our model.
    sampling_rate = 48000
    rg0 = 0.95
    rl0 = 0.9
    v_sound = 35000.0  # Speed of sound in cm/s.
    hpf_cutoff_frequency = 2000

    # Define our Glottal emitter. This models the "source" of the sound.
    glo = Glottal(tclosed=2.5, trise=3.0, tfall=1.0, sampling_rate=sampling_rate)

    # Define our N-tube component. This transforms the output of our glottal
    # emitter.
    ntube = NTubeFilter(
        tube_props=tube_parameters,
        rg0=rg0,
        rl0=rl0,
        C0=v_sound,
        sampling_rate=sampling_rate,
    )

    # Define our high-pass filter. This mimics the transformation of sound
    # after leaving the mouth.
    hpf = HPF(cutoff_frequency=hpf_cutoff_frequency, sampling_rate=sampling_rate)

    # Generate the final output waveform by chaining all three components.
    return hpf.iir1(ntube.process(glo.get_output())), sampling_rate


def find_optimal_parameters(target_waveform, loss_function, fft_cutoff):
    """Find the 2-tube model that best mimicks the target waveform."""

    def gen_waveform_wrapper(x):
        t1_len, t1_area, t2_len, t2_area = x
        generated_waveform = generate_waveform(((t1_len, t1_area), (t2_len, t2_area)))
        return loss_function(target_waveform, generated_waveform, fft_cutoff)

    res = scipy.optimize.minimize(gen_waveform_wrapper, (1, 1, 1, 1))
    assert res.success, res.message

    t1_len, t1_area, t2_len, t2_area = res.x
    return (t1_len, t1_area), (t2_len, t2_area)
