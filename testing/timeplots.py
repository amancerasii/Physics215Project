import numpy as np
import matplotlib.pyplot as plt

with open('../data/times.txt', 'r') as file:
    data_array = [line.strip().split() for line in file.readlines()]  # Assumes first 2 lines

# base vs timestep
trials = 2
tsvals = np.arange(100,400,100)

for mode in ['base','ngit']:
    calctimevals = []

    for ts in tsvals:
        val = 0
        for i in range(len(data_array)):
            filename = data_array[i][0]
            
            if filename.find(mode) != -1 and filename.find('s'+str(ts)) != -1 :
                val += float(data_array[i][3])
        
        print(val/trials)
        calctimevals.append(val/trials)

    plt.plot(tsvals,calctimevals,label=mode)


for mode in ['parallel','ngitparallel']:
    for cores in range(1,5):
        calctimevals = []

        for ts in tsvals:
            val = 0
            for i in range(len(data_array)):
                filename = data_array[i][0]
                
                if filename.find(mode) != -1\
                        and filename.find('s'+str(ts)) != -1\
                            and filename.find('c'+str(cores)) != -1:
                    val += float(data_array[i][3])
            
            print(val/trials)
            calctimevals.append(val/trials)

        plt.plot(tsvals,calctimevals,label=mode+str(cores))

plt.legend()
plt.show()