import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, generate_binary_structure
import datetime
import time
from multiprocessing import Pool
import configparser

tstart = time.perf_counter()

def get_energy(lattice):
    kern = generate_binary_structure(2,2)
    kern[1][1] = False
    arr = -lattice * convolve(lattice, kern, mode='constant')
    return arr.sum()

def metropolis(spin_arr, times, BJ, energy,N):
    spin_arr = spin_arr.copy()
    net_spins = np.zeros(sspoints)
    net_energy = np.zeros(sspoints)

    for t in range(0,times):
        # pick random point on array and flip spin
        x = np.random.randint(0,N)
        y = np.random.randint(0,N)
        spin_i = spin_arr[x,y] # initial spin
        spin_f = spin_i*-1 # proposed spin flip

        # compute change in energy
        E_i = 0
        E_f = 0
        if x > 0:
            E_i += -spin_i*spin_arr[x-1,y]
            E_f += -spin_f*spin_arr[x-1,y]
        if x < N-1:
            E_i += -spin_i*spin_arr[x+1,y]
            E_f += -spin_f*spin_arr[x+1,y]
        if y > 0:
            E_i += -spin_i*spin_arr[x,y-1]
            E_f += -spin_f*spin_arr[x,y-1]
        if y < N-1:
            E_i += -spin_i*spin_arr[x,y+1]
            E_f += -spin_f*spin_arr[x,y+1]

        dE = E_f - E_i
        if (dE > 0)*(np.random.random() < np.exp(-BJ*dE)) or dE <= 0:
            spin_arr[x,y] = spin_f
            energy += dE
       
        if (t >= times-sspoints):
            net_spins[t-times+sspoints] = abs(spin_arr.sum())
            net_energy[t-times+sspoints] = energy

    return net_spins, net_energy

def isingRun(args):
    B = args[0]
    np.random.seed(args[1])

     # Create Random Negative Lattice
    # init_random = np.random.random((N,N))
    # lattice_n = np.zeros((N,N))

    # lattice_n[init_random >= 0.5] = 1
    # lattice_n[init_random < 0.5] = -1
    lattice_n = np.ones((N,N))

    spins, energies = metropolis(lattice_n, t, B, get_energy(lattice_n),N)

    return spins, energies

###############################################################################

config = configparser.ConfigParser()
config.read('../config.ini')

N = int(config['Settings']['lattice size'])
t = int(config['Settings']['time steps'])
runs = int(config['Settings']['runs'])
cores = int(config['Settings']['cores'])
Tstart = float(config['Settings']['start T'])
Tend = float(config['Settings']['end T'])
Tnum = int(config['Settings']['number of T'])
sspoints = int(config['Settings']['ss points'])
filename = str(config['Settings']['file name'])

Tvals = np.linspace(Tstart,Tend,Tnum)

if __name__ == '__main__':
    # tspins = np.zeros(t)
    # for r in range(runs):
    #     spins, energies = isingRun(r)
    #     tspins = tspins + spins

    spindata = np.zeros((sspoints+1,Tnum))
    energydata = np.zeros((sspoints+1,Tnum))

    for j in range(Tnum):
        T = Tvals[j]
        print("T = ",T)
        B = 1/T

        spindata[0,j] = T
        energydata[0,j] = T

        with Pool(cores) as p:
            args = [[B,i] for i in range(runs)]
            val = p.map(isingRun, args)
            
            tspins = np.zeros(sspoints)
            tenergy = np.zeros(sspoints)

            for i in range(runs):
                tspins = tspins + val[i][0]
                tenergy = tenergy + val[i][1]

            spindata[1:,j] = tspins
            energydata[1:,j] = tenergy

    calctime = time.perf_counter() - tstart
    print(filename,calctime)

    dataformat = '_parallel_'+'l'+str(N)+'ts'+str(t)+'r'+str(runs)+'c'+str(cores)

    np.savetxt("../data/"+filename+dataformat+"spin.txt",spindata,'%f')
    # np.savetxt("../data/"+filename+dataformat+"energy.txt",energydata,'%f')


    with open("../data/times.txt", "a") as f:
        f.write(filename+dataformat+"\t"+str(datetime.datetime.now())+"\t"+str(calctime)+"\n")
