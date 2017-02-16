import subprocess
#a=[0.2,0.55,0.38,0.48,0.28];
#a=[0.1,0.15,0.25,0.3,0.35,0.4,0,45,0.5,0.6,0.7,0.8]
a=[0.38]
for i in a:
    arg='ipython2 manyObj.py '+str(i)+' &';
    subprocess.call(arg,shell=True);


