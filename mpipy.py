import subprocess;
import sys;
sys.path.append('/home/nyadav/pyscr/')
import funcs;
import ipVar;


Re=

cwd=os.getcwd();
funcs.ReCh(cwd,'bd.xml',Re);
subprocess.call('qsub /home/nyadav/pbs/mpipbs.sh',shell=True);

