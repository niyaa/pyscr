import sys, os;
import numpy as np;
sys.path.append('/home/nyadav/pyscr/')
from output import *;
import ipVar;
out=Output();


cwd=os.getcwd();

for root, dir, files in os.walk("./"):
    for file in files:
        if(file.endswith("-.mdl")):
            inE=os.path.join(root,file);
            print(inE)
            [a,b]=ipVar.poptEnRa(inE);
            out.sigma.append(a[1]/2.0);
            print(a[1]/2.0);
            if os.path.exists(root+'/TimeValues.his'):
                hiE=os.path.join(root,'TimeValues.his');
                print(hiE);
            else:
                print('There is no file \n');
                print(root);
            try:
                [a,b,c]=ipVar.nekFre3(hiE,1,0,-1,3);
                F=1;
            except:
                F=0;
                print('Cound not defind for above\n');
            if(F):out.sigmaR.append(c);
            if not (F):out.sigmaR.append(0);
            out.Re.append(float(root.split('/')[-1]));
            out.beta.append(float(root.split('/')[-2]));
            out.alpha.append(float(1));
                

n=len(out.sigma);
x=np.zeros((n,5),dtype=np.float);
x[:,0]=out.alpha[:];
x[:,1]=out.beta[:];
x[:,2]=out.Re[:];
x[:,3]=out.sigma[:];
x[:,4]=out.sigmaR[:];
np.savetxt('out.txt',x)
#np.savetxt('out.csv',x,delimiter="\t");

