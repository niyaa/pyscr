import subprocess;
import readline
readline.parse_and_bind("tab: complete");
import sys,os;
sys.path.append('/home/nyadav/pyscr/');
print('Enter the name of the geom file \n');
file1=raw_input('-->');
print('if filed file name is same as geom enter y else enter name without extension and Number\n');
file2=raw_input('-->');
if(file2=='y'):
    file2=file1;
    file2=file2.split('.')[0]
print('Enter the number of fld files to convert \n');
N=raw_input('-->');
N=int(N);
for i in range(0,N+1):
    args='FieldConvert '+str(file1)+' '+str(file2)+'_'+str(i)+'.fld '+str(file2)+'_'+str(i)+'.vtu';
    subprocess.call(args,shell=True);

