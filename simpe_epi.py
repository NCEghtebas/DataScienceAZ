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
    # number of susceptibles
    S = s
    # seeding the outbreak with one infectious individual
    I = i
    # number of recovered
    R = r

    # total poopulation in system
    N = S+I+R

    N = float(N)
    # time
    t = 0

    sList = []
    iList = []
    rList = []
    # number of newly infected people on each step
    newIList = []

    while I > 0:
        newI = 0

        # there is a single random trial for each susceptible individual
        for _ in xrange(S):
            # frequency dependent
            if random.random() < beta*(I/N):
                newI += 1

            # Density dependent
            # if random.random() < b*I:
            #    newI += 1

        recoverI = 0
        for _ in xrange(I):
            if random.random() < gamma:
                recoverI += 1

        # Update values
        S -= newI
        I += (newI - recoverI)
        R += recoverI

        # add values at this timestep
        sList.append(S)
        iList.append(I)
        rList.append(R)
        newIList.append(newI)

        t += 1

    return iList
