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
ReList=[61,65,70,80]
betas=glob("*/");
betas=[np.float(i.split("/")[0]) for i in betas];
betas=[i for i in betas if i<0.5 and i>=0.05];
print(betas);
print(os.getcwd());
path=os.getcwd();
for i in betas:
    for j in ReList:
        betaPath=path+'/'+str(i);
        cmd=[];
        time.sleep(3)
        cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/manyObj3.py '+str(i)+' '+str(j));
        crdir=os.getcwd();
        ipVar.pbs(rse,path+str(i),module,os.getcwd(),cmd);
        subprocess.call("qsub pbs.sh",shell=True);
        os.chdir(path);
    
