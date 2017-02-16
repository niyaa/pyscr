import manySim3;
import betaCrSimulation;
import sys;
import os;
import subprocess;
import ipVar;

first_arg=sys.argv[1];
a=[];
print(a)
cwd=os.getcwd();
if os.path.exists(os.getcwd()+'/bd.xml'):
    subprocess.call('rm bd.xml',shell=True);
if not os.path.exists(os.getcwd()+'/bd.xml'):
    args='cp /home/nyadav/pyscr/bd.xml'+' '+cwd;
    subprocess.call(args,shell=True); 
alpha=float(cwd.split('/')[-2]);
sval=float(cwd.split('/')[-1]);
if(first_arg=='smooth'):
    b=betaCrSimulation.CriticalRe(alpha,sval);
    b.CreForBeta3();
else:
    a.append(float(first_arg));
    b=manySim3.CriticalRe(a,alpha,sval);
    b.CreForBeta3();

