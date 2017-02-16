import os,sys;
from output import *;
import shutil;
import subprocess;
path=os.getcwd();
import numpy as np;
from glob import glob;
import time
sys.path.append('/home/nyadav/pyscr');
import ipVar;
rse='nodes=1:ppn=1';
#rse='nodes=newton-02:ppn=1';
module='module load gmsh/2.9.2';
cwd=os.getcwd();
ReMul=[0.05];

out=Output();
out.alpha, out.beta, out.S, out.ReC=np.loadtxt('/home/nyadav/test/ReCr.txt',usecols=(0,1,2,3),unpack=True);
alpha=float(cwd.split('/')[-2]);
sval=float(cwd.split('/')[-1]);
Re=out.ReC[(out.alpha==alpha)&(out.S==sval)];
beta=out.beta[(out.alpha==alpha)&(out.S==sval)];
for j in ReMul:
    betaList=[];
    ReMin=min(Re);
    for i in range(0,len(Re)):
        if(ReMin+ReMin*j > Re[i]):
            betaList.append(beta[i]);
    print(betaList);
    reExe=ReMin+ReMin*j;
    print('THE REYNOLDS NUMBER \n');
    print(reExe);
    path=os.getcwd();
    for i in betaList:
        betaPath=path+'/'+str(i);
        cmd=[];
        time.sleep(3)
        cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/manyObj3.py '+str(i)+' '+str(reExe));
        crdir=os.getcwd();
        ipVar.pbs(rse,path+str(i),module,os.getcwd(),cmd);
        subprocess.call("qsub pbs.sh",shell=True);
        os.chdir(path);
    
