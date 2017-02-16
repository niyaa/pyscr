from decimal import Decimal;
import sys, os;
sys.path.append('/home/nyadav/pyscr/');
import ipVar;
import numpy as np;
from output import *;
    
out=Output();
for root, dir, files in os.walk("./"):
    for file in files:
        if (file.endswith(".mdl")and not file == "EnergyFile.mdl"):
            print(file);
            inE=os.path.join(root, file)
            out.Re.append(Decimal(root.split('/')[-1]));
            out.beta.append(Decimal(root.split('/')[-2]));
            out.alpha.append(Decimal(root.split('/')[-3]));
            [popt, perr]=ipVar.popt(inE);
            out.sigma.append(popt[1]/2.0); 
            
n=len(out.Re);
x=np.zeros((n,4),dtype=np.float)
x[:,0]=out.alpha[:];
x[:,1]=out.beta[:];
x[:,2]=out.Re[:];
x[:,3]=out.sigma[:];
np.savetxt('out.csv',x,delimiter=" ");
