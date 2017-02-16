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
        a=[];
        [a,b]=ipVar.nsFile(os.getcwd());
        f=interpolate.interp1d(a,b);
        xnew=np.linspace(min(a),max(a),10000);
        ynew=f(xnew);
        ReMin.append(min(ynew));
        m=min(ynew);
        index=[k for k, j in enumerate(ynew) if j == m]
        index=index[0];
        betaLoc.append(xnew[index]);


    except:
        print('not defined');
        print(os.getcwd());
        if(len(a)>1):
            [a,b]=ipVar.nsFile(os.getcwd());
            f=interpolate.interp1d(a,b);
            xnew=np.linspace(min(a),max(a),10000);
            ynew=f(xnew);
            ReMin.append(min(ynew));
            m=min(ynew);
            index=[k for k, j in enumerate(ynew) if j == m]
            index=index[0];
            betaLoc.append(xnew[index]);

    os.chdir(cwd);
if(len(ReMin)>1):
    l1, l2, l3 = zip(*sorted(zip(S, ReMin,betaLoc)));
    S=list(l1);ReMin=list(l2);betaLoc=list(l3);
    c=(S,ReMin,betaLoc);
    c=np.asarray(c);
    np.savetxt('ReMinS.txt',c.T);
