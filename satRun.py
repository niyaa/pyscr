import os, sys, subprocess;
sys.path.append('/home/nyadav/pyscr/');
import ipVar, funcs;
from case import *;
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
from glob import glob;
pathA=os.getcwd();
FileList=['geom.xml','bd.xml','geomBplusD.fld'];
FilePath=pathA+'/'+'bd.xml';
tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
root=tree.getroot();
Re=int(root[1][1][5].text.split('=')[-1]);
a=[-1,-1];

if not os.path.exists(str(Re)):
    os.makedirs(str(Re));
os.chdir(str(Re));
pathB=os.getcwd();
time=500
NZ=8;
np=int(NZ/2);
para=[0.005,time,'FinalTime/TimeStep','',NZ,0.4,'','','','1'];
funcs.CopyFile(pathA,os.getcwd(),FileList);
funcs.simPara(os.getcwd(),'bd.xml',para);
while(a[1]<0):
    a=[-1,-1];
    subprocess.call('mpirun -np '+np+' /home/nyadav/bin/mpiInc --npz '+np+' geom.xml bd.xml',shell=True);    
    #subprocess.call('mpirun -np 32 /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
    if(Re>1000):Re=int(Re+0.01*Re);
    if(Re<1000 and Re>100):Re=int(Re+0.02*Re);
    if(Re <100):Re=int(Re+0.04*Re);
    funcs.ReCh(os.getcwd(),'bd.xml',Re);
    [a,b]=ipVar.poptEnRa('EnergyFile.mdl');

time=50;
para=[0.005,time,'FinalTime/TimeStep','',NZ,0.4,'','','','1'];

funcs.simPara(os.getcwd(),'bd.xml',para);
if not os.path.exists(str(2)):
    os.makedirs(str(2));
os.chdir(str(2));
funcs.CopyFile(pathB,os.getcwd(),FileList);
funcs.ICFile(pathB,os.getcwd(),'geom.fld','bd.xml');
#subprocess.call('mpirun -np 32 /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
subprocess.call('mpirun -np '+np+' /home/nyadav/bin/mpiInc --npz '+np+' geom.xml bd.xml',shell=True);    
subprocess.call('rm -r IC.bse',shell=True);
subprocess.call('mv geom.fld IC.bse',shell=True);
funcs.addEnergyFile(os.getcwd(),'energyfile.mdl');
bc=funcs.MaxChk(os.getcwd());
ac=funcs.MaxChk(pathB);
funcs.moveChk(os.getcwd(),pathB,ac,bc);
time=50
while(not ipVar.CheckEnergySat('EnergyFile.mdl')):
    para=[0.005,time,'FinalTime/TimeStep','',NZ,0.4,'','','','1'];
    funcs.simPara(os.getcwd(),'bd.xml',para);
    funcs.ICFile(pathB,os.getcwd(),'geom.fld','bd.xml');
    #subprocess.call('mpirun -np 32 /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
    subprocess.call('mpirun -np 32 /home/nyadav/bin/mpiInc --npz '+np+' geom.xml bd.xml',shell=True);    
    subprocess.call('rm -r IC.bse',shell=True);
    subprocess.call('mv geom.fld IC.bse',shell=True);
    funcs.addEnergyFile(os.getcwd(),'energyfile.mdl');
    bc=funcs.MaxChk(os.getcwd());
    ac=funcs.MaxChk(pathB);
    funcs.moveChk(os.getcwd(),pathB,ac,bc);





