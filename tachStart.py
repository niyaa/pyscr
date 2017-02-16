import os, sys, subprocess;
def tachStart():
    cwd=os.getcwd();
    fileExe=sys.argv[0]
    f=open('/home/nyadav/.tachStart.sh','w');
    d=[];
    d1='cd '+cwd+';'+'\n';
    d.append(d1);
    #d1='ipython2 '+fileExe+';'+'\n';
    #d.append(d1);
    d1='exit 0'+';'
    d.append(d1);
    f.writelines(d);
    f.close();
    subprocess.call('qsub -I -l nodes=newton-01:ppn=1',shell=True);
    print('everything is fine');
