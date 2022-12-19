# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 13:38:22 2021

@author: 921677
"""

import numpy as np
import pandas as pd

from lib.ISA import ISA

def aircraft_climbprofile(aircraftproperties, aircraft, cruise_alt, num_par):
    ## Constants
    R = 287         # specific gas constant
    k = 1.4         # specific heat
    T_0, rho_0, c_0 = ISA(0)
    p_0 = rho_0*R*T_0
    dT = -6.5E-3    # change in temperature with altitude (K/m)
    
    h_cruise = cruise_alt   # cruise altitude in m
    g = 9.81                # gravity acceleration constant
    cd0_init = aircraftproperties[11]    # zero lift drag coefficient
    cd0_ic = 0.02           # initial climb drag penalty (flaps)
    
    
    
    ## Climb Profile Specification
    h_ic = 0.3048*5000
    h_fl150 = 0.3048*15000
    h_fl240 = 0.3048*24000
    climbprofiles = pd.read_csv('./data/aircraft_climbprofiles.csv',delimiter=';',index_col='CP')
    aircraft_index = list(climbprofiles.columns)
    climbprofiles = climbprofiles.to_numpy()
    climbprofiles[0,:] = climbprofiles[0,:]*0.5144; climbprofiles[2,:] = climbprofiles[2,:]*0.5144; climbprofiles[4,:] = climbprofiles[4,:]*0.5144
    climbprofiles[1,:] = climbprofiles[1,:]*0.00508; climbprofiles[3,:] = climbprofiles[3,:]*0.00508; climbprofiles[5,:] = climbprofiles[5,:]*0.00508; climbprofiles[7,:] = climbprofiles[7,:]*0.00508; 
    T_cruise, rho_cruise, c_cruise = ISA(h_cruise)
     
    
    index = aircraft_index.index(aircraft)
    climbprofile = climbprofiles[:,index]
    
    def VTAS(c, VIAS, p):
        M_ps = VIAS/c_0
        q = ((M_ps*M_ps*(k-1)/2 + 1) ** (k/(k-1)) - 1)*p_0
        Mx = ((((q/p+1)**((k-1)/k) - 1)*2/(k-1)))**(1/2)
        vx = c * Mx
        # vx = VIAS
        return vx, Mx
    
    # Initialize inputs, desired order: t, h, s, vx, Mx, vz, theta, T, rho, c, cd0, ivx
    t = []; t0 = 0; t.append(t0)
    ivx0 = climbprofile[0]
    vx0, Mx0 = VTAS(c_0, ivx0, p_0)
    vx = []; vx.append(vx0)
    Mx = []; Mx.append(Mx0)
    vz = []; vz0 = climbprofile[1]; vz.append(vz0)
    theta = []; theta0 = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(theta0)
    h = []; h0 = 0; h.append(h0)
    s = []; s0 = 0; s.append(s0)
    T = []; T.append(T_0)
    rho = []; rho.append(rho_0)
    c = []; c.append(c_0)
    cd0 = []; cd0.append(cd0_init + cd0_ic)
    ivx = []; ivx0 = climbprofile[0]; ivx.append(ivx0)
    
    # Initialize calculations
    h_trigger = 0
    t_step = num_par.t_step_climb # CLIMB
    
    while h[h_trigger] < h_cruise - 5: # 5 is senstivity factor (if altitude is 5meters away from h_cruise, climb is stopped)
        if h[h_trigger] <= h_ic:
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            ivxnew = climbprofile[0]; ivx.append(ivxnew)
            vxnew, Mxnew = VTAS(c[-1], ivx[-1], p); vx.append(vxnew); Mx.append(Mxnew)
            vznew = climbprofile[1]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init + cd0_ic; cd0.append(cd0new)
        elif h[h_trigger] >= h_ic and h[h_trigger] <= h_fl150:
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            ivxnew = climbprofile[2]; ivx.append(ivxnew)
            vxnew, Mxnew = VTAS(c[-1], ivx[-1], p); vx.append(vxnew); Mx.append(Mxnew)
            vznew = climbprofile[3]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init; cd0.append(cd0new)
        elif h[h_trigger] >= h_fl150 and h[h_trigger] <= h_fl240:
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            ivxnew = climbprofile[4]; ivx.append(ivxnew)
            vxnew, Mxnew = VTAS(c[-1], ivx[-1], p); vx.append(vxnew); Mx.append(Mxnew)
            vznew = climbprofile[5]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init; cd0.append(cd0new)
        elif h[h_trigger] >= h_fl240:    
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            Mxnew = climbprofile[6]; Mx.append(Mxnew)
            vxnew = cnew*Mxnew; vx.append(vxnew); ivx.append(0)
            vznew = climbprofile[7]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init; cd0.append(cd0new)
       
        h_trigger += 1
    aircraft_climbprofile = np.column_stack([t, h, s, vx, Mx, vz, theta, T, rho, c, cd0, ivx])
    if h_cruise > h_fl240:
        v_cruise = aircraftproperties[3]
    else:
        v_cruise = aircraft_climbprofile[-1,3]
        
    v_cruise_new = v_cruise
    return aircraft_climbprofile, v_cruise_new
