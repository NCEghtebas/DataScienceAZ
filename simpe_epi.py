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
 
#generate data 
#takes n, alpha, and beta
def gendata():
    #number of susceptibles
    S = 1000 
    #seeding the outbreak with one infectious individual
    I = 1 
    #number of recovered
    R = 0 
     
    #total poopulation in system 
    N = S+I+R
     
    N = float(N)
    #time
    t = 0
        
    #Infectivity (probability of generating a new case at each step)
    b = .09
     
    #Probability of recovering @ each step
    g = .05
      
    sList = []
    iList = []
    rList = [] 
    #number of newly infected people on each step
    newIList = [] 
     
    while I > 0:
        newI = 0
        
        #there is a single random trial for each susceptible individual
        for i in range(S):
            #here, we're using a frequency dependent transmission process;
            #density dependence would be b*I
            
            #we use the method 'random.random()' to draw uniformly distributed numbers
            #in the range [0,1).
            if random.random() < b*(I/N):
                newI += 1
            
            #to switch to density dependence, comment out the block above and
            #uncomment the following:
            # if random.random() < b*I:
            #    newI += 1
        
        #Now we're going to see how many individuals recovery on this step.    
        recoverI = 0
        for i in range(I):
            if random.random() < g:
                recoverI += 1
        
        #Then, we wait to the all of the final accounting at the end of the step.
        #This is because we're making the assumption that all events on a step
        #happen simultaneously, so that individuals are infected on this step 
        #at the same time as others recover.
        
        S -= newI
        I += (newI - recoverI)
        R += recoverI
        
        #Then we add these values to their respective lists
        sList.append(S)
        iList.append(I)
        rList.append(R)
        newIList.append(newI)
        
        #print('t', t)
        t += 1

    # print('sList', sList)
    # print('iList', iList)
    # print('rList', rList)
    # print('newIList', newIList)

    return iList


pl.figure()
x = []
for i in range(10):
    while len(x) < 200:
        x= gendata()
    pl.plot(x, hold= True)
    print i, gendata()
    x = []

# fig = pl.gcf()
# fig.canvas.set_window_title('Simple SIR Model Number of Infected')

pl.suptitle("Simple SIR Model Number of Infected")

pl.xlabel("Time Steps")
pl.ylabel("Number of Infected")
pl.show()