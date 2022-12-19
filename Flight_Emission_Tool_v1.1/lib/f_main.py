# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 10:10:18 2022

@author: SYSTEM
"""
import numpy as np
import pandas as pd


from lib.aircraftclimbprofile import aircraft_climbprofile
from lib.aircraftdescentprofile import aircraft_descentprofile
from lib.landingweightapproximation import landing_weight
from lib.aircraftdescentfc import descent_fc
from lib.aircraftcruisefc import cruise_fc
from lib.aircraftclimbfc import climb_fc
from lib.aircrafttripanalysis import trip_analysis
from lib.emissionsanalysis import emissions_analysis
from lib.aircraftproperties import aircraftproperties_data


## Engine offdesign fuel consumption penalty
TSFC_idle_penalty = 1.6        # When engines operate offdesign (N1 /= 90%), the TSFC is not optimal
TSFC_FT_penalty   = 1.1
F_idle_perc = 0.07                      # Idle thrust percentage of max thrust
consumption_prop = np.array([TSFC_idle_penalty, TSFC_FT_penalty, F_idle_perc])

def f_main(par, num_par, aircraft, r):
    ## Range correction (to correct for deviations from great circle distance, for instance caused by the use of airways)
    if r < 550E3:
        r_corrected = r + 90E3
    elif r < 5500E3 and r > 550E3:
        r_corrected = r + 100E3
    else:
        r_corrected = r + 125E3
    
    ## Alternate and final reserve requirements
    alt_prop = np.array([par.t_alt, par.t_fr]) 
    
    ## Load aircraft properties

    (aircraftproperties, aircraftproperties_all, cruise_fl, cruise_alt, cruise_alt_max, ac_type) = aircraftproperties_data(aircraft, par.full_economy, par.n_seats, r_corrected) # returns MTOW, fuel mass, cruise velocity, wing surface area, wing span, number of passengers, engine efficiency, LD ratio, Cl, Cd, Cd0, Cdi, range
    # n_p = aircraftproperties[7]*par.n_p_load_factor
    n_p = par.n_passengers
    
    ## Load climb profile
    climbprofile, cruise_vel = aircraft_climbprofile(aircraftproperties, aircraft, cruise_alt, num_par)
         
    ## Load descent profile
    (descentprofile, v_hold) = aircraft_descentprofile(aircraftproperties, aircraft, cruise_alt, par.t_hold, num_par)
       
    ## Get minimum and maximum flight distance
    d_min = max(climbprofile[:,2])+max(descentprofile[:,2])
    d_max = aircraftproperties[13]*1000 
   
    if r_corrected < d_min:
        d_ver = 1
    elif r > d_max:
        d_ver = 2
    else:
        d_ver = 0
    
    ## Calculate landing weight
    W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight = landing_weight(aircraftproperties, par, n_p, v_hold, consumption_prop, alt_prop, ac_type)
    
    ## Read thrust penalty mapping
    thrust_var = pd.read_csv('./data/thrust_variation.csv',sep=';')
    thrust_var = np.transpose(thrust_var.to_numpy())  
  
    ## Calculate descent fuel consumption
    total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise = descent_fc(aircraftproperties, descentprofile, cruise_alt_max, consumption_prop, W_start_alt, thrust_var)
    
    ## Calculate cruise fuel consumption
    total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise = cruise_fc(aircraftproperties, r_corrected, climbprofile, descentprofile, cruise_alt, cruise_vel, W_descent, num_par)

    ## Calculate climb fuel consumption
    total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb = climb_fc(aircraftproperties, climbprofile, cruise_alt_max, consumption_prop, W_cruise, thrust_var, F_opt_cruise)


    trip_properties, total_fuel_taxi, total_fuel_trip, total_fuel_CD, total_fuel_CR, E_taxi, E_TO = trip_analysis(aircraftproperties, consumption_prop, par.t_taxi_in, par.t_taxi_out, climbprofile, descentprofile, t_cruise, r_cruise, fc_climb, fc_cruise, fc_descent, total_fuel_TO, W_climb, W_cruise, W_descent, F_climb, F_cruise, F_descent)

    emissions = emissions_analysis(trip_properties, E_taxi, E_TO, par.fuel_type, par.conversion_metric, par.reference)

    fuel_consumption = {'total_fuel_descent': total_fuel_descent,
                        'total_fuel_cruise': total_fuel_cruise,
                        'total_fuel_climb': total_fuel_climb,
                        'total_fuel_TO': total_fuel_TO,
                        'total_fuel_taxi': total_fuel_taxi}

    results = (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max,
               ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt,
               W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent,
               W_descent, F_descent, F_opt_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, fc_climb,
               W_climb, F_climb, trip_properties, E_taxi, E_TO)

    return results, emissions, fuel_consumption
