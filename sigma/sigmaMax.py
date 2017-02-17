from case import *
import numpy as np
from scipy import interpolate, optimize
from scipy.interpolate import griddata
from decimal import Decimal
import ipVar, funcs, os;
from output import *;
import numpy as np;
from case import *;
from glob import glob;
import numpy as np;
import extractdata;
from output import *;
import subprocess;
def betaCr(path):
    os.chdir(path);
    out=Output();
    subprocess.call('ipython2 ~/pyscr/sigmaR2.py',shell=True);
    out.alpha, out.S, out.beta, out.Re,out.sigma, out.sigmaR=np.loadtxt('out.txt',usecols=(0,1,2,3,4,5),unpack=True);
    beta=set(out.beta);
    Re=set(out.Re);
    Re=list(Re);Re.sort();
    betacr=[];
    sigmaMax=[];
    rlist=[];
    for k in Re:
        y=out.sigma[(out.sigma>0)&(out.Re==k)];
        x=out.beta[(out.sigma>0)&(out.Re==k)];
        if(len(x)>3):
            if len(x)>3:
                f2=interpolate.interp1d(x, -y, kind='cubic')
            elif len(x)==3:
                f2=interpolate.interp1d(x, -y, kind='quadratic')
            else:
                f2=interpolate.interp1d(x, -y, kind='slinear')
            try:
                initmu=x[y==max(y)]
                mumax=optimize.fmin(f2, initmu, maxiter=10000, disp=False)
                sigax=f2(mumax);
                betacr.append(mumax[0]);
                sigmaMax.append(sigax[0]);
                rlist.append(k);
                print(mumax[0])
                print(sigax[0])
            except:
        #                print ("No Solution for: ", alist[0].S, blist[0].Re)
                continue
    subprocess.call('rm out.txt',shell=True);
    return rlist[0], betacr[0];
