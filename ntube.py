# coding:utf-8

#
# Two Tube Model, A python Class to calculate frequecny response and procee reflection transmission of resonance tube
#

import numpy as np
from matplotlib import pyplot as plt

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0


class Class_NTube(object):
    def __init__(self, tube_props, rg0, rl0, sampling_rate, C0):
        self.tube_props = tube_props
        self.sr = sampling_rate

        self.tu = []
        for tube_prop in self.tube_props:
            self.tu.append(tube_prop[0] / C0)
        self.r = [rg0]  # rg is reflection coefficient between glottis and 1st tube
        for i in range(len(tube_props) - 1):
            curr_tube_props = tube_props[i]
            next_tube_props = tube_props[i + 1]

            self.r.append(
                (next_tube_props[1] - curr_tube_props[1])
                / (next_tube_props[1] + curr_tube_props[1])
            )
        self.r.append(rl0)  # reflection coefficient between last tube and mouth

    def fone(self, xw):
        # calculate one point of frequency response
        yi = 0.5
        for r_elem in self.r:
            yi *= 1.0 + r_elem
        yi *= np.exp(-1.0j * np.sum(self.tu) * xw)

        yb = 1.0
        for i in range(len(self.tu)):
            for j in range(len(self.tu) - i):
                yb_add = (
                    self.r[j + i + 1]
                    * self.r[j]
                    * np.exp(-2.0j * np.sum(self.tu[j : j + i + 1]) * xw)
                )

                yb += yb_add

        val = yi / yb
        return np.sqrt(val.real ** 2 + val.imag ** 2)

    def H0(self, freq_low=100, freq_high=5000, Band_num=256):
        # get Log scale frequency response, from freq_low to freq_high, Band_num points
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
            fone_out = self.fone(f * 2.0 * np.pi)
            amp.append(fone_out)
        return np.log10(amp) * 20, bands  # = amp value, freq list

    def process(self, yg):
        # process reflection transmission of resonance tube: yg is input, y2tm is output
        # two serial resonance tube
        #                      ---------------------
        #                      |                    |
        #   -------------------                     |
        #   |                                       |
        #   |                                       |
        #   -------------------                     |
        #                      |                    |
        #                      ---------------------
        # reflection ratio
        #   rg                 r1                   rl0
        #   y1[0]---(forward)--->   y1[1]---(forward)--->
        #   <-----(backward)--y2[0]  <---(backward)---y2[1]
        # input yg                                 output y2tm
        #
        #
        y2tm = np.zeros(len(yg))

        y1 = [np.zeros(round(self.tu[i] * self.sr) + 1) for i in range(len(self.tu))]
        y2 = [np.zeros(round(self.tu[i] * self.sr) + 1) for i in range(len(self.tu))]

        for tc0 in range(len(yg)):

            for i in range(len(self.tu)):
                for j in range((len(y1[i]) - 1), 0, -1):  # process one step
                    y1[i][j] = y1[i][j - 1]
                    y2[i][j] = y2[i][j - 1]

            # calculate reflection
            for i in range(len(self.tu)):
                # Handling y1
                if i == 0:
                    y1[i][0] = ((1.0 + self.r[i]) / 2.0) * yg[tc0] + self.r[i] * y2[i][
                        -1
                    ]
                else:
                    y1[i][0] = (1 + self.r[i]) * y1[i - 1][-1] + self.r[i] * y2[i][-1]

                # Handling y2
                y2[i][0] = -1.0 * self.r[i + 1] * y1[i][-1]
                if i != len(self.tu) - 1:
                    y2[i][0] += (1.0 - self.r[i + 1]) * y2[i + 1][-1]

            y2tm[tc0] = (1 + self.r[-1]) * y1[-1][-1]

        return y2tm
