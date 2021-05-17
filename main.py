#coding:utf-8

#
# two tube model, draw frequency response and waveform, considering glottal voice source and mouth radiation
#                 save generated waveform as a wav file

import numpy as np
from matplotlib import pyplot as plt
import json

import matplotlib.patches as patches
from twotube import *
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
	print (config)

	glo=Class_Glottal()
	hpf=Class_HPF()

	fig = plt.figure()

	i = 1
	for (key, val) in config["tube_values"].items():
		[L1, A1], [L2, A2] = val
		twotube = Class_TwoTube(L1, L2, A1, A2)

		plt.subplot(4,2,i)
		plot_freq_res(twotube, '/' + key + '/', glo, hpf)
		plt.subplot(4,2,i+1)
		yout = plot_waveform(twotube, '/' + key + '/', glo, hpf)
		save_wav(yout, 'yout_' + key + '.wav')  # save generated waveform as a wav file

		i += 2

	fig.tight_layout()
	plt.show()