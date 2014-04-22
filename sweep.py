import random 
import pylab as pl
from simple_sir import gendataSIR
from simple_sis import gendataSIS
import numpy as np


def prepare_figure(title="Simple SIR Model Number of Infected"):
    pl.suptitle(title)
    pl.xlabel("Time Steps")
    pl.ylabel("Number of Infected")


def sweep_sir(s, i, r, gs, bs):
    for g in gs:
        for b in bs:
            res = gendataSIR(s, i, r, g, b)
            yield (g, b, res)

def sweep_sis(s, i, gs , bs):
    for g in gs:
        for b in bs:
            res = gendataSIS(s, i, g, b)
            yield (g, b, res)

def sweep_range(start, stop, count):
    return np.logspace(np.log10(start), np.log10(stop), count)

def main():
    subplots, (sp, ip) = pl.subplots(2, sharex=True, sharey=True)
    srg = sweep_range(0.99, 0.01, 5)
    srb= sweep_range(0.9, 0.01, 5)
    for g, b, sw in sweep_sis(1000, 5, srg, srb):
        print 'g:', g, 'b:', b, 'len:', len(sw)
        s, i= zip(*sw)
        sp.plot(s)
        ip.plot(i)
    prepare_figure()
    subplots.subplots_adjust(hspace=0)
    pl.show()
    '''
    subplots, (sp, ip, rp) = pl.subplots(3, sharex=True, sharey=True)
    sr = sweep_range(0.99, 0.01, 25)
    for g, b, sw in sweep_sir(1000, 5, 0, sr, sr):
        print 'g:', g, 'b:', b, 'len:', len(sw)
        s, i, r = zip(*sw)
        sp.plot(s)
        ip.plot(i)
        rp.plot(r)
    prepare_figure()
    subplots.subplots_adjust(hspace=0)
    pl.show()
    '''


if __name__ == '__main__':
    main()
