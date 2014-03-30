import random 
import pylab as pl
from simple_sir import gendataSIR
import numpy as np


def prepare_figure(title="Simple SIR Model Number of Infected"):
	pl.suptitle(title)
	pl.xlabel("Time Steps")
	pl.ylabel("Number of Infected")


def sweep(gs, bs):
	for g in gs:
		for b in bs:
			res = gendataSIR(S,I,R, g, b)
			print 'g:', g, 'b:', b, 'len:', len(res)
			yield res


def sweep_range(start, stop, count):
	curr = start
	incr = (stop - start) / count
	for _ in xrange(count):
		yield curr
		curr += incr



subplots, (sp, ip, rp) = pl.subplots(3, sharex=True, sharey=True)
for sw in sweep(np.logspace(np.log10(0.9), np.log10(0.01), 25), np.logspace(np.log10(0.9), np.log10(0.1), 25)):
	s, i, r = zip(*sw)
	sp.plot(s)
	ip.plot(i)
	rp.plot(r)
prepare_figure()
subplots.subplots_adjust(hspace=0)
pl.show()

