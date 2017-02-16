import os,sys;
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
path=os.getcwd();
os.chdir(path);
betaList=[]


#N=int(raw_input('Enter N \n'));
#st=str(raw_input('Enter the starting point \n'));
#st=float(st);
#dbeta=str(raw_input("STEP SIZE \n",));
#dbeta=float(dbeta);
N=13; st=0.6; dbeta=0.05;mod=0;
for i in range(0,N):
    betaList.append(st+dbeta*i)
Betas=glob("*/");
#for ii in Betas:
#    betaList.append(float(ii.split('/')[0]));
#print('For interactive Enter 1 and for qsub enter 0 \n');
#mod=int(raw_input());

path=os.getcwd();
print(betaList);
for i in betaList:
    betaPath=path+'/'+str(i);
    cmd=[];
    time.sleep(2)
    cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/manyObj2.py '+str(i));
    crdir=os.getcwd();
    ipVar.pbs(rse,"-".join(crdir.split('/')[-2:])+"-"+str(i),module,os.getcwd(),cmd);
    if(mod==1):
        cmd[0]=cmd[0]+' &';
        subprocess.call(cmd[0],shell=True);
    if(mod==0):
        subprocess.call("qsub pbs.sh",shell=True);
    os.chdir(path);
    
