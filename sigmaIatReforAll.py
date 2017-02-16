import subprocess;
import os,sys,shutil;
from glob import *;
import time;
cwd=os.getcwd();
Sval=[0.05];
import funcs;

for i in Sval:
    os.chdir(str(i));
    spath=os.getcwd();
    #betaVal=[0.1,0.22,0.3,0.4,0.5,0.6];
    betaVal=glob("*/");
    cricRe=[];
    for j in betaVal:
        os.chdir(str(j));
        betapath=os.getcwd();
        #[a,b]=ipVar.poptDir(os.getcwd());
        #ReVal=glob("*/");
        #re=funcs.calcReC(a,b);
        #ReVal=[];
        #cricRe.append(re);
        #print("The critical Reynolds number is \n");
        #print(re);
        ReVal=[600,650,700,750,800,900,1000,1200,1400,1500,2000];
        #ReVal.append(re);
        RePath=os.getcwd()
        for k in ReVal:
            if not os.path.exists(str(k)):
                os.makedirs(str(k));
            os.chdir(str(k));
            if os.path.exists(os.getcwd()+'/bd.xml'):
                subprocess.call('rm bd.xml',shell=True);
            #kk=float(k.split('/')[0]);
            jj=float(j.split('/')[0]);
            print(os.getcwd());

            funcs.ReCh('/home/nyadav/pyscr','1000.xml',k);
            funcs.LzCh('/home/nyadav/pyscr','1000.xml',jj);
            funcs.FTCh('/home/nyadav/pyscr','1000.xml',150);
            if not os.path.exists(os.getcwd()+'/geomHplusD.fld'):
                shutil.copy(spath+'/geomHplusD.fld',os.getcwd());

            if not os.path.exists(os.getcwd()+'/geom.xml'):
                shutil.copy(spath+'/geom.xml',os.getcwd());
            shutil.copy('/home/nyadav/pyscr'+'/1000.xml',os.getcwd()+'/bd.xml');

            print(os.getcwd());

            subprocess.call('qsub /home/nyadav/pbs/pbs.sh',shell=True);

            time.sleep(2);
            os.chdir(RePath);

        os.chdir(spath);
    #np.savetxt(str(i)+'ReCrforbeta.txt',np.array(cricRe));
    os.chdir(cwd);
