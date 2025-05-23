import numpy as np
import matplotlib.pyplot as plt
from lattice import Lattice
import datetime
# from numba import njit
import time
from wolff import *
import configparser

tstart = time.perf_counter()

def isingrun(N,T,h,sst):
    print(T)
    lattice = Lattice(N, T, h)
    M = np.zeros(sst)

    # equilibrate 
    for i in range(1000):
        lattice.spins, Mval = wolff(lattice.spins, lattice.N, lattice.b)

    for i in range(sst):
        lattice.spins, Mval = wolff(lattice.spins, lattice.N, lattice.b)
        M[i] = Mval

    return(M)


config = configparser.ConfigParser()
config.read('../config.ini')

L = int(config['Settings']['lattice size'])
Tstart = float(config['Settings']['start T'])
Tend = float(config['Settings']['end T'])
Tnum = int(config['Settings']['number of T'])
sst = int(config['Settings']['ss points'])
filename = str(config['Settings']['file name'])

h = 0.
tvals = np.linspace(Tstart,Tend,Tnum)
Mdata = np.zeros((sst+1,Tnum))

############################################################
############################################################

for tind in range(Tnum):
    Mdata[0,tind] = tvals[tind]
    Mdata[1:,tind] = isingrun(L,tvals[tind],h,sst)

dataformat = '_base_'+'l'+str(L)+'ts'+str(sst)

############################################################
############################################################

calctime = time.perf_counter() - tstart
print("time",calctime)

print(filename+dataformat,calctime)


np.savetxt("../data/"+filename+dataformat+"spin.txt",Mdata,'%f')


with open("../data/times.txt", "a") as f:
    f.write(filename+dataformat+"\t"+str(datetime.datetime.now())+"\t"+str(calctime)+"\n")


