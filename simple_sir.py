'''
Alethea Butler and Chloe Eghtebas
March 25, 2014

based on code from:

A simple SIR model written in Python
Jon Zelner
University of Michigan
October 8, 2009
'''

import random
import pylab as pl


def gendataSIR(s, i, r, gamma, beta):
    '''
    Generates randomized data based on a Simple SIR Model.

    Inputs: Takes the susceptible, infected, and recovered populations
            Takes the infection rate or likeliness to go from S to I
            Takes the recovery rate or likeliness to go from I to R

    Returns: Array of the number of infected at each time step
    '''
    # total poopulation in system
    n = float(s+i+r)

    res = []

    while i > 0:
        newI = 0

        # this is a single random trial for each susceptible individual
        for _ in xrange(s):
            # frequency dependent
            if random.random() < beta*(i/n):
                newI += 1

            # Density dependent
            # if random.random() < b*i:
            #    newI += 1

        recoverI = 0
        for _ in xrange(i):
            if random.random() < gamma:
                recoverI += 1

        # Update values
        s -= newI
        i += (newI - recoverI)
        r += recoverI

        # add values at this timestep
        res.append((s, i, r))

    return res
