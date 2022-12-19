# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 11:53:14 2021

@author: 921677
"""

import numpy as np
import pandas as pd


from lib.ISA import ISA
from lib.determinecruisealt import determine_cruise_alt

def aircraftproperties_data(aircraft, full_economy, overwrite_ns, r_corrected):
    ## Physical constants 
    rho_f = 0.786   # kerosene density (kg/l)
    g = 9.81
    e0 = 0.8
    # h_cruise = 11000 # cruise altitude in m
    T_0 = 288.15    # sea level temperature (K)
    p_0 = 101325    # sea level pressure (Pa)
    dT = -6.5E-3    # change in temperature with altitude (K/m)
    R = 287         # specific gas constant

    
    # T_cruise = T_0 + dT*h_cruise
    # p_cruise = p_0*(T_cruise/T_0)**(-g/(dT*R))
    # rho_cruise = p_cruise/(R*T_cruise)
    
    
    ## Aircraft properties
    aircraftproperties = pd.read_csv('./data/aircraftproperties.csv',index_col='Index')
    aircraft_index = aircraftproperties.index.tolist()
    mtow = aircraftproperties.MTOW.to_numpy()
    oew = aircraftproperties.OEW.to_numpy()
    m_fuel = aircraftproperties.M_fuel.to_numpy()
    v_cruise = aircraftproperties.V_cruise.to_numpy()
    S = aircraftproperties.S.to_numpy()
    b = aircraftproperties.b.to_numpy()
    if full_economy == True:
        n = aircraftproperties.n_full.to_numpy()
    else:
        n = aircraftproperties.n.to_numpy()
    LD = aircraftproperties.LD.to_numpy()
    r = aircraftproperties.r.to_numpy()
    TSFC = aircraftproperties.TSFC.to_numpy()
    TSFC_SL = aircraftproperties.TSFC_SL.to_numpy()
    T_max = aircraftproperties.T_max.to_numpy()
    ac_type = aircraftproperties.type.to_numpy()
    ICAO = aircraftproperties.ICAO.to_numpy()
    IATA = aircraftproperties.IATA.to_numpy()
    variable_list =  ["MTOW","OEW","M_fuel","V_cruise","h_cruise","S", "b", "n", "LD","cl_cruise","cd_cruise","cd0", "cdi_cruise", "r", "TSFC", "TSFC_SL", "T_max"]
    index = aircraft_index.index(aircraft)
    
    
    ## Obtain most seen cruise altitude

    cruise_fl, cruise_alt, cruise_fl_max, cruise_alt_max = determine_cruise_alt(aircraft, r_corrected)
    h_cruise = cruise_alt_max
    
    # Calculate aircraft cruise properties
    T_cruise = np.zeros(np.size(h_cruise))
    rho_cruise = np.zeros(np.size(h_cruise))
    c_cruise = np.zeros(np.size(h_cruise))
    for i in range(np.size(h_cruise)):
        T_cruise[i], rho_cruise[i], c_cruise[i] = ISA(h_cruise[i])
    
    D = mtow*g/LD
    cl_cruise = (g*mtow)/(0.5*rho_cruise*v_cruise**2*S)                      # aircraft cruise lift coefficient, using average weight and cruise velocity
    cdi = (cl_cruise**2)/(np.pi*b**2*e0/S)
    cd = D/(0.5*rho_cruise*v_cruise**2*S)
    cd0 = cd - cdi

    data = np.transpose(np.array([mtow[index], oew[index], m_fuel[index], v_cruise[index], h_cruise[index], S[index], b[index], n[index], LD[index], cl_cruise[index], cd[index], cd0[index], cdi[index], r[index], TSFC[index], TSFC_SL[index], T_max[index]]))
    cruise_alt = cruise_alt[index]
    cruise_fl = cruise_fl[index]
    cruise_alt_max = cruise_alt_max[index]
    ac_type = ac_type[index]
    
    #aircraft_index = ["BCS1","BCS3","A318","A319","A320","A321","A19N","A20N","A21N","A332", "A333", "A338", "A339", "A359", "A388", "B737", "B738","B744", "B772", "B77W", "B788"]
    
    
    if overwrite_ns != -1:
        data[7] = overwrite_ns
        n = np.ones(np.shape(n))*overwrite_ns
    
    
    dfdata = np.column_stack([mtow, oew, m_fuel, v_cruise, h_cruise, S, b, n, LD, cl_cruise, cd, cd0, cdi, r, TSFC, TSFC_SL, T_max])
    dataframe = pd.DataFrame(dfdata, index=aircraft_index, columns=variable_list)
    return data, dataframe, cruise_fl, cruise_alt, cruise_alt_max, ac_type
