import os;
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
import sys;
sys.path.append('/home/nyadav/pyscr');
import ipVar, funcs;
import numpy as np;
from scipy.interpolate import InterpolatedUnivariateSpline;
class CriticalRe:
    def __init__(self,aa):
        self.bdFname='bd.xml';
        cwd=os.getcwd();
        sval=cwd.split('/')[-1]
        aval=cwd.split('/')[-2];
        if(aval=='1'):
            self.bdFPath='/home/nyadav/symm/'+sval+'/bd';
        self.bdFPath='/home/nyadav/symm/'+aval+'/'+sval+'/bd';
        self.geomFname='geom.xml';
        self.FileList=['geom.xml','bd.xml','geomHplusD.fld'];
        self.RePath=os.getcwd();
        self.ReList=[];
        self.exe='/home/nyadav/bin/IncNavierStokesSolver';
        self.FilePath=os.getcwd();
        self.BetaPath=os.getcwd();
        self.betaList=aa;
        self.Re=0;
        self.beta=0;
        self.temp=0;
#        self.CreForBeta(); 
        

    def IG(self,beta,ReNm):
        if not (self.bdFname=='0'):
            self.ReList=[];
            self.beta=beta;
            tree=ET.parse(self.bdFPath+'/'+self.bdFname,OrderedXMLTreeBuilder());
            root=tree.getroot();
            Re=float(root[1][1][5].text.split('=')[-1]);
            self.ReList.append(int(Re)-0.4*int(Re));
            ReNew=float(Re)+float(Re)*4*(abs(beta-0.4));
            self.ReList.append(int(ReNew));
            self.CritRe(100);
            [a,b]=ipVar.poptDir(self.RePath);
            self.temp=Re;
            while(all(i<0 for i in a)):
                self.ReList=[];
                ReNew=float(ReNew)+0.5*(float(ReNew));
                self.ReList.append(ReNew);
                self.CritRe(100);
                [a,b]=ipVar.poptDir(self.RePath);
            while(all(i>0 for i in a)):
                self.ReList=[];
                Re=float(Re)-0.5*(float(Re));
                self.ReList.append(Re);
                self.CritRe(100);
                [a,b]=ipVar.poptDir(self.RePath);
        else:
            self.ReList=[];
            self.ReList.append(ReNm);
            ReNew=ReNm**(abs(beta-0.4)+1);
            self.ReList.append(ReNew);
        return self.ReList;

    def CritRe(self,FT):
        for i in self.ReList:
            if not os.path.exists(str(i)):
                os.makedirs(str(i));
            os.chdir(str(i));
            funcs.CopyFileVal(self.FilePath,os.getcwd(),self.FileList,str(i),self.beta);
            funcs.FTCh(os.getcwd(),self.FileList[1],FT);
            funcs.incSolver(self.exe,self.FileList[:-1]);
            os.chdir(self.RePath);

    def ReIter(self,FT):
        [a,b]=ipVar.poptDir(self.RePath);
        while(all(i > 0 for i in a)):
            self.ReList=[];
            ReNew=float(b[0])- 0.2*float(b[0]);
            self.ReList.append(ReNew);
            self.CritRe(FT);
            [a,b]=ipVar.poptDir(self.RePath);

        while(all(i < 0 for i in a)):
            self.ReList=[];
            ReNew=float(b[-1])+0.3*float(b[-1]);
            self.ReList.append(ReNew);
            self.CritRe(FT);
            [a,b]=ipVar.poptDir(self.RePath); 
        [a,b]=ipVar.poptDir(self.RePath);
        z=np.where(np.diff(np.sign(a)))[0];
        i=z[0];
        r1=b[i];r2=b[i+1];
        print(r1);print(r2);
        print("the value of the ");
        temp=[0];
        ReCr=funcs.calcReC(a,b);
        temp.append(ReCr);
        while(abs(temp[-1]-temp[-2])>1):
            self.ReList=[];
            ReCr=funcs.calcReC(a,b);
            self.ReList.append(ReCr+0.1*abs(r1-r2));
            self.ReList.append(ReCr-0.1*abs(r1-r2));
            self.CritRe(FT);
            print(r1);print(r2);
            ReCr=funcs.calcReC(a,b);
            temp.append(ReCr);
            [a,b]=ipVar.poptDir(self.RePath);
            z=np.where(np.diff(np.sign(a)))[0];
            r1=b[z[0]];r2=b[z[0]+1];

        [a,b]=ipVar.poptDir(self.RePath);
        if(len(a)>3):func=InterpolatedUnivariateSpline(b,a,k=3);
        ReC=func.roots();
        return ReC;


    def ReIter2(self,FT):
        [a,b]=ipVar.poptDir(self.RePath);
        z=np.where(np.diff(np.sign(a)))[0];
        r1=b[z[0]];r2=b[z[0]+1];
        while(abs(r1-r2)>11):
            [a,b]=ipVar.poptDir(self.RePath);
            ReCr=funcs.calcReC(a,b);
            self.ReList.append(ReCr+5);
            self.ReList.append(ReCr-5);
            self.CritRe(FT);
            [a,b]=ipVar.poptDir(self.RePath);
            ReCr=funcs.calcReC(a,b);
            z=np.where(np.diff(np.sign(a)))[0];
            r1=b[z[0]];r2=b[z[0]+1];

        if(abs(r1-r2)< 11):
            [a,b]=ipVar.poptDir(self.RePath);
            ReCr=funcs.calcReC(a,b);
            self.ReList.append(ReCr);
            self.CritRe(FT);

        [a,b]=ipVar.poptDir(self.RePath);
        if(len(a)>3):func=InterpolatedUnivariateSpline(b,a,k=3);
        ReC=func.roots();
        return ReC;

    def CreForBeta(self):
        os.chdir(self.BetaPath);
        for i in self.betaList:
            if not os.path.exists(str(i)):
                os.makedirs(str(i));
            os.chdir(str(i));
            self.RePath=os.getcwd();
            self.beta=i;
            self.IG(i,600);
            self.ReIter(100);
            self.ReIter2(300);
            os.chdir(self.BetaPath);
    
    # intial guess is calculate more accurately 
    #based on previous calculations
    def CreForBeta2(self):
        os.chdir(self.BetaPath);
        path=glob('*/');
        beta=self.betaList[0];
        path=glob('*/');
        path=[float(i.split('/')[0]) for i in beta];
     #   adjacentB=[i 

    #    for i in sorted(path):
            
      #      adjacentB.append(
        
        
        
        
     







