i=int(raw_input("Enter the mode whose differentiation is required \n"));

case=Case();
case.time,case.mod,case.energy = np.loadtxt(file1, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True)
if(case.time[0] > 100):N1=case.time[0]; case.time[0::2]=case.time[0::2]-N1;case.time[1::2]=case.time[1::2]-N1;
myset = set(case.mod)
modlist=list(myset)

t=case.time[(case.mod==i)]
E=case.energy[(case.mod==mod)]
d1=np.diff(E,x=1);
print\

