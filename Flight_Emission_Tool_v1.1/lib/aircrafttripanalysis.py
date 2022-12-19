# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 19:46:33 2022

@author: 921677
"""
import numpy as np
from scipy import integrate

from lib.findnearest import find_nearest


def trip_analysis(aircraftproperties, consumption_prop, t_taxi_in, t_taxi_out, climbprofile, descentprofile, t_cruise, r_cruise, fc_climb, fc_cruise, fc_descent, total_fuel_TO, W_climb, W_cruise, W_descent, F_climb, F_cruise, F_descent):
    ## Aircraft trip analysis
    # Add taxi and TO fuel consumption, combine profiles to single t, r, fc, W, F
    # Output emissions
    
    # Taxi fuel consumption
    v_cruise = aircraftproperties[3]
    H_cruise = aircraftproperties[4]
    TSFC_SL = aircraftproperties[15]/1E6
    F_max_TO = aircraftproperties[16]
    TSFC_idle_penalty = consumption_prop[0]
    F_idle_perc = consumption_prop[2]
    
    F_idle = F_idle_perc*F_max_TO 
    TSFC_idle_SL = TSFC_SL*TSFC_idle_penalty
    total_fuel_taxi = TSFC_idle_SL*F_idle*(t_taxi_in + t_taxi_out)
    
    # Trip properties (climb/desecentprofile order: t, h, s, vx, Mx, vz, theta, T, rho, c, cd0, ivx)
    t_trip = np.append(climbprofile[:,0], t_cruise+climbprofile[-1,0])
    t_trip = np.append(t_trip, t_trip[-1]+descentprofile[:,0])
    
    r_trip = np.append(climbprofile[:,2], r_cruise+climbprofile[-1,2])
    r_trip = np.append(r_trip, r_trip[-1]+descentprofile[:,2])
    
    v_climb = (climbprofile[:,3]**2+climbprofile[:,5]**2)**(1/2)
    v_cruise = np.ones(np.size(r_cruise))*v_cruise
    v_descent = (descentprofile[:,3]**2+descentprofile[:,5]**2)**(1/2)
    v_trip = np.append(v_climb, v_cruise)
    v_trip = np.append(v_trip, v_descent)
    
    H_trip = np.append(climbprofile[:,1], np.ones(np.size(r_cruise))*H_cruise)
    H_trip = np.append(H_trip, descentprofile[:,1])
    
    fc_trip = np.append(fc_climb, fc_cruise, 0)
    W_trip = np.append(W_climb, W_cruise)
    fc_trip = np.append(fc_trip, fc_descent, 0)
    W_trip = np.append(W_trip, W_descent)
    
    F_trip = np.append(F_climb, F_cruise)
    F_trip = np.append(F_trip, F_descent)
    
    # Energy
    E_jetA1= 43.15              # Jet A1 energy density in MJ/kg
    # E_jetA1= 3.16*1000/73.2
    E_trip = fc_trip*E_jetA1    # Energy use in MJ/s
    E_taxi = total_fuel_taxi*E_jetA1    # Taxi energy use in MJ
    E_TO = total_fuel_TO*E_jetA1        # TO energy use in MJ
    trip_properties = np.column_stack([t_trip, r_trip, v_trip, H_trip, fc_trip, W_trip, F_trip, E_trip])
    
  
    # Total trip fuel consumption
    H_limit = 9000                  # non-CO2 effects only considered above this altitude
    if H_limit - max(climbprofile[:,1]) < 10:
        idx_9000c = find_nearest(climbprofile[:,1],H_limit)
        idx_9000d = np.size(climbprofile[:,1]) + np.size(r_cruise) + find_nearest(descentprofile[:,1],H_limit)
        total_fuel_CD = integrate.trapz(fc_trip[:idx_9000c+1],t_trip[:idx_9000c+1]) + integrate.trapz(fc_trip[idx_9000d:],t_trip[idx_9000d:]) + total_fuel_taxi + total_fuel_TO 
        total_fuel_CR = integrate.trapz(fc_trip[idx_9000c:idx_9000d+1],t_trip[idx_9000c:idx_9000d+1])
    else:
        total_fuel_CD = integrate.trapz(fc_trip,t_trip) + total_fuel_taxi + total_fuel_TO 
        total_fuel_CR = 0
    total_fuel_trip = integrate.trapz(fc_trip,t_trip) + total_fuel_taxi + total_fuel_TO 


 

    return trip_properties, total_fuel_taxi, total_fuel_trip, total_fuel_CD, total_fuel_CR, E_taxi, E_TO