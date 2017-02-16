import numpy as np;
import os;
import xml.etree.ElementTree as ET;
def CheckEnergy(filename):
    
    
    energy = np.loadtxt(filename,skiprows=1);
    
    a=energy[-1,-1];
    if((a > 1e-6) or ( a < 1e-24)):   return 0;
    else: return 1;



        
    
    
