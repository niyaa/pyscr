from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
import sys;
import funcs;
sys.path.append('/home/llaniewski/TP/build/lib')
sys.path.append('/home/llaniewski/TP/build/lib/site-packages')
sys.path.append('/home/nyadav/anaconda2/lib/python2.7/site-packages')
from paraview.simple import *;
from paraview.numeric import fromvtkarray;
from scipy import interpolate, optimize, integrate;
import math;
from glob import glob;
import os;
import numpy as np;
import funcs;


print("Enter 0 for the TimeStep calculation \n");
print("Else enter the time step size \n");

def calcTimeStep():
    cwd=os.getcwd();
    N=len(glob("*.chk/"))-1;
    t1=0;t2=0;
    while(t1 ==0 and t2 == 0 ):
        os.chdir('geom_'+str(N-1)+'.chk');
        FilePath=os.getcwd()+'/Info.xml';
        tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
        root=tree.getroot();
        t1=float(root[0][4].text);
        os.chdir(cwd);
        os.chdir('geom_'+str(N)+'.chk');
        FilePath=os.getcwd()+'/Info.xml';
        tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
        root=tree.getroot();
        t2=float(root[0][4].text);
        os.chdir(cwd);
        N=N-1;
        if(N<1):t1=t2=1;
    return t2-t1;
 
        


def satFlowRate(tt):
    if (tt==0):
        t=calcTimeStep();
    else:
        t=tt;
    vtuN=glob("*.vtu");
    N=len(vtuN);
    Qx=[];
    Qy=[];
    Qz=[];
    for i in range(0,N):
        inE=os.getcwd()+'/geom_'+str(i)+'.vtu';
        if os.path.exists(inE):
            geomvtu = XMLUnstructuredGridReader(FileName=[inE])
            geomvtu.PointArrayStatus = ['u', 'v', 'w', 'p']
            slice1=Slice(Input=geomvtu)
            slice1.SliceType='Plane';
            slice1.SliceOffsetValues = [0.0];
            xslice = math.pi / 0.5
            slice1.SliceType.Origin = [xslice, 0.0, 0.0];
            slice1.SliceType.Normal=[0,0,-1]
            slice1.SliceOffsetValues = [0.0]
            slice1.UpdatePipeline();
            pl = servermanager.Fetch(slice1)
            nbp = pl.GetNumberOfPoints()
            pos1 = fromvtkarray(pl.GetPoints().GetData())
            integrateVariables1 = IntegrateVariables(Input=slice1);
            Q=integrateVariables1.PointData[3]
            qz=Q.GetRange()[0];
            Qz.append(qz);
            Q=integrateVariables1.PointData[2]
            qy=Q.GetRange()[0];
            Qy.append(qy);
            Q=integrateVariables1.PointData[1];
            qx=Q.GetRange()[0];
            Qx.append(qx);

    a=np.zeros((len(Qz),4),dtype=np.float);
    for i in range(0,len(Qz)):
        a[i,0]=t*i;
    Qp=2*np.pi*4/3.0;
    for i in range(0,len(Qz)):
        a[i,3]=Qz[i]/Qp;
        a[i,2]=Qy[i];
        a[i,1]=Qx[i];
    cwd=os.getcwd();
    np.savetxt('SatFr_'+cwd.split('/')[-2]+'_'+cwd.split('/')[-1]+'.txt',a);


def FlowRateForS(t):
    cwd=os.getcwd();
    path=glob("*/");
    for i in path:
        os.chdir(i);
        satFlowRate(t);
        os.chdir(cwd);


