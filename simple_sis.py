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


def gendataSIS(s, i, gamma, beta, max_time=100):
    '''
    Generates randomized data based on a Simple SIR Model.

    Inputs: Takes the susceptible, infected, and recovered populations
            Takes the infection rate or likeliness to go from S to I
            Takes the recovery rate or likeliness to go from I to S

    Returns: Array of the number of infected at each time step
    '''
    # total poopulation in system
    n = float(s+i)

    res = []
    t = 0

    while i > 0 and s < n and t < max_time:
        newly_infected = 0
        newly_susceptible = 0

        for _ in xrange(s):
            if random.random() < beta*(i/n):
                newly_infected += 1

        for _ in xrange(i):
            if random.random() < gamma:
                newly_susceptible += 1

        # Update values
        s += newly_susceptible - newly_infected
        i += newly_infected - newly_susceptible

        # add values at this timestep
        res.append((s, i))
        t += 1

    return res

def main():
    s, i = zip(*gendataSIS(1000, 5, 0.5, 0.9, 100))
    pl.plot(s, hold= True)
    pl.plot(i)
    pl.show()


if __name__ == '__main__':
    main()
