import os;
from glob import glob;
import base;
path=
cwd=os.getcwd();

os.chdir(path);
path1=glob("*/");

for i in path1:
    if not os.path.exists(i):
        os.makedirs(i);
    os.chdir(i);
    bdFilePath=path+'/'+str(i)+'bd';
    base.preHoly(bdFilePath,os.getcwd());
    os.chdir(cwd);

