# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 17:37:41 2022

@author: Pieter
"""
import numpy as np
def great_circle_new(lon1_array, lat1_array, lon2_array, lat2_array):
    coor_set = np.array([lon1_array, lat1_array, lon2_array, lat2_array])/180*np.pi
    distance = 6371 * 1000 *(np.arccos(np.sin(coor_set[1,:]) * np.sin(coor_set[3,:]) + np.cos(coor_set[1,:]) * np.cos(coor_set[3,:]) * np.cos(coor_set[0,:] - coor_set[2,:])))
    return distance