import numpy as np;
import os;
def genPointFile(a,fileName='file.pts',fld='u,v,w'):
    b=np.zeros((len(a[:,0]),4),dtype=np.float);
    for i in range(0,len(a[:,0])):
        b[i,0]=i+1;
        b[i,1:4]=a[i,:];
    d=[];
    path=os.getcwd()+'/'+fileName;
    f=open(path,'w');
    d.append('<?xml version="1.0" encoding="utf-8" ?> \n');
    d.append('<NEKTAR> \n');
    d.append('<POINTS DIM="1" FIELDS="'+fld+'"> \n');
    for i in range(0,len(a[:,0])):
       d.append(str(b[i,0])+' '+str(b[i,1])+' '+str(b[i,2])+' '+str(b[i,3])+str('\n'));
    d.append('</POINTS> \n');
    d.append('</NEKTAR> \n');
    f.writelines(d);
    f.close();



