import random 
import pylab as pl
from simpe_epi import gendataSIR

def plotdata(x, title="Simple SIR Model Number of Infected"):
	pl.figure()
	pl.plot(x, hold= True)
	pl.suptitle(title)
	pl.xlabel("Time Steps")
	pl.ylabel("Number of Infected")
	pl.show()

def sweep(var):
	x=[]
	if(var== hbeta):
		for i in range(len(hbeta)):
			while len(x)<20:
				x= gendataSIR(S,I,R, hbeta[i], 0.05)
			plotdata(x)
	elif(var==lbeta):
		for i in range(len(lbeta)):
			while len(x)<20:
				x= gendataSIR(S,I,R, lbeta[i], 0.05)
			plotdata(x)
	elif(var==hgamma):
		for i in range(len(hgamma)):
			while len(x)<20:
				x= gendataSIR(S,I,R, hgamma[i], 0.05)
			plotdata(x)
	elif(var==lgamma):
		for i in range(len(lgamma)):
			while len(x)<20:
				x= gendataSIR(S,I,R, lgamma[i], 0.05)
			plotdata(x)
	return x

#b = .09
#g = .05

S = 1000 
#seeding the outbreak with one infectious individual
I = 1 
#number of recovered
R = 0 

#likelyness to get infected is high
hbeta= [0.9, 0.8, 0.7, 0.6]
#likeliness to get infected is low
lbeta= [0.01, 0.05, 0.1, 0.2]

#likelyness to get cured (or die) is high
hgamma= [0.9, 0.8, 0.7, 0.6]
#likelyness to get cured (or die) is low
lgamma= [0.01,0.05, 0.1, 0.2]

'''
xx=[]
x = []
for i in range(5):
    while len(x) < 200:
        x= gendata(S, I, R, 0.09, 0.05)
        xx.append(x)
    plotdata(x)
    #print i, x
    x = []
'''
