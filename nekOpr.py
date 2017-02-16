import sys, os, subprocess;

sys.path.append("/home/nyadav/pyscr")
import funcs;

def dist():
    N=funcs.MaxChk(os.getcwd());

    for i in range(0,N+1):
        args='FieldConvert -m concatenate geom.xml geom_'+str(i)+'.chk/*.fld geom_'+str(i)+'.fld';
        subprocess.call(args,shell=True);
        args='FldAddFld -1 1 geom3D.bse  geom_'+str(i)+'.fld '+'geom'+str(i)+'.fld';
        subprocess.call(args,shell=True);
        args='FieldConvert geom.xml geom'+str(i)+'.fld geom'+str(i)+'.vtu';
        subprocess.call(args,shell=True);


def vtu():
    path=os.getcwd();
    N=funcs.MaxChk(path);
    for i in range(0,N+1):
        if not (os.path.exists(os.getcwd()+'/geom_'+str(i)+'.vtu')):
            args='FieldConvert geom.xml '+'geom_'+str(i)+'.chk '+'geom_'+str(i)+'.vtu';
            subprocess.call(args,shell=True);

        
def vtuHyp():
    path=os.getcwd();
    N=funcs.MaxChk(path);
    for i in range(0,N+1):
        if not (os.path.exists(os.getcwd()+'/geom_'+str(i)+'.vtu')):
            args='~/.sg/FieldConvert geom.xml '+'geom_'+str(i)+'.chk '+'geom_'+str(i)+'.vtu';
            subprocess.call(args,shell=True);
