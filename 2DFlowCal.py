G -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 12:07:36 2016

@author: niyaa
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:46:40 2016

@author: niyaa
"""
import numpy as np;import os, sys;
from glob import glob;
import subprocess;
import funcs;
sys.path.append('/home/llaniewski/TP/build/lib')
sys.path.append('/home/llaniewski/TP/build/lib/site-packages')

sys.path.append('/home/nyadav/anaconda2/lib/python2.7/');
sys.path.append('/home/nyadav/pyscr/');


import math;
from decimal import Decimal;
import output;
from paraview.simple import *;
from paraview.numeric import fromvtkarray;
from scipy import interpolate, optimize, integrate;
import pickle;


#Conversion to
#VTK files using tachion
aPath=os.getcwd();
os.chdir(aPath);

path=glob('*/');
path.sort();
#with PdfPages('multipage_pdf.pdf') as pdf:
aaa=[];
for i in path:
    os.chdir(os.getcwd()+'/'+i);
    alpha=i.split('/')[0]
     
    path1=glob('0.*/');
    path1.sort();
    sPath=os.getcwd();
    for i in path1:
        os.chdir(i);
        os.chdir('b');
        print(os.getcwd());
        if not os.path.exists(os.getcwd()+'/geom1.vtu'):
            subprocess.call('rm geom.vtu',shell=True);
            subprocess.call('rm geom1.vtu',shell=True);
            arg='XmlToVtk geom.xml';
            subprocess.call(arg,shell=True);
            arg='mv geom.vtu geom1.vtu';
            subprocess.call(arg,shell=True);
        
        if not os.path.exists(os.getcwd()+'/geom.vtu'):
            i=funcs.MaxChk(os.getcwd());
            arg='FieldConvert geom.xml geom.fld geom.vtu';
            subprocess.call(arg,shell=True);
            print(os.getcwd())
        os.chdir(sPath);
    os.chdir(aPath);

aPath=os.getcwd();
os.chdir(aPath);

f=open('obejNew.p','wb');
path=glob('*/');
path.sort();
#with PdfPages('multipage_pdf.pdf') as pdf:
for i in path:
    os.chdir(os.getcwd()+'/'+i);
    alpha=i.split('/')[0]
     
    path1=glob('0.*/');
    path1.sort();
    sPath=os.getcwd();
    for i in path1:
        os.chdir(i);
        Sval=i.split('/')[0];
        out=output.Output();
        out.alpha.append(float(alpha));  
        out.S.append(float(Sval));
        os.chdir('b');
        inE=os.getcwd()+'/geom1.vtu';        
        geomvtu = XMLUnstructuredGridReader(FileName=[inE]);
        integrateVariables1 = IntegrateVariables(Input=geomvtu);
        ig=integrateVariables1.CellData[0]
        out.area.append(ig.GetRange()[0]);
        inE=os.getcwd()+'/'+'geom.vtu';
        geomvtu = XMLUnstructuredGridReader(FileName=[inE]);
        geomvtu.PointArrayStatus = ['u', 'v', 'w', 'p']
        slice1 = Slice(Input=geomvtu)
        slice1.SliceType = 'Plane'
        slice1.SliceOffsetValues = [0.0]
    # init the 'Plane' selected for 'SliceType'
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
        out.qz.append(qz);
        
        slice2=Slice(Input=slice1);
        slice2.SliceType = 'Plane'
        slice2.SliceOffsetValues = [0.0]
        # init the 'Plane' selected for 'SliceType'
        xslice = math.pi / 0.5
        slice2.SliceType.Origin = [xslice, 0.0, 0.0];
        slice2.SliceType.Normal=[0,1,0];
        slice2.SliceOffsetValues = [0.0];
        pl2 = servermanager.Fetch(slice2)
        nbp = pl2.GetNumberOfPoints()
        pos1 = fromvtkarray(pl2.GetPoints().GetData())
    
        valsW = fromvtkarray(pl2.GetPointData().GetScalars("w"));
        out.W=valsW;
        out.X=pos1[:,0];
        pickle.dump(out,f);        
        os.chdir(sPath);
    os.chdir(aPath);
f.close();

planeFr=2/3.0;


i=1;
f=open('obejNew.p','rb');
for i in range(0,1000):
    out=pickle.load(f);
    i=i+1;
    print(i)
f.close()


Nobj=i;
a=np.zeros((Nobj,5),dtype=np.float);
f=open('obejNew.p','rb');
for i in range(0,Nobj):
    out=pickle.load(f);
    a[i,0]=out.alpha[0];
    a[i,1]=out.S[0];
    a[i,2]=out.qz[0]/(out.area[0]*planeFr);
    a[i,3]=out.area[0];
    a[i,4]=out.qz[0];
f.close();
              
out.alpha=a[:,0];
out.S=a[:,1];
out.qz=a[:,2]

alpha=set(out.alpha);
S=set(out.S);



#calculate the length of the dumped object
i=1;
f=open('obejNew.p','rb');
for i in range(0,1000):
    out=pickle.load(f);
    i=i+1;
    print(i)
f.close()


area=[];S=[]; qz=[];
f=open('obejNew.p','rb');
for i in range(0,188):
    out=pickle.load(f);
    print(out.alpha);
    if(out.alpha[0]==1.0):
        print(out.alpha[0]);
        S.append(out.S[0]);
        area.append(out.area[0]);
        qz.append(out.qz[0]);
f.close();

    
 

for i in alpha:

    xx=out.S[out.alpha==i];
    yy=out.qz[out.alpha==i];
    
    
    
    
    

        
        out.Wmax.append(max(valsW));
        out.Wmin.append(min(valsW))
        out.Wdif.append(max(valsW)-min(valsW));
        print(os.getcwd());
        print(max(valsW));
        print(min(valsW));
        os.chdir(sPath);
        dv = (valsW[1:,0]-valsW[:-1,0])/(pos1[1:,0]-pos1[:-1,0])
        pos3 = (pos1[1:,0]+pos1[:-1,0])/2
        ddv = (dv[1:]-dv[:-1])/(pos3[1:]-pos3[:-1])
        linestyle=linestyles[1];l=0;
        line, = plt.plot(pos1[:-1,0], dv,linestyle,marker=markers[l],label='S='+str(Sval));
        marker = next(linecycler);l=l+1;
    
    #os.chdir(aPath);
    plt.legend(handler_map={line: HandlerLine2D(numpoints=2)}, scatterpoints = 1) 
    plt.title('Shear Stress along the symmetric line on xy plane \n for different corrugation amplitude, S  for alpha=1, beta=0.4');
    plt.ylabel('Shear Stress') ;   
    plt.xlabel('Spanwise coordinate , x');
    plt.grid()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(6.5,4)
    fig.savefig('uvelo.png',dpi=200)


plt.plot(out.S,out.Wdif,marker='o')
plt.title('Maximum variations in streamwise velocity along the \n symmetric line on xy plane for different corrugation amplitude, S \n for alpha=1, beta=0.4');
plt.ylabel('Max variations in streamwise velocity, S') ;   
plt.xlabel('Corrugation ampltude, S');
plt.grid()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.5,4)
fig.savefig('DiffU.png',dpi=200)


plt.plot(a,b,marker='o')
plt.title('Variations of flow rate in the stream wise direction for different corrugation amplitude, S \n for alpha=1, beta=0.4');
plt.ylabel('Flow rate') ;   
plt.xlabel('Corrugation ampltude, S');
plt.grid()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.5,4)
fig.savefig('flowrate.png',dpi=200)





aPath='/home/niyaa/Data/alpha/s/';
os.chdir(aPath);
out=output.Output();
path=glob('*/');
path.sort();
#with PdfPages('multipage_pdf.pdf') as pdf:
for i in path:
    os.chdir(os.getcwd()+'/'+i);
    alpha=i.split('/')[0]
      
    
    path1=glob('0.*/');
    path1.sort();
    sPath=os.getcwd();
    for j in path1:
        
        Sval=j.split('/')[0];
        if(Sval=='0.4'):
            os.chdir(j);
            out.alpha.append(float(alpha)); 
            print(os.getcwd());
   
            out.S.append(Decimal(Sval));
            os.chdir('b');
            i=funcs.MaxChk(os.getcwd());
            if(i==0):
                arg='FldToVtk geom.xml geom.fld';
                subprocess.call(arg,shell=True);
                inE=os.getcwd()+'/'+'geom.vtu';
            else:
                arg='FldToVtk geom.xml '+'geom_'+str(i)+'.chk';
                subprocess.call(arg,shell=True);    
                inE=os.getcwd()+'/'+'geom_'+str(i)+'.vtu';
            geomvtu = XMLUnstructuredGridReader(FileName=[inE]);
            geomvtu.PointArrayStatus = ['u', 'v', 'w', 'p']
            slice1 = Slice(Input=geomvtu)
            slice1.SliceType = 'Plane'
            slice1.SliceOffsetValues = [0.0]
        # init the 'Plane' selected for 'SliceType'
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
            out.qz.append(qz);
            
    #os.chdir(aPath)      
            slice2=Slice(Input=slice1);
            slice2.SliceType = 'Plane'
            slice2.SliceOffsetValues = [0.0]
            # init the 'Plane' selected for 'SliceType'
            xslice = math.pi / 0.5
            slice2.SliceType.Origin = [xslice, 0.0, 0.0];
            slice2.SliceType.Normal=[0,1,0];
            slice2.SliceOffsetValues = [0.0];
            pl2 = servermanager.Fetch(slice2)
            nbp = pl2.GetNumberOfPoints()
            pos1 = fromvtkarray(pl2.GetPoints().GetData())
        
            valsW = fromvtkarray(pl2.GetPointData().GetScalars("w"));
         
            out.Wmax.append(max(valsW));
            out.Wmin.append(min(valsW))
            out.Wdif.append(max(valsW)-min(valsW));
            print(os.getcwd());
            print(max(valsW));
            print(min(valsW));
            os.chdir(sPath);
            dv = (valsW[1:,0]-valsW[:-1,0])/(pos1[1:,0]-pos1[:-1,0])
            pos3 = (pos1[1:,0]+pos1[:-1,0])/2
            ddv = (dv[1:]-dv[:-1])/(pos3[1:]-pos3[:-1])
            linestyle=linestyles[1];l=0;
            line, = plt.plot(pos1[:,0],valsW,linestyle,marker=markers[l],label='alpha='+str(alpha));
            marker = next(linecycler);l=l+1;
    
    os.chdir(aPath);
plt.legend(handler_map={line: HandlerLine2D(numpoints=2)}, scatterpoints = 1) 
plt.title('Stream wise velocity component along the symmetric line on xy plane \n for different alpha ,for S=0.4, beta=0.4');
plt.ylabel('Stream wise velocity') ;   
plt.xlabel('Spanwise coordinate , x');
plt.grid()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(20,4)
fig.savefig('veloc.png',dpi=200)
    
    
l2, l1 = zip(*sorted(zip(out.alpha, d)))
out.alpha=list(l2);out.Wdif =list(l1);
plt.plot(out.alpha,c,marker='o')
plt.title(' (Wmax-Wmin) on xy plane for different alpha, for S=0.4, beta=0.4');
plt.ylabel('Wmax-Wmin/Wmax') ;   
plt.xlabel('alpha');
plt.grid()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(8,5.85)
fig.savefig('DiffU.png',dpi=200)


l2, l1 = zip(*sorted(zip(out.qz, out.alpha)))
out.alpha=list(l1);out.qz =list(l2);
plt.plot(out.alpha,out.qz,marker='o')
plt.title('Variations of flow rate in the stream wise direction for different alpha \n for S=0.4, beta=0.4');
plt.ylabel('Flow rate') ;   
plt.xlabel('alpha');
plt.grid()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.5,4)
fig.savefig('flowrate_for_alpha.png',dpi=200)



