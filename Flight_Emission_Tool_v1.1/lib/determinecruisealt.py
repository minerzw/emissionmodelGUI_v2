# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 12:28:50 2022

@author: SYSTEM
"""

import numpy as np
import pandas as pd
import math
from scipy.interpolate import interp1d


def determine_cruise_alt(aircraft, r):      
    cruise_fl_data = pd.read_csv('./data/cruise_fl.csv',delimiter=';',index_col='Index')
    aircraft_index = cruise_fl_data.index.tolist()
    index = aircraft_index.index(aircraft)

    distance_list = list(cruise_fl_data)
    d_col = np.array(distance_list, dtype=np.float32)*1852

    # ac_cruise_fl = cruise_fl_data.to_numpy()[index,:] 

    cruise_fl = np.zeros(np.size(aircraft_index))
    cruise_alt = np.zeros(np.size(aircraft_index))
    cruise_fl_max = np.zeros(np.size(aircraft_index))
    cruise_alt_max = np.zeros(np.size(aircraft_index))
    for i in range(np.size(aircraft_index)):
        ac_cruise_fl = cruise_fl_data.to_numpy()[i,:]
        f = interp1d(d_col, ac_cruise_fl)
        if r < max(d_col):
            cruise_fl[i] = math.floor(f(r)/10)*10
            cruise_alt[i] = cruise_fl[i]*0.3048*100
        else:
            cruise_fl[i] = max(ac_cruise_fl)
            cruise_alt[i] = cruise_fl[i]*0.3048*100
        cruise_fl_max[i] = max(ac_cruise_fl)
        cruise_alt_max[i] = cruise_fl_max[i]*0.3048*100
    return cruise_fl, cruise_alt, cruise_fl_max, cruise_alt_max
    
