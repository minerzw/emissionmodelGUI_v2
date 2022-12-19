# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:47:15 2022

@author: 921677
"""

import numpy as np
# import pandas as pd
from scipy import interpolate

def thrust_interpol(hnew, Mnew, thrust_var):
    m = np.linspace(0,0.9,10)
    h = np.linspace(0,12000,7)
    f = interpolate.interp2d(m, h, thrust_var, kind='cubic')
    F_rel = f(Mnew, hnew)
    return F_rel
