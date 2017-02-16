import os;
def main(path):
    count=1;
    for roots, dirs, files in os.walk(path):
	for i in files:
	    
            os.rename(os.path.join(root,i),os.path.join(root,"geom_"+str(count)+".chk";
	    count+=1;
    
