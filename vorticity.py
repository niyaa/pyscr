import subprocess;
from glob import glob;

N=glob("*.fld");
N=len(N);
for i in range(0,N):
    args='FieldConvert -m vorticity geom.xml geom_'+str(i)+'.fld '+'geom-vort'+str(i)+'.fld';
    subprocess.call(args,shell=True);
