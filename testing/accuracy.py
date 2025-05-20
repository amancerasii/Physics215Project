import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filename = "t1_base_l10ts2000r5"


def getTc(filename):
    N = 10*10
    sdata = np.loadtxt("../data/"+filename+"spin.txt")

    Tvals = sdata[0,:]

    Mave = np.mean(sdata[2:,:],axis=0)
    Msqave = np.mean(sdata[2:,:]**2,axis=0)

    Xvals = np.divide(Msqave - Mave**2, Tvals*N)

    def lorentzian(T, Tc, A, B):
        return A/((T-Tc)**2 + B)
    

    xdata = np.linspace(1,5,100)

    plt.scatter(Tvals,Xvals)
    popt, pcov = curve_fit(lorentzian, Tvals, Xvals)
    # print("T =",popt[0])
    # plt.plot(xdata,lorentzian(xdata, *popt))
    plt.show()

    return popt[0]


modes = ["base","ngit","parallel","ngitparallel"]

tsvals = np.arange(1000,4000,1000)

for mode in modes:
    errors = []
    for ts in tsvals:
        if mode == "parallel" or mode == "ngitparallel":
            Tc = getTc('t1_'+mode+'_l10ts'+str(ts)+'r5c5')
        else:
            Tc = getTc('t1_'+mode+'_l10ts'+str(ts)+'r5')
        TcError = abs(Tc-2.269)/2.269
        print(mode,ts)
        print(TcError)
        errors.append(TcError)

    plt.plot(tsvals,errors,label=mode)

plt.show()
