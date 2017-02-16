import ipVar, funcs, os;
from output import *;
from decimal import Decimal;
import numpy as np;
from case import *;
from glob import glob;
import numpy as np;
import extractdata;

out=Output();
cwd=os.getcwd();

for root, dir, files in os.walk("./"):
    for file in files:
        if(file.endswith(".mdl")):
            os.chdir(root);
            case=Case();
            path=os.getcwd();
            inE=os.path.join(os.getcwd(),file);
            out.S.append(Decimal(path.split('/')[-1]));
            out.beta.append(Decimal(path.split('/')[-2]));
            out.alpha.append(Decimal(path.split('/')[-3]));
            out.Re.append(Decimal(file.split('-')[-2]));
            [popt, perr]=ipVar.poptEnRa(inE,1e-8,1e-21);
            if(len(popt)>0):
                out.sigma.append(popt[1]/2.0);
            else:
                out.sigma.append(0);
            his=file.split('-')[:-1];
            his="-".join(his);
            his=his+'-.his';
            if(os.path.exists(os.path.join(os.getcwd(),his))):
                inE=os.path.join(os.getcwd(),his);
                [a,b,c]=ipVar.nekFre3(inE,1,0,-1,1);
                out.sigmaR.append(c);
                print(inE);
            
            else:
                out.sigmaR.append(0);
                print("this file not produce Frequecny \n");
                print(his);

            os.chdir(cwd);
            
n=len(out.Re);
x=np.zeros((n,6),dtype=np.float);
x[:,0]=out.alpha[:];
x[:,1]=out.beta[:];
x[:,2]=out.S[:];
x[:,3]=out.Re[:];
x[:,4]=out.sigma[:];
x[:,5]=out.sigmaR[:];
np.savetxt('out.txt',x,delimiter=" ");



