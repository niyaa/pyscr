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
Re=100;
if(Re==0):
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    Re=int(root[1][1][5].text.split('=')[-1]);

betaList=[0.4];
for beta in betaList:
    a=[-1,-1];
    #if not os.path.exists(str(Re)):
    #    os.makedirs(str(Re));
    #os.chdir(str(Re));
    if not os.path.exists(str(beta)):
        os.makedirs(str(beta));
    os.chdir(str(beta));
    pathB=os.getcwd();
    time=100; time2=1000;
    NZ=8;
    np=NZ/2;
    para=[0.005,time,'FinalTime/TimeStep','',NZ,beta,'','','','1'];
    funcs.CopyFile(pathA,os.getcwd(),FileList);
    funcs.simPara(os.getcwd(),'bd.xml',para);
    while(a[1]<0):
        funcs.ReCh(os.getcwd(),'bd.xml',Re);
        subprocess.call('mpirun -np '+str(np)+' /home/nyadav/bin/mpiInc --npz '+str(np)+' geom.xml bd.xml',shell=True);    
        #subprocess.call('mpirun -np '+str(np)+' /home/nyadav/.sg/IncNavierStokesSolver --npz '+str(np)+' geom.xml bd.xml',shell=True);    
        if(Re>1000):Re=int(Re+0.01*Re);
        if(Re<1000 and Re>100):Re=int(Re+0.02*Re);
        if(Re <=100):Re=int(Re+0.04*Re);
        [a,b]=ipVar.poptEnRa('EnergyFile.mdl');
    if not os.path.exists(str(2)):
        os.makedirs(str(2));
    os.chdir(str(2));
    funcs.CopyFile(pathB,os.getcwd(),FileList[:-1]);
    para=[0.005,time2,'FinalTime/(5*TimeStep)','',NZ,beta,'','','','1'];
    funcs.simPara(os.getcwd(),'bd.xml',para);
    funcs.ICFile(pathB,os.getcwd(),'geom.fld','bd.xml');
    subprocess.call('mpirun -np '+str(np)+' /home/nyadav/bin/mpiInc --npz '+str(np)+' geom.xml bd.xml',shell=True);    
    subprocess.call('rm -r IC.bse',shell=True);
    subprocess.call('mv geom.fld IC.bse',shell=True);
    funcs.addEnergyFile(os.getcwd(),'energyfile.mdl');
    bc=funcs.MaxChk(os.getcwd());
    ac=funcs.MaxChk(pathB);
    funcs.moveChk(os.getcwd(),pathB,ac,bc);

    subprocess.call('mpirun -np '+str(np)+' /home/nyadav/bin/mpiInc --npz '+str(np)+' geom.xml bd.xml',shell=True);    
    subprocess.call('rm -r IC.bse',shell=True);
    subprocess.call('mv geom.fld IC.bse',shell=True);
    funcs.addEnergyFile(os.getcwd(),'energyfile.mdl');
    bc=funcs.MaxChk(os.getcwd());
    ac=funcs.MaxChk(pathB);
    funcs.moveChk(os.getcwd(),pathB,ac,bc);


    while ( ipVar.CheckSaturation(1)):
        para=[0.005,time2,'FinalTime/(5*TimeStep)','',NZ,beta,'','','','1'];
        funcs.simPara(os.getcwd(),'bd.xml',para);
        subprocess.call('mpirun -np '+str(np)+' /home/nyadav/bin/mpiInc --npz '+str(np)+' geom.xml bd.xml',shell=True);    
        #subprocess.call('mpirun -np '+str(np)+' /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
        subprocess.call('rm -r IC.bse',shell=True);
        subprocess.call('mv geom.fld IC.bse',shell=True);
        funcs.addEnergyFile(os.getcwd(),'energyfile.mdl');
        bc=funcs.MaxChk(os.getcwd());
        ac=funcs.MaxChk(pathB);
        funcs.moveChk(os.getcwd(),pathB,ac,bc);
    os.chdir(pathA);





