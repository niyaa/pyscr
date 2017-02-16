from glob import glob;
import os;
import sys;
sys.path.append('/home/nyadav/pyscr/');
import ipVar;
pathS=glob("*/");

cwd=os.getcwd()
aa=[];
bb=[];

for i in pathS:
    pathBeta=cwd+"/"+i;
    os.chdir(pathBeta);
    [a,b]=ipVar.poptDir(os.getcwd());
    if(ipVar.calcReC(a,b)):
        c=ipVar.calcReC(a,b);
    aa.append(c);

print(aa);



    
