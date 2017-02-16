from MonkeyPatch import *;
import xml.etree.ElementTree as ET;




class IpParameter(object):
    """A simple example class"""
    def __init__(self):
        self.FT = 0 #Final time
        self.TS = 0 #Time steps    
        self.IO = 0 # IO_CheckSteps
        self.Re = 0 # Reynolds Number
        self.HZ = 0 # Homozenous MOdes
        self.LZ = 0 # lenght in z direction
        self.ChkN = 0 # writing interval 
    

    def ConPara(self,fileName):
        tree=ET.parse(fileName);
        root=tree.getroot();
        
        #HomModes in Z direction
        a=root[1][1][7].text;
        a=a.split('=');
        a=a[1];
        self.HZ=float(a);
       
        #LZ length in Z direction
        a=root[1][1][8].text;
        a=a.split('=');
        a=a[1];
        self.LZ=float(a);            
    
        #Reynolds number
        a=root[1][1][5].text;
        a=a.split('=');
        a=a[1];
        self.RE=float(a);
    
    	#Final Time
        a=root[1][1][1].text;
        a=a.split('=');
        a=a[1];
        self.FT=float(a);
    
    	#CheckSteps
        a=root[1][1][3].text;
        a=a.split('=');
        a=a[1];
        self.IO=float(a);
    
    	#TimeStep]
        a=root[1][1][0].text;
        a=a.split('=');
        a=a[1];
        self.TS=float(a);
        ChkN=self.FT/(self.TS*self.IO);
        self.ChkN=int(ChkN);
        return self.FT, self.TS, self.IO, self.RE, self.ChkN, self.HZ, self.LZ;
