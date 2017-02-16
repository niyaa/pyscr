# -*- coding: utf-8 -*-
from case import Case

from scipy.optimize import curve_fit
from itertools import groupby
import numpy as np;

def extractData(icase, t1, up=1e-8, down=1e-18):
    #1 get smaller than some, and not letter than some
    t0 = icase.time[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>500) ]
    e0 = icase.energy[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>500) ]
    #need some sek back from here, but not less than 300
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>400) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>400) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>300) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>300) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>150) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>150) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>100) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>100) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>50) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>50) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>30) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>30) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>0) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>0) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1)]
        e0 = icase.energy[(icase.mod==1)]
    print icase.S, icase.Re, icase.mu, len(t0), icase.Name
    tmax = max(t0)
    tmin = min(t0)
    
    if tmax-tmin>50:
        tmin = tmax-50
    if tmax-tmin<25:
        tmin=tmax-25
    tt0=icase.time[(icase.mod==1)];
    if((tt0[-1]-tt0[-2])>1):tmin=tmax-50*(tt0[-1]-tt0[-2]);
#    
#    tmax=140
#    tmin=120
    
    t = icase.time[(icase.mod==1) & (icase.time>tmin) & (icase.time<tmax)]
    e = icase.energy[(icase.mod==1) & (icase.time>tmin) & (icase.time<tmax)]
         
    return (t,e)
    
def solv(icase, t, e):
    try:
        popt, pcov = curve_fit(func, t, e, p0=(1e-15, 1e-2))
        perr = np.sqrt(np.diag(pcov))[0]+np.sqrt(np.diag(pcov))[1]
        icase.sigma=0.5*popt[1] # I am traking energy!
        return popt, perr        
    except:
        print("mu" + str(icase.mu) + " a"+str(icase.alfa)+" S"+str(icase.S)+" Re"+str(icase.Re))
        print("Failed to Converge!")
        print(t)
        print(e)
        print(len(icase.time))
        print(len(icase.energy))
        return None, None
        
def calculate(caseList, up=1e-8, down=1e-18):
    print("Calculating Growth factors")
    failed = []
    for icase in caseList:                 
        icase.t,icase.e=extractData(icase, 1000, up, down)
        icase.popt, icase.perr = solv(icase, icase.t, icase.e)
        if icase.popt == None:
            failed.append(icase)
    makeplots.makePlots(failed)

def linearPt(file='EnergyFile.mdl',up=1e-8, down=1e-18):
    icase=Case();
    icase.time, icase.mod, icase.energy= np.loadtxt(file,comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
    t1=icase.time[-1];
    print(t1); 
    
    #1 get smaller than some, and not letter than some
    t0 = icase.time[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>500) ]
    e0 = icase.energy[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>500) ]
    #need some sek back from here, but not less than 300
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>400) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>400) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>300) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<up) & (icase.energy>down) & (icase.time<t1) & (icase.time>300) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>150) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>150) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>100) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>100) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>50) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>50) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>30) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>30) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>0) ]
        e0 = icase.energy[(icase.mod==1) & (icase.energy<10*up) & (icase.energy>0.1*down) & (icase.time<t1) & (icase.time>0) ]
    if len(t0) < 3:
        t0 = icase.time[(icase.mod==1)]
        e0 = icase.energy[(icase.mod==1)]
    print icase.S, icase.Re, icase.mu, len(t0), icase.Name
    tmax = max(t0)
    tmin = min(t0)
    
    if tmax-tmin>50:
        tmin = tmax-50
    if tmax-tmin<25:
        tmin=tmax-25
    tt0=icase.time[(icase.mod==1)];
    if((tt0[-1]-tt0[-2])>1):tmin=tmax-50*(tt0[-1]-tt0[-2]);
#    
#    tmax=140
#    tmin=120
    
    t = icase.time[(icase.mod==1) & (icase.time>tmin) & (icase.time<tmax)]
    e = icase.energy[(icase.mod==1) & (icase.time>tmin) & (icase.time<tmax)]
    print(t);
    print(e);
    return (t,e)
 
