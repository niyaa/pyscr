import manySim3hyp;
import sys;
import os;
import subprocess;

first_arg=sys.argv[1];
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
b=manySim3hyp.CriticalRe(a,alpha,sval)
b.CreForBeta3();
