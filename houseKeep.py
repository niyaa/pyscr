import os, sys;
from glob import glob;

from glob import glob;

import os, os.path;

def SubDirPath (d):
    return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)]);

def LatestDirectory (d):
    return max(SubDirPath(d), key=os.path.getmtime)

def comparSubDirNs(path1):
    os.chdir(path1);
    cwd=os.getcwd();
    path=glob("*/");
    for i in path:
        pathA=cwd+'/'+i;
        os.chdir(pathA);
        

