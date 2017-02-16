# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 17:08:18 2016

@author: niya
"""
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
from glob import glob;
import sys, os, shutil;
import os, extractdata;
import numpy as np;
from case import *;
from decimal import Decimal; 
import pickle; 
import subprocess;
from scipy.interpolate import UnivariateSpline;
import numpy as np;
import ipVar;
import numpy as np;
from case import *;
import extractdata;
from scipy.optimize import curve_fit;

def CheckEnergyUD(path,filename,up,down):
    filePath=path+'/'+filename;
    energy = np.loadtxt(filePath,skiprows=1);
    a=energy[-1,-1];
    if((a > up) or ( a < down)):   return 0;
    else: return 1;

def CheckEnergyUp(path,filename,up):
    filePath=path+'/'+filename;
    energy = np.loadtxt(filePath,skiprows=1);
    a=energy[-1,-1];
    if(a > up) :   return 0;
    else: return 1;

def ConPara(fileName):
    filePath=path+'/'+filename;
    tree=ET.parse(filePath);
    root=tree.getroot();

	#Reynolds number
    a=root[1][1][5].text;
    a=a.split('=');
    a=a[1];
    RE=float(a);

	#Final Time
    a=root[1][1][1].text;
    a=a.split('=');
    a=a[1];
    FT=float(a);

	#CheckSteps
    a=root[1][1][3].text;
    a=a.split('=');
    a=a[1];
    IO=float(a);

	#TimeStep]
    a=root[1][1][0].text;
    a=a.split('=');
    a=a[1];
    TS=float(a);
    ChkN=FT/(TS*IO);
    ChkN=int(ChkN);
    return FT, TS, IO, RE, ChkN;

def moveChk(CurrentPath,NewPath,i,j):
    for k in range (1,j+1):
        d='geom_'+str(k)+'.chk';        
        b=i+k;c='geom_'+str(b)+'.chk';shutil.copy(CurrentPath+'/'+d,NewPath+'/'+c);

def func(x, a, b):
        return a*np.exp(b*x);

def MaxChk(path):
    pwd=os.getcwd();
    os.chdir(path);
    j=0;
    for file in glob("*.chk"):
        f=file.split('.')[0].split('_')[1];
        f=int(f);
        if(f>j):j=f;
    os.chdir(pwd);
    return j;

def incSolver(exe,filelist):
    args=exe+' '+filelist[0]+' '+filelist[1];
    print('Working in this directory \n');
    print(os.getcwd());
    subprocess.call(args,shell=True);

def FaF(exe,filelist,a,b):
    args=exe+' '+a+' '+' '+b;
    for i in filelist:
		args=args+' '+i;
    print('Working in this directory \n');
    print(os.getcwd());
    subprocess.call(args,shell=True);

def ICFile(path1,path2,chkStr,CondFile):
    if not (path1 == path2):
    	shutil.copy((path1+'/'+chkStr),path2);
    os.rename(chkStr,'IC.bse');
    tree=ET.parse(path2+'/'+CondFile,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[1][6][0].set('FILE','IC.bse');
    tree.write(CondFile);

def CopyFile(pathA,pathB,FileList):
    for i in FileList:
        shutil.copy(pathA+'/'+i,pathB);

def pbs(rse,name,module,wd,exe):
    f=open('pbs.sh','w');
    d=[];
    d.append('#!/bin/bash\n');
    d.append('#PBS -l '+rse+',walltime=03:00:00:00\n');
    d.append('#PBS -N '+name+'\n');
    d.append('#PBS -M nyadav@meil.pw.edu.pl\n');
    d.append('#PBS -m abe\n');
    d.append(module+'\n');
    d.append('cd '+wd+'\n');
    for i in exe:
        d.append(i+'\n');
    d.append('exit 0\n')
    f.writelines(d);
    f.close();


def editGeo(pathS,pathD,a,S):
    path=pathS+'/'+'divConv2D.scr';      
    f=open(path,'r');
    d=f.readlines();
    d[3]='S='+str(S)+';\n';
    d[4]='a='+str(a)+';\n';
    f.close();
    path=pathD+'/'+'divConv2D.scr';
    f=open(path,'w');
    f.writelines(d);
    f.close();

def ReCh(path,fileName,R):
    FilePath=path+'/'+fileName
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    Re='Re='+str(R);
    root[1][1][5].text=Re;
    tree.write(FilePath);

def lzCh(path,fileName,Beta):
    FilePath=path+'/'+fileName
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    lz='LZ='+str((np.pi*2/(Beta)));
    root[1][1][8].text=lz
    tree.write(FilePath)

def FTCh(path,fileName,FT):
    FilePath=path+'/'+fileName
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    FT='FinalTime ='+str(FT);
    root[1][1][1].text=FT
    tree.write(FilePath)


def addEnergyFile(pathA,fileName):
    pwd=os.getcwd();
    os.chdir(pathA);  
    subprocess.call(['sed "1,3d" EnergyFile.mdl > abc.txt'],shell=True);
    subprocess.call('cat ../EnergyFile.mdl abc.txt > ../abc.txt',shell=True);
    subprocess.call('mv ../abc.txt ../EnergyFile.mdl', shell=True);
    os.chdir(pwd);

def nsvalues(path1):
    cwd=path1;
    path=glob('*/');
    x=[];y=[];
    for x in path:
        f=i.split('/')[0];
        newPath=cwd+'/'+f;
        print('the new path \n \n \n \n \n');
        print(newPath);
        print('\n \n \n \n \n \n');
        [a,b,c]=ipVar.sigma(newPath);
        x.append(float(f));
        y.append(c);
    return x, y;

def nsplot(Re,beta):
    x=Re;y=beta;
    YX=zip(y,x);
    YX.sort();
    
    xx=[];yy=[];
    for i in range(0,len(YX)):
        yy.append(YX[i][0]);
        xx.append(YX[i][1]);
    fig, ax=plt.subplots();
    ax.plot(xx,yy);
    ax.grid(True);
    plt.ylabel('Beta');
    plt.xlabel('Reynolds Number');
    plt.show()
     
    os.chdir(pwd);
  
def popt(file,up=1e-8,down=1e-18):
    case=Case();
    case.time,case.mod,case.energy = np.loadtxt(file, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True)
    if(case.time[0] > 100):N1=case.time[0]; case.time[0::2]=case.time[0::2]-N1;case.time[1::2]=case.time[1::2]-N1;
    case.t,case.e=extractdata.extractData(case,case.time[-1],up, down);
    print(case.t);
    popt, pcov = curve_fit(func, case.t, case.e, p0=(1e-15, 1e-2))
    perr = np.sqrt(np.diag(pcov))[0]+np.sqrt(np.diag(pcov))[1] ;
    return popt, perr;   

def calcReC(x,y):
    x.sort();y.sort();
    func=UnivariateSpline(x,y,k=3,s=0);
    for i in range(0,len(x)-1):
	temp=y[i+1];
	if((y[i] > 0 and temp <0) or (y[i]<0 and temp >0)):
	    a=x[i]; b=x[i+1];
    tol=1e-6;
    while(abs(a-b)>tol):
        c=(a+b)/2.0;
        if(samesign(func,a,c)):b=c;
        else: a=c
    c=(a+b)/2.0;
    return c;

def samesign(func,a,b):
    c=func(a)*func(b);
    if(c<0):return 1;
    else: return 0;

def bdexe(path,exe,fileList,energyVal,itrVal):
    incSolver(exe,fileList);
    itr=0;
    while((CheckEnergyUp(path,'EnergyFile.mdl',energyVal)) and itr < itrVal):
        path2=path+'/2';
        f=MaxChk(path);        
        icFile='geom_'+str(f)+'.chk';
        print(icFile)
        if not os.path.exists(path2):
            os.makedirs(path2);
        os.chdir(path2);
        CopyFile(path,path2,fileList);
        ICFile(path,path2,icFile,'bd.xml');                                            
        incSolver(exe,fileList);
        addEnergyFile(path2,'EnergyFile.mdl');
        itr=itr+1
        bc=MaxChk(path2);  
        ac=MaxChk(path);
        moveChk(path2,path,ac,bc)
        itr=itr+1;
        os.chdir(path);   
        

def first(path,exe,fileList,energyVal,FT,Re,FT2,incre):
    ReCh(path,fileList[1],Re);
    FTCh(path,fileList[1],FT);
    incSolver(exe,fileList);
    fileName='EnergyFile.mdl';
    energy=np.loadtxt(fileName,skiprows=1);
    a=energy[-1,-1];

    while(a< energyVal):
        Re=Re+incre;
        ReCh(path,fileList[1],Re);
        incSolver(exe,fileList);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];
    FTCh(path,fileList[1],FT2);
        

def firstExt(path,exe,fileList,energyVal,FT,Re,FT2,incre):
    ReCh(path,fileList[1],Re);
    FTCh(path,fileList[1],FT);
    incSolver(exe,fileList);
    fileName='EnergyFile.mdl';
    energy=np.loadtxt(fileName,skiprows=1);
    a=energy[-1,-1];

    while(a< energyVal):
        Re=Re+incre;
        ReCh(path,fileList[1],Re);
        incSolver(exe,fileList);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];
    FTCh(path,fileList[1],FT2);
    path2=os.getcwd()+'/2';
    if not os.path.exists(path2):
        os.makedirs(path2);
    os.chdir(path2);
    f=MaxChk(path);
    icFile='geom_'+str(f)+'.chk';
    CopyFile(path,path2,fileList);
    ICFile(path,path2,icFile,'bd.xml'); 
    incSolver(exe,fileList);
    addEnergyFile(path2,'EnergyFile.mdl');
    bc=MaxChk(path2);
    ac=MaxChk(path);
    moveChk(path2,path,ac,bc);                                                      os.chdir(path);
    addEnergyFile(path2,'EnergyFile.mdl');
    os.chdir(path);


def NekMesh(exe,rootPath,simPath,alpha,Sval):
    editGeo(rootPath,simPath,alpha,Sval);
    os.chdir(simPath);
    subprocess.call("/tools/gmsh/2.9.2/bin/gmsh -2 -order 9 divConv2D.scr" ,shell=True);
    args=exe+'/MeshConvert'+' '+'divConv2D.msh'+' '+'geom.xml';
    subprocess.call(args,shell=True);

    
def PrepareBD(exe,simPath):
    j=MaxChk(simPath+'/b');
    baseFile=simPath+'/b/'+'geom_'+str(j)+'.chk';
    shutil.copy(baseFile,simPath+'/bd');
    shutil.copy(simPath+'/d/geom_0.chk',simPath+'/bd');
    args='mv'+' '+baseFile+' '+'geom3D.bse';    
    subprocess.call(args,shell=True);
    args='mv'+' '+'geom_0.chk'+' '+'geom3D-dist.bse';
    subprocess.call(args,shell=True);
    args=exe+' '+str(1)+' '+str(1e-9)+' '+'geom3D.bse'+' '+'geom3D-dist.bse'+' '+'geomBplusD.fld';
    subprocess.call(args,shell=True);
    print('Finished Copying files from base and dist\n');
    pirnt('and Adding them together for Initial Condition\n');
    
