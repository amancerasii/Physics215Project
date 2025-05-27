import numpy as np
import matplotlib.pyplot as plt

with open('../data/times.txt','r') as file:
    data_array = [line.strip().split() for line in file.readlines()]

basedata = []
njitdata = []

parallel1data = []
parallel2data = []
parallel3data = []
parallel4data = []
parallel5data = []

njitparallel1data = []
njitparallel2data = []
njitparallel3data = []
njitparallel4data = []
njitparallel5data = []

def getData(mode,core):

    data = np.zeros((len(Lvalues),trials))

    for i in range(len(data_array)):
        name = data_array[i][0]
        time = data_array[i][3]
        
        for l in range(len(Lvalues)):
            for t in range(trials):
                if mode == "parallel" or mode == "njitparallel":
                    if name.find("_"+mode+"_") > -1 \
                            and name.find("l"+str(Lvalues[l])) > -1\
                            and name.find("t"+str(t+1)+"_") > -1\
                            and name.find("c"+str(core)) > -1:
                        #print(name, time)
                        data[l,t] = float(time)


                else:
                    if name.find("_"+mode+"_") > -1 \
                            and name.find("l"+str(Lvalues[l])) > -1\
                            and name.find("t"+str(t+1)) > -1:
                        #print(name, time)
                        data[l,t] = float(time)



    return data

def plotData(data,l,col,ls,m):
    if m == ".":
        plt.plot(Lvalues, np.mean(data,1),label=str(l),color=col,linestyle=ls,marker="o")
    else:
        plt.plot(Lvalues, np.mean(data,1),label=str(l),color=col,linestyle=ls,marker="o",markerfacecolor='none')

            
Lvalues = [4,8,12,16,20,24,28,32]
trials = 3
core = 5

color1 = "#991f17" 
color21 = "#76c68f" 
color22 = "#48b5c4"
color23 = "#22a7f0"
color24 = "#1984c5"
color25 = "#115f9a"

basedata = getData('base',1)
njitdata = getData('njit',1)
parallel1data = getData('parallel',1)
parallel2data = getData('parallel',2)
parallel3data = getData('parallel',3)
parallel4data = getData('parallel',4)
parallel5data = getData('parallel',5)

njitparallel1data = getData('njitparallel',1)
njitparallel2data = getData('njitparallel',2)
njitparallel3data = getData('njitparallel',3)
njitparallel4data = getData('njitparallel',4)
njitparallel5data = getData('njitparallel',5)

plotData(basedata,"base",color1,"-",".")
plotData(njitdata,"njit",color1,"--","o")
plotData(njitparallel5data,"njit parallel (5 cores)",color25,"--","o")
plotData(parallel5data,"parallel (5 cores)",color25,"-",".")


print(1/njitdata)
print(1/basedata)
print("njit",np.mean(basedata/njitdata,1))
print("parallel",np.mean(basedata/parallel5data,1))
print("njit parallel",np.mean(basedata/njitparallel5data,1))

plt.yscale("log")
plt.legend()
plt.xlabel("$L$")
plt.ylabel("$t$ (s)")

plt.savefig("plots/fig01.png")
#plt.subplot(1,3,2)

plt.figure()
plotData(basedata,"base","#226E9C","-",".")
plt.yscale("log")
plt.legend()
plt.xlabel("$L$")
plt.ylabel("$t$ (s)")
plotData(parallel1data,"1 core",color21,"-",".")
plotData(parallel2data,"2 cores",color22,"-",".")
plotData(parallel3data,"3 cores",color23,"-",".")
plotData(parallel4data,"4 cores",color24,"-",".")
plotData(parallel5data,"5 cores",color25,"-",".")
plt.savefig("plots/fig02.png")


plt.figure()
plotData(njitdata,"njit",color1,"--","o")
plotData(njitparallel1data,"1 core",color21,"--","o")
plotData(njitparallel2data,"2 cores",color22,"--","o")
plotData(njitparallel3data,"3 cores",color23,"--","o")
plotData(njitparallel4data,"4 cores",color24,"--","o")
plotData(njitparallel5data,"5 cores",color25,"--","o")
plt.yscale("log")
plt.legend()
plt.xlabel("$L$")
plt.ylabel("$t$ (s)")

plt.savefig("plots/fig03.png")


Lvalues = [2,4,6,8,10,12]
trials = 3
core = 5

basedata = getData('base',1)
njitdata = getData('njit',1)
parallel1data = getData('parallel',1)
parallel2data = getData('parallel',2)
parallel3data = getData('parallel',3)
parallel4data = getData('parallel',4)
parallel5data = getData('parallel',5)

njitparallel1data = getData('njitparallel',1)
njitparallel2data = getData('njitparallel',2)
njitparallel3data = getData('njitparallel',3)
njitparallel4data = getData('njitparallel',4)
njitparallel5data = getData('njitparallel',5)

#plt.subplot(1,3,1)

plt.figure()
plotData(basedata,"base",color1,"-",".")
plotData(njitdata,"njit",color1,"--","o")
plotData(parallel5data,"parallel (5 cores)",color25,"-",".")
plotData(njitparallel5data,"njit parallel (5 cores)",color25,"--","o")

plt.yscale("log")
plt.legend()
plt.xlabel("$L$")
plt.ylabel("$t$ (s)")

plt.savefig("plots/fig04.png")
#plt.subplot(1,3,2)

plt.figure()
plotData(basedata,"base",color1,"-",".")
plotData(parallel1data,"1 core",color21,"-",".")
plotData(parallel2data,"2 cores",color22,"-",".")
plotData(parallel3data,"3 cores",color23,"-",".")
plotData(parallel4data,"4 cores",color24,"-",".")
plotData(parallel5data,"5 cores",color25,"-",".")

plt.yscale("log")
plt.legend()
plt.xlabel("$L$")
plt.ylabel("$t$ (s)")

plt.savefig("plots/fig05.png")


plt.figure()
plotData(njitdata,"njit",color1,"--","o")
plotData(njitparallel1data,"1 core",color21,"--","o")
plotData(njitparallel2data,"2 cores",color22,"--","o")
plotData(njitparallel3data,"3 cores",color23,"--","o")
plotData(njitparallel4data,"4 cores",color24,"--","o")
plotData(njitparallel5data,"5 cores",color25,"--","o")

plt.yscale("log")
plt.legend()
plt.xlabel("$L$")
plt.ylabel("$t$ (s)")

plt.savefig("plots/fig06.png")
