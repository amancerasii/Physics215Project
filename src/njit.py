import numpy as np
import matplotlib.pyplot as plt
from lattice import Lattice
import datetime
from numba import njit
import time
from njitwolff import *
import configparser
from multiprocessing import Pool

tstart = time.perf_counter()

def isingrun(args):
    N = args[0]
    T = args[1]
    h = args[2]
    sst = args[3]
    print(T)
    lattice = Lattice(N, T, h)
    M = np.zeros(sst)
    E = np.zeros(sst)

    # equilibrate 
    for i in range(2000):
        lattice.spins, Mval = wolff(lattice.spins, lattice.N, lattice.b)

    for i in range(sst):
        lattice.spins, Mval = wolff(lattice.spins, lattice.N, lattice.b)
        M[i] = Mval
        E[i] = lattice.get_energy()

    return(E)


config = configparser.ConfigParser()
config.read('../config.ini')

L = int(config['Settings']['lattice size'])
Tstart = float(config['Settings']['start T'])
Tend = float(config['Settings']['end T'])
Tnum = int(config['Settings']['number of T'])
sst = int(config['Settings']['ss points'])
trial = int(config['Settings']['trial number'])
cores = int(config['Settings']['cores'])

filename = 't'+str(trial)
np.random.seed(trial)

h = 0.
tvals = np.linspace(Tstart,Tend,Tnum)
Mdata = np.zeros((sst+1,Tnum))
Edata = np.zeros((sst+1,Tnum))

############################################################
############################################################


for tind in range(Tnum):
    Edata[0,tind] = tvals[tind]
    args = [L, tvals[tind], h, sst]
    Edata[1:,tind] = isingrun(args)

dataformat = '_njit_'+'l'+str(L)+'ts'+str(sst)

calctime = time.perf_counter() - tstart
print("time",calctime)

print(filename+dataformat,calctime)

np.savetxt("../data/"+filename+dataformat+"energy.txt",Edata,'%f')

with open("../data/times.txt", "a") as f:
    f.write(filename+dataformat+"\t"+str(datetime.datetime.now())+"\t"+str(calctime)+"\n")