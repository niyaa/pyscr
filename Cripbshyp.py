import os,sys;
import shutil;
import subprocess;
from glob import glob;
path=os.getcwd();
import numpy as np;
import time
sys.path.append('/home/nyadav/pyscr');
import ipVar;
rse='nodes=1:ppn=1';
#rse='nodes=newton-02:ppn=1';
module='module load openmpi/1.X.X-debian';
path=os.getcwd();
os.chdir(path);
betaList=[]
#betaList=[0.1,0.3,0.2,0.25 ,0.35,0.4,0.45,0.5,0.6]
#betaList=[0.85,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6];
#betaList=[0.05,0.25 ,0.35,0.6,0.8,0.15 ,0.3,0.4,0.5,0.7,0.1, 0.8, 0.9,1,1.1,1.2,1.3,1.4,1.5,1.6]
#betaList=[0.7,0.75,0.05]
for i in range(0,18):
    betaList.append(0.5+i*0.1);
#Betas=glob("*/");
#for ii in Betas:
#    betaList.append(float(ii.split('/')[0]));

path=os.getcwd();
print(betaList);
for i in betaList:
    betaPath=path+'/'+str(i);
    cmd=[];
    time.sleep(1)
    cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/manyObj2hyp.py '+str(i));
    crdir=os.getcwd();
    ipVar.pbs(rse,'ReC'+str(i),module,os.getcwd(),cmd);
    subprocess.call("qsub pbs.sh",shell=True);
    os.chdir(path);
    
