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
from scipy.interpolate import interp1d;
import funcs;
import color;

def CheckEnergy(filename):
    energy = np.loadtxt(filename,skiprows=1);
    a=energy[-1,-1];
    if((a > 1e-9) or ( a < 1e-20)):   return 0;
    else: return 1;

def CheckEnergySat(filename):
    case=Case();
    case.time, case.mod, case.energy = np.loadtxt(filename,  comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
    mm=set(case.mod);
    j=0;
    for i in mm:
        time=case.time[case.mod==i];
        en=case.energy[case.mod==i];
        print(en[-1]);
        if(en[-1]>0):j=j+1;
    if(j>20):return 1;
    return 0;

                   
def CheckEnergySat4Mode(filename):
    case=Case();
    case.time, case.mod, case.energy = np.loadtxt(filename,  comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
    mm=set(case.mod);
    j=1;
    time=case.time[case.mod==j];
    en=case.energy[case.mod==j];
    del case;
    if(np.abs(np.log10(en[-1]/en[0]))>=1.0):return 1;
    return 0;

def CheckSaturation(mod):
    case=Case();
    case.time,case.mod,case.energy = np.loadtxt('EnergyFile.mdl', comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True)
    t0=case.time[(case.mod==mod)];
    e0=case.energy[(case.mod==mod)];
    y1=np.gradient(e0,2);
    y2=np.where(y1<=0);
    if(len(y2[0])>1):return 0;
    return 1;


    os.chdir('/home/nyadav/pbs');
    f1=open('/home/nyadav/pbs/jobBezmpi.sh','r');
    d=f1.readlines();
    d[2]='#PBS -N '+name;
    d[6]='cd '+path;
    f1.close();
    # subprocess('rm /home/nyadav/pbs/jobBezmpi.sh',shell=True);
    f1=open('/home/nyadav/pbs/abc.sh','w');	
    f1.writelines(d);
    f1.close();

    subprocess("chmod" "u+x" "/home/nyadav/pbs/abc.sh",shell=True);
                
def moveChk(CurrentPath,NewPath,ChkN):
    for files in glob(CurrentPath+'/*.chk'):
        a= os.path.basename(files);b=a.split('.')[0].split('_')[1];
        b=int(b)+ChkN;c='geom_'+str(b)+'.chk';os.rename(files,NewPath+'/'+c);
        
def ICFile(fileName,count,path1,path2):
    chkStr='geom_'+str(int(count))+'.chk';
    shutil.copy((path1+'/'+chkStr),path2);

    tree=ET.parse('1000.xml',OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[1][6][0].set('FILE',chkStr);
    tree.write('1000.xml');

      
  
def sigma(path):
    fileList=[];x=[];y=[];
    for root, dirs, files in os.walk(path):
        for file in files:
            if (file.endswith(".mdl")):
                inE = os.path.join(root, file);
                fileList.append(inE);
    for f in fileList:
        case_str = f.split("/")
        case = Case();
        #case.alfa = Decimal(case_str[-5]);
        #case.mu = Decimal(case_str[-4]);                              
        #case.S = Decimal(case_str[-3]);
        case.Re = Decimal(float(case_str[-2]))
        #case.Name=str(case.alfa)+'_'+str(case.mu)+'_'+str(case.S)+'_'+str(case.Re);	 
        [pt,pr]=popt(f);
        print(pt[1]);print(case.Re);		
        case.popt=pt[1]/2.0;
        x.append(int(case.Re));
        y.append((pt[1]/2.0));
    if(all(i<0 for i in y)):
        return 0, 0, 0;
    print('the Reynolds number listi\n');
    print(x);
    print('the growth rate list \n');
    print(y);
    try:
        ReC=calcReC(x,y);
    except:
        print("the ReC is not defined for \t");
        ReC=-1;
    return x,y, ReC



def incSolver(exe,filelist):
    args=exe+'/IncNavierStokesSolver'+' '+filelist[0]+' '+filelist[1];
    print('Working in this directory \n');
    print(os.getcwd());
    subprocess.call(args,shell=True);

def incSolverP(exe,filelist):
    args=exe+' '+filelist[0]+' '+filelist[1]+' &';
    print('Working in this directory \n');
    print(os.getcwd());
    subprocess.call(args,shell=True); 

def incSolverHyp(np,npz,filelist):
    args='mpirun -np '+str(np)+' ~/.sg/IncNavierStokesSolver --npz '+str(npz)+' '+filelist[0]+' '+filelist[1];
    subprocess.call(args,shell=True);


def incSolverHypS(filelist):
    args='~/.sg/IncNavierStokesSolver'+' '+filelist[0]+' '+filelist[1];
    subprocess.call(args,shell=True);


import numpy as np;
from case import *;
import extractdata;
from scipy.optimize import curve_fit;
def func(x, a, b):
    return a*np.exp(b*x);
    
def popt(file):
    case=Case();
    case.time,case.mod,case.energy = np.loadtxt(file, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True)
    up=1e-8;down=1e-18;
    if(case.time[0] > 100):N1=case.time[0]; case.time[0::2]=case.time[0::2]-N1;case.time[1::2]=case.time[1::2]-N1;
    case.t,case.e=extractdata.extractData(case,case.time[-1], up, down);
    print(case.t);
    popt, pcov = curve_fit(func, case.t, case.e, p0=(1e-15, 1e-2))
    perr = np.sqrt(np.diag(pcov))[0]+np.sqrt(np.diag(pcov))[1] ;
    print(popt[1]/2.0);
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

def pbs(rse,name,module,wd,exe):
    f=open('pbs.sh','w');
    d=[];
    d.append('#!/bin/bash\n');
    d.append('#PBS -l '+rse+',walltime=15:00:00:00\n');
    d.append('#PBS -N '+name+'\n');
    d.append(module+'\n');
    d.append('cd '+wd+'\n');
    for i in exe:
        d.append(i+'\n');
    d.append('exit 0\n')
    f.writelines(d);
    f.close();

def nsvalues(path1):
    cwd=path1;
    path=glob('*/');
    x=[];y=[];
    for i in path:
        f=i.split('/')[0];
        newPath=cwd+'/'+f;
        print('the new path \n \n \n \n \n');
        print(newPath);
        print('\n \n \n \n \n \n');
        [a,b,c]=sigma(newPath);
        if(c > 0): 
            x.append(float(f));
            y.append(c);
    YX=zip(x,y);
    YX.sort();
    xx=[];yy=[];
    for i in range(0,len(YX)):
        yy.append(YX[i][0]);
        xx.append(YX[i][1]);
    c=(xx,yy);
    c=np.asarray(c);
    sVal=path1.split('/')[-1];
    alpha=path1.split('/')[-2];
    np.savetxt('ns.'+sVal+'.'+alpha+'.txt',c.T);

    return xx, yy;


def nekFre(inE,obsPointNos,velDir):
    #skipRows number of points obspoints Number =+1 
    time=[]; fre=[];
    a=np.loadtxt(inE,skiprows=obsPointNos+1);
    x=a[:,0];
    y=a[:,velDir];
    del a;
    f=interp1d(x,y,kind='cubic');

    xnew=np.linspace(x[0],x[-1],len(a[:,0]));
    ynew=f(xnew);

    for i in range(1,len(ynew)):
        if(np.sign(ynew[i-1])*np.sign(ynew[i]) < 0):
            time.append(xnew[i]);
    if(len(time)> 3 ):fre.append(time[-1]-time[-3]);
    return fre, time;


def nekFre3(inE,obsP,stp=0,points=-1,vel=3):
    #skipRows number of points obspoints Number =+1 
    time=[]; fre=[];
    a=np.loadtxt(inE,skiprows=obsP+1);
    #[ts,ft,a,d,e]=funcs.paramVal('bd.xml');
    if(len(a)>10):
        x=a[stp:points,0];
        y=a[stp:points,vel];
    else:
        return 0,[0],0;

    del a;
    if(len(x) <2000):
        f=interp1d(x,y,kind='cubic');
        xnew=np.linspace(x[0],x[-1],100*len(x));
        ynew=f(xnew);
    elif(len(x)>=2000):
        xnew=x;
        ynew=y;

    for i in range(1,len(ynew)):
        if(np.sign(ynew[i-1])*np.sign(ynew[i]) < 0):
            time.append(xnew[i]);
    if(len(time)> 3 ):
        for i in range(0,len(time)-2):
            fre.append(time[i+2]-time[i]);
            if(len(fre)%2==0):ans=fre[int(len(fre)/2)];
            if(len(fre)%2!=0 and len(fre)>2):ans=fre[int(len(fre)/2+1)];
        return ans, time, 2*np.pi/ans;
    if(len(time)==3):
        ans=time[2]-time[0];
        return ans, time, 2*np.pi/ans;
    if(len(time)<3 and len(time)>1):
        ans=(time[1]-time[0])*2;
        return ans,time, 2*np.pi/ans;
    if(len(time)<=1):
        return 0,[0],0;

def nekFre2(inE,obsPointNos,velDir,enFilePath):
    #skipRows number of points obspoints Number =+1
    [t,e]=extractdata.linearPt('EnergyFile.mdl')
    enFile=os.getcwd()+'/fileName';
    aa=np.loadtxt(enFile,skiprows=1,usecols=(0,1));
    tS=aa[0,0]; tE=aa[-1,0];
    t=t-tS;
    del aa;
    time=[]; fre=[];
    a=np.loadtxt(inE,skiprows=obsPointNos+1,usecols=(0,velDir));
    x=a[:,0]-a[0,0];
    y=a[:,1];
    del a;
    aa=[];cc=[];
    for i in range(0,len(y)-1):
        if(y[i]*y[i+1]<0): 
            aa.append(x[i]);
            cc.append(i);
    tree=ET.parse(enFilePath,OrderedXMLTreeBuilder());      
    root=tree.getroot();
    ts=float(root[1][1][0].text.split('=')[-1]);
    hsP=float(root[3][1][1].text);
    
    aa=np.array(aa)*ts/hsp;
    hisStep=aa[-1]-aa[-3];
    linearRange=t[-1]-t[0];
    if(hisStep < linearRange):
        i=np.where(aa>t[0]);
        i=(i[0][0]-1);
        j=np.where(aa<t[-1]);
        j=j[0][-1];
        xx=x[cc[i]:cc[j]]; 
        yy=x[cc[i]:cc[j]];
        f=interp1d(xx,yy,kind='cubic');
        xnew=np.linspace(xx[0],xx[-1],5*len(xx));
        ynew=f(xnew);
        for i in range(1,len(ynew)):
            if(np.sign(ynew[i-1])*np.sign(ynew[i]) < 0):
                time.append(xnew[i]);
        if(len(time)> 3 ):fre.append(time[3]-time[1]);
        return fre, time;



def poptEnRa(file,up=1e-8,down=1e-20):
    case=Case();
    case.time,case.mod,case.energy = np.loadtxt(file, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True)
    if(case.time[0] > 100):N1=case.time[0]; case.time[0::2]=case.time[0::2]-N1;case.time[1::2]=case.time[1::2]-N1;
    try:
        case.t,case.e=extractdata.extractData(case,case.time[-1], up, down);
    except:
        return [], 0 ;
    print(case.t);
    try:
        popt, pcov = curve_fit(func, case.t, case.e, p0=(1e-15, 1e-2))
    except:
        return [], 0;
    perr = np.sqrt(np.diag(pcov))[0]+np.sqrt(np.diag(pcov))[1] ;
    print(popt[1]/2.0);
    return popt, perr;   


def poptDir(path):
    os.chdir(path)
    cwd=path;
    path=glob('*/');
    x=[];y=[];
    for i in path:
        f=i.split('/')[0];
        newPath=cwd+'/'+f;
        os.chdir(newPath);
        print('working in this path \n \n \n \n \n');
        print(newPath);
        file=glob("*.mdl");
        file1=file[0];
        [a,b]=poptEnRa(file1,1e-8,1e-20);
        x.append(a[1]/2);
        y.append(float(f));
        os.chdir(cwd);
    if(len(x)==0):
        l1=x;
        l2=y;
    else:
        l2, l1 = zip(*sorted(zip(y, x)));
        l2=list(l2);l1=list(l1);
    return l1, l2;

def nsFile(path):
    os.chdir(path);
    cwd=path;
    path1=glob('*/');
    aa=[];
    bb=[];
    for i in path1:
        os.chdir(i);
        
def nsFile(path):
    os.chdir(path)
    col=color.color();
    cwd=path;
    p1=glob("*/");
    aa=[];bb=[];cc=[];dd=[];ee=[];
    for i in p1:
        try:
            [a,b]=poptFile(cwd+'/'+i);
        except:
            os.chdir(cwd);
            continue;
        try:
            c=funcs.calcReC(a,b);
            if(c>0):
                bb.append(c);
                aa.append(float(i.split('/')[0]));  
        except:
            args='The Critical Reynolds can not be found for '+i;
            print col.YELLOW + args+ col.END;
            cc.append(float(i.split('/')[0]));
            dd.append(a);
            ee.append(b);
            continue;
        os.chdir(cwd);

    l2, l1 = zip(*sorted(zip(aa, bb)));
    l2=list(l2);l1=list(l1);
    c=(l2,l1)
    c=np.asarray(c);
    sVal=cwd.split('/')[-1];
    alpha=cwd.split('/')[-2];
    np.savetxt('ns-'+sVal+'-'+alpha+'-.txt',c.T);
    print(col.DARKCYAN+'The Critical Reynolds can not be found for '+str(cc)+col.END);

    print(col.CYAN+'The corresponding growth rates \t'+col.END);
    print(col.PURPLE+'Reynolds  Number '+col.END);
    for i in range(0,len(dd)):
        c=(dd[i],ee[i]);
        c=np.asarray(c);
        print(col.CYAN+str(c.T[:,0])+col.END);
        print(col.PURPLE+str(c.T[:,1])+col.END);
    return l2, l1;



def poptFile(path):
    cwd=os.getcwd();
    os.chdir(path);
    path1=glob('*.mdl');
    x=[];y=[];
    for i in path1:
        f=i.split('-')[-2];
        try:
            [a,b]=poptEnRa(i);
        except:
            continue;
        if not (len(a) ==0 and b ==0):
            x.append(a[1]/2);
            y.append(float(f));
    os.chdir(cwd);
    if(len(x)==0):
        l1=x;
        l2=y;
    else:
        l2, l1 = zip(*sorted(zip(y, x)));
        l2=list(l2);l1=list(l1);
    return l1, l2;

def poptDirEn(path1,up,down):
    cwd=path1;
    path=glob('*/');
    x=[];y=[];
    for i in path:
        f=i.split('/')[0];
        newPath=cwd+'/'+f;
        os.chdir(newPath);
        print('working in this path \n \n \n \n \n');
        print(newPath);
        file=glob("*.mdl");
        file1=file[0];
        [a,b]=poptEnRa(file1,up,down);
        x.append(a[1]/2);
        y.append(float(f));
        os.chdir(cwd);
    #if(len(path==0):
    l2, l1 = zip(*sorted(zip(y, x)));
    l2=list(l2);l1=list(l1);
    return l1, l2;

def find_nearest(array,value):
    idx=(np.abs(array-value)).argmin();
    return array[idx],idx;

def find_nearest2D(x,y,z,point):
    if(x.ndim>1):x=x.flatten();

    if(y.ndim>1):y=y.flatten();
    if(z.ndim>1):z=z.flatten();
    
    xy=(x-point[0])**2+(y-point[1])**2;
    idx=[l for l,m in enumerate(xy) if m==min(np.abs(xy))];
    return z[idx]; 

    
