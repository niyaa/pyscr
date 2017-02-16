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
Re=155
if(Re ==0):
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    Re=int(root[1][1][5].text.split('=')[-1]);
    a=[-1,-1];

    os.chdir(str(Re));
    FilePath=os.getcwd()+'/'+'bd.xml';
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    Re=int(root[1][1][5].text.split('=')[-1]);
    os.chdir(pathA);
ReMult=[15,10,10,10];
beta=0.4;
for f in ReMult:   
    Re=int(Re+f);
    if not os.path.exists(str(Re)):
        os.makedirs(str(Re));
    os.chdir(str(Re));
    pathB=os.getcwd();
    time=5000;
    para=[0.005,time,'FinalTime/(25*TimeStep)',Re,64,beta,'','','','1'];
    funcs.CopyFile(pathA,os.getcwd(),FileList);
    funcs.simPara(os.getcwd(),'bd.xml',para);
    #subprocess.call('mpirun -np 32 /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
    subprocess.call('mpirun -np 16 /home/nyadav/bin/mpiInc --npz 16 geom.xml bd.xml > log.txt',shell=True);    
    os.chdir(pathA);





