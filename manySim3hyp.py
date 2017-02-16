import os;
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
import sys;
import subprocess;
sys.path.append('/home/nyadav/pyscr');
import ipVar, funcs;
import numpy as np;
from scipy.interpolate import InterpolatedUnivariateSpline;
class CriticalRe:
    def __init__(self,aa,alpha,Sval):
        self.bdFname='bd.xml';
        cwd=os.getcwd();
        self.alpha=alpha;
        self.Sval=Sval
        if(alpha=='n'):
            self.Sval=cwd.split('/')[-1]
            self.aval=cwd.split('/')[-2];
        #self.bdFPath=cc;
        #if(self.bdFPath==' '):
        #    if(float(aval)==1):
        #        self.bdFPath='/home/nyadav/symm/'+sval+'/bd';
        #    self.bdFPath='/home/nyadav/symm/'+aval+'/'+sval+'/bd';
        #if not (self.bdFPath==' '):
        #    self.bdFPath=self.bdFPath+'/'+aval+'/'+sval+'/bd';
        self.geomFname='geom.xml';
        self.FileList=['geom.xml','bd.xml','geomHplusD.fld'];
        self.BetaPath=os.getcwd();
        self.ReList=[];
        self.exe='/home/nyadav/.sg/IncNavierStokesSolver';
        self.FilePath=os.getcwd();
        self.BetaPath=os.getcwd();
        self.betaList=aa;
        self.Re=0;
        self.beta=0;
        self.temp=0;
#        self.CreForBeta(); 
    def CreForBeta3(self):
        os.chdir(self.BetaPath);
        for i in self.betaList:
            if not os.path.exists(str(i)):
                os.makedirs(str(i));
            os.chdir(str(i));
            self.RePath=os.getcwd();
            self.beta=i;
            simRe=[];
            funcs.CopyFile(self.BetaPath,os.getcwd(),self.FileList);
            #reList=[60,80,100,200,350,400,600,800];
            #for re in reList:
            #    ReHisFile=str(self.alpha)+'-'+str(i)+'-'+str(self.Sval)+'-'+str(re)+'-'+'.his';
            #    print(ReHisFile);   
            #    if os.path.exists(os.getcwd()+'/'+ReHisFile):
            #        print('yes');
             #       totalHisPt=np.loadtxt(ReHisFile);
             #       print(totalHisPt[-1,0]-totalHisPt[1,0]);
              #      if(totalHisPt[-1,0]-totalHisPt[1,0]<400):
               #         print('less');
                #        simRe.append(re);
                        
                #else:    
                 #   print('no');
                  #  simRe.append(re);
            #print(simRe);
            #self.ReFre(simRe,400);
            
            self.Re1000(9,50);
            self.Re100(8,100);
            self.Re10(5,150);
            #self.ReFinal2(200);
            #self.ReExt([110,120],200);
            os.chdir(self.BetaPath);



    def Re1000(self,N,time):
        self.ReList=[];
        self.ReList.append(50);
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



    def ReFinal(self):
        [a,b]=ipVar.poptFile(os.getcwd());
        re=funcs.calcReC(a,b);
        re=int(re);
        self.ReList=[];
        self.ReList.append(re);
        path=os.getcwd();
        if not os.path.exists(str(re)):
            os.makedirs(str(re));
        os.chdir(str(re));
        para=[0.005,400,'0.1*FinalTime/TimeStep','','',self.beta,'','0.2/TimeStep',str(np.pi/self.alpha)+' 0 0 ','1'];
        funcs.CopyFile(path,os.getcwd(),self.FileList);
        self.CritRe2(para);
        

    def ReFinal2(self,time):
        [a,b]=ipVar.poptFile(os.getcwd());
        re=funcs.calcReC(a,b);
        re=int(re);
        self.ReList=[];
        self.ReList.append(re);
        para=[0.005,time,'0.1*FinalTime/TimeStep','','',self.beta,'','0.2/TimeStep',str(np.pi/self.alpha)+' 0 0 ','1'];
        self.CritRe2(para);


    def ReExt(self,rlist,time):
        self.ReList=rlist;
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','2*FinalTime/TimeStep',str(np.pi/self.alpha)+' 0 0 ','0.5'];
        self.CritRe2(para);
        
    
    def ReFre(self,rlist,time):
        self.ReList=rlist;
        para=[0.005,time,'2*FinalTime/TimeStep','','',self.beta,'','0.2/TimeStep',str(np.pi/self.alpha)+' 0 0 ','0.5'];
        self.IncModFreFile(para);

    def CritRe2(self,para):
        for i in self.ReList:
            para[6]=str(self.alpha)+'-'+str(self.Sval)+'-'+str(self.beta)+'-'+str(int(i))+'-.mdl';
            para[3]=i;
            para[5]=self.beta;
            funcs.simPara(os.getcwd(),self.FileList[1],para);
            funcs.incSolver(self.exe,self.FileList[:-1]);
        
            
    def IncModFreFile(self,para):
        for i in self.ReList:
            para[6]=str(self.alpha)+'-'+str(self.Sval)+'-'+str(self.beta)+'-'+str(int(i))+'-.mdl';
            para[3]=i;
            para[5]=self.beta;
            funcs.simPara(os.getcwd(),self.FileList[1],para);
            funcs.incSolver(self.exe,self.FileList[:-1]);
            fileName=str(self.alpha)+'-'+str(self.Sval)+'-'+str(self.beta)+'-'+str(int(i))+'-'+'.his';
            arg='mv TimeValues.his '+fileName;
            subprocess.call(arg,shell=True);
        
            filelist=['geom.xml','bd.xml','geomHplusD.fld'];
            #ipVar.incSolverHypS(filelist);
            #ipVar.incSolverHyp(1,4,filelist);
            ipVar.incSolver('~/.sg',filelist);
            #self.IncSolver();


    def IncSolver(self):
        FileList=['geom.xml','bd.xml','geomHplusD.fl'];
        args='mpirun -np 1 ~/.sg/IncNavierStokesSolver --npz 4 '+FileList[0]+' '+FileList[1];
        subprocess.call(args,shell=True);







