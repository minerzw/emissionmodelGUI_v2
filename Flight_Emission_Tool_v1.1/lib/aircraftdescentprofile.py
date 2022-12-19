# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 11:31:14 2021

@author: 921677
"""

import numpy as np
import pandas as pd
import math


from lib.ISA import ISA


#aircraft = "B788"

def aircraft_descentprofile(aircraftproperties, aircraft, cruise_alt, t_hold, num_par):
    ## Constants
    R = 287         # specific gas constant
    k = 1.4         # specific heat
    T_0, rho_0, c_0 = ISA(0)
    p_0 = rho_0*R*T_0
    dT = -6.5E-3    # change in temperature with altitude (K/m)
    
    h_cruise = cruise_alt   # cruise altitude in m
    g = 9.81                # gravity acceleration constant
    cd0_init = aircraftproperties[11] # zero lift drag coefficient
    cd0_id = 0              # initial descent drag penalty
    cd0_d = 0               # descent drag penalty 
    cd0_app = 0.03          # approach drag penalty
    cd0_hold = 0.06         # holding drag penalty
    cd0_landing = 0.095     # landing drag penalty
        
    ## Speed of sound at cruise altitude
    T_cruise, rho_cruise, c_cruise = ISA(h_cruise)
    p_cruise = rho_cruise*R*T_cruise
    
    ## Descent Profile Specification
    h_fl240 = 0.3048*24000
    h_fl100 = 0.3048*10000
    h_final = 0.3048*3000
    
    
    descentprofiles = pd.read_csv('./data/aircraft_descentprofiles.csv',delimiter=';',index_col='CP')
    aircraft_index = list(descentprofiles.columns)
    descentprofiles = descentprofiles.to_numpy()
    # descentprofiles[0,:] = descentprofiles[0,:]*c
    descentprofiles[1,:] = descentprofiles[1,:]*-0.00508; descentprofiles[3,:] = descentprofiles[3,:]*-0.00508; descentprofiles[5,:] = descentprofiles[5,:]*-0.00508; descentprofiles[7,:] = descentprofiles[7,:]*0.00508; descentprofiles[9,:] = descentprofiles[9,:]*-0.00508
    descentprofiles[2,:] = descentprofiles[2,:]*0.5144; descentprofiles[4,:] = descentprofiles[4,:]*0.5144; descentprofiles[6,:] = descentprofiles[6,:]*0.5144; descentprofiles[8,:] = descentprofiles[8,:]*0.5144; 
    
    index = aircraft_index.index(aircraft)
    descentprofile = descentprofiles[:,index]
    
    def VTAS(c, VIAS, p):
        M_ps = VIAS/c_0
        q = ((M_ps*M_ps*(k-1)/2 + 1) ** (k/(k-1)) - 1)*p_0
        Mx = ((((q/p+1)**((k-1)/k) - 1)*2/(k-1)))**(1/2)
        vx = c * Mx
        # vx = VIAS
        return vx, Mx
    
    # Initialize inputs, desired order: t, h, s, vx, Mx, vz, theta, T, rho, c, cd0, ivx
    if h_cruise < h_final:
        vx = [];
        Mx = [];
        ivx = []; ivx0 = descentprofile[8]; ivx.append(ivx0)
        vx0, Mx0 = VTAS(c_cruise, ivx0, p_cruise); vx.append(vx0); Mx.append(Mx0)
        vz = []; vz0 = descentprofile[9]; vz.append(vz0)
        cd0 = []; cd0.append(cd0_init + cd0_landing)
    elif h_cruise < h_fl100:
        vx = [];
        Mx = [];
        ivx = []; ivx0 = descentprofile[4]; ivx.append(ivx0)
        vx0, Mx0 = VTAS(c_cruise, ivx0, p_cruise); vx.append(vx0); Mx.append(Mx0)
        vz = []; vz0 = descentprofile[5]; vz.append(vz0)
        cd0 = []; cd0.append(cd0_init + cd0_app)
    elif h_cruise < h_fl240:
        vx = [];
        Mx = [];
        ivx = []; ivx0 = descentprofile[2]; ivx.append(ivx0)
        vx0, Mx0 = VTAS(c_cruise, ivx0, p_cruise); vx.append(vx0); Mx.append(Mx0)
        vz = []; vz0 = descentprofile[3]; vz.append(vz0)
        cd0 = []; cd0.append(cd0_init + cd0_d)
    else:
        vx = []; vx0 = descentprofile[0]*c_cruise; vx.append(vx0)
        Mx = []; Mx0 = descentprofile[0]; Mx.append(Mx0)
        ivx = []; ivx0 = 0; ivx.append(ivx0)
        vz = []; vz0 = descentprofile[1]; vz.append(vz0)
        cd0 = []; cd0.append(cd0_init + cd0_id)
    t = []; t0 = 0; t.append(t0)
    h = []; h0 = h_cruise; h.append(h0)
    s = []; s0 = 0; s.append(s0)
    theta = []; theta0 = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(theta0)
    T = []; T.append(T_cruise)
    rho = []; rho.append(rho_cruise)
    c = []; c.append(c_cruise)
    
    ## Initialise hold inputs
    t_hold_total = []
    h_hold = []
    s_hold_total =[]
    vx_hold = []
    Mx_hold = []
    vz_hold = []
    theta_hold = []
    cd0_hold_total = []
    ivx_hold = []
    T_hold = []
    rho_hold = [] 
    c_hold = [] 
    
    h_trigger = 0
    t_step = num_par.t_step_descent
    
    while h[h_trigger] > 0:
        if h[h_trigger] >= h_fl240:
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            Mxnew = descentprofile[0]; Mx.append(Mxnew)
            vxnew = cnew*Mxnew; vx.append(vxnew); ivx.append(0)
            vznew = descentprofile[1]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init + cd0_id; cd0.append(cd0new)
        elif h[h_trigger] >= h_fl100 and h[h_trigger] <= h_fl240:
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            ivxnew = descentprofile[2]; ivx.append(ivxnew)
            vxnew, Mxnew = VTAS(c[-1], ivx[-1], p); vx.append(vxnew); Mx.append(Mxnew)
            vznew = descentprofile[3]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init + cd0_d; cd0.append(cd0new)
        elif h[h_trigger] >= h_final and h[h_trigger] <= h_fl100:
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            ivxnew = descentprofile[4]; ivx.append(ivxnew)
            vxnew, Mxnew = VTAS(c[-1], ivx[-1], p); vx.append(vxnew); Mx.append(Mxnew)
            vznew = descentprofile[5]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init + cd0_app; cd0.append(cd0new)
            if hnew < h_final:
                ## Initialise holding
                t_hold_steps = math.ceil(t_hold/t_step)
                t_hold_total.append(tnew)
                hnew_2 = hnew + t_step*vz[-1]; h_hold.append(hnew_2)
                snew_2 = snew + t_step*vx[-1]; s_hold_total.append(snew_2)
                Tnew, rhonew, cnew = ISA(hnew_2); T_hold.append(Tnew); rho_hold.append(rhonew); c_hold.append(cnew)
                p = rhonew*R*Tnew
                ivxnew_2 = descentprofile[6]; ivx_hold.append(ivxnew_2)
                vxnew_2, Mxnew_2 = VTAS(c_hold[-1], ivx_hold[-1], p); vx_hold.append(vxnew_2); Mx_hold.append(Mxnew_2)
                vznew_2 = descentprofile[7]; vz_hold.append(vznew_2)
                thetanew_2 = np.arctan(vz_hold[-1]/vx_hold[-1])/np.pi*180; theta_hold.append(thetanew_2)
                cd0new_2 = cd0_init + cd0_hold; cd0_hold_total.append(cd0new_2)
                ## Loop holding
                for i in range(t_hold_steps):
                    tnew_2 = t_hold_total[i] + t_step; t_hold_total.append(tnew_2)
                    hnew_2 = h_hold[i] + t_step*descentprofile[7]; h_hold.append(hnew_2)
                    snew_2 = s_hold_total[i] + t_step*vx_hold[-1]; s_hold_total.append(snew_2)
                    T_hold.append(Tnew); rho_hold.append(rhonew); c_hold.append(cnew)
                    ivx_hold.append(ivxnew_2); vx_hold.append(vxnew_2); Mx_hold.append(Mxnew_2); vz_hold.append(vznew_2); theta_hold.append(thetanew_2)
                    cd0_hold_total.append(cd0new_2)
                    h_trigger += 1
                t_hold_total.pop(0); h_hold.pop(0); s_hold_total.pop(0); T_hold.pop(0); rho_hold.pop(0); c_hold.pop(0); ivx_hold.pop(0); vx_hold.pop(0); Mx_hold.pop(0); vz_hold.pop(0); theta_hold.pop(0); cd0_hold_total.pop(0)
                t.extend(t_hold_total)
                h.extend(h_hold)
                s.extend(s_hold_total)
                vx.extend(vx_hold)
                Mx.extend(Mx_hold)
                vz.extend(vz_hold)
                theta.extend(theta_hold)
                T.extend(T_hold)
                rho.extend(rho_hold)
                c.extend(c_hold)
                cd0.extend(cd0_hold_total)
                ivx.extend(ivx_hold)
        
        else:
            tnew = t[h_trigger] + t_step; t.append(tnew)
            hnew = h[h_trigger] + t_step*vz[-1]; h.append(hnew)
            snew = s[h_trigger] + t_step*vx[-1]; s.append(snew)
            Tnew, rhonew, cnew = ISA(hnew); T.append(Tnew); rho.append(rhonew); c.append(cnew)
            p = rhonew*R*Tnew 
            ivxnew = descentprofile[8]; ivx.append(ivxnew)
            vxnew, Mxnew = VTAS(c[-1], ivx[-1], p); vx.append(vxnew); Mx.append(Mxnew)
            vznew = descentprofile[9]; vz.append(vznew)
            thetanew = np.arctan(vz[-1]/vx[-1])/np.pi*180; theta.append(thetanew)
            cd0new = cd0_init + cd0_landing; cd0.append(cd0new)    
                
        h_trigger += 1
    aircraft_descentprofile = np.column_stack([t, h, s, vx, Mx, vz, theta, T, rho, c, cd0, ivx])
    v_hold = descentprofile[6]

    
    return aircraft_descentprofile, v_hold