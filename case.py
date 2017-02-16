# -*- coding: utf-8 -*-

class Case(object):
    """A simple example class"""
    def __init__(self):
        self.Name = "Empty Name"
        self.S = 0 #amplitude    
        self.Re = 0 # Reynolds number
        self.alfa = 0 # wave number
        self.mu = 0 #wave number
#        self.FinalTime = 0
#        self.Factors = []
        self.time = []
#        self.mod = []
        self.energy = []
        self.t=[]
        self.e=[]
#        self.fit_res = []
        self.sigma=0 #growth rate
        self.popt = ''
        self.perr = ''
    
        