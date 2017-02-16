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
ReList=[]
out=Output();
out.alpha, out.S, out.betaCr, out.Re=np.loadtxt('/home/nyadav/test2/new.txt',usecols=(0,1,2,3),unpack=True);
print(os.getcwd());
path=os.getcwd();

alpha=float(path.split('/')[-2]);
sval=float(path.split('/')[-1]);
#betaCr=np.loadtxt('/home/nyadav/freq/al-s-betaCr.txt');
ReCr=np.loadtxt('/home/nyadav/freq/al-s-ReCr.txt');
#aa=ipVar.find_nearest2D(betaCr[:,0],betaCr[:,1],betaCr[:,2],[alpha,sval]);
Re=ipVar.find_nearest2D(ReCr[:,0],ReCr[:,1],ReCr[:,2],[alpha,sval]);
#a=[aa[0]-0.3*aa[0],aa[0]+0.3*aa[0]];
ReList=[Re[0]-0.02*Re[0], Re[0]-0.05*Re[0]];
#print(a);print(ReList);

#for i in range(0,16):
#    ReList.append(55+25*i);
#for i in range(0,20):
#    ReList.append(60+i*10);
betaPath=glob("*/");
betas=[];
for i in betaPath:
    k=float(i.split('/')[0]);
    #if(k<2.0 and k > 1.21):
    betas.append(k);



#betas=a;
for i in betas:
    for j in ReList:
        betaPath=path+'/'+str(i);
        cmd=[];
        time.sleep(1)
        cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/manyObj3.py '+str(i)+' '+str(j));
        crdir=os.getcwd();
        ipVar.pbs(rse,path+str(i),module,os.getcwd(),cmd);
        subprocess.call("qsub pbs.sh",shell=True);
        os.chdir(path);
    
