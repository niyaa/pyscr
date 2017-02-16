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


cmd=[];
time.sleep(1)
cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/betaCrObj.py');
crdir=os.getcwd();
ipVar.pbs(rse,"-".join(crdir.split('/')[-2:])+"-"+'smth',module,os.getcwd(),cmd);
subprocess.call("qsub pbs.sh",shell=True);
os.chdir(path);

