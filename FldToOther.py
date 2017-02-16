import os, sys;
sys.path.append('/home/nyadav/pyscr/');
import subprocess;
import funcs;
import readline
readline.parse_and_bind("tab: complete");
from glob import *;


print("1 if to process chk else 0 \n");
process=int(raw_input());
if(process==0):	
    print('Enter the fld file \n');
    fldfile=str(raw_input('-->'));
    print('Enter the geom file \n');
    geofile=str(raw_input('-->'));
    dtype=fldfile.split('.')[0]+'.vtu';
    print("Ener  1 for tach 0 for hyp \n");
    exe=int(raw_input());
    if(exe==1):
        args='~/bin/FieldConvert '+fldfile+' '+geofile+' '+dtype;
    if(exe==0):
        args='~/bin/sgFiled '+fldfile+' '+geofile+' '+dtype;
    subprocess.call(args,shell=True);
if(process==1):
    N=len(glob("*.chk"));
    if(N==0):N=len(glob("*.chk/"));

    print('Enter output type if its not VTU \n');
    dtype=str(raw_input());
    if(dtype=='1'):
	dtype='vtu';
    dtype='.'+str(dtype);

    print("Ener 1 for tach 0 for hyp \n");
    exe=int(raw_input());
    if(exe==1):
        for i in range(0,N+1):
            args='~/bin/FieldConvert '+'geom.xml '+'geom_'+str(i)+'.chk ' +'geom_'+str(i)+dtype;
            subprocess.call(args,shell=True);
    if(exe==0):
        for i in range(0,N+1):
            args='~/bin/sgField '+'geom.xml '+'geom_'+str(i)+'.chk ' +'geom_'+str(i)+dtype;
            subprocess.call(args,shell=True);
