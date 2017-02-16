

import os;

import pickle;
import ipVar;



path='set the path'


os.chdir(path);
a=1
if not os.path.exists(str(a)):
	os.makedirs(str(a));
pathA=path+'/'+str(a);
os.chdir(pathA);
s=0.4;
if not os.path.exists(str(s)):
	os.makedirs(str(s));
pathS=pathA+'/'+str(s);
os.chdir(pathS);
beta=[0.2];
for b in beta:
    if not os.path.exists(str(b)):
        os.makedirs(str(b));
    pathB=pathS+'/'+str(b);
    os.chdir(pathB);



    ReList=[40,60,80,100,120,140,160,180,200,220,240];
    
    ipVar.ReSimulation(ReList);            
    os.chdir(pathB);
    [re,t1,t2]=ipVar.sigma(pathB);
    NewRe=[];
    for i in ReList:
        if(abs(i-re)<10):NewRe.append(re);NewRe.append(re-2);NewRe.append(re+2);
    ipVar.ReSimulation(NewRe);
    ReList=NewRe+ReList;
    [ReCr,t1,t2]=ipVar.sigma(pathB);
    fileName=str(ReCr)+'.cr';
    fileObject=open(fileName,'rb');c=[t1,t2];
    pickle.dump(c,fileObject);
    fileObject.close();
	
	
	
		
		
                  
#subprocess.call("exit",shell=True);


	
















	


