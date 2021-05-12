#coding:utf-8

#
# two tube model, draw frequency response and waveform, considering glottal voice source and mouth radiation
#                 save generated waveform as a wav file

import numpy as np
from matplotlib import pyplot as plt

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
	#
	# /a/
	L1_a=9.0    # set list of 1st tube's length by unit is [cm]
	A1_a=1.0    # set list of 1st tube's area by unit is [cm^2]
	L2_a=8.0    # set list of 2nd tube's length by unit is [cm]
	A2_a=7.0    # set list of 2nd tube's area by unit is [cm^2]
	# /ae/
	L1_ae=4.0    # set list of 1st tube's length by unit is [cm]
	A1_ae=1.0    # set list of 1st tube's area by unit is [cm^2]
	L2_ae=13.0   # set list of 2nd tube's length by unit is [cm]
	A2_ae=8.0    # set list of 2nd tube's area by unit is [cm^2]
	# /i/
	L1_i=9.0    # set list of 1st tube's length by unit is [cm]
	A1_i=8.0    # set list of 1st tube's area by unit is [cm^2]
	L2_i=6.0    # set list of 2nd tube's length by unit is [cm]
	A2_i=1.0    # set list of 2nd tube's area by unit is [cm^2]
	# /u/
	L1_u=10.0   # set list of 1st tube's length by unit is [cm]
	A1_u=7.0    # set list of 1st tube's area by unit is [cm^2]
	L2_u=7.0    # set list of 2nd tube's length by unit is [cm]
	A2_u=3.0    # set list of 2nd tube's area by unit is [cm^2]
	
	# insatnce
	twotube_a  =  Class_TwoTube(L1_a,L2_a,A1_a,A2_a)
	twotube_ae =  Class_TwoTube(L1_ae,L2_ae,A1_ae,A2_ae)
	twotube_i  =  Class_TwoTube(L1_i,L2_i,A1_i,A2_i)
	twotube_u  =  Class_TwoTube(L1_u,L2_u,A1_u,A2_u)
	
	glo=Class_Glottal()   # instance as glottal voice source
	hpf=Class_HPF()       # instance for mouth radiation effect
	
	# draw
	fig = plt.figure()
	
	# /a/
	plt.subplot(4,2,1)
	plot_freq_res(twotube_a, '/a/', glo, hpf)
	plt.subplot(4,2,2)
	yout_a=plot_waveform(twotube_a, '/a/', glo, hpf)
	save_wav(yout_a, 'yout_a.wav')  # save generated waveform as a wav file
	# /ae/
	plt.subplot(4,2,3)
	plot_freq_res(twotube_ae, '/ae/', glo, hpf)
	plt.subplot(4,2,4)
	yout_ae=plot_waveform(twotube_ae, '/ae/', glo, hpf)
	save_wav(yout_ae, 'yout_ae.wav')  # save generated waveform as a wav file
	# /i/
	plt.subplot(4,2,5)
	plot_freq_res(twotube_i, '/i/', glo, hpf)
	plt.subplot(4,2,6)
	yout_i=plot_waveform(twotube_i, '/i/', glo, hpf)
	save_wav(yout_i, 'yout_i.wav')  # save generated waveform as a wav file
	# /u/
	plt.subplot(4,2,7)
	plot_freq_res(twotube_u, '/u/', glo, hpf)
	plt.subplot(4,2,8)
	yout_u=plot_waveform(twotube_u, '/u/', glo, hpf)
	save_wav(yout_u, 'yout_u.wav')  # save generated waveform as a wav file
	#
	fig.tight_layout()
	plt.show()
	
#This file uses TAB
