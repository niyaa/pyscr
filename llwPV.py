# -*- coding: utf-8 -*-

import sys

#sys.path.append('/home/niyaa/projects/ParaView-bin/lib');

#sys.path.append('/home/niyaa/projects/ParaView-bin/lib/site-packages')
sys.path.append('/home/llaniewski/TP/build/lib')
sys.path.append('/home/llaniewski/TP/build/lib/site-packages')

sys.path.append('/home/nyadav/anaconda2/lib/python2.7/site-packages')

import os
import numpy as np
import math
#import matplotlib.pyplot as plt
from paraview.simple import *
from paraview.numeric import fromvtkarray
from scipy import interpolate, optimize, integrate

from matplotlib.font_manager import FontProperties
from itertools import cycle
from matplotlib.lines import Line2D
markers = Line2D.filled_markers
print(markers)
#    lines = [4,5,6,7,"8",">","<","^","v","d","s"]
linecycler = cycle(markers)

def symmetry(filePath):
    print(filePath)
    inE = filePath
    geomvtu = XMLUnstructuredGridReader(FileName=[inE])
    geomvtu.PointArrayStatus = ['u', 'v', 'p']
    # create a new 'Slice'
    slice1 = Slice(Input=geomvtu)
    slice1.SliceType = 'Plane'
    slice1.SliceOffsetValues = [0.0]
    # init the 'Plane' selected for 'SliceType'
    xslice = math.pi / 0.5
    slice1.SliceType.Origin = [xslice, 0.0, 0.0]
    # to get the number of points on the plotoverline line
    pl = servermanager.Fetch(slice1)
    nbp = pl.GetNumberOfPoints()
    pos = fromvtkarray(pl.GetPoints().GetData())
    valsU = fromvtkarray(pl.GetPointData().GetScalars("u"))
    valsV = fromvtkarray(pl.GetPointData().GetScalars("v"))
    
    xn = [val[0] for val in pos]
    yn = [val[1] for val in pos]
    un = np.hstack([val for val in reversed(valsU)])
    vn = np.hstack([val for val in reversed(valsV)])
    
    fu = interpolate.interp1d(yn, un, 'cubic')
    fv = interpolate.interp1d(yn, vn, 'cubic')
    
#    print yn
#    print un
#    print integrate.quad(lambda x: np.abs(fu(x)-fu(-x)), yn[-1], yn[0])
#    print integrate.quad(lambda x: np.abs(fv(x)+fv(-x)), yn[-1], yn[0])

    marker = next(linecycler)
    line, = plt.plot(yn, un, marker=marker)
    line.set_label("$u_n$")
    
    marker = next(linecycler)
    line, = plt.plot(yn, vn, marker=marker)
    line.set_label("$v_n$")
    
#    plt.legend(fancybox=True, shadow=True, bbox_to_anchor=(1, 0.45))
#    plt.grid()
#    plt.show()
    
def calculateQ(filePath):
    print(filePath)
    inE = filePath
    geomvtu = XMLUnstructuredGridReader(FileName=[inE])
    geomvtu.PointArrayStatus = ['u', 'v', 'p']
    
    integrateVariables1 = IntegrateVariables(Input=geomvtu)
    a = integrateVariables1.PointData[0]
    print a
    print a.GetRange()[0]
    
    
    
