import os;
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
import sys;
sys.path.append('/home/nyadav/pyscr');
import ipVar, funcs;
import numpy as np;
from scipy.interpolate import InterpolatedUnivariateSpline;
import subprocess;
import sigmaMax;
class CriticalRe:
    def __init__(self,alpha,Sval):
        self.bdFname='bd.xml';
        cwd=os.getcwd();
        self.alpha=alpha;
        self.Sval=Sval
        self.geomFname='geom.xml';
        self.FileList=['geom.xml','bd.xml','geomHplusD.fld'];
        self.BetaPath=os.getcwd();
        self.ReList=[];
        self.exe='/home/nyadav/.bin/IncNavierStokesSolver';
        self.FilePath=os.getcwd();
        self.BetaPath=os.getcwd();
        self.betaList=[];
        self.Re=0;
        self.beta=0;
        self.temp=0;
#        self.CreForBeta(); 
    def CreForBeta3(self):
        os.chdir(self.BetaPath);
        [rmax,rmin,be,betaBound]=sigmaMax.betaCr(os.getcwd());
        self.betaList=[be+0.01,be-0.01];
        for i in self.betaList:
            if not os.path.exists(str(i)):
                os.makedirs(str(i));
            os.chdir(str(i));
            funcs.CopyFile(self.BetaPath,os.getcwd(),self.FileList);
            self.beta=i;
            self.RePath=os.getcwd();
            self.ReExt([rmax,rmin],80);
            self.ReSmooth(100,2);
            self.ReSmooth(100,0.3);
            os.chdir(self.BetaPath);
        self.betaList=betaBound;
        for i in self.betaList:
            if not os.path.exists(str(i)):
                os.makedirs(str(i));
            os.chdir(str(i));
            funcs.CopyFile(self.BetaPath,os.getcwd(),self.FileList);
            self.beta=i;
            self.RePath=os.getcwd();
            self.ReSmooth(100,2);
            self.ReSmooth(100,0.3);
            os.chdir(self.BetaPath);
    def calReCForS(self):
        [a,b]=ipVar.nsFile(os.getcwd());
        return a,b;

    def Re1000(self,N,time):
        self.ReList=[];
        self.ReList.append(50);
        selg.ReList.append(900);
        for i in range(0,N):
            self.ReList.append(int(300+i*1000));
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','0.5'];
        self.CritRe2(para);
    
    def Re100(self,N,time):
        self.ReList=[];
        [a,b]=ipVar.poptFile(os.getcwd());
        xx=(i for i in range(0,len(a)) if a[i] > 0 ).next();
        self.ReList.append(abs(b[xx]-100));
        para=[0.005,150,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','0.5'];
        self.CritRe2(para);
        self.ReList=[];

        re=funcs.calcReC(a,b);
        a=np.floor(re/1000)*1000;
        b=np.ceil(re/1000)*1000;
        c=(b-a)/N;
        c=int(c);
        for i in range(1,N):
            self.ReList.append(int(a+i*c));
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','0.5'];
        self.CritRe2(para);

    def Re10(self,N,time):
        self.ReList=[];
        [a,b]=ipVar.poptFile(os.getcwd());
        xx=[];
        for i in range(0,len(a)-1):
            if(a[i]*a[i+1] < 0):xx.append(i);
        if(len(xx) >2):
            self.ReList.append(b[xx[1]]+10);
            self.ReList.append(abs(b[xx[1]]-10));
            self.ReList.append(b[xx[2]]+10);
            self.ReList.append(abs(b[xx[2]]-10));
        para=[0.005,150,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','0.5'];
        self.CritRe2(para);
        self.ReList=[];


        [a,b]=ipVar.poptFile(os.getcwd());
        re=funcs.calcReC(a,b);
        a=np.floor(re/100)*100;
        b=np.ceil(re/100)*100;
        c=(b-a)/N;
        c=int(c);
        for i in range(1,N):
            self.ReList.append(int(a+i*c));
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','1'];
        self.CritRe2(para);



    def ReFinal(self,time):
        [a,b]=ipVar.poptFile(os.getcwd());
        re=funcs.calcReC(a,b);
        re=int(re);
        self.ReList=[];
        self.ReList.append(re);
        path=os.getcwd();
        if not os.path.exists(str(re)):
            os.makedirs(str(re));
        os.chdir(str(re));
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','1'];
        funcs.CopyFile(path,os.getcwd(),self.FileList);
        self.CritRe2(para);
        
    def ReSmooth(self,time,incre):
        [a,b]=ipVar.poptFile(os.getcwd());
        re=funcs.calcReC(a,b);
        self.ReList=[];
        self.ReList.append(re);
        self.ReList.append(re+incre);
        self.ReList.append(re-incre);
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','1'];
        self.CritRe2(para);

    def ReFinal2(self,time):
        [a,b]=ipVar.poptFile(os.getcwd());
        re=funcs.calcReC(a,b);
        self.ReList=[];
        self.ReList.append(re);
        para=[0.005,time,'0.1*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','1'];
        self.CritRe2(para);


    def ReExt(self,rlist,time):
        self.ReList=rlist;
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','0.5'];
        self.CritRe2(para);
        
    
    def CritRe2(self,para):
        for i in self.ReList:
            para[6]=str(self.alpha)+'-'+str(self.Sval)+'-'+str(self.beta)+'-'+str(i)+'-.mdl';
            para[3]=i;
            para[5]=self.beta;
            funcs.simPara(os.getcwd(),self.FileList[1],para);
            funcs.incSolver(self.exe,self.FileList[:-1]);
            fileName=str(self.alpha)+'-'+str(self.Sval)+'-'+str(self.beta)+'-'+str(i)+'-'+'.his';
            arg='mv TimeValues.his '+fileName;
###################################################################
####uncomment this line for History point production##############
            #subprocess.call(arg,shell=True);
            
            #ipVar.incSolverP(self.exe,self.FileList[:-1]);







