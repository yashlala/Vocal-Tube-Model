# two tube model, draw frequency response and waveform, considering glottal
# voice source and mouth radiation save generated waveform as a wav file
# Length & Area value, from problems 3.8 in "Digital Processing of Speech
# Signals" by L.R.Rabiner and R.W.Schafer

import json

import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write as wavwrite

from ntube import NTube
from glottal import Glottal
from high_pass_filter import HPF


def gen_waveform(twotube, glo, hpf):
    """Generate a sonic waveform given model components.

    Arguments:
        - A glottal model (simulates source).
        - A 2-tube model (simulates filter).
        - A high-pass filter model (simulates post-mouth).
    """
    yg_repeat = glo.get_output()
    y2tm = twotube.process(yg_repeat)
    return hpf.iir1(y2tm)


def save_wav(waveform, file_path, sampling_rate):
    """Save the input waveform to the given file path as a .wav file.

    The waveform is looped, for ease of listening.
    """
    waveform_data = (waveform * 2 ** 15).astype(np.int16)
    wavwrite(file_path, sampling_rate, waveform_data)


# TODO: pull out of the parameters out of JSON form.
#       Just loop over them in this script.
#
# glottal_parameters =  {
#         "rg0": 0.95,
#         "rl0": 0.9,
#         "sampling_rate": 48000,
#         "C0": 35000.0,
#         "glottal_tclosed": 2.5,
#         "glottal_trise": 3.0,
#         "glottal_tfall": 1.0,
#         "hpf_fc": 2000
#         }
#
# 	"tube_values" : {
# 		"random": [[5, 1], [4, 2]],
# 		"a": [[9, 1], [8, 7]],
# 		"ae": [[4, 1], [13, 8]],
# 		"i": [[9, 8], [6, 1]],
# 		"u": [[10, 7], [7, 3]],
# 		"o": [[9, 1], [8, 7], [5.6, 3]]
# 	}
# }


if __name__ == "__main__":

    sampling_rate = 48000

    # Define our Glottal emitter. This models the "source" of the sound.
    # As per the source-filter model, its frequency should not significantly
    # affect the pitch of the resulting sound (although this remains to be
    # confirmed). We keep it constant for all vowel runs.
    glo = Glottal(tclosed=2.5, trise=3.0, tfall=1.0, sampling_rate=sampling_rate)

    # Define our high-pass filter. This models the transformations that occur
    # to sounds as/after they are leaving the human mouth. We don't optimize
    # over these parameters, either.
    hpf = HPF(fc=2000, sampling_rate=sampling_rate)

    with open("config.json", "r") as f:
        config = json.load(f)
    params = config["parameters"]

    output_waveforms = {}

    # Save the unfiltered output of the generator -- ie. just the sound of the
    # glottal generator.
    output_waveforms["source"] = glo.yg_repeat.tolist()
    save_wav(glo.yg_repeat, "source.wav", sampling_rate)

    # Test out various parameters of the N-tube model component.
    for (vowel_name, val) in config["tube_values"].items():

        # Define our N-tube component. This transforms the output of our
        # glottal emitter, modelling the way that sounds are transformed inside
        # the vocal tract. We optimize over these parameters.
        twotube = NTube(val, params["rg0"], params["rl0"], sampling_rate, params["C0"])

        # Generate the final output waveform using all three model components.
        y_out = gen_waveform(twotube, glo, hpf)
        output_waveforms[vowel_name] = y_out.tolist()
        save_wav(y_out, vowel_name + ".wav", sampling_rate)

    # Save the output waveforms in JSON format. Who needs `.wav`?
    output = {
        "sampling_rate": sampling_rate,
        "output_waveforms": output_waveforms,
    }
    with open("output.json", "w") as f:
        json.dump(output, f)
