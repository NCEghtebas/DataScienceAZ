'''
simple exponential smoothing
go back to last N values
y_t = a * y_t + a * (1-a)^1 * y_t-1 + a * (1-a)^2 * y_t-2 + ... + a*(1-a)^n * y_t-n
'''
from __future__ import division
import sys
from database import connect, select
from random import random, randint
import pylab as pl
from sweep import prepare_figure
import numpy as np


def retrievedata(id):
	return [i for i, in select('sir_results', ('i',), {'id': id}, order=('t',))]

def windowsize(data):
    '''Will eventually calculate window size based on data length'''
    return data

def sumstatextract(data):
    a= max(data)
    b = None
    c = None
    for t in xrange(len(data)):
        if data[t] > a/2.0:
            b = t
            break
    for t in xrange(len(data) -1, -1, -1):
        if data[t] > a/2.0:
            c = t
            break
    return a,b, c


def main():
    connect(sys.argv[1])

    data= retrievedata(sys.argv[2])
    print data
    pl.plot(data, hold= True)

    smoothed = np.convolve(data, np.ones(10)/10)
    print sumstatextract(smoothed)
    #print smoothed
    pl.plot(smoothed)

    prepare_figure()
    pl.show()
    
   

if __name__ == '__main__':
    main()