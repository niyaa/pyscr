from decimal import Decimal;
from glob import glob;
import sys, os;
sys.path.append('/home/nyadav/pyscr/');
import ipVar;
import numpy as np;
import ipVar;
from output import *;
import xlsxwriter;
from output import *;
out=Output();

def paramAna(fileName):
    workbook=xlsxwriter.Workbook(fileName);
    worksheet=workbook.add_worksheet();

    out=Output();
    for root, dir, files in os.walk("./"):
        for file in files:
            if (file.endswith(".mdl")and not root.split('/')[-1] == "b"):
                print(file);
                inE=os.path.join(root, file)
                out.Re.append(Decimal(root.split('/')[-1]));
                out.beta.append(Decimal(root.split('/')[-2]));
                out.alpha.append(Decimal(root.split('/')[-3]));
                [popt, perr]=ipVar.popt(inE);
                out.sigma.append(popt[1]/2.0); 
            
    n=len(out.Re);
    x=np.zeros((n,4),dtype=np.float)
    x[:,0]=out.alpha[:];
    x[:,1]=out.beta[:];
    x[:,2]=out.Re[:];
    x[:,3]=out.sigma[:];

    row=0;
    col=0;
    for i in range(0,len(out.Re)):
        worksheet.write(row,col,x[row,col]);
        worksheet.write(row,col+1,x[row,col+1]);
        worksheet.write(row,col+2,x[row,col+2]);
        worksheet.write(row,col+3,x[row,col+3]);
    workbook.close();

    
def ns(fileName,a,b):
    workbook=xlsxwriter.Workbook(fileName);
    worksheet=workbook.add_worksheet();
           
    n=len(a);
    x=np.zeros((n,2),dtype=np.float)
    x[:,0]=a;
    x[:,1]=b;

    row=0;
    col=0;
    for i in range(0,len(a)):
        worksheet.write(row,col,x[row,col]);
        worksheet.write(row,col+1,x[row,col+1]);
        row+=1;
    workbook.close();

def ns4diffs(filename,alpha,betaList):
    cwd=os.getcwd();
    for i in betaList:
        pathA=cwd+'/'+str(i);
        os.chdir(pathA);
        [a,b]=ipVar.nsvalues(os.getcwd());
        fileName='ns.'+str(alpha)+'.'+str(i)+'.'+filename+'.xlsx'
        ns(fileName,a,b);
        os.chdir(cwd);

def nstxt(betaList):
    cwd=os.getcwd();
    for i in betaList:
        pathA=cwd+'/'+str(i);
        os.chdir(pathA);
        [a,b]=ipVar.nsvalues(os.getcwd());
        c=(a,b);
        d=np.asarray(c);
        np.savetxt('ns'+str(i)+'.txt',d.T);
        os.chdir(cwd);

