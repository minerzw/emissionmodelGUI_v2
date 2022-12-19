# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:10:19 2022

@author: 921677
"""
import numpy as np
import math
import scipy
from scipy import integrate


from lib.thrustinterpol import thrust_interpol
from lib.ISA import ISA


def descent_fc(aircraftproperties, descentprofile, cruise_alt_max, consumption_prop, W_start_alt, thrust_var):
    
    ## Constants
    g = 9.81
    gamma = 1.4
    R = 287
    e0 = 0.8    
    
    ## Initialize # order: t, h, s, vx, Mx, vz, theta, T, rho, c, cd0, ivx
    t = descentprofile[:,0]
    vx = descentprofile[:,3]
    vz = descentprofile[:,5]
    theta = descentprofile[:,6]/180*np.pi
    H = descentprofile[:,1]
    T = descentprofile[:,7]
    rho = descentprofile[:,8]
    cd0 = descentprofile[:,10]
    v_cruise = aircraftproperties[3]
    S = aircraftproperties[5]
    b = aircraftproperties[6]
    cd0_init = aircraftproperties[11]
    r = aircraftproperties[13]
    ct = aircraftproperties[14]/1E6*g
    TSFC_max = aircraftproperties[14]/1E6 
    TSFC_min = aircraftproperties[15]/1E6
    F_max_TO = aircraftproperties[16]
    TSFC_idle_penalty = consumption_prop[0]
    TSFC_FT_penalty = consumption_prop[1]
    F_idle_perc = consumption_prop[2]
    
    ## Calculate cruise properties
    T_cruise, rho_cruise, c_cruise = ISA(cruise_alt_max)
    
    
    ## Determine variation of thrust specific fuel consumption (as function of air density)
    rho_norm = (rho - min(rho))/max(rho - min(rho))
    dTSFC = TSFC_max - TSFC_min
    TSFC_shape = (rho_norm - 1)*-1
    TSFC = TSFC_min + TSFC_shape*dTSFC
    
    ## Assume optimum thrust 
    D_ec = (1/2)*rho_cruise*v_cruise**2*cd0_init*S + (2*(W_start_alt)**2)/(np.pi*e0*b**2*rho_cruise*v_cruise**2)
    L_ec = W_start_alt
    LD_ec = L_ec/D_ec
    r_opt = r*1000/2
    W_opt = W_start_alt*math.exp(r_opt*(1/LD_ec)*ct/v_cruise)
    F_opt_cruise = (1/2)*rho_cruise*v_cruise**2*cd0_init*S + (2*(W_opt)**2)/(np.pi*e0*b**2*rho_cruise*v_cruise**2)
    
    ## Initialize weight, thrust and consumption calculation
    v = (vx**2 + vz**2)**(1/2)
    dt = t[1] - t[0]
    W = np.zeros(np.size(t))
    F = np.zeros(np.size(t))
    fc = np.zeros(np.size(t))
    F_coef = np.zeros(np.size(t))
    TSFC_penalty = np.zeros(np.size(t))
    
    ## Calculate Mach number, optimum thrust, maximum thrust, idle thrust, for penalty mapping
    M = v/(gamma*R*T)**(1/2)
    M_cruise = v_cruise/(gamma*R*T[0])**(1/2)
    H_cruise = cruise_alt_max
    F_rel = thrust_interpol(H_cruise, M_cruise, thrust_var)
    for i in range(np.size(t)):
        F_coef[i] = thrust_interpol(H[i], M[i], thrust_var)
    F_opt = F_opt_cruise/F_rel*F_coef
    F_max = F_max_TO*F_coef
    F_idle = F_idle_perc*F_max
    
    ## Calculate W(t) and fc(t)
    W[-1] = W_start_alt
    for i in reversed(range(np.size(t))):
        L = W[i]*np.cos(theta[i])
        CL = L/(0.5*rho[i]*v[i]**2*S)
        D = (1/2)*rho[i]*v[i]**2*S*(cd0[i] + (CL**2)/(np.pi*((b**2)/S)*e0))
        F[i] = W[i]*np.sin(theta[i]) + D
        if F[i] < F_idle[i]:
            F[i] = F_idle[i]
            
        # Calculate TSFC penalty (off-design operation), assume cruise TSFC and thrust is on-design optimum, assume that optimum, maximum and idle thrust do not depend on environment  
        if F[i] < F_opt[i]:
            TSFC_0 = 1 - F_opt[i]*(1 - TSFC_idle_penalty)/(F_opt[i] - F_idle[i])
            TSFC_penalty[i] = F[i]*(1 - TSFC_idle_penalty)/(F_opt[i] - F_idle[i]) + TSFC_0
            TSFC[i] = TSFC[i]*TSFC_penalty[i]
        else:
            TSFC_0 = 1 - F_opt[i]*(TSFC_FT_penalty - 1)/(F_max[i] - F_opt[i])
            TSFC_penalty[i] = F[i]*(TSFC_FT_penalty - 1)/(F_max[i] - F_opt[i]) + TSFC_0
            TSFC[i] = TSFC[i]*TSFC_penalty[i]
        fc[i] = F[i]*TSFC[i]
        if i > 0:
            W[i-1] = W[i] + fc[i]*g*dt 
    
    total_fuel_descent = scipy.integrate.simps(fc,t)    
    
    return total_fuel_descent, fc, W, F, F_opt_cruise