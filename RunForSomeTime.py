#I/p Time for second run
#It will delete the 2 diretory after execution

import os, sys, subprocess;
sys.path.append('/home/nyadav/pyscr/');
import ipVar, funcs;
from case import *;
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
from glob import glob;
pathA=os.getcwd();
i=funcs.MaxChk(os.getcwd());
icFile='geom_'+str(i)+'.chk';
arg='cp -r '+icFile+' IC.bse';
subprocess.call(arg, shell=True);
FileList=['geom.xml','bd.xml'];
time=400;
Nchk=int(time/200);

if not os.path.exists(str(2)):
    os.makedirs(str(2));
os.chdir(str(2));
funcs.CopyFile(pathA,os.getcwd(),FileList);
subprocess.call('cp -r ../IC.bse .',shell=True);
para=[0.005,time,'FinalTime/('+str(Nchk)+'*TimeStep)','',64,'','','','','1'];
path2=os.getcwd();
funcs.simPara(os.getcwd(),'bd.xml',para);
icFile='IC.bse';
funcs.ICFile(pathA,path2,icFile,'bd.xml');
subprocess.call('mpirun -np 16 /home/nyadav/.sg/IncNavierStokesSolver --npz 16 geom.xml bd.xml',shell=True);
funcs.addEnergyFile(path2,'EnergyFile.mdl');
bc=funcs.MaxChk(path2);
ac=funcs.MaxChk(pathA);
funcs.moveChk(path2,pathA,ac,bc);
os.chdir(pathA);
subprocess.call("rm -r 2",shell=True);
