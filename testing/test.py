import os
import configparser
import numpy as np
import time

config = configparser.ConfigParser()
config = configparser.ConfigParser()
config.sections()
config.read('../config.ini')

# Increasing timesteps
tstart = time.perf_counter()

trials = 3
Lvals = [2,6,10]

for t in range(trials):
    config['Settings']['file name'] = str(t+1)

    with open('../config.ini', 'w') as configfile:
        config.write(configfile)

    for L in Lvals:
        config['Settings']['lattice size'] = str(L)

        with open('../config.ini', 'w') as configfile:
            config.write(configfile)

        os.system('python ../src/base.py')
        os.system('python ../src/njit.py')

        for cores in range(1,6):
            config['Settings']['cores'] = str(cores)
            with open('../config.ini', 'w') as configfile:
                config.write(configfile)

            os.system('python ../src/parallel.py')
            os.system('python ../src/njitparallel.py')
 
calctime = time.perf_counter() - tstart
print("total time:",calctime)
