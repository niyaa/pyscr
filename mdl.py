import os;
from glob import glob;
import subprocess;
cwd=os.getcwd()
path1=glob("*/");
print(path1);
alpha=cwd.split('/')[-2]
sval=cwd.split('/')[-1]

for j in path1:
    os.chdir(j);
    path=glob("*.mdl");

    for i in path:
        if(i.split('.')[-2]=='0'): 
            jj=int(i.split('.')[-3]);
        else:
            jj=int(i.split('.')[-2]);
        print(j)
        args='mv '+i+' '+alpha+'-'+sval+'-'+j.split('/')[0]+'-'+str(jj)+'-.mdl'
        print(args)
        subprocess.call(args,shell=True)
    os.chdir(cwd);

