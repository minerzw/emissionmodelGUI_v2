# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 14:16:26 2022

@author: 921677
"""
import pandas as pd
from dataclasses import dataclass
from scipy import integrate
import numpy as np

def emissions_analysis(trip_properties, E_taxi, E_TO, fuel_type, conversion_metric, reference):
    # fuel_type = 'Jet-A1'
    # conversion_metric = 'GWP_100_star'
    # reference = '(Lee, 2021)'
    energy_carriers = pd.read_csv('./data/energy_carriers.csv')
    energy_carriers = energy_carriers.set_index(['Name','Conversion_Metric','Reference'])
    # carrier_types = (energy_carriers.Name +' '+ energy_carriers.Conversion_Metric +' '+ energy_carriers.Reference).to_list()

    t_trip = trip_properties[:,0]
    E_trip = trip_properties[:,7]    
    # ## Emission indices and CO2e conversion metrics
    # EI_TtW = 3.16               # Tank to wheel emission index for CO2 in kg CO2/kg fuel Ja (specific energy = 43.15 MJ/kg)
    # EI_WtT = 0.62               # Well to tank emission index for CO2e in kg CO2e/kg fuel (specific energy = 43.15 MJ/kg)
    # GWP_100 = 1.74              # 100 year global warming potential, Paris agreement (does not adequately appreciate SLCPs)
    # GWP_star = 3.01             # warming equivalent emission: sustained emissions of an SLCP result in similar impact to one-off release of fixed amount of CO2 (appreciates delayed response associated with equilibration to a past increase in forcing)

    fuel_properties = energy_carriers.loc[(fuel_type,conversion_metric,reference)]
    
    ## Find altitude indices
    # Non-CO2 effects
    H_non_CO2 = 9000
    if max(trip_properties[:,3]>H_non_CO2):  
        start_non_CO2= int(min(np.argwhere(trip_properties[:,3]>H_non_CO2)))
        stop_non_CO2 = int(max(np.argwhere(trip_properties[:,3]>H_non_CO2)))
    else:
        start_non_CO2 = 0
        stop_non_CO2 = 0
    
    @dataclass
    class emissions:
        CO2_WtT = (integrate.trapz(E_trip,t_trip) + E_taxi + E_TO)*fuel_properties.Upstream_CO2/1000
        non_CO2_WtT = (integrate.trapz(E_trip,t_trip) + E_taxi + E_TO)*fuel_properties.Upstream_non_CO2/1000
        CO2_TtW = (integrate.trapz(E_trip,t_trip) + E_taxi + E_TO)*fuel_properties.Combustion_CO2/1000
        non_CO2_TtW = (integrate.trapz(E_trip[start_non_CO2:stop_non_CO2+1],t_trip[start_non_CO2:stop_non_CO2+1]))*fuel_properties.Combustion_non_CO2/1000
    
    return emissions