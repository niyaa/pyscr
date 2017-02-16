import sys;
import readline;
sys.path.append('/home/nyadav/pyscr/');
import nekOpr;
import os;
from glob import glob;
cwd=os.getcwd();
path=glob("*/");
print('Enter 1 for tachion and 0 for hyperion \n');
val=raw_input('-->');
for i in path:
    os.chdir(i);
    try:
        if(val==1):
            nekOpr.vtu();
        else:
            nekOpr.vtuHyp();
        if os.path.exists(os.getcwd()+'/2'):
            arg='rm -r 2/';
            subprocess.call(arg,shell=True);
    except:
        print("there is no vtu file \n");
    
    pathNew=os.getcwd();
    path1=glob("*/");
    for i in path1:
        os.chdir(i);
        try:
            if(val==1):
                nekOpr.vtu();
            else:
                nekOpr.vtuHyp();
        except:
            print("There is no vtu file \n");
        os.chdir(pathNew);
    os.chdir(cwd);
