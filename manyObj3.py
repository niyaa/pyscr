import manySim4;
import sys;
sys.path.append('/home/nyadav/pyscr');
from output import *;
import os;
import subprocess;
import ipVar;

first_arg=sys.argv[1];
second_arg=sys.argv[2];
a=[];
a.append(float(first_arg));
print(a)
cwd=os.getcwd();
if os.path.exists(os.getcwd()+'/bd.xml'):
    subprocess.call('rm bd.xml',shell=True);
if not os.path.exists(os.getcwd()+'/bd.xml'):
    args='cp /home/nyadav/pyscr/bd.xml'+' '+cwd;
    subprocess.call(args,shell=True); 
alpha=float(cwd.split('/')[-2]);
sval=float(cwd.split('/')[-1]);
betaList=[]; 
rlist=[];
#ReMul=[0.1,0.5,2,4];
#out=Output(); 
#out.alpha, out.beta, out.S, out.ReC=np.loadtxt('/home/nyadav/test/ReCr.txt',usecols=(0,1,2,3),unpack=True);
#ReBeta=out.ReC[(out.alpha==alpha)&(out.S==sval)&(out.beta==a[0])];
#Re=out.ReC[(out.alpha==alpha)&(out.S==sval)];
rlist=[];
rlist.append(float(second_arg));

#ReMin=min(Re); 
#for j in ReMul: 
#    k=0; 
#    if(ReMin+ReMin*j > ReBeta):
#        rlist.append(ReMin+ReMin*j); 


print(a);print(rlist);
#[a,b]=ipVar.nsFile(os.getcwd());
b=manySim4.CriticalRe(a,alpha,sval,rlist);
b.CreForBeta3();
