import os;
from scipy import interpolate;
path=glob("*/");

cwd=os.getcwd();
S=[];
ReMin=[];
betaLoc=[];
for i in path:
    os.chdir(i);
    S.append(float(i.split('/')[0]));
    try:
        [a,b]=ipVar.nsvalues(os.getcwd());
        f=interpolate.interp1d(b,a);
        xnew=np.linspace(min(b),max(b),10000);
        ynew=f(xnew);
        ReMin.append(min(ynew));
        m=min(ynew);
        index=[k for k, j in enumerate(ynew) if j == m]
        index=index[0];
        betaLoc.append(xnew[index]);


    except:
        print('not defined');
        print(os.getcwd());


    os.chdir(cwd);

l1, l2, l3 = zip(*sorted(zip(S, ReMin,betaLoc)));
S=list(l1);ReMin=list(l2);betaLoc=list(l3);
c=(S,ReMin,betaLoc);
c=np.asarray(c);
np.savetxt('ReMinS.txt',c.T);
