# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:13:32 2022

@author: 921677
"""
import numpy as np
import math
import scipy

def cruise_fc(aircraftproperties, r_corrected, climbprofile, descentprofile, cruise_alt, cruise_vel, W_descent, num_par):
    ## Cruise fuel consumption
    ## Constants
    h_cruise = cruise_alt # cruise altitude in m
    T_0 = 288.15    # sea level temperature (K)
    p_0 = 101325    # sea level pressure (Pa)
    dT = -6.5E-3    # change in temperature with altitude (K/m)
    R = 287         # specific gas constant
    g = 9.81        # gravity acceleration constant
    e0 = 0.8
    
    # r_steps = 2000
    
    T_cruise = T_0 + dT*h_cruise
    p_cruise = p_0*(T_cruise/T_0)**(-g/(dT*R))
    rho_cruise = p_cruise/(R*T_cruise)
    
    # change v_cruise depending on altitude
    ## Descent Profile Specification
    h_fl240 = 0.3048*24000
    h_fl100 = 0.3048*10000
    h_final = 0.3048*3000


    cd0_id = 0
    cd0_d = 0
    cd0_app = 0.03
    cd0_hold = 0.06
    cd0_landing = 0.095
    if h_cruise < h_final:
        cd0 = aircraftproperties[11] + cd0_landing
    elif h_cruise < h_fl100:
        cd0 = aircraftproperties[11] + cd0_app
    elif h_cruise < h_fl240:
        cd0 = aircraftproperties[11] + cd0_d
    else:
        cd0 = aircraftproperties[11] + cd0_id

    v_cruise = cruise_vel
    S = aircraftproperties[5]
    b = aircraftproperties[6]
    TSFC = aircraftproperties[14]/1E6 # thrust specific fuel consumption in kg/Ns
    ct = aircraftproperties[14]/1E6*g
    
    r_cruise = r_corrected - max(climbprofile[:,2]) - max(descentprofile[:,2])
    if r_cruise < 0:
        print('Mission too short to reach cruise altitude, analysis invalid')
    
    r_steps = abs(round(r_cruise/v_cruise/num_par.t_step_cruise))
    
    r_step = np.linspace(0, r_cruise, r_steps+1)
    t_step = r_step/v_cruise
    
    W_end_cr = max(W_descent)
    dr = r_cruise/r_steps
    dt = dr/v_cruise
    
    W = np.zeros(np.size(t_step))
    D = np.zeros(np.size(t_step))
    LD = np.zeros(np.size(t_step))
    F = np.zeros(np.size(t_step))
    fc = np.zeros(np.size(t_step))
    W_old = W_end_cr
    
    for i in reversed(range(np.size(t_step))):
        W[i] = W_old
        D[i] = (1/2)*rho_cruise*v_cruise**2*cd0*S + (2*(W[i])**2)/(np.pi*e0*b**2*rho_cruise*v_cruise**2)
        LD[i] = W[i]/D[i]
        F[i] = D[i]
        fc[i] = F[i]*TSFC
        W_old = W[i] * (math.exp(dr*(1/LD[i])*ct/v_cruise))     # use Breguet mass approximation to calculate fuel consumption via drag equation (weight influence on lift induced drag)              
        # W_old = W[i] + fc[i]*dt*g     # use Breguet mass approximation to calculate fuel consumption via drag equation (weight influence on lift induced drag)
    # total_fuel_cruise = (max(W) - min(W))/g                     # increase number of steps to decrease LD induced error
    total_fuel_cruise = scipy.integrate.simps(fc,t_step)    

    return total_fuel_cruise, fc, W, F, t_step, r_step