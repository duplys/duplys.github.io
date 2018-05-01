#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Hardware Security Lab Robert Bosch GmbH on 2017-07-02.
Copyright (c) 2017 . All rights reserved.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def main():
	plt.title("Non-negligible vs negligible function")
	
	# evenly sampled intervals
	x = np.arange(0.001, 100.0, 0.001)

	# yrange from 0 to 1

	# red dashes, blue squares and green triangles
	# plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
	# plt.show()
	#plt.plot(x, 1/x, 'r', 1/(2**x))
	plt.ylim((0,0.2))
	plt.plot(x, 1/x, 'b', label='$1/x$')
	plt.plot(x, 1/(2**x), 'r', label='$2^{-x}$')
	#plt.legend([line_up, line_down], ['Line Up', 'Line Down'])
	plt.legend()
	# add a legend 
	
	plt.show()


if __name__ == '__main__':
	main()

