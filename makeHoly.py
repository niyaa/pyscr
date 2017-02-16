import os, sys, subprocess;
from case import *;
import numpy as np
import funcs;
sys.path.append('/home/nyadav/pyscr/');

def PreHoly(cpu,CurPath,FilePath):
    os.chdir(FilePath);
    case=Case();
    case.time, case.mod, case.energy = np.loadtxt('EnergyFile.mdl',  comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
    if(case.energy[-1]>1e-11):
        if os.path.exists(os.getcwd()+'/2'):
            os.chdir('2');
            FilePath=os.getcwd()+'geom.fld';
            case.time, case.mod, case.energy = np.loadtxt('EnergyFile.mdl',  comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
            En=case.energy[-1];
            f=np.sqrt(1e-9/En)*1e-4;
            print(f*f*En);
            subprocess.call(cpu+'FldAddFld 1 -1 geom.fld ../geom3D.bse geomMid.fld',shell=True);
            subprocess.call(cpu+'FldAddFld 1 '+str(f)+' ../geom3D.bse geomMid.fld geomHplusD.fld',shell=True);
            subprocess.call('rm geomMid.fld',shell=True);
            funcs.CopyFile(os.getcwd(),CurPath,['geom.xml','geomHplusD.fld']);
            os.chdir(CurPath);
        
        else:
            FilePath=os.getcwd()+'geom.fld';
            case.time, case.mod, case.energy = np.loadtxt('EnergyFile.mdl',  comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
            En=case.energy[-1];
            f=np.sqrt(1e-9/En)*1e-4;
            print(f*f*En);
            

            subprocess.call(cpu+'FldAddFld 1 -1 geom.fld geom3D.bse geomMid.fld',shell=True);
            subprocess.call(cpu+'FldAddFld 1 '+str(f)+' geom3D.bse geomMid.fld geomHplusD.fld',shell=True);
            subprocess.call('rm geomMid.fld',shell=True);
            funcs.CopyFile(os.getcwd(),CurPath,['geom.xml','geomHplusD.fld']);
            os.chdir(CurPath);    

    else:
        print("The disturnace have not fully evolved till now \n ");
