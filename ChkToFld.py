import subprocess;
import os;
from glob import glob;

N=glob("*.chk");
N=len(N);
for i in range(0,N):
    args='FieldConvert geom.xml geom_'+str(i)+'.chk '+'geom_'+str(i)+'.fld';
    
    subprocess.call(args,shell=True);

