# glottal voice source as input of Two Tubes Model of vocal tract
# Glottal Volume Velocity
# based on A.E.Rosenberg's formula as Glottal Volume Velocity

import numpy as np

class Glottal(object):
    def __init__(self, tclosed, trise, tfall, sampling_rate):
        # initalize
        self.tclosed = tclosed  # duration time of close state [mSec]
        self.trise = trise  # duration time of opening [mSec]
        self.tfall = tfall  # duration time of closing [mSec]
        self.sr = sampling_rate
        self.yg = self.make_one_plus()
        self.yg_repeat = self.make_N_repeat()

    def make_one_plus(
        self,
    ):
        # output yg
        self.N1 = int((self.tclosed / 1000.0) * self.sr)
        self.N2 = int((self.trise / 1000.0) * self.sr)
        self.N3 = int((self.tfall / 1000.0) * self.sr)
        self.LL = self.N1 + self.N2 + self.N3
        yg = np.zeros(self.LL)
        # print ('Length= ', self.LL)
        for t0 in range(self.LL):
            if t0 < self.N1:
                pass
            elif t0 <= (self.N2 + self.N1):
                yg[t0] = 0.5 * (1.0 - np.cos((np.pi / self.N2) * (t0 - self.N1)))
            else:
                yg[t0] = np.cos((np.pi / (2.0 * self.N3)) * (t0 - (self.N2 + self.N1)))
        return yg

    def make_N_repeat(self, repeat_num=200):
        self.yg_repeat = np.zeros(len(self.yg) * repeat_num)
        for loop in range(repeat_num):
            self.yg_repeat[len(self.yg) * loop : len(self.yg) * (loop + 1)] = self.yg
        return self.yg_repeat

    def get_output(self):
        return self.yg_repeat

    def fone(self, f):
        # calculate one point of frequecny response
        xw = 2.0 * np.pi * f / self.sr
        yi = 0.0
        yb = 0.0
        for v in range(0, (self.N2 + self.N3)):
            yi += self.yg[self.N1 + v] * np.exp(-1j * xw * v)
            yb += self.yg[self.N1 + v]
        val = yi / yb
        return np.sqrt(val.real ** 2 + val.imag ** 2)

    def H0(self, freq_low=100, freq_high=5000, Band_num=256):
        # get Log scale frequecny response, from freq_low to freq_high, Band_num points
        amp = []
        freq = []
        bands = np.zeros(Band_num + 1)
        fcl = freq_low * 1.0  # convert to float
        fch = freq_high * 1.0  # convert to float
        delta1 = np.power(fch / fcl, 1.0 / (Band_num))  # Log Scale
        bands[0] = fcl
        # print ("i,band = 0", bands[0])
        for i in range(1, Band_num + 1):
            bands[i] = bands[i - 1] * delta1
            # print ("i,band =", i, bands[i])
        for f in bands:
            amp.append(self.fone(f))
        return np.log10(amp) * 20, bands  # = amp value, freq list
