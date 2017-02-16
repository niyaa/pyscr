# -*- coding: utf-8 -*-

from case import Case
from tools import *

import numpy as np
from itertools import groupby
from scipy import interpolate, optimize
from scipy.interpolate import griddata

from itertools import cycle

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from decimal import Decimal

markers = Line2D.filled_markers
#print(markers)
#    lines = [4,5,6,7,"8",">","<","^","v","d","s"]
linecycler = cycle(markers)

def makePlots(caseList):
    '''
    Makes plots of energy as a function of time
    Normally called only for verification and debugging
    '''
    caseList.sort(key=lambda l: l.alfa)
    for key, group in groupby(caseList, lambda x: x.alfa):
        alist = list(group)
        print( " For alfaa " + str(alist[0].alfa))
        alist.sort(key=lambda l: l.mu)
        for key, group in groupby(alist, lambda x: x.mu):
            blist = list(group)
            print( " For mu " + str(blist[0].mu))
            blist.sort(key=lambda l: l.S)
            for key, group in groupby(blist, lambda x: x.S):
                plt.figure(key, (16,9), 300)
                a=list(group)
                print( " For S " + str(a[0].S))
                a.sort(key=lambda l: l.Re)
            
                for i, icase in enumerate(a, 1):
                    print("S %f Re %f." % (icase.S, icase.Re))
                             
                    ax = plt.subplot(1, 1, i)
                    line, = plt.plot(icase.time[(icase.mod==1)], icase.energy[(icase.mod==1)])
                    plt.setp(line, linestyle='--')
                    plt.xlabel('')
                    plt.ylabel('Energy')
                    plt.title(icase.Name)
                    plt.yscale('log')
                    
                    popt = icase.popt
                    perr = icase.perr
                    if popt!=None:
                        ee=func(icase.t, *popt)
                        line, = plt.plot(icase.t, ee)
                        plt.setp(line, linewidth=2, color='r')
#                        textstr = '$%.5e \cdot \exp(%.5e x), E=%.5e$, $\sigma=$%.5e'%(popt[0], popt[1], perr, icase.sigma)
                        textstr = '$%.5e \cdot \exp(%.5e x), E=%.5e$, $\sigma=$%.5e, popt[1]/2=%.5e '%(popt[0], popt[1], perr, icase.sigma, popt[1]*0.5)
                        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
                        
                    
                filename =  "a"+str(a[0].alfa)+"_mu"+str(a[0].mu) +"_s"+ str(a[0].S) + ".png"
                plt.savefig(filename)
                plt.clf()
                #plt.show()

from xlrd import open_workbook
import xlwt
def plotSigmaMu(caseList):
    '''
    Produces a set of plots sigma(mu) for all Re for a given alfa
    Also tries to find the max(sigma(mu))
    '''
    caseList.sort(key=lambda l: l.S)
    
    book = xlwt.Workbook()
    sh = book.add_sheet("a" + str(caseList[0].alfa) + "_Sig_mu")
    col=0
    newCol=False
    for key, group in groupby(caseList, lambda x: x.S):
        row=0
        if newCol: col+=3
        newCol=False
        fig = plt.figure(0, (10,10), 100)
        ax = plt.subplot(111)
        plt.xlabel('$\mu$')
        plt.ylabel('$\sigma$', rotation = 0)
        
        alist = list(group)
#        print( " For S " + str(alist[0].S))
        alist.sort(key=lambda l: l.Re)
        mu=[]
        sig=[]
        for key, group in groupby(alist, lambda x: x.Re):
            blist = list(group)
#            print( " For Re " + str(blist[0].Re))
            
            marker = next(linecycler)
            blist.sort(key=lambda l: l.mu)
            x = np.array([float(icase.mu) for icase in blist])
            y = np.array([icase.sigma for icase in blist])
            
            if max(y)>0:
                sh.write(row, col, "S ")
                sh.write(row, col+1, alist[0].S)
                row+=1
                sh.write(row, col, "Re ")
                sh.write(row, col+1, blist[0].Re)
                row+=1
                for i in range(0,len(x)):
                    sh.write(row, col, x[i])
                    sh.write(row, col+1, y[i])
                    row+=1
                newCol=True
            
            xnew = np.linspace(x[0], x[-1], num=100, endpoint=True)
            if len(x)>3:
#                f=interpolate.UnivariateSpline(x, y)
                f=interpolate.interp1d(x, y, kind='cubic')
                line, = plt.plot(xnew, f(xnew))
                line, = plt.plot(x, y, marker=marker, color=line.get_color(), linestyle='None')
#                f2 = interpolate.UnivariateSpline(x, -y)
                f2=interpolate.interp1d(x, -y, kind='cubic')
            elif len(x)==3:
                f=interpolate.interp1d(x, y, kind='quadratic')
                line, = ax.plot(xnew, f(xnew), marker=marker,markevery=10)
                f2 = interpolate.interp1d(x, -y, kind='quadratic')
            else:
                f=interpolate.interp1d(x, y, kind='slinear')
                line, = ax.plot(xnew, f(xnew), marker=marker,markevery=10)
                f2 = interpolate.interp1d(x, -y, kind='slinear')
            line.set_label("S "+str(blist[0].S) + " Re " + str(blist[0].Re))
            
            try:
                initmu=x[y==max(y)]
                mumax=optimize.fmin(f2, initmu, maxiter=10000, disp=False)
                sigax=f(mumax)
                mu.append(mumax[0])
                sig.append(sigax[0])
            except:
#                print ("No Solution for: ", alist[0].S, blist[0].Re)
                continue            
#        print mu, sig
        line, = ax.plot(mu, sig)
        fontP = FontProperties()
        fontP.set_size('small')

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, 0.99*box.width, box.height])

        plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
        ax.grid()
        fig.set_size_inches(20, 10.5)
        fig.savefig("sig_mu_S"+str(alist[0].S)+".png", dpi=200)
#        plt.show()
        fig.clf()
    book.save("out.dat")
        
def plotSigmaRe(caseList):
    '''
    Plots sigma(Re) for all mu, for a given alfa
    '''
    caseList.sort(key=lambda l: l.S)
    for key, group in groupby(caseList, lambda x: x.S):
        fig = plt.figure(0, (10,10), 100)
        ax = plt.subplot(111)
        plt.xlabel('$Re$')
        plt.ylabel('$\sigma$', rotation = 0)
        
        alist = list(group)
        print( " For S " + str(alist[0].S))
        alist.sort(key=lambda l: l.mu)
        for key, group in groupby(alist, lambda x: x.mu):
            blist = list(group)
            print( " For mu " + str(blist[0].mu))
            
            blist.sort(key=lambda l: l.Re)
            x = [icase.Re for icase in blist]
            y = [icase.sigma for icase in blist]

            marker = next(linecycler)
            line, = ax.plot(x, y, marker=marker,markevery=1)
            line.set_label("S "+str(blist[0].S) + " mu " + str(blist[0].mu))
            
            
        fontP = FontProperties()
        fontP.set_size('small')

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, 0.99*box.width, box.height])

        plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
        ax.grid()
        fig.set_size_inches(20, 10.5)
        fig.savefig("sig_Re_S"+str(alist[0].S)+".png", dpi=200)
#        plt.show()
        fig.clf()

# caclulates and returns a touple (S, sig) for a given Re
def getSig_S(caseList, Re=0):
    '''
    caclulates and returns a touple (S, sig) for a given Re
    Re>0 gets only values for the given Re
    Otherwise all Re are used
    '''
    if Re>0: #get only the given Re
        alist = filter(lambda l: float(l.Re)==float(Re), caseList)
    else:
        alist = caseList
    
    alist.sort(key=lambda l: l.S)
#    print "\n============================="
#    print" For Re %s, min S %s, max S %s" % ( str(alist[0].Re), str(alist[0].S), str(alist[-1].S))
    s=[]
    sig=[]
    for key, group in groupby(alist, lambda x: x.S):
        blist = list(group)
#            print( " For S " + str(blist[0].S))
        x = np.array([float(icase.mu) for icase in blist])
        y = np.array([icase.sigma for icase in blist])
#        print "S=%f, Re=%f"  % (blist[0].S, blist[0].Re)
        if len(x)>3:
            f1=interpolate.interp1d(x, y, kind='cubic')
            f2=interpolate.interp1d(x, -y, kind='cubic')
        elif len(x)>2:
            f1=interpolate.interp1d(x, y, kind='quadratic')
            f2=interpolate.interp1d(x, -y, kind='quadratic')
        elif len(x)>1:
            f1=interpolate.interp1d(x, y, kind='linear')
            f2=interpolate.interp1d(x, -y, kind='linear')
        else:
            continue
        
        try:
            mumu=x[y==max(y)]
#                0.5*(x[0]+x[-1])
            mumax=optimize.fmin(f2, mumu, maxiter=100000, maxfun=100000, disp=False)
            sigax=f1(mumax)[0]
            sig.append(sigax)            
            s.append(float(blist[0].S))
        except Exception as error:
#            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'        
#            print 'Caught this error: ' + repr(error)
#            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' 
#            print "No Solution for getting max: %f %f" % (alist[0].S, blist[0].Re)
            sigax=max(y)
            sig.append(sigax)
            s.append(float(blist[0].S))
            continue                          
    return (s, sig)
    
def getSig_Re(caseList, S=0):
    '''
    caclulates and returns a touple (Re, sig) for a given S
    S>0 gets only values for the given Re
    Otherwise all S are used
    '''
    if S>0: #get only the given Re
        alist = filter(lambda l: float(l.S)==S, caseList)
    else:
        alist = caseList
    
    alist.sort(key=lambda l: l.Re)
#    print "\n=============================", len(alist), len(caseList), S
#    print" For Re %s, min S %s, max S %s" % ( str(alist[0].Re), str(alist[0].S), str(alist[-1].S))
    re=[]
    sig=[]
    for key, group in groupby(alist, lambda x: x.Re):
        blist = list(group)
#            print( " For S " + str(blist[0].S))
        x = np.array([float(icase.mu) for icase in blist])
        y = np.array([icase.sigma for icase in blist])
#        print "S=%f, Re=%f"  % (blist[0].S, blist[0].Re)
        if len(x)>3:
            f1=interpolate.interp1d(x, y, kind='cubic')
            f2=interpolate.interp1d(x, -y, kind='cubic')
        elif len(x)>2:
            f1=interpolate.interp1d(x, y, kind='quadratic')
            f2=interpolate.interp1d(x, -y, kind='quadratic')
        elif len(x)>1:
            f1=interpolate.interp1d(x, y, kind='linear')
            f2=interpolate.interp1d(x, -y, kind='linear')
        else:
            continue
        
        try:
            mumu=x[y==max(y)]
#                0.5*(x[0]+x[-1])
            mumax=optimize.fmin(f2, mumu, maxiter=100000, maxfun=100000, disp=False)
            sigax=f1(mumax)[0]
            sig.append(sigax)            
            re.append(float(blist[0].Re))
        except Exception as error:
#            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'        
#            print 'Caught this error: ' + repr(error)
#            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' 
#            print "No Solution for getting max: %f %f" % (alist[0].S, blist[0].Re)
            sigax=max(y)
            sig.append(sigax)
            re.append(float(blist[0].Re))
            continue                    
        
    return (re, sig)

def calculateSigmaForS(caseList, S, Re):
    '''
    Calculate sigma for a given S, Re using interpolation in the direction of Re
    '''
    re, sig = getSig_Re(caseList, S)
    f=interpolate.InterpolatedUnivariateSpline(re, sig, k=1)
    return float(f(float(Re)))

def extra_a3():
    '''
    Just for testing. Prints some missing data for the a3 meandering case
    '''
    #extra manual ...
    if float(alist[0].Re) == 1900:
        ssig = calculateSigmaForS(caseList, 0.025, 1900)
        s.insert(1, 0.025)
        sig.insert(1, ssig)
        print ssig
        
    #extra manual ...
    if float(alist[0].Re) == 1500:
        ssig = calculateSigmaForS(caseList, 0.025, 1500)
        s.insert(1, 0.025)
        sig.insert(1, ssig)
        print ssig
   
def calcSLowUpMax(caseList):
    caseList.sort(key=lambda l: l.Re)
    S = [0.01, 0.025, 0.04, 0.055, 0.07, 0.085, 0.1, 0.115, 0.13, 0.145, 0.16, 0.175, 0.19, 0.205, 0.22, 0.235, 0.25]
    Re= np.linspace(300, 2500, num=12, endpoint=True)
    out=[]
    
    book = xlwt.Workbook()
    sh = book.add_sheet("a" + str(caseList[0].alfa) + "_Sig_S")
    col=0
    newCol=False
    for key, group in groupby(caseList, lambda x: x.Re):
        row=0
        if newCol: col+=3
        newCol=False    
    
        alist = list(group)        
        s, sig = getSig_S(alist)
        
        i=0
        if s[0] > S[0]:
            for ss in S:
                if ss in s:
                    break
                s.insert(i, ss)
                sig.insert(i, calculateSigmaForS(caseList, ss, alist[0].Re))
                i=i+1
                
        if s[-1] < S[-1]:
            for ss in S:
                if ss not in s: continue
                if ss <= s[-1]:
                    continue
                else:
#                    print ss, alist[0].Re
                    s.insert(len(s), ss)
                    sig.insert(len(sig), calculateSigmaForS(caseList, ss, alist[0].Re))
#                    print s, sig
        
        if float(alist[0].alfa) == 3:    
            #extra manual ...
            if float(alist[0].Re) == 1900:
                ssig = calculateSigmaForS(caseList, 0.025, 1900)
                s.insert(1, 0.025)
                sig.insert(1, ssig)
#                print ssig
                
            #extra manual ...
            if float(alist[0].Re) == 1500:
                ssig = calculateSigmaForS(caseList, 0.025, 1500)
                s.insert(1, 0.025)
                sig.insert(1, ssig)
#                print ssig
        
        if max(sig) > 0:
            sh.write(row, col, "Re ")
            sh.write(row, col+1, alist[0].Re)
            row+=1
            for i in range(0,len(s)):
                sh.write(row, col, s[i])
                sh.write(row, col+1, sig[i])
                row+=1
            newCol=True
        
        marker = next(linecycler)
        snew = np.linspace(s[0], s[-1], num=100, endpoint=True)
        f1=interpolate.interp1d(s, sig, kind='cubic')
        f2=interpolate.interp1d(s, -np.array(sig), kind='cubic')
        line, = plt.plot(snew, f1(snew))
        line, = plt.plot(s, sig, marker=marker, color=line.get_color(), linestyle='None')                        
        line.set_label("Re "+str(alist[0].Re))
        
        #This Part looks for S_low, S_high, and S_max
        #look for the S crit
        if max(sig) > 0:
            case = Case()
            case.alfa=alist[0].alfa
            case.Re=alist[0].Re
            smax=0
            s_l=0
            s_u=0
            try:
                ss = 0.5*(s[0]+s[-1])
                smax=optimize.fmin(f2, ss, maxiter=100000, maxfun=100000, disp=False)[0]
                sigmax=f1(smax)
                plt.scatter(smax,sigmax)
            except Exception as error:
                smax=0
            
            if sig[-1] < 0: # there are two roots
                s_m = 0.1
                s_l = optimize.brentq(f1, s[0], s_m)
                s_u = optimize.brentq(f1, s_m, s[-1])
                plt.scatter(s_l,f1(s_l))
                plt.scatter(s_u,f1(s_u))
                print alist[0].Re, s_l, s_u, smax
            else: #there is one root
#                print alist[0].Re, max(sig)
                s_l = optimize.brentq(f1, s[0], s[-1])
                plt.scatter(s_l,f1(s_l))
                print alist[0].Re, s_l, smax
            case.smax=smax
            case.s_l=s_l
            case.s_u=s_u
            out.append(case)
       
    fontP = FontProperties()
    fontP.set_size('small')
    
    plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
    plt.grid()
    plt.show()
    book.save("out.dat")
    return out

def printS_LUM_alfaRe(caseList):
    caseList.sort(key=lambda l: l.alfa)
    print "aRe ,",
    for re in range(500, 2501, 200):
            print re, ",",
    print ""
    print "SL"
    for key, group in groupby(caseList, lambda x: x.alfa):
        alist = list(group)
        print alist[0].alfa, ",",
        for re in range(500, 2501, 200):
            blist = filter(lambda l: float(l.Re)==re, alist)
            if len(blist)>0:
                print blist[0].s_l, ",",
            else:
                print " ", ",",
        print ""
    print "SU"
    for key, group in groupby(caseList, lambda x: x.alfa):
        alist = list(group)
        print alist[0].alfa, ",",
        for re in range(500, 2501, 200):
            blist = filter(lambda l: float(l.Re)==re, alist)
            if len(blist)>0:
                print blist[0].s_u, ",",
            else:
                print " ", ",",
        print ""
    print "SM"
    for key, group in groupby(caseList, lambda x: x.alfa):
        alist = list(group)
        print alist[0].alfa, ",",
        for re in range(500, 2501, 200):
            blist = filter(lambda l: float(l.Re)==re, alist)
            if len(blist)>0:
                print blist[0].smax, ",",
            else:
                print " ", ",",
        print ""
        

#Get Smin and Smax, extrapolates if necessary
def plotMaxSigmaS_extrapolateFromRe(caseList):
    caseList.sort(key=lambda l: l.Re)
    S = [0.01, 0.025, 0.04, 0.055, 0.07, 0.085, 0.1, 0.115, 0.13, 0.145, 0.16, 0.175, 0.19, 0.205, 0.22, 0.235, 0.25]
#    S = [0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
    Re= np.linspace(500, 2500, num=12, endpoint=True)
    
    book = xlwt.Workbook()
    sh = book.add_sheet("a" + str(caseList[0].alfa) + "_Sig_S")
    col=0
    newCol=False
    for key, group in groupby(caseList, lambda x: x.Re):
        row=0
        if newCol: col+=3
        newCol=False    
    
        alist = list(group)
        s, sig = getSig_S(alist)
        
        i=0
        if s[0] > S[0]:
            for ss in S:
                if ss in s:
                    break
                s.insert(i, ss)
                sig.insert(i, calculateSigmaForS(caseList, ss, alist[0].Re))
                i=i+1
                
        if s[-1] < S[-1]:
            for ss in S:
                if ss <= s[-1]:
                    continue
                else:
#                    print ss, alist[0].Re
                    s.insert(len(s), ss)
                    sig.insert(len(sig), calculateSigmaForS(caseList, ss, alist[0].Re))
#                    print s, sig
        
        if float(alist[0].alfa) == 3:    
            #extra manual ...
            if float(alist[0].Re) == 1900:
                ssig = calculateSigmaForS(caseList, 0.025, 1900)
                s.insert(1, 0.025)
                sig.insert(1, ssig)
#                print ssig
                
            #extra manual ...
            if float(alist[0].Re) == 1500:
                ssig = calculateSigmaForS(caseList, 0.025, 1500)
                s.insert(1, 0.025)
                sig.insert(1, ssig)
#                print ssig
        
        if max(sig) > 0:
            sh.write(row, col, "Re ")
            sh.write(row, col+1, alist[0].Re)
            row+=1
            for i in range(0,len(s)):
                sh.write(row, col, s[i])
                sh.write(row, col+1, sig[i])
                row+=1
            newCol=True
        
        marker = next(linecycler)
        snew = np.linspace(s[0], s[-1], num=100, endpoint=True)
        f1=interpolate.interp1d(s, sig, kind='cubic')
        f2=interpolate.interp1d(s, -np.array(sig), kind='cubic')
        line, = plt.plot(snew, f1(snew))
        line, = plt.plot(s, sig, marker=marker, color=line.get_color(), linestyle='None')                        
        line.set_label("Re "+str(alist[0].Re))
        
        #This Part looks for S_low, S_high, and S_max
        #look for the S crit
        if max(sig) > 0:
            try:
                ss = 0.5*(s[0]+s[-1])
                smax=optimize.fmin(f2, ss, maxiter=100000, maxfun=100000, disp=False)[0]
                sigmax=f1(smax)
                plt.scatter(smax,sigmax)
            except Exception as error:
                smax=0
            
            if sig[-1] < 0: # there are two roots
                s_m = smax
                s_l = optimize.brentq(f1, s[0], s_m)
                s_u = optimize.brentq(f1, s_m, s[-1])
                plt.scatter(s_l,f1(s_l))
                plt.scatter(s_u,f1(s_u))
                print alist[0].Re, s_l, s_u, smax
            else: #there is one root
#                print alist[0].Re, max(sig)
                s_l = optimize.brentq(f1, s[0], s[-1])
                plt.scatter(s_l,f1(s_l))
                print alist[0].Re, s_l, smax
       
    fontP = FontProperties()
    fontP.set_size('small')
    
    fig = plt.figure(0, (10,10), 100)
    ax = fig.add_subplot(111)
    plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
    plt.grid()
    fig.set_size_inches(20, 10.5)
    fig.savefig("alfa" + str(caseList[0].alfa) + "_maxSig_S.png", dpi=200)
#        plt.show()
    fig.clf()
    book.save("out.dat")

def plotMaxSigmaS(caseList):
    caseList.sort(key=lambda l: l.Re)
    S=[]
    Re=[]
    Sig=[]
    book = xlwt.Workbook()
    sh = book.add_sheet("a" + str(caseList[0].alfa) + "_Sig_S")
    col=0
    newCol=False
    for key, group in groupby(caseList, lambda x: x.Re):
        row=0
        if newCol: col+=3
        newCol=False
        
        alist = list(group)        
        s, sig = getSig_S(alist)
        if len(s)<1:
            continue
        marker = next(linecycler)
        snew = np.linspace(s[0], s[-1], num=100, endpoint=True)
        if len(s)>3:
            f1=interpolate.interp1d(s, sig, kind='cubic')
#            f1=interpolate.InterpolatedUnivariateSpline(s, sig, k=3)
            f2=interpolate.interp1d(s, -np.array(sig), kind='cubic')
#            f2=interpolate.InterpolatedUnivariateSpline(s, -np.array(sig), k=3)
        elif len(s)>2:
            f1=interpolate.interp1d(s, sig, kind='quadratic')
            f2=interpolate.interp1d(s, -np.array(sig), kind='quadratic')
        else:
            f1=interpolate.interp1d(s, sig, kind='slinear')
            f2=interpolate.interp1d(s, -np.array(sig), kind='slinear')
        
        if max(sig) > 0:
            sh.write(row, col, "Re ")
            sh.write(row, col+1, alist[0].Re)
            row+=1
            for i in range(0,len(s)):
                sh.write(row, col, s[i])
                sh.write(row, col+1, sig[i])
                row+=1
            newCol=True
        
        line, = plt.plot(snew, f1(snew))
        line, = plt.plot(s, sig, marker=marker, color=line.get_color(), linestyle='None')                        
        line.set_label("Re "+str(alist[0].Re))
        try:
            ss = 0.5*(s[0]+s[-1])
            smax=optimize.fmin(f2, ss, maxiter=100000, maxfun=100000, disp=False)
            sigmax=f1(smax)[0]
            
            if float(alist[0].Re<=2500):
                Sig.append(sigmax)
                S.append(smax[0])
                Re.append(float(alist[0].Re))
#                print "Store Sig %f, S%f, Re %f" %( sigmax, smax[0], alist[0].Re )
        except Exception as error:
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'        
            print 'Caught this error: ' + repr(error)
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            print "No Solution for S=%s Re=%s " % (str(alist[0].S), str(alist[0].Re))
            continue
#        print "======================"
    book.save("out.dat")
    fontP = FontProperties()
    fontP.set_size('small')
    
    fig = plt.figure(0, (10,10), 100)
    ax = fig.add_subplot(111)
    plt.xlabel('S')
    plt.ylabel('$max_{\mu}\sigma$', rotation = 0)
    
    print "======================"
    try:
        S, Sig, Re = (list(x) for x in zip(*sorted(zip(S, Sig, Re), key=lambda pair: pair[1])))
        snew = np.linspace(S[0], S[-1], num=100, endpoint=True)

        #try with parametric curve definition
        tck, u = interpolate.splprep([S, Sig, Re], s=0)
        unew = np.linspace(u[0], u[-1], num=100, endpoint=True)
        out = interpolate.splev(unew, tck)
        
#        line, = ax.plot(snew, f1(snew))
        line, = plt.plot(out[0], out[1])
        line, = plt.plot(S, Sig, marker= next(linecycler), color=line.get_color(), linestyle='None')
        line.set_label("Max line")
        
        
        f0=interpolate.interp1d(unew, out[0], kind='cubic')
        f1=interpolate.interp1d(unew, out[1], kind='cubic')
        f2=interpolate.interp1d(unew, out[2], kind='cubic')
        
        u = optimize.brentq(f1, 0, 1)
        re = f2(u)        
        s = f0(u)
        plt.scatter(s,f1(u))

        print '=> Parameter vaulue u=%f' % u
        print "=> Re=",re, " S=", s, "\n f0(u)=", f0(u), " f1(u)=", f1(u), " f2(u)=", f2(u), 

        textstr = '$Re_{crit}=%.1f$  $S_{crit}=%.3f$'%(re, s)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        plt.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)    
        
        box = ax.axes.get_position()
        ax.axes.set_position([box.x0, box.y0, 0.99*box.width, box.height])    
    except Exception as error:
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'        
        print 'Caught this error: ' + repr(error)
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print "Failed to find Critical Re"
        print S, Sig, Re

    plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
    plt.grid()
    fig.set_size_inches(20, 10.5)
    fig.savefig("alfa" + str(caseList[0].alfa) + "_maxSig_S.png", dpi=200)
#        plt.show()
    fig.clf()
    
def plotMaxSigmaRe(caseList):
    caseList.sort(key=lambda l: l.S)
    for key, group in groupby(caseList, lambda x: x.S):
        alist = list(group)
        print( " For S " + str(alist[0].S))
        alist.sort(key=lambda l: l.Re)
        re, sig = getSig_Re(alist)
        if len(re)<1:
            continue
        marker = next(linecycler)
        renew = np.linspace(re[0], re[-1], num=100, endpoint=True)
        if len(re)>3:
            f=interpolate.interp1d(re, sig, kind='cubic')
        elif len(re)>2:
            f=interpolate.interp1d(re, sig, kind='quadratic')
        else:
            f=interpolate.interp1d(re, sig, kind='slinear')

        line, = plt.plot(renew, f(renew))
        line, = plt.plot(re, sig, marker=marker, color=line.get_color(), linestyle='None')
        
        line.set_label("S "+str(alist[0].S))
    
    fontP = FontProperties()
    fontP.set_size('small')

    fig = plt.figure(0, (10,10), 100)
    ax = plt.subplot(111)
    plt.xlabel('Re')
    plt.ylabel('$max_{\mu}\sigma$', rotation = 0)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.99*box.width, box.height])

    plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
    ax.grid()
    fig.set_size_inches(20, 10.5)
    fig.savefig("alfa" + str(caseList[0].alfa) + "_maxSig_Re.png", dpi=200)
#        plt.show()
    fig.clf()
    
def plotReCritS(caseList):
    caseList.sort(key=lambda l: l.S)
    S=[]
    ReC=[]
    MuC=[]
    for key, group in groupby(caseList, lambda x: x.S):
        alist = list(group)
        print "============================================"
        print( " For S " + str(alist[0].S))
        alist.sort(key=lambda l: l.Re)
        re, sig = getSig_Re(alist)
        if len(re)<1:
            continue
#        if len(re)>3:
        f=interpolate.InterpolatedUnivariateSpline(re, sig, k=1)
#        elif len(re)>2:
#            f=interpolate.interp1d(re, sig, kind='slinear')
#        else:
#            continue
        
        try:
            recrit = optimize.fsolve(f, 2000)
        except:
            try:
                recrit = optimize.fsolve(f, 2500)
            except:
                print ("No Solution for: ", alist[0].S)
                continue
        print "Solution for ", alist[0].S, " is ", recrit, " | eps= ", f(recrit)
        
        S.append(float(alist[0].S))
        ReC.append(recrit[0])

    fig = plt.figure(0, (10,10), 100)
    ax = plt.subplot(111)
    plt.xlabel('S')
    plt.ylabel('$Re_{c}$', rotation = 0)
    snew = np.linspace(S[0], S[-1], num=100, endpoint=True)
    f1=interpolate.InterpolatedUnivariateSpline(S, ReC, k=3)
    line, = ax.plot(snew, f1(snew))
    line, = ax.plot(S, ReC, marker=next(linecycler), color=line.get_color(), linestyle='None')

    for i in range(0, len(S)):
        print S[i], ", ", ReC[i]
    print "----"

    fontP = FontProperties()
    fontP.set_size('small')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.99*box.width, box.height])

    ax.grid()
    fig.set_size_inches(20, 10.5)
    fig.savefig("alfa" + str(caseList[0].alfa) + "_ReCrit_S.png", dpi=200)
#        plt.show()
    fig.clf()
       
def plotSigmaMu2(caseList):
    fig = plt.figure(0, (10,10), 100)
    ax = plt.subplot(111)
    plt.xlabel('$\mu$')
    plt.ylabel('$\sigma$', rotation = 0)  
    
    caseList.sort(key=lambda l: l.alfa) 
    for key, group in groupby(caseList, lambda x: x.alfa):
        alist = list(group)
        print "alfa=", alist[0].alfa        
        alist.sort(key=lambda l: l.S)
        for key, group in groupby(alist, lambda x: x.S):
            blist = list(group)
            print "S=", alist[0].S
            blist.sort(key=lambda l: l.Re)
            mu=[]
            sig=[]
            for key, group in groupby(blist, lambda x: x.Re):
                clist = list(group)
                print "Re=", clist[0].Re
                marker = next(linecycler)
                clist.sort(key=lambda l: l.mu)
                x = np.array([float(icase.mu) for icase in clist])
                y = np.array([icase.sigma for icase in clist])
#                if max(y)<0:
#                    continue
                xnew = np.linspace(x[0], x[-1], num=100, endpoint=True)
#                print x[0], x[-1]
                if len(x)>3:
                    f=interpolate.interp1d(x, y, kind='cubic')
                    line, = plt.plot(xnew, f(xnew))
                line, = plt.plot(x, y, marker=marker, color=line.get_color(), linestyle='None')
                line.set_label("a=" +str(clist[0].alfa)+ "S "+str(clist[0].S) + " Re " + str(clist[0].Re))
            
#                print
                print "a=", str(clist[0].alfa), "Re=", str(clist[0].Re), "S=", str(clist[0].S)
                for val in xnew:
                    print val, ", ", f(val)
            
    fontP = FontProperties()
    fontP.set_size('small')        
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.99*box.width, box.height])
    
    plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
    ax.grid()
    fig.set_size_inches(20, 10.5)
    #            fig.savefig("sig_mu_S"+str(alist[0].S)+".png", dpi=200)
    plt.show()
#        fig.clf()
    
def plotAlfaMu(caseList):
    a=[]
    mu_0=[]
    mu_1=[]
    fig = plt.figure(0, (10,10), 100)
    ax = plt.subplot(111)
    plt.xlabel('$\mu$')
    plt.ylabel('$a$', rotation = 0)  
    
    caseList.sort(key=lambda l: l.alfa) 
    for key, group in groupby(caseList, lambda x: x.alfa):
        alist = list(group)
        alist.sort(key=lambda l: l.S)
        for key, group in groupby(alist, lambda x: x.S):
            blist = list(group)
            blist.sort(key=lambda l: l.Re)
            mu=[]
            sig=[]
            for key, group in groupby(blist, lambda x: x.Re):
                clist = list(group)
            
                marker = next(linecycler)
                clist.sort(key=lambda l: l.mu)
                x = np.array([float(icase.mu) for icase in clist])
                y = np.array([icase.sigma for icase in clist])
                if max(y)<0:
                    continue
                xnew = np.linspace(x[0], x[-1], num=100, endpoint=True)
                
                if len(x)>3:
                    f=interpolate.InterpolatedUnivariateSpline(x, y, k=3)
            
                mu_0.append(optimize.brentq(f,x[0], 2))
                mu_1.append(optimize.brentq(f,2, x[-1]))
                a.append(clist[0].alfa)
    
    line, = plt.plot(a, mu_0)
    line, = plt.plot(a, mu_1)
    fontP = FontProperties()
    fontP.set_size('small')        
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, 0.99*box.width, box.height])
    
    plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
    ax.grid()
    fig.set_size_inches(20, 10.5)
    #            fig.savefig("sig_mu_S"+str(alist[0].S)+".png", dpi=200)
    plt.show()
#        fig.clf()
    
def plotReCritMu(caseList):
    caseList.sort(key=lambda l: l.S)
    fig = plt.figure(0, (10,10), 100)

    book = xlwt.Workbook()
    sh = book.add_sheet("a" + str(caseList[0].alfa) + "_ReC_mu")
    col=0
    newCol=False
    for key, group in groupby(caseList, lambda x: x.S):
        row=0
        if newCol: col+=3
        newCol=False
        
        alist = list(group)
        if max( np.array([icase.sigma for icase in alist]) )<0:
            print "S" + str(alist[0].S) + " has no sig>0"
            continue
        print( " For S " + str(alist[0].S))
        alist.sort(key=lambda l: l.Re)
        re=[]
        s_mu=[]
        for key, group in groupby(alist, lambda x: x.Re):
            blist = list(group)
            blist.sort(key=lambda l: l.mu)
            x = np.array([float(icase.mu) for icase in blist])
            y = np.array([icase.sigma for icase in blist])
            f=interpolate.InterpolatedUnivariateSpline(x, y, k=3)
            re.append(float(blist[0].Re))
            s_mu.append(f)

        mu=np.linspace(x[0], x[-1], num=50, endpoint=True)
        mu_c=[]
        re_c=[]
        for m in mu: #for each of the test mu
            s_re=[]
            for kvp in zip(re,s_mu):
                v = float(kvp[1](m))
                s_re.append(v)
            if max(s_re) < 0:
                print "skipping %f to low" % (m)
                continue
            if min(s_re) > 0:
                print "skipping %f to high" % (m)
                continue
            f=interpolate.InterpolatedUnivariateSpline(re, s_re, k=1)
            xnew = np.linspace(re[0], re[-1], num=9, endpoint=True)
#            print max(s_re), min(s_re), re[0], re[-1], f(re[0]), f(re[-1])
            try:
                rec = optimize.brentq(f,re[0], re[-1])
            except:
#                continue
                if len(re_c)>0:
                    rec = optimize.fsolve(f, re_c[-1])[0]
                else:
                    rec = optimize.fsolve(f, re[0])[0]
            re_c.append(rec)
            mu_c.append(m)
            print m, ", ", rec
        
        if max(mu_c)>0:
            sh.write(row, col, "S ")
            sh.write(row, col+1, alist[0].S)
            row+=1
            for i in range(0,len(mu_c)):
                sh.write(row, col, mu_c[i])
                sh.write(row, col+1, re_c[i])
                row+=1
            newCol=True        
        
        marker = next(linecycler)
        line, = plt.plot(mu_c, re_c, marker=marker)
        line.set_label("S "+str(alist[0].S))
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(fancybox=True, shadow=True, loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP)
    plt.grid()
    fig.savefig("alfa_" + str(alist[0].alfa) + "_ReCrit_Mu.png", dpi=200)
    fig.clf()
    #    plt.show(block=True)
    book.save("out.dat")

#############################################################################

def calcMaxSigma(caseList):
    '''
    For a given caseList (single alfa) returns a colection of Re, S, Sig
    '''
    caseList.sort(key=lambda l: l.Re)
    S = [0.01, 0.025, 0.04, 0.055, 0.07, 0.085, 0.1, 0.115, 0.13, 0.145, 0.16, 0.175, 0.19, 0.205, 0.22, 0.235, 0.25]
#    S = [0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
    out=[]
    
    for key, group in groupby(caseList, lambda x: x.Re):
        alist = list(group)        
        s, sig = getSig_S(alist)
#        print s, sig
        i=0
        if s[0] > S[0]:
            for ss in S:
                if ss in s:
                    break
                s.insert(i, ss)
                sig.insert(i, calculateSigmaForS(caseList, ss, alist[0].Re))
                i=i+1
                
        if s[-1] < S[-1]:
            for ss in S:
                if ss not in s: continue
                if ss <= s[-1]:
                    continue
                else:
#                    print ss, alist[0].Re
                    s.insert(len(s), ss)
                    sig.insert(len(sig), calculateSigmaForS(caseList, ss, alist[0].Re))
#                    print s, sig
        
        if float(alist[0].alfa) == 3:  
            #extra manual ...
            if float(alist[0].Re) == 1900:
                ssig = calculateSigmaForS(caseList, 0.025, 1900)
                s.insert(1, 0.025)
                sig.insert(1, ssig)
#                print ssig
                
            #extra manual ...
            if float(alist[0].Re) == 1500:
                ssig = calculateSigmaForS(caseList, 0.025, 1500)
                s.insert(1, 0.025)
                sig.insert(1, ssig)
#                print ssig
                
#        print alist[0].Re, s, sig
        case=Case()
        case.alfa = alist[0].alfa
        case.Re = alist[0].Re
        case.S = s
        case.sigma = sig
        out.append(case)        
        
    return out

def CreateColectionForCriticalPlot():
    '''
    Creates a CC colection for use with 3D interpolation
    THIS DOES NOT WORK!! since a05, a1, ... are not known
    '''
    c05=calcMaxSigma(a05)
    c1=calcMaxSigma(a1)
    c2=calcMaxSigma(a2)
    c3=calcMaxSigma(a3)
    c4=calcMaxSigma(a4)
    c5=calcMaxSigma(a5)
    c6=calcMaxSigma(a6)
    c7=calcMaxSigma(a7)
    c8=calcMaxSigma(a8)
    c10=calcMaxSigma(a10)
    cc=c05+c1+c2+c3+c4+c5+c6+c7+c8+c10
    return cc

def MaxSigmaS_with3Dinterpolation_griddata(caseList):
    '''
    creates interpolation using griddata linear interpolation. This is for testing, not for use
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('alpha')
    ax.set_ylabel('S')
    ax.set_zlabel('Sigma')
    
    a=[]
    s=[]
    sig=[]
    
    for case in caseList:
        for p in zip(case.S,case.sigma):
            a.append(float(case.alfa))
            s.append(p[0])
            sig.append(p[1])
    
    Anew = np.linspace(min(a), max(a), num=500, endpoint=True)    
    Snew = np.linspace(min(s), max(s), num=500, endpoint=True)
    Anew, Snew = np.meshgrid(Anew, Snew)
    interp = interpolate.griddata((a, s), sig, (Anew, Snew), method='linear')

    ax.plot_surface(Anew, Snew, interp, cmap=cm.jet, linewidth=0.2)
    
    plt.grid()
    fig.set_size_inches(20, 10.5)
    plt.show()
    fig.clf()  

def  MaxSigmaS_Surface_with3Dinterpolation(caseList, with3D, InterType):
    '''
    calculates in interpolation polynomial in 3D for a given calselist
    to be used with cases filtered for a single Re: re=filter(lambda l: float(l.Re)==1500, cc)
    '''
    alfa=[]
    S=[]
    sig=[]
    
    #This here makes a grid for a given Re (alfa,S) and for each point sigma
    for case in caseList:
#        print case.alfa, case.Re
        for p in zip(case.S,case.sigma):
            alfa.append(float(case.alfa))
            S.append(p[0])
            sig.append(p[1])
    
    p=[] #this grid (alfa,S) is stored in p, and used to find an interpolant
    for pair in zip(alfa,S):
        p.append([pair[0], pair[1]])
    if InterType==1:
        interp = interpolate.LinearNDInterpolator(p, sig)
    elif InterType==2:
        interp = interpolate.CloughTocher2DInterpolator(p, sig)
    else:
        raise "Unknown Interpolation type"
    
    if with3D:
        Anew = np.linspace(min(alfa), max(alfa), num=200, endpoint=True)    
        Snew = np.linspace(min(S), max(S), num=200, endpoint=True)
        Anew, Snew = np.meshgrid(Anew, Snew)
        zz = interp(Anew, Snew)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel('alpha')
        ax.set_ylabel('S')
        ax.set_zlabel('Sigma')
        plt.title('Re='+str(caseList[0].Re))
        
        ax.plot_surface(Anew, Snew, zz, cmap=cm.jet, linewidth=0.2)
        lve=[0]
        cset = ax.contour(Anew, Snew, zz,lve, offset=min(sig), cmap=cm.coolwarm)
        
        plt.grid()
        plt.show()
        fig.clf()
    return (caseList[0].Re, interp, min(alfa), max(alfa), min(S), max(S))#tuple
    

def CriticalSContourPlots(caseList, with3D=False, InterType=2):
    '''
    Creates a contour plot using caseList as input
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('alpha')
    ax.set_ylabel('S')

    caseList.sort(key=lambda l: l.Re)
    res=[]        
    for key, group in groupby(caseList, lambda x: x.Re):
        alist = list(group)
        #Re, interp, minA, maxA, minS, maxS
        res.append(MaxSigmaS_Surface_with3Dinterpolation(alist, with3D, InterType))

    xy=[]
    for Re, interp, minA, maxA, minS, maxS in res:
        Anew = np.linspace(0, maxA, num=200, endpoint=True)    
        Snew = np.linspace(0, maxS, num=200, endpoint=True)
        Anew, Snew = np.meshgrid(Anew, Snew)
        zz=interp(Anew, Snew)
        
        CS = plt.contour(Anew, Snew, zz, levels=[0])
        fmt = {}
        for l in CS.levels:
            fmt[l] = str(Re)

        p= CS.collections[0].get_paths() 
        x=[]
        y=[]
        for pp in p:
            v = pp.vertices
            x.extend(v[:,0])
            y.extend(v[:,1])
        xy.append((Re,x,y))
#        plt.plot(x,y, 'o')
        if len(x)>0:
            manual_loc=[(x[len(x)/2], y[len(x)/2])]
            plt.clabel(CS, inline=1, fmt=fmt, manual=manual_loc)

    book = xlwt.Workbook()
    sh = book.add_sheet("a" + str(caseList[0].alfa) + "_Sig_S")
    col=0
    newCol=False
    maxl=0
    for e in xy:
        maxl=max(maxl, len(e[1]))
#    print maxl
    for e in xy:
        row=0
        sh.write(row, col, " , ")
        sh.write(row, col+1, "Re")
        sh.write(row, col+2, " , ")
        sh.write(row, col+3, e[0])
        row+=1
#        for p in zip(e[1],e[2]):
        for i in range(0,maxl):
            if i<len(e[1]): p=(e[1][i],e[2][i])
            else: p=("", "")
            sh.write(row, col, " , ")
            sh.write(row, col+1, p[0])
            sh.write(row, col+2, " , ")
            sh.write(row, col+3, p[1])
            row+=1
        col+=4
            
    book.save("CriticalSContourPlots.dat")
    plt.grid()
    plt.show()
    fig.clf()

def calculateSigmaThroughInterpolation(caseList, Re):
    '''
    Creates, through interpolation new result for a given Re
    accepts caseList for a given alfa
    '''
    S = [0.01, 0.025, 0.04, 0.055, 0.07, 0.085, 0.1, 0.115, 0.13, 0.145, 0.16, 0.175, 0.19, 0.205, 0.22, 0.235, 0.25]
    caseList.sort(key=lambda l: l.alfa)
    out=[]        
    for key, group in groupby(caseList, lambda x: x.alfa):
        alist = list(group)
    
        case=Case()
        case.alfa = alist[0].alfa
        case.Re = Re
        stab=[]
        sigma=[]
        for s in S:
#            try:
            sig=calculateSigmaForS(alist, s, Re)
            sigma.append(sig)
            stab.append(s)
#            except:
#                print "Failed for:"
#                print "Alfa=" + str(case.alfa) + " S=" + str(s)
#                continue
        case.S=stab
        case.sigma=sigma
        out.append(case)
    return out

def allPlots(caselist):
    plotSigmaMu(caselist)
    plotReCritMu(caselist)
#    plotSigmaRe(caselist)
#    plotMaxSigmaRe(caselist)
    plotMaxSigmaS(caselist)
    plotReCritS(caselist)
    
    





























