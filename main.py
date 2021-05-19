#coding:utf-8

#
# two tube model, draw frequency response and waveform, considering glottal voice source and mouth radiation
#                 save generated waveform as a wav file

import numpy as np
from matplotlib import pyplot as plt
import json

import matplotlib.patches as patches
from ntube import *
from glottal import *
from HPF import *
from utils import *

if __name__ == '__main__':
	# Length & Area value, from problems 3.8 in "Digital Processing of Speech Signals" by L.R.Rabiner and R.W.Schafer
	with open("config.json", 'r') as f:
		config = json.load(f)
	params = config["parameters"]

	glo=Class_Glottal(params["glottal_tclosed"], params["glottal_trise"], params["glottal_tfall"], params["sampling_rate"])
	hpf=Class_HPF(params["hpf_fc"], params["sampling_rate"])

	fig = plt.figure()
	fig_rows = len(config["tube_values"])
	fig_cols = 2

	i = 1

	output_waveforms = {}

	output_waveforms["source"] = glo.yg_repeat.tolist()
	save_wav(glo.yg_repeat, 'source' + '.wav', params["sampling_rate"])
	for (key, val) in config["tube_values"].items():
		twotube = Class_NTube(val, params["rg0"], params["rl0"], params["sampling_rate"], params["C0"])

		#plt.subplot(fig_rows,fig_cols,i)
		plot_freq_res(twotube, '/' + key + '/', glo, hpf)
		#plt.subplot(fig_rows,fig_cols,i+1)
		yout = plot_waveform(twotube, '/' + key + '/', glo, hpf)
		
		output_waveforms[key] = yout.tolist()

		save_wav(yout, 'yout_' + key + '.wav', params["sampling_rate"])  # save generated waveform as a wav file

		i += 2

	output = {
		"sampling_rate": params["sampling_rate"],
		"output_waveforms": output_waveforms
	}
	with open('output.json', 'w') as f:
		json.dump(output, f)

	#fig.tight_layout()
	#plt.show()