# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:57:04 2022

@author: 921677
"""
import numpy as np
import math 
## Landing mass approximation function
def landing_weight(aircraftproperties, par, n_p, v_hold, consumption_prop, alt_prop, ac_type):
    ## Constants
    g= 9.81
    T_0 = 288.15    # sea level temperature (K)
    p_0 = 101325    # sea level pressure (Pa)
    dT = -6.5E-3    # change in temperature with altitude (K/m)
    R = 287         # specific gas constant
    cd0_hold = 0.06 # Hold drag penalty (e.g. flaps)
    e0 = 0.8        # Oswald factor
    
    ## Aircraft specific inputs
    MTOW = aircraftproperties[0]*g
    OEW = aircraftproperties[1]*g
    M_fuel = aircraftproperties[2]
    v_cruise = aircraftproperties[3]
    S = aircraftproperties[5]
    b = aircraftproperties[6]
    n_s = aircraftproperties[7]             # Number of seats on aircraft
    cd0_init = aircraftproperties[11]   

    ## Analysis inputs
    m_pax = par.m_pax
    overwrite_m_freight = par.overwrite_m_freight
    dm_bag = par.dm_payload 
    t_taxi_in = par.t_taxi_in
    p_f_factor = par.p_f_factor

    ## Additional fuel
    # Taxi in fuel
    TSFC_idle_penalty = consumption_prop[0]
    T_idle_perc = consumption_prop[2]
    TSFC_SL = TSFC_idle_penalty*aircraftproperties[15]/1E6
    T_idle = T_idle_perc*aircraftproperties[16]
    taxi_in_fuel = TSFC_SL*T_idle*t_taxi_in

    ## Calculate cargo weight    
    if overwrite_m_freight != -1:
        m_freight = overwrite_m_freight
    elif overwrite_m_freight == -1 and ac_type != 'cg':
        m_freight = (n_p*m_pax + n_s*50)/p_f_factor - (n_p*m_pax + n_s*50)       # 50 kg add_on per seat for on-board equipment and infrastructure
    elif ac_type == 'cg':
        m_freight = overwrite_m_freight
    
    ## Minimum landing fuel
    # Minimum required landing fuel (extreme scenario)
    W_landing_ext = OEW + (n_p*m_pax)*g + m_freight*g + dm_bag*g + taxi_in_fuel*g    
    M_landing_ext = W_landing_ext/g
    
    
    # Final reserve fuel: fly 30 minutes at 1500 feet at v_hold (use Breguet)
    # Estimate final reserve fuel consumption using estimated LD (assume landing mass, SL TSFC)
    t_fr = alt_prop[1]
    rho_fr = 1.121                         # holding altitude (914.4m) air density (ISA conditions)
    cd0_fr = cd0_init + cd0_hold
    D_fr = (1/2)*rho_fr*v_hold**2*cd0_fr*S + (2*(W_landing_ext)**2)/(np.pi*e0*b**2*rho_fr*v_hold**2)
    L_fr = W_landing_ext
    LD_fr = L_fr/D_fr
    r_fr = t_fr*60*v_hold
    ct_SL = aircraftproperties[15]/1E6*g
    W_start_fr = W_landing_ext*math.exp(r_fr*(1/LD_fr)*ct_SL/v_hold) # Breguet equation
    M_start_fr = W_start_fr/g
    M_fuel_fr = (W_start_fr - W_landing_ext)/g

    # Alternate fuel: assume 45 minute cruise
    # Estimate alternate fuel using estimated LD (assume final reserve mass, cruise TSFC)
    t_alt = alt_prop[0]
    h_cruise = aircraftproperties[4] # cruise altitude in m
    T_cruise = T_0 + dT*h_cruise; p_cruise = p_0*(T_cruise/T_0)**(-g/(dT*R))
    rho_cruise = p_cruise/(R*T_cruise)
    r_alt = v_cruise*t_alt*60
    D_alt = (1/2)*rho_cruise*v_cruise**2*cd0_init*S + (2*(W_start_fr)**2)/(np.pi*e0*b**2*rho_cruise*v_cruise**2)
    L_alt = W_start_fr
    LD_alt = L_alt/D_alt
    ct = aircraftproperties[14]/1E6*g
    W_start_alt = W_start_fr*math.exp(r_alt*(1/LD_alt)*ct/v_cruise)
    M_start_alt = W_start_alt/g
    M_fuel_alt = (W_start_alt - W_start_fr)/g

    # Remaining fuel upon landing after normal trip
    landing_fuel = taxi_in_fuel + M_fuel_alt + M_fuel_fr
    reserve_fuel = M_fuel_alt + M_fuel_fr
    return W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight