# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 18:58:10 2022

@author: 921677
"""
import numpy as np
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx