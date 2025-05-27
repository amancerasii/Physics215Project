from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def getTc(filename):

    sdata = np.loadtxt("../data/"+filename+"energy.txt")

    Tvals = sdata[0,:]

    Eave = np.mean(sdata[2:,:],axis=0)
    Esqave = np.mean(sdata[2:,:]**2,axis=0)

    Cvals = np.divide(Esqave - Eave**2, N*Tvals**2)

    def lorentzian(T, Tc, A, B):
        return A/((T-Tc)**2 + B)
        # return A/(abs(T-Tc)**(7/4)) + B
    
    popt, pcov = curve_fit(lorentzian, Tvals, Cvals, p0=[2.23, 0, 0] ,maxfev = 5000)
    # popt, pcov = curve_fit(lorentzian, Tvals, Xvals, maxfev = 5000)

    #plt.figure()
    #plt.scatter(Tvals,Cvals)
    #xdata = np.linspace(2,2.5,200)
    #plt.plot(xdata,lorentzian(xdata, *popt))
    #plt.show()
    

    perr = np.sqrt(np.diag(pcov))
    #print(perr[0])
    return popt[0]

def plotAccuracy(mode,l,core,c,ls):

    datapoints = np.zeros(len(Lvals))
    for i in range(len(Lvals)):
        for t in range(1,trials+1):
            L = Lvals[i]
            N = L*L
            if mode == "base" or mode == "njit":
                file = f"t{t}_{mode}_l{L}ts2000"
            else:
                file = f"t{t}_{mode}_l{L}ts2000c{core}"
            
            Tc = 2.26918531421
            acc = abs(getTc(file)-Tc)/Tc
            datapoints[i] += acc

            #print(t,datapoints[i],L)
    if ls == "-":
        plt.plot(Lvals,datapoints/trials,label=l,color=c,linestyle=ls,marker="o")
    else:
        plt.plot(Lvals,datapoints/trials,label=l,color=c,linestyle=ls,markerfacecolor='none',marker="o")

        

#Lvals = [4,8]
Lvals = [8,12,16,20,24,28,32]
trials = 1
N = 2

color1 = "#991f17" 
color21 = "#76c68f" 
color22 = "#48b5c4"
color23 = "#22a7f0"
color24 = "#1984c5"
color25 = "#115f9a"


# Showing that njit has a different implementation
plt.figure()
plotAccuracy("base","base",0,color1,"-")
plotAccuracy("njit","njit",0,color1,"--")
plotAccuracy("parallel","parallel (1 core)",1,color21,"-")
plotAccuracy("njitparallel","njit parallel (1 core)",1,color21,"--")
plt.ylabel("relative error")
plt.xlabel("$L$")
plt.ylim(0,0.025)
plt.legend()
plt.savefig("plots/fig07.png")

# Showing accuracy differences
plt.figure()
plotAccuracy("base","base",0,color1,"-")
plotAccuracy("njit","njit",0,color1,"--")
plotAccuracy("parallel","parallel (5 cores)",5,color25,"-")
plotAccuracy("njitparallel","njit parallel (5 cores)",5,color25,"--")
plt.ylabel("relative error")
plt.xlabel("$L$")
plt.ylim(0,0.025)

plt.legend()

plt.savefig("plots/fig08.png")

# Showing accuracy differences per core parallel
plt.figure()
plotAccuracy("base","base",0,color1,"-")
plotAccuracy("parallel","1 core",1,color21,"-")
plotAccuracy("parallel","2 cores",2,color22,"-")
plotAccuracy("parallel","3 cores",3,color23,"-")
plotAccuracy("parallel","4 cores",4,color24,"-")
plotAccuracy("parallel","5 cores",5,color25,"-")
plt.ylabel("relative error")
plt.xlabel("$L$")
plt.ylim(0,0.025)

plt.legend()
plt.savefig("plots/fig09.png")

# Showing accuracy differences per core njit parallel
plt.figure()
plotAccuracy("njit","njit",0,color1,"--")
plotAccuracy("njitparallel","1 core",1,color21,"-")
plotAccuracy("njitparallel","2 cores",2,color22,"-")
plotAccuracy("njitparallel","3 cores",3,color23,"-")
plotAccuracy("njitparallel","4 cores",4,color24,"-")
plotAccuracy("njitparallel","5 cores",5,color25,"-")
plt.ylabel("relative error")
plt.xlabel("$L$")
plt.ylim(0,0.025)

plt.legend()
plt.savefig("plots/fig10.png")


