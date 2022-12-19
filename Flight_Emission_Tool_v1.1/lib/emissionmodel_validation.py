# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:39:41 2022

@author: 921677
"""

# 0. Input analysis type (and file name)
# 1. Input flight distances
# 2a. Input default n_p and m_freight for each aircraft type
# 2b. Input numerical parameters (for verfification purposes)
# 3. Run f_main for every aircraft and flight distance
# 4. Store in csv

import time
start = time.time()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate
from dataclasses import dataclass
from lib.f_main import f_main

## ========================= General input parameters =========================
## Analaysis type
analysis_type = 'single validation'

## Distance range
r = np.array([232,370,463,926,1389,1852,2778,3704,4630,5556,6482,7408,8334,9260,10186,11112,12038,12964,13890,14816,15742])*1000
# r = np.array([10000, 20000])
## Cargo load

## ========================= Validation aircraft type =========================
aircraft = 'CR9'

# Select from:
# BCS1,BCS3,A306F,A310F,A318,A319,A320,A321,A19N,A20N,A21N,A332,A333,A338,A339,A343,A346,A359,...
# A35K,A388,B733,B734,B734F,B735,B737,B738,B739,B38M,B744,B744F,B752,B752F,B763,B763F,B772,B77LF,...
# B77W,B788,B789,B78X,E175,E190,E195,E290,E295,F70,F100     

## Analysis inputs
@dataclass
class input_parameters:
    # Pax input parameters
    full_economy:       bool = True                     # Specify aircraft seat configuration (full economy or 2/3 class configuration)
    overwrite_ns:       int = -1                        # Specify number of seats on aircraft, use -1 for default
    n_p_load_factor:    float = 0.8                    # Passenger load factor
    dm_payload:         float = 0                       # change in absolute payload
    dm_pax:             float = 0   	                # change in average payload
    m_pax:              float = 100.2                   # Average pax mass (passenger + carry-on baggage), don't provide if m_pas is not 0
    overwrite_m_freight:float = 0 
    p_f_factor:         float = 0.9
     
    # Secondary input parameters 
    t_hold:             float = 0               # Arrival holding time in minutes
    t_taxi_out:         float = 10.5            # Taxi out time in minutes
    t_taxi_in:          float = 5.3             # Taxi in time in minutes
    t_alt:              float = 45              # Alternate airport flight time in minutes
    t_fr:               float = 30              # Final reserve flight duration in minutes
    
    # Driving comparison
    car_TtW = 0.1223                            # car driving kg CO2/km
    car_WtT = 0.0318                            # car driving kg CO2/km
    
    # Analysis type
    fuel_type:          str = 'Jet-A1'
    conversion_metric:  str = 'GWP_100_star'
    reference:          str = '(Lee, 2021)'

class numerical_parameters:
    t_step_climb:       int = 1
    t_step_descent:     int = 1
    t_step_cruise:      int = 10
    
## Time corrections (minutes to seconds)
input_parameters.t_hold = input_parameters.t_hold*60
input_parameters.t_taxi_out = input_parameters.t_taxi_out*60
input_parameters.t_taxi_in = input_parameters.t_taxi_in*60
  
if analysis_type == 'verification':
    ## Read aircraftproperties
    aircraftproperties = pd.read_csv('./data/aircraftproperties.csv',sep=';',index_col='Index')
    aircraft_index = aircraftproperties.index.tolist()
    aircraftproperties_np = aircraftproperties.to_numpy()
    
    ver_matrix = np.zeros([np.size(aircraft_index), np.size(r)])
    
    for i in range(np.size(aircraft_index)):
        if aircraftproperties_np[i,14] == 'nb':
            input_parameters.full_economy = True
        elif aircraftproperties_np[i,14] == 'wb':
            input_parameters.full_economy = False

        aircraft = aircraft_index[i]
        for j in range(np.size(r)):
            (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max, ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise, total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb, trip_properties, total_fuel_taxi, total_fuel_trip, total_fuel_CD, total_fuel_CR, E_taxi, E_TO, emissions) = f_main(input_parameters, numerical_parameters, aircraft, r[j])
            ver_matrix[i,j] = d_ver

elif analysis_type == 'single validation':
    # Read aircraftproperties
    aircraftproperties = pd.read_csv('./data/aircraftproperties.csv',sep=';',index_col='Index')
    aircraft_index = aircraftproperties.index.tolist()
    aircraftproperties_np = aircraftproperties.to_numpy()
    index = aircraft_index.index(aircraft)

    total_fuel_matrix = np.zeros(np.size(r))
    ver_matrix = np.zeros(np.size(r))
    if aircraftproperties_np[index,16] == 'nb':
        input_parameters.full_economy = True
    elif aircraftproperties_np[index,16] == 'wb':
        input_parameters.full_economy = False
        
    for j in range(np.size(r)):
        (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max, ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise, total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb, trip_properties, total_fuel_taxi, total_fuel_trip, total_fuel_CD, total_fuel_CR, E_taxi, E_TO, emissions) = f_main(input_parameters, numerical_parameters, aircraft, r[j])
        ver_matrix[j] = d_ver
        if d_ver == 0:
            total_fuel_matrix[j] = total_fuel_trip
    print(total_fuel_matrix)
elif analysis_type == 'multi validation':
    ## Read aircraftproperties
    aircraftproperties = pd.read_csv('./data/aircraftproperties.csv',sep=';',index_col='Index')
    aircraft_index = aircraftproperties.index.tolist()
    aircraftproperties_np = aircraftproperties.to_numpy()
    
    fuel_matrix = np.zeros([np.size(aircraft_index), np.size(r)])
    for i in range(np.size(aircraft_index)):
        if aircraftproperties_np[i,14] == 'nb':
            input_parameters.full_economy = True
        elif aircraftproperties_np[i,14] == 'wb':
            input_parameters.full_economy = False
    
        aircraft = aircraft_index[i]
        for j in range(np.size(r)):
            (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max, ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise, total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb, trip_properties, total_fuel_taxi, total_fuel_trip, total_fuel_CD, total_fuel_CR, E_taxi, E_TO, emissions) = f_main(input_parameters, numerical_parameters, aircraft, r[j])
            if d_ver == 0:   
                fuel_matrix[i,j] = total_fuel_trip


time = time.time() - start