import os, sys;
from glob import glob;
import subprocess;
i=10;
cwd=os.getcwd();
path=glob('*/');
S=[];Qx=[];Qy=[];Qy=[];
for i in path:
    base=os.getcwd()+'/'+i+'b';
    os.chdir(base);
    subprocess.call("~/tachold/dist/bin/FldToVtk geom.xml geom_10.chk ",shell=True);
    os.chdir(cwd);
