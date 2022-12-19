# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 10:56:02 2022

@author: Pieter
"""

import time
start = time.time()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate
import dataclasses
from lib.f_main import f_main
from lib.findnearest import find_nearest

## ========================= General input parameters =========================

r = 5055.24E3


# aircraft mission distance in m (GCD distance between airports)

# 1 nautical mile = 1852 metres

## ====================== Trigger aircraft to be analysed =====================
# Single aircraft
single_ac  = "332"         # Choose aircraft from list below:
    
# Multi aircraft
regional   = False
narrowbody = False
widebody   = True

## ======================== Secondary input parameters ========================
## Pack input parameters
@dataclasses.dataclass
class input_parameters:
    # Pax input parameters
    full_economy:       bool = True                    # Specify aircraft seat configuration (full economy or 2/3 class configuration)
    overwrite_ns:       int =264                     # Specify number of seats on aircraft, use -1 for default
    n_p_load_factor:    float = 1                   # Passenger load factor
    dm_payload:         float = 0                       # change in absolute payload
    dm_pax:             float = 0   	                # change in average payload
    m_pax:              float = 100.2                   # Average pax mass (passenger + carry-on baggage), don't provide if m_pas is not 0
    m_pas_addons:       float = 50 
    overwrite_m_freight:float = -1 
    p_f_factor:         float = 0.7996
               
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
    
@dataclasses.dataclass
class numerical_parameters:
    t_step_climb:       int = 1
    t_step_descent:     int = 1
    t_step_cruise:      int = 10
    
## Time corrections (minutes to seconds)
input_parameters.t_hold = input_parameters.t_hold*60
input_parameters.t_taxi_out = input_parameters.t_taxi_out*60
input_parameters.t_taxi_in = input_parameters.t_taxi_in*60
    
## =========================== Trigger output type ============================
analysis_type =1               
printing = True
plotting = True
sorting = False


## ============================= Numerical contants ===========================
m_steps = 2
@dataclasses.dataclass
class emissions_set:
    CO2_WtT_set = []
    non_CO2_WtT_set = []
    CO2_TtW_set = []
    non_CO2_TtW_set = []


## ================================= Analysis =================================
if analysis_type == 0:
    aircraft = single_ac
    input_parameters.dm_payload = 0
    input_parameters.dm_pax = 0
    (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max, ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise, total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb, trip_properties, total_fuel_taxi, total_fuel_trip, total_fuel_CD, total_fuel_CR, E_taxi, E_TO, emissions) = f_main(input_parameters, numerical_parameters, aircraft,r)
    
    ## Verification and validation
    M_TO = max(trip_properties[:,5])/9.81
    M_TO_max = aircraftproperties[0]
    M_f_TO = landing_fuel + total_fuel_trip - total_fuel_taxi/(input_parameters.t_taxi_in+input_parameters.t_taxi_out)*input_parameters.t_taxi_in
    M_f_TO_max = aircraftproperties[2]
    
    # Find 3000ft/9km indices in trip analysis (directly from profiles?)

    H_CCD = 914.4       # 3000 ft in metres
    climb_idx = find_nearest(climbprofile[:,1],H_CCD)
    descent_idx = np.size(climbprofile[:,1]) + np.size(r_cruise) + find_nearest(descentprofile[:,1],H_CCD)
    r_CCD = trip_properties[descent_idx,1] - trip_properties[climb_idx,1]
    total_fuel_CCD = (trip_properties[climb_idx,5] - trip_properties[descent_idx,5])/9.81
    total_fuel_LTO = total_fuel_trip - total_fuel_CCD
    
    ## Printing
    print('Verification analysis:')   
    print('Total flight trip fuel consumption is %.2f kg'%total_fuel_trip)
    print('MTOW is %.0f kg,'%M_TO_max, 'actual TO weight is %.0f kg'%M_TO) 
    print('Maximum fuel load is %.0f kg,'%M_f_TO_max, 'actual fuel load is %.0f'%M_f_TO)
    print('\n')
    print('Validation analysis:')
    print('Climb-cruise-descent distance is %.2f km'%(r_CCD/1000))
    
    ## Plotting
    plt.figure(0,figsize=(6,5))
    # plt.title('%s flight path on ' %aircraft + '%.0fkm mission' %(r/1000))
    plt.ylabel('Altitude (km)')
    plt.xlabel('Time travelled (min)')
    plt.plot(trip_properties[:,0]/60,trip_properties[:,3]/1000,linewidth=2)
    plt.grid()
    # plt.ylim(bottom = 0) 
    
    plt.figure(1,figsize=(6,5))
    # plt.title('%s flight path on ' %aircraft + '%.0fkm mission' %(r/1000))
    plt.ylabel('Thrust setting (kN)')
    plt.xlabel('Time travelled (min)')
    plt.plot(trip_properties[:,0]/60,trip_properties[:,6]/1000,linewidth=2)
    plt.grid()
    # plt.ylim(bottom = 0) 
    
    plt.figure(2,figsize=(6,5))
    # plt.title('%s flight path on ' %aircraft + '%.0fkm mission' %(r/1000))
    plt.ylabel('Fuel consumption (kg/s)')
    plt.xlabel('Time travelled (min)')
    plt.plot(trip_properties[:,0]/60,trip_properties[:,4],linewidth=2)
    plt.grid()
    # plt.ylim(bottom = 0) 
    
    plt.figure(3,figsize=(6,5))
    # plt.title('%s flight path on ' %aircraft + '%.0fkm mission' %(r/1000))
    plt.ylabel('Aircraft weight (kN)')
    plt.xlabel('Time travelled (min)')
    plt.plot(trip_properties[:,0]/60,trip_properties[:,5]/1000,linewidth=2)
    plt.grid()
    # plt.ylim(bottom = 0) 

elif analysis_type == 1: # single aircraft fuel consumption
    aircraft = single_ac
    input_parameters.dm_payload = 0
    input_parameters.dm_pax = 0
    (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max, ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise, total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb, trip_properties, total_fuel_taxi, total_fuel_trip, total_fuel_CD, total_fuel_CR, E_taxi, E_TO, emissions) = f_main(input_parameters, numerical_parameters, aircraft,r)
    emissions_set.CO2_WtT_set.append(emissions.CO2_WtT)
    emissions_set.non_CO2_WtT_set.append(emissions.non_CO2_WtT)
    emissions_set.CO2_TtW_set.append(emissions.CO2_TtW)
    emissions_set.non_CO2_TtW_set.append(emissions.non_CO2_TtW)
    CO2_TtW = emissions.CO2_TtW
    CO2_WtW = emissions.CO2_WtT + emissions.CO2_TtW
    CO2e_TtW = emissions.CO2_TtW + emissions.non_CO2_TtW
    CO2e_WtW = emissions.CO2_TtW + emissions.non_CO2_TtW + emissions.CO2_WtT + emissions.non_CO2_WtT
    
    payload = (n_p*input_parameters.m_pax + aircraftproperties[7]*input_parameters.m_pas_addons)+m_freight
    
    if n_p > 0:
        fuel_consumption_pp = total_fuel_trip/n_p
        fuel_consumption_pkg = total_fuel_trip/payload
        fuel_consumption_pp_2 = fuel_consumption_pkg*(input_parameters.m_pax + input_parameters.m_pas_addons)
        CO2_TtW_pp = CO2_TtW/n_p
        CO2_WtW_pp = CO2_WtW/n_p
        CO2e_TtW_pp = CO2e_TtW/n_p
        CO2e_WtW_pp = CO2e_WtW/n_p
    else:
        fuel_consumption_pp = 0
        CO2_TtW_pp = 0
        CO2_WtW_pp = 0
        CO2e_TtW_pp = 0
        CO2e_WtW_pp = 0
        
    ## Printing
    if printing == True:
        print("Total trip fuel consumption is", "%.5f" % total_fuel_trip, "kg for " + str(aircraft), "on %.0fkm mission" %(r/1000), "or %.2f"%fuel_consumption_pp, "(%.2f)" %fuel_consumption_pp_2, "kg fuel per passenger")
        print("Total trip CO2 emission is %.1f"%CO2_TtW, "kg CO2, or %.1f"%CO2_TtW_pp, "kg CO2/passenger, or %.3f"%(CO2_TtW_pp/(r/1000)), "kg CO2/passenger/km (excludig upstream effects)")
        print("Total trip CO2 equivalent emission is %.1f"%CO2e_TtW, "kg CO2e, or %.1f"%CO2e_TtW_pp, "kg CO2e/passenger (excluding upstream effects)")
        print("Total trip CO2 equivalent emission is %.1f"%CO2e_WtW, "kg CO2e, or %.1f"%CO2e_WtW_pp, "kg CO2e/passenger (including upstream effects)")
    if plotting == True:
        plt.figure(0,figsize=(6,5))
        # plt.title('%s in air fuel consumption profile on ' %aircraft + '%.0fkm mission' %(r/1000))
        plt.ylabel('Fuel consumption (kg/s)')
        plt.xlabel('Time travelled (min)')
        plt.plot(trip_properties[:,0]/60,trip_properties[:,4])
        plt.ylim(bottom = 0) 
        plt.grid()
        
        plt.figure(1,figsize=(10,5))
        plt.title('%s CO2(e) emissions on ' %aircraft + '%.0fkm mission' %(r/1000))
        x = range(0,3,1)
        color_blue = 'tab:blue'
        plt.ylabel('Total trip CO2(e) emissions (kg/passenger)')
        plt.bar(0, CO2_TtW_pp, width=0.8, color=color_blue)
        plt.bar(1, CO2e_TtW_pp, width=0.8, color=color_blue)
        plt.bar(2, CO2e_WtW_pp, width=0.8, color=color_blue)
        labels = ['$CO_{2,TtW}$','$CO_{2}e_{TtW}$','$CO_{2}e_{WtW}$']
        plt.xticks(x, labels)

        plt.figure(2,figsize=(10,5))
        plt.title('%s CO2(e) emissions on ' %aircraft + '%.0fkm mission' %(r/1000))
        x = range(0,3,1)
        color_blue = 'tab:blue'
        plt.ylabel('Total trip CO2(e) emissions (kg/passenger/km)')
        plt.bar(0, CO2_TtW_pp/(r/1000), width=0.8, color=color_blue)
        plt.bar(1, CO2e_TtW_pp/(r/1000), width=0.8, color=color_blue)
        plt.bar(2, CO2e_WtW_pp/(r/1000), width=0.8, color=color_blue)
        labels = ['$CO_{2,TtW}$','$CO_{2}e_{TtW}$','$CO_{2}e_{WtW}$']
        plt.xticks(x, labels)

elif analysis_type == 2:
    aircraft = single_ac
    input_parameters.dm_payload = 0
    m_pax = np.linspace(input_parameters.m_pax,input_parameters.m_pax+input_parameters.dm_pax,m_steps)
    total_fuel_trip = np.zeros(np.size(m_pax))
    m_landing_ext = np.zeros(np.size(m_pax))
    emissions_all = np.array([])
    trip_properties_all = np.array([])
    
    for i in range(np.size(m_pax)):
        input_parameters.m_pax = m_pax[i]
        (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max, ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise, total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb, trip_properties, total_fuel_taxi, total_fuel_trip[i], total_fuel_CD, total_fuel_CR, E_taxi, E_TO, emissions) = f_main(input_parameters, numerical_parameters, aircraft,r)
        m_landing_ext[i] = W_landing_ext/9.81
        trip_properties = trip_properties[np.newaxis,...]
        if np.size(trip_properties_all) == 0:
            trip_properties_all = trip_properties
        else:
            trip_properties_all = np.concatenate((trip_properties_all, trip_properties))
        emissions_set.CO2_WtT_set.append(emissions.CO2_WtT)
        emissions_set.non_CO2_WtT_set.append(emissions.non_CO2_WtT)
        emissions_set.CO2_TtW_set.append(emissions.CO2_TtW)
        emissions_set.non_CO2_TtW_set.append(emissions.non_CO2_TtW)

    CO2_TtW = np.array(emissions_set.CO2_TtW_set)
    CO2_WtW = np.array(emissions_set.CO2_WtT_set) + np.array(emissions_set.CO2_TtW_set)
    CO2e_TtW = np.array(emissions_set.CO2_TtW_set) + np.array(emissions_set.non_CO2_TtW_set)
    CO2e_WtW = np.array(emissions_set.CO2_TtW_set) + np.array(emissions_set.non_CO2_TtW_set) + np.array(emissions_set.CO2_WtT_set) + np.array(emissions_set.non_CO2_WtT_set)
    if n_p > 0:
        fuel_consumption_pp = total_fuel_trip/n_p
        CO2_TtW_pp = CO2_TtW/n_p
        CO2_WtW_pp = CO2_WtW/n_p
        CO2e_TtW_pp = CO2e_TtW/n_p
        CO2e_WtW_pp = CO2e_WtW/n_p
    else:
        fuel_consumption_pp = 0
        CO2_TtW_pp = 0
        CO2_WtW_pp = 0
        CO2e_TtW_pp = 0
        CO2e_WtW_pp = 0
    
    driving_TtW = (CO2e_TtW[0]-CO2e_TtW[-1])/input_parameters.car_TtW
    driving_WtW = (CO2e_WtW[0]-CO2e_WtW[-1])/(input_parameters.car_TtW+input_parameters.car_WtT)
    
    if printing == True:
        print("Total trip reduction in fuel consumption is", "%.3f" %(total_fuel_trip[0]-total_fuel_trip[-1]), "kg for " + str(aircraft), "on %.0fkm mission" %(r/1000))
        print("Total trip reduction in CO2 emission is %.1f"%(CO2_TtW[0]-CO2_TtW[-1]), "kg CO2, or %.1f"%(CO2_TtW_pp[0]-CO2_TtW_pp[-1]), "kg CO2/passenger")
        print("Total trip reduction in CO2 equivalent emission is %.3f"%(CO2e_TtW[0]-CO2e_TtW[-1]), "kg CO2e (equivalent to %.1f km drive)"%driving_TtW, "or %.1f"%(CO2e_TtW_pp[0]-CO2e_TtW_pp[-1]), "kg CO2e/passenger (excluding upstream effects)")
        print("Total trip reduction in CO2 equivalent emission is %.3f"%(CO2e_WtW[0]-CO2e_WtW[-1]), "kg CO2e (equivalent to %.1f km drive)"%driving_WtW, "or %.1f"%(CO2e_WtW_pp[0]-CO2e_WtW_pp[-1]), "kg CO2e/passenger (including upstream effects)")
        
    if plotting == True:
        plt.figure(0,figsize=(6,5))
        # plt.title('%s in air fuel consumption profile on ' %aircraft + '%.0fkm mission' %(r/1000))
        plt.ylabel('Fuel consumption (kg/s)')
        plt.xlabel('Time travelled (min)')
        for i in range(np.size(m_pax)):
            legend_str = str('m_pax = %.1f' %m_pax[i] + ' kg')
            plt.plot(trip_properties_all[i,:,0]/60,trip_properties_all[i,:,4],label = legend_str)
        plt.ylim(bottom = 0)
        plt.legend(loc="upper right")
        plt.grid()
         
        plt.figure(1,figsize=(10,5))
        plt.title('%s CO2(e) emissions on ' %aircraft + '%.0fkm mission' %(r/1000))
        plt.ylabel('Total trip CO2(e) emissions (kg)')
        x = range(0,3,1)
        color_blue = 'tab:blue'
        color_orange = 'tab:orange'
        width = 0.40
        legend_str = str('Pax mass = %.0f' %m_pax[0] + ' kg')
        plt.bar(0-0.2, CO2_TtW[0], width=width, color=color_blue, label=legend_str)
        plt.text(0-0.2, CO2_TtW[0], str('%.0f'%CO2_TtW[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        legend_str = str('Pax mass = %.0f' %m_pax[-1] + ' kg')
        plt.bar(0+0.2, CO2_TtW[-1], width=width, color=color_orange, label=legend_str)
        plt.text(0+0.2, CO2_TtW[-1], str('%.0f'%CO2_TtW[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1-0.2, CO2e_TtW[0], width = width, color=color_blue)
        plt.text(1-0.2, CO2e_TtW[0], str('%.0f'%CO2e_TtW[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1+0.2, CO2e_TtW[-1], width = width, color=color_orange)
        plt.text(1+0.2, CO2e_TtW[-1], str('%.0f'%CO2e_TtW[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2-0.2, CO2e_WtW[0], width = width, color=color_blue)
        plt.text(2-0.2, CO2e_WtW[0], str('%.0f'%CO2e_WtW[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2+0.2, CO2e_WtW[-1], width = width, color=color_orange)
        plt.text(2+0.2, CO2e_WtW[-1], str('%.0f'%CO2e_WtW[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        labels = ['$CO_{2,TtW}$','$CO_{2}e_{TtW}$','$CO_{2}e_{WtW}$']
        plt.xticks(x, labels)
        plt.ylim(bottom = 0)
        plt.legend()
        
        plt.figure(2,figsize=(10,5))
        plt.title('%s CO2(e) emissions on ' %aircraft + '%.0fkm mission' %(r/1000))
        plt.ylabel('Total trip CO2(e) emissions (kg/passenger)')
        x = range(0,3,1)
        color_blue = 'tab:blue'
        color_orange = 'tab:orange'
        width = 0.40
        legend_str = str('Pax mass = %.0f' %m_pax[0] + ' kg')
        plt.bar(0-0.2, CO2_TtW_pp[0], width=width, color=color_blue, label=legend_str)
        plt.text(0-0.2, CO2_TtW_pp[0], str('%.1f'%CO2_TtW_pp[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        legend_str = str('Pax mass = %.0f' %m_pax[-1] + ' kg')
        plt.bar(0+0.2, CO2_TtW_pp[-1], width=width, color=color_orange, label=legend_str)
        plt.text(0+0.2, CO2_TtW_pp[-1], str('%.1f'%CO2_TtW_pp[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1-0.2, CO2e_TtW_pp[0], width = width, color=color_blue)
        plt.text(1-0.2, CO2e_TtW_pp[0], str('%.1f'%CO2e_TtW_pp[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1+0.2, CO2e_TtW_pp[-1], width = width, color=color_orange)
        plt.text(1+0.2, CO2e_TtW_pp[-1], str('%.1f'%CO2e_TtW_pp[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2-0.2, CO2e_WtW_pp[0], width = width, color=color_blue)
        plt.text(2-0.2, CO2e_WtW_pp[0], str('%.1f'%CO2e_WtW_pp[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2+0.2, CO2e_WtW_pp[-1], width = width, color=color_orange)
        plt.text(2+0.2, CO2e_WtW_pp[-1], str('%.1f'%CO2e_WtW_pp[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        labels = ['$CO_{2,TtW}$','$CO_{2}e_{TtW}$','$CO_{2}e_{WtW}$']
        plt.xticks(x, labels)
        plt.ylim(bottom = 0)
        plt.legend()
        
elif analysis_type == 3:
    aircraft = single_ac
    input_parameters.dm_pax = 0
    dm_bag = np.linspace(0,input_parameters.dm_payload,m_steps)
    total_fuel_trip = np.zeros(np.size(dm_bag))
    m_landing_ext = np.zeros(np.size(dm_bag))
    emissions_all = np.array([])
    trip_properties_all = np.array([])
    
    
    for i in range(np.size(dm_bag)):
        input_parameters.dm_payload = dm_bag[i]
        (r_corrected, aircraftproperties, aircraftproperties_all, n_p, cruise_fl, cruise_alt, cruise_alt_max, ac_type, climbprofile, cruise_vel, descentprofile, v_hold, d_min, d_max, d_ver, W_start_alt, W_landing_ext, W_start_fr, landing_fuel, reserve_fuel, m_freight, total_fuel_descent, fc_descent, W_descent, F_descent, F_opt_cruise, total_fuel_cruise, fc_cruise, W_cruise, F_cruise, t_cruise, r_cruise, total_fuel_climb, total_fuel_TO, fc_climb, W_climb, F_climb, trip_properties, total_fuel_taxi, total_fuel_trip[i], total_fuel_CD, total_fuel_CR, E_taxi, E_TO, emissions) = f_main(input_parameters, numerical_parameters, aircraft,r)
        m_landing_ext[i] = W_landing_ext/9.81
        trip_properties = trip_properties[np.newaxis,...]
        if np.size(trip_properties_all) == 0:
            trip_properties_all = trip_properties
        else:
            trip_properties_all = np.concatenate((trip_properties_all, trip_properties))
        emissions_set.CO2_WtT_set.append(emissions.CO2_WtT)
        emissions_set.non_CO2_WtT_set.append(emissions.non_CO2_WtT)
        emissions_set.CO2_TtW_set.append(emissions.CO2_TtW)
        emissions_set.non_CO2_TtW_set.append(emissions.non_CO2_TtW)

    CO2_TtW = np.array(emissions_set.CO2_TtW_set)
    CO2_WtW = np.array(emissions_set.CO2_WtT_set) + np.array(emissions_set.CO2_TtW_set)
    CO2e_TtW = np.array(emissions_set.CO2_TtW_set) + np.array(emissions_set.non_CO2_TtW_set)
    CO2e_WtW = np.array(emissions_set.CO2_TtW_set) + np.array(emissions_set.non_CO2_TtW_set) + np.array(emissions_set.CO2_WtT_set) + np.array(emissions_set.non_CO2_WtT_set)
    if n_p > 0:
        fuel_consumption_pp = total_fuel_trip/n_p
        CO2_TtW_pp = CO2_TtW/n_p
        CO2_WtW_pp = CO2_WtW/n_p
        CO2e_TtW_pp = CO2e_TtW/n_p
        CO2e_WtW_pp = CO2e_WtW/n_p
    else:
        fuel_consumption_pp = 0
        CO2_TtW_pp = 0
        CO2_WtW_pp = 0
        CO2e_TtW_pp = 0
        CO2e_WtW_pp = 0
    
    driving_TtW = (CO2e_TtW[0]-CO2e_TtW[-1])/input_parameters.car_TtW
    driving_WtW = (CO2e_WtW[0]-CO2e_WtW[-1])/(input_parameters.car_TtW+input_parameters.car_WtT)
    
    if printing == True:
        print("Total trip reduction in fuel consumption is", "%.3f" %(total_fuel_trip[0]-total_fuel_trip[-1]), "kg for " + str(aircraft), "on %.0fkm mission" %(r/1000))
        print("Total trip reduction in CO2 emission is %.1f"%(CO2_TtW[0]-CO2_TtW[-1]), "kg CO2, or %.2f"%(CO2_TtW_pp[0]-CO2_TtW_pp[-1]), "kg CO2/passenger")
        print("Total trip reduction in CO2 equivalent emission is %.3f"%(CO2e_TtW[0]-CO2e_TtW[-1]), "kg CO2e (equivalent to %.1f km drive)"%driving_TtW, "or %.2f"%(CO2e_TtW_pp[0]-CO2e_TtW_pp[-1]), "kg CO2e/passenger (excluding upstream effects)")
        print("Total trip reduction in CO2 equivalent emission is %.3f"%(CO2e_WtW[0]-CO2e_WtW[-1]), "kg CO2e (equivalent to %.1f km drive)"%driving_WtW, "or %.2f"%(CO2e_WtW_pp[0]-CO2e_WtW_pp[-1]), "kg CO2e/passenger (including upstream effects)")
        
    if plotting == True:
        plt.figure(0,figsize=(6,5))
        # plt.title('%s in air fuel consumption profile on ' %aircraft + '%.0fkm mission' %(r/1000))
        plt.ylabel('Fuel consumption (kg/s)')
        plt.xlabel('Time travelled (min)')
        for i in range(np.size(dm_bag)):
            legend_str = str('mass reduction = %.1f' %dm_bag[i] + ' kg')
            plt.plot(trip_properties_all[i,:,0]/60,trip_properties_all[i,:,4],label = legend_str)
        plt.ylim(bottom = 0)
        plt.legend(loc="upper right")
        plt.grid()
        
        plt.figure(1,figsize=(10,5))
        plt.title('%s CO2(e) emissions on ' %aircraft + '%.0fkm mission' %(r/1000))
        plt.ylabel('Total trip CO2(e) emissions (kg)')
        x = range(0,3,1)
        color_blue = 'tab:blue'
        color_orange = 'tab:orange'
        width = 0.40
        legend_str = str('Baggage mass reduction = %.0f' %dm_bag[0] + ' kg')
        plt.bar(0-0.2, CO2_TtW[0], width=width, color=color_blue, label=legend_str)
        plt.text(0-0.2, CO2_TtW[0], str('%.0f'%CO2_TtW[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        legend_str = str('Baggage mass reduction = %.0f' %dm_bag[-1] + ' kg')
        plt.bar(0+0.2, CO2_TtW[-1], width=width, color=color_orange, label=legend_str)
        plt.text(0+0.2, CO2_TtW[-1], str('%.2f'%CO2_TtW[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1-0.2, CO2e_TtW[0], width = width, color=color_blue)
        plt.text(1-0.2, CO2e_TtW[0], str('%.2f'%CO2e_TtW[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1+0.2, CO2e_TtW[-1], width = width, color=color_orange)
        plt.text(1+0.2, CO2e_TtW[-1], str('%.2f'%CO2e_TtW[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2-0.2, CO2e_WtW[0], width = width, color=color_blue)
        plt.text(2-0.2, CO2e_WtW[0], str('%.2f'%CO2e_WtW[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2+0.2, CO2e_WtW[-1], width = width, color=color_orange)
        plt.text(2+0.2, CO2e_WtW[-1], str('%.2f'%CO2e_WtW[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        labels = ['$CO_{2,TtW}$','$CO_{2}e_{TtW}$','$CO_{2}e_{WtW}$']
        plt.xticks(x, labels)
        plt.ylim(bottom = 0)
        plt.legend()
        
        plt.figure(2,figsize=(10,5))
        plt.title('%s CO2(e) emissions on ' %aircraft + '%.0fkm mission' %(r/1000))
        plt.ylabel('Total trip CO2(e) emissions (kg/passenger)')
        x = range(0,3,1)
        color_blue = 'tab:blue'
        color_orange = 'tab:orange'
        width = 0.40
        legend_str = str('Baggage mass reduction = %.0f' %dm_bag[0] + ' kg')
        plt.bar(0-0.2, CO2_TtW_pp[0], width=width, color=color_blue, label=legend_str)
        plt.text(0-0.2, CO2_TtW_pp[0], str('%.2f'%CO2_TtW_pp[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        legend_str = str('Baggage mass reduction = %.0f' %dm_bag[-1] + ' kg')
        plt.bar(0+0.2, CO2_TtW_pp[-1], width=width, color=color_orange, label=legend_str)
        plt.text(0+0.2, CO2_TtW_pp[-1], str('%.2f'%CO2_TtW_pp[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1-0.2, CO2e_TtW_pp[0], width = width, color=color_blue)
        plt.text(1-0.2, CO2e_TtW_pp[0], str('%.2f'%CO2e_TtW_pp[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(1+0.2, CO2e_TtW_pp[-1], width = width, color=color_orange)
        plt.text(1+0.2, CO2e_TtW_pp[-1], str('%.2f'%CO2e_TtW_pp[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2-0.2, CO2e_WtW_pp[0], width = width, color=color_blue)
        plt.text(2-0.2, CO2e_WtW_pp[0], str('%.2f'%CO2e_WtW_pp[0]), ha='center',bbox=dict(facecolor='red', alpha=1))
        plt.bar(2+0.2, CO2e_WtW_pp[-1], width = width, color=color_orange)
        plt.text(2+0.2, CO2e_WtW_pp[-1], str('%.2f'%CO2e_WtW_pp[-1]), ha='center',bbox=dict(facecolor='red', alpha=1))
        labels = ['$CO_{2,TtW}$','$CO_{2}e_{TtW}$','$CO_{2}e_{WtW}$']
        plt.xticks(x, labels)
        plt.ylim(bottom = 0)
        plt.legend()        

time = time.time() - start