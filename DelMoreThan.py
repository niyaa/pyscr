#!/usr/bin/python
x=input('Enter file number higher than willbe trashed \n');
y=raw_input('Enter the * & format of file  \n');
z=0;
import os, glob,shutil;
for file in glob.glob(y):
	a=file.split('_')[1];
	b=float(a.split('.')[0]);
	if(os.path.isfile(file)):a=file.split
	if(b>x): 
		if(os.path.isfile(file)):(os.remove(file))
		else:
			shutil.rmtree(file);
