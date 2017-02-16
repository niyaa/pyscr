import subprocess;

def qdel(i,j):
    for k in range(0,j):
        i=i+k
        arg=str(i)+'.tachion-a &';
        arg1='qdel '+arg;
        subprocess.call(arg1,shell=True);
