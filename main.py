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

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 
#  matplotlib  2.1.1
#  scipy 1.0.0

if __name__ == '__main__':
	# Length & Area value, from problems 3.8 in "Digital Processing of Speech Signals" by L.R.Rabiner and R.W.Schafer
	with open("config.json", 'r') as f:
		config = json.load(f)

	glo=Class_Glottal()
	hpf=Class_HPF()

	fig = plt.figure()
	fig_rows = 5
	fig_cols = 2

	i = 1

	for (key, val) in config["tube_values"].items():
		twotube = Class_NTube(val)

		plt.subplot(fig_rows,fig_cols,i)
		plot_freq_res(twotube, '/' + key + '/', glo, hpf)
		plt.subplot(fig_rows,fig_cols,i+1)
		yout = plot_waveform(twotube, '/' + key + '/', glo, hpf)
		save_wav(yout, 'yout_' + key + '.wav')  # save generated waveform as a wav file

		i += 2

	fig.tight_layout()
	plt.show()