import sys;
import os;
import subprocess;
sys.path.append('/home/nyadav/pyscr/');
import betaCrSimulation;
cwd=os.getcwd();
if os.path.exists(os.getcwd()+'/bd.xml'):
    subprocess.call('rm bd.xml',shell=True);
if not os.path.exists(os.getcwd()+'/bd.xml'):
    args='cp /home/nyadav/pyscr/bd.xml'+' '+cwd;
    subprocess.call(args,shell=True);
alpha=float(cwd.split('/')[-2]);
sval=float(cwd.split('/')[-1]);
b=betaCrSimulation.CriticalRe(alpha,sval);
b.CreForBeta3();

