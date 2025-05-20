import os
import configparser
import numpy as np



config = configparser.ConfigParser()
config = configparser.ConfigParser()
config.sections()
config.read('../config.ini')

# Increasing timesteps
trials = 1
tsvals = np.arange(5000,10000,1000)

for trial in range(trials):
    config['Settings']['file name'] = 't'+str(trial+1)

    with open('../config.ini', 'w') as configfile:
        config.write(configfile)

    for ts in tsvals:
        config['Settings']['time steps'] = str(ts)
        config['Settings']['ss points'] = str(int(ts*0.8))

        with open('../config.ini', 'w') as configfile:
            config.write(configfile)

        os.system('python ../src/base.py')
        os.system('python ../src/ngit.py')

        for cores in range(1,6):
            config['Settings']['cores'] = str(cores)
            with open('../config.ini', 'w') as configfile:
                config.write(configfile)

            os.system('python ../src/parallel.py')
            os.system('python ../src/ngit_parallel.py')
    
    