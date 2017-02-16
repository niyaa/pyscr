import subprocess;
exe='/home/nyadav/nekNewton/dist/bin/'
i=int(raw_input("Enter the number of chk file\n"));
chkFile='geom_'+str(i)+'.chk';
j=raw_input("Enter the scaling factor\n");
arg=exe+'FldAddFld -1 1 geom3D.bse '+chkFile+' geomHplusD.fld';
subprocess.call(arg,shell=True);
arg=exe+'FldAddFld 1 '+str(j)+' geom3D.bse geomHplusD.fld geomHplusD.fld';
subprocess.call(arg,shell=True);
