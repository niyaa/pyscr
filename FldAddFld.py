import sys, os;

sys.path.append("~/Dropbox/script")
import funcs;

N=funcs.MaxChk(os.getcwd());

for i in range(0,N+1):
    args='FldAddFld -1 1 geom3D.bse  geom_'+str(i)+'.chk '+'geom'+str(i)+'.fld';
    subprocess.call(args,shell=True);
    args='FieldConvert geom.xml'+' geom'+str(i)+'.fld'+' geom'+str(i)+'.vtu';
    subprocess.call(args,shell=True);

