from glob import glob;
import os;
import ipVar;
import numpy as np;
from scipy.interpolate import UnivariateSpline;
cwd=os.getcwd();
S=[];bCr=[];
path=glob("*/");
for k in path:
    os.chdir(k);
    path1=glob("*/");
    cwd1=os.getcwd();
    bb=[];aa=[];cc=[];
    for i in path1:
        os.chdir(i);
        mdl=glob("*.mdl");
        if(len(mdl)>5):
            [a,b]=ipVar.poptFile(os.getcwd());
        if(len(a)>5):
            for j in a:
                c=[j for j in a if j>0];
        if(len(c)>0):
            c=min(c);aa.append(c);c=np.where(a==c);
            bb.append(b[c[0]]);
            cc.append(float(i.split('/')[0]));
        os.chdir(cwd1);
    if(len(bb)>2):
        l2, l1 = zip(*sorted(zip(cc,bb)));
        cc=list(l2);bb=list(l1);
        f=UnivariateSpline(cc,bb,k=2);
        cc=np.linspace(min(cc),max(cc),1000);
        bb=f(cc);
        MIN=min(bb);
        ll=[l for l,m in enumerate(bb) if m==MIN];
        bCr.append(cc[ll][0]);
        S.append(float(k.split('/')[0]));
    os.chdir(cwd);
c=(S,bCr);
c=np.asarray(c);

np.savetxt(cwd.split('/')[-1],c.T);

#cc is beta  and bb is Re
def MinumCal(cc,bb):
    l2, l1 = zip(*sorted(zip(cc,bb)));
    cc=list(l2);bb=list(l1);
    f=UnivariateSpline(cc,bb,k=2);
    cc=np.linspace(min(cc),max(cc),1000);
    bb=f(cc);
    MIN=min(bb);
    ll=[l for l,m in enumerate(bb) if m==MIN];
    return cc[ll][0];
