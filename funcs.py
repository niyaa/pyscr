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
from scipy.interpolate import InterpolatedUnivariateSpline;
import time;


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

def simPara(path,fileName,paraList):
    if not paraList[0]=='':
        DtCh(path,fileName, paraList[0]); 
    if not paraList[1]=='':  
        FTCh(path,fileName, paraList[1]);
    if not paraList[2]=='':
        ChkCh(path,fileName, paraList[2]);
    if not paraList[3]=='':
        ReCh(path, fileName, paraList[3]);   
    if not paraList[4]=='':
        HmCh(path,fileName, paraList[4]);
    if not paraList[5]=='':
        LzCh(path,fileName, paraList[5]);
    if not paraList[6]=='':
        EnCh(path,fileName, paraList[6]);
    if not paraList[7]=='':
        HiFCh(path,fileName, paraList[7]);
    if not paraList[8]=='':
        HiCh(path,fileName, paraList[8]);
    if not paraList[9]=='':
        EnFCh(path,fileName,paraList[9]);
        


def moveChk(CurrentPath,NewPath,i,j):
    for k in range (1,j+1):
        d='geom_'+str(k)+'.chk';        
        b=i+k;c='geom_'+str(b)+'.chk';
        arg='mv '+CurrentPath+'/'+d+' '+NewPath+'/'+c;
        subprocess.call(arg,shell=True);
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

def chkPerUnitTime(fileName,path=os.getcwd(),efile='EnergyFile.mdl'):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    ft=float(root[1][1][1].text.split('=')[-1]);
    ts=float(root[1][1][0].text.split('=')[-1]);
    chkOut=float(root[1][1][3].text.split('=')[-1]);
    
    case=Case();
    # Name of the energy file ot be changed for other names 
    case.time,case.mod,case.energy = np.loadtxt(efile, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
    tn=case.time[-1];
    chkMax=tn/(ts*chkOut); 
    [t,e]=extractdata.linearPt(efile);
    
    aa=np.ceil(t/(chkOut*ts));
    j=0;
    for i in aa:
        if(i.is_integer()):break
        j=j+1;
    energy=e[j];

    return 1/(ts*chkOut),chkMax,np.median(aa), energy;

def paramVal(fileName,path=os.getcwd()):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    ft=float(root[1][1][1].text.split('=')[-1]);
    ts=float(root[1][1][0].text.split('=')[-1]);
    chkOut=float(root[1][1][3].text.split('=')[-1]);

    Re=float(root[1][1][5].text.split('=')[-1]);
    LZ=float(root[1][1][8].text.split('=')[-1]);

    para=[ts,ft,chkOut,Re,LZ];
    
    return para;


    

def incSolver(exe,filelist):
    args=exe+' '+filelist[0]+' '+filelist[1]+' >log.txt';
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
        if not (os.path.isdir(path1+'/'+chkStr)):
    	    shutil.copy((path1+'/'+chkStr),path2);
        if (os.path.isdir(path1+'/'+chkStr)):
            args='cp -r '+path1+'/'+chkStr+' '+path2;
            subprocess.call(args,shell=True);
    args='mv '+chkStr+' IC.bse';
    subprocess.call(args,shell=True); 
    tree=ET.parse(path2+'/'+CondFile,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[1][6][0].set('FILE','IC.bse');
    tree.write(CondFile);

def CopyFile(pathA,pathB,FileList):
    for i in FileList:
        shutil.copy(pathA+'/'+i,pathB);

def CopyFileVal(pathA,pathB,FileList,Re,beta):
    for i in FileList:
        shutil.copy(pathA+'/'+i,pathB);
    if not (Re=='0'):ReCh(pathB,FileList[1],Re);
    if not (beta=='0'):LzCh(pathB,FileList[1],beta);

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


def editGeo(pathS,pathD,a,S,nx,ny):
    path=pathS+'/'+'divConv2D.scr';      
    f=open(path,'r');
    d=f.readlines();
    d[1]='nx='+str(nx)+';\n';
    d[2]='ny='+str(ny)+';\n';
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

def EnCh(path,fileName,name):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[3][0][0].text=name;
    tree.write(FilePath);

def EnFCh(path,fileName,name):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[3][0][1].text=name+'/TimeStep';
    tree.write(FilePath);

def HiCh(path,fileName,name):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[3][1][3].text='\n'+name+'\n';
    tree.write(FilePath);


def HiFCh(path,fileName,name):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[3][1][1].text=name;
    tree.write(FilePath);


def HiFileCh(path,fileName,name):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[3][1][0].text=name;
    tree.write(FilePath);

def LzCh(path,fileName,Beta):
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

def DtCh(path,fileName,dt):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    Dt='TimeStep ='+str(dt);
    root[1][1][0].text=Dt
    tree.write(FilePath)

def ChkCh(path,fileName,chkN):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    ChkN='IO_CheckSteps ='+str(chkN);
    root[1][1][3].text=ChkN;
    tree.write(FilePath);

def HmCh(path,fileName,hmz):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    Hmz='HomModesZ ='+str(hmz);
    root[1][1][7].text=Hmz;
    tree.write(FilePath);

def ExCh(path,fileName,ex):
    FilePath=path+'/'+fileName;
    tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[0][0].attrib['NUMMODES']=str(ex);
    tree.write(FilePath);


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
        

def firstExt(path,exe,fileList,energyVal,FT,Re,FT2,incre,energyVal2):
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
    while(a< energyVal2):
        FTCh(path,fileList[1],FT2);
        path2=os.getcwd()+'/2';
        if not os.path.exists(path2):
            os.makedirs(path2);
        os.chdir(path2);
        f=MaxChk(path);
        icFile='geom_'+str(f)+'.chk';
        CopyFile(path,path2,fileList);
        ICFile(path,path2,icFile,'bd.xml');
        subprocess.call('rm *.chk',shell=True);
        subprocess.call('rm ../*.chk',shell=True);
        incSolver(exe,fileList);
        addEnergyFile(path2,'EnergyFile.mdl');
        bc=MaxChk(path2);
        ac=MaxChk(path);
        moveChk(path2,path,ac,bc);                 
        os.chdir(path);
        addEnergyFile(path2,'EnergyFile.mdl');
        os.chdir(path);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];

# This function evalutes the growth rate for finding the unstable Re number
# 

def firstExt3(path,exe,fileList,energyVal,FT,Re,FT2,incre,energyVal2):
    ReCh(path,fileList[1],Re);
    FTCh(path,fileList[1],FT);
    incSolver(exe,fileList);
    fileName='EnergyFile.mdl';
    energy=np.loadtxt(fileName,skiprows=1);
    a=energy[-1,-1];
    loop=0;

    while(a< energyVal):
        Re=Re+incre;
        ReCh(path,fileList[1],Re);
        incSolver(exe,fileList);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];
    while(a< energyVal2):
        FTCh(path,fileList[1],FT2);
        path2=os.getcwd()+'/2';
        if not os.path.exists(path2):
            os.makedirs(path2);
        os.chdir(path2);
        f=MaxChk(path);
        icFile='geom'+'.fld';
        CopyFile(path,path2,fileList);
        if(loop==0):ICFile(path,path2,icFile,'bd.xml');
        if(loop>0):ICFile(path2,path2,icFile,'bd.xml');
        incSolver(exe,fileList);
        addEnergyFile(path2,'EnergyFile.mdl');
        os.chdir(path);
        addEnergyFile(path2,'EnergyFile.mdl');
        os.chdir(path);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];
        subprocess.call('rm -r IC.bse',shell=True);
        loop=loop+1;

def firstExt2(path,exe,fileList,energyVal,FT,Re,FT2,incre,energyVal2):
    ReCh(path,fileList[1],Re);
    FTCh(path,fileList[1],FT);
    incSolver(exe,fileList);
    fileName='EnergyFile.mdl';
    energy=np.loadtxt(fileName,skiprows=1);
    a=energy[-1,-1];
    args='mv EnergyFile.mdl '+str(Re)+'.mdl';
    subprocess.call(args,shell=True);
    while(a< energyVal):
        Re=Re+incre;
        ReCh(path,fileList[1],Re);
        incSolver(exe,fileList);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];
        args='mv EnergyFile.mdl '+str(Re)+'.mdl';
        subprocess.call(args,shell=True);
    args="mv "+str(Re)+'.mdl'+' EnergyFile.mdl';
    subprocess.call(args,shell=True);
    while(a< energyVal2):
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
        moveChk(path2,path,ac,bc);                 
        os.chdir(path);
        addEnergyFile(path2,'EnergyFile.mdl');
        os.chdir(path);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];



def DeStab(path,exe,fileList,energyVal,FT,Re,FT2,incre,energyVal2,N):
    a=[-1,-2]; FileList=['geom.xml','bd.xml','geomBplusD.fld'];
    cwd=os.getcwd();
    FTCh(path,fileList[1],FT);
    while(all(i<0 for i in a)):
        for i in range(0,N):
            if not os.path.exists(str(int(Re+i*incre))):
                os.makedirs(str(int(Re+i*incre)));
            os.chdir(str(int(Re+i*incre)));
            CopyFileVal(cwd,os.getcwd(),FileList,str(int(Re+i*incre)),'0');
            ReCh(path,fileList[1],Re);
            print('the value of i\n');print(i);
            if(i<N-1):
                ipVar.incSolverP(exe,fileList);
                os.chdir(cwd);
        incSolver(exe,fileList);
        os.chdir(cwd);
        [a,b]=ipVar.poptDirEn(cwd,1e-8,1e-34);
        Re=Re+N*incre;
    os.chdir(path);
    ReP=[];
    [a,b]=ipVar.poptDirEn(path,1e-8,1e-33);
    for i in range(0,len(b)):
        if(a[i]>0):ReP.append(int(b[i]));
    re=min(ReP);
    os.chdir(str(re));
    print(os.getcwd())
    path1=glob('*');
    for i in path1:
        shutil.copy(os.getcwd()+'/'+i,path+'/'+i);
    os.chdir(path);
    path1=glob('*/');
    for i in path1:
        arg='rm -rf '+i;
        subprocess.call(arg,shell=True);
    fileName='EnergyFile.mdl';
    energy=np.loadtxt(fileName,skiprows=1);
    a=energy[-1,-1];
    while(a< energyVal2):
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
        moveChk(path2,path,ac,bc);                 
        os.chdir(path);
        addEnergyFile(path2,'EnergyFile.mdl');
        os.chdir(path);
        energy=np.loadtxt('EnergyFile.mdl',skiprows=1);
        a=energy[-1,-1];
            
def Fibonacci(n):
    if n==0: return 0;
    elif n==1: return 1;
    else: return Fibonacci(n-1)+Fibonacci(n-2);

def calcReC(x,y):
    if(len(x)==2):func=InterpolatedUnivariateSpline(y,x,k=1);
    if(len(x)==3):func=InterpolatedUnivariateSpline(y,x,k=2);
    if(len(x)>3):func=InterpolatedUnivariateSpline(y,x,k=3);
    
    z=np.where(np.diff(np.sign(x)))[0];
    a=y[z[0]];b=y[z[0]+1];

    tol=1e-6;
    while(abs(a-b)>tol):
        c=(a+b)/2.0;
        if(ipVar.samesign(func,a,c)):b=c;
        else: a=c
        #print(c)
        #print(func(c));
    c=(a+b)/2.0;
    return c;
