import os,sys;
import shutil;
import subprocess;
import numpy as np;
sys.path.append('/home/nyadav/pyscr');
import ipVar;
import funcs;
exe='~/nekNewton/dist/bin/IncNavierStokesSolver';
alpha=1;
rootPath='/home/nyadav/symm'#+'/'+str(alpha);
path=os.getcwd();
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
from glob import glob
simPath=os.getcwd();
Sval=path.split('/')[-1];
ipVar.editGeo(rootPath,simPath,alpha,float(Sval));
os.chdir(simPath);
subprocess.call("/tools/gmsh/2.9.2/bin/gmsh -2 -order 9 divConv2D.scr" ,shell=True);
subprocess.call("~/nekNewton/dist/bin/MeshConvert divConv2D.msh geom.xml",shell=True);
if not os.path.exists(os.getcwd()+'/b'):
    os.mkdir('b');
shutil.copy(rootPath+'/base.xml',os.getcwd()+'/b'); 
shutil.copy(simPath+'/geom.xml',os.getcwd()+'/b');
os.chdir(simPath+'/b');
filelist=['geom.xml','base.xml']; 
#funcs.incSolver(exe,filelist);

        
os.chdir(simPath);    
if not os.path.exists(os.getcwd()+'/d'):
    os.mkdir('d');

shutil.copy(rootPath+'/dist.xml',os.getcwd()+'/d'); 
shutil.copy(simPath+'/geom.xml',os.getcwd()+'/d');
os.chdir(simPath+'/d');
filelist=['geom.xml','dist.xml']; 
funcs.incSolver(exe,filelist);
os.chdir(simPath); 

if not os.path.exists(os.getcwd()+'/bd'):
    os.mkdir('bd');
shutil.copy(rootPath+'/bd.xml',os.getcwd()+'/bd'); 
shutil.copy(simPath+'/geom.xml',os.getcwd()+'/bd')
shutil.copy((simPath+'/b/geom_10.chk'),(os.getcwd()+'/bd'));
shutil.copy((simPath+'/d/geom_0.chk'),(os.getcwd()+'/bd'));
        
os.chdir(simPath+'/bd');
subprocess.call("mv geom_10.chk geom3D.bse",shell=True);
subprocess.call("mv geom_0.chk geom3D-dist.bse",shell=True);        
subprocess.call("~/nekNewton/dist/bin/FldAddFld 1 1e-9 geom3D.bse geom3D-dist.bse geomBplusD.fld ",shell=True);
fileList=['geom.xml','bd.xml'];
funcs.first(os.getcwd(),exe,fileList,1e-29,700,1200,1000)
funcs.bdexe(os.getcwd(),exe,fileList,1e-5,8);
       
    

