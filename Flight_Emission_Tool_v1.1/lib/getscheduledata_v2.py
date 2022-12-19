# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:38:33 2022

@author: SYSTEM
"""

import pandas as pd


def get_schedule_data_v2(fileN, data_type):

    # Read dataframes from files
    fs = pd.read_csv(fileN,sep=',')

    fs['Aircraft type ICAO'] = fs['Aircraft type ICAO'].astype(str)


    aircraftproperties = pd.read_csv('./data/aircraftproperties.csv',sep=',',index_col='Index')
    aircraft_index = aircraftproperties.index.tolist()
    
    # Remove all flights with aircraft having MTOW < 10000
    fs_update = fs.drop(fs[fs.MTOW < 10000].index); fs_update = fs_update.reset_index(drop=True)
    
    # Remove all cargo flights with aircraft having MTOW < 40000 (model not capable of turboprop)
    fs_update = fs_update.drop(fs_update[(fs_update['MTOW'] < 40000) & (fs_update['FlightType'].str.contains('CGO'))].index); fs_update = fs_update.reset_index(drop=True)
    
    # If cargo: add -F to aircraft ICAO code
    fs_update.loc[(fs_update['FlightType'].str.contains('CGO')), 'Aircraft type ICAO'] = fs_update['Aircraft type ICAO']+'F'
    
    # For aircraft not in aircraftproperties list, specify if cargo or pax aircraft, update with generic name
    fs_update.loc[(~fs_update['Aircraft type ICAO'].isin(aircraft_index)) & (~fs_update['FlightType'].str.contains('CGO')), 'Aircraft type ICAO'] = 'GNP'
    fs_update.loc[(~fs_update['Aircraft type ICAO'].isin(aircraft_index)) & (fs_update['FlightType'].str.contains('CGO')), 'Aircraft type ICAO'] = 'GNC'
    
    # Add suffix to generic aircraft name: S, M, L, XL depending on aircraft MTOW
    fs_update.loc[(fs_update['Aircraft type ICAO'].str.contains('GNP' or 'GNC')) & (fs_update['MTOW'] >= 10000) & (fs_update['MTOW'] < 40000), 'Aircraft type ICAO'] = fs_update['Aircraft type ICAO']+'S'
    fs_update.loc[(fs_update['Aircraft type ICAO'].str.contains('GNP' or 'GNC')) & (fs_update['MTOW'] >= 40000) & (fs_update['MTOW'] < 100000), 'Aircraft type ICAO'] = fs_update['Aircraft type ICAO']+'M'
    fs_update.loc[(fs_update['Aircraft type ICAO'].str.contains('GNP' or 'GNC')) & (fs_update['MTOW'] >= 100000) & (fs_update['MTOW'] < 300000), 'Aircraft type ICAO'] = fs_update['Aircraft type ICAO']+'L'
    fs_update.loc[(fs_update['Aircraft type ICAO'].str.contains('GNP' or 'GNC')) & (fs_update['MTOW'] >= 300000), 'Aircraft type ICAO'] = fs_update['Aircraft type ICAO']+'XL'


    FlightNumber = fs_update['FlightNumber']
    TravelDate = fs_update['TravelDate']
    AirlineCode = fs_update['AirlineCode']
    Origin = fs_update['OriginCode']
    Destination = fs_update['DestinationCode']
    aircraft = fs_update['Aircraft type ICAO']
    airport_distance = fs_update['Distance_km']
    Seats = fs_update['Seats']

    schedule_data = pd.DataFrame({})

    if(data_type == 1):
        schedule_data = pd.concat([FlightNumber, TravelDate, AirlineCode, Origin, Destination, aircraft, airport_distance,Seats], axis=1)
        schedule_data = schedule_data.rename(columns={'Aircraft type ICAO': 'Aircraft', 'Distance_km': 'Flight_distance'})

    if(data_type == 2):
        m_cargo = fs_update['CargoMass'].to_numpy()
        m_mail = fs_update['MailMass'].to_numpy()
        m_freight = m_cargo + m_mail
        m_freight = pd.DataFrame(m_freight, columns=['m_freight'])

        m_package = fs_update['BaggageMass'].to_numpy()
        m_checked_baggage = pd.DataFrame(m_package, columns=['m_checked_baggage'])

        passengers = fs_update['Number of passengers'].to_numpy()
        n_pas = pd.DataFrame(passengers, columns=['n_p'])

        schedule_data = pd.concat([FlightNumber, TravelDate, AirlineCode, Origin, Destination, aircraft, airport_distance,Seats,
                                   n_pas, m_freight, m_checked_baggage],axis=1)

        schedule_data = schedule_data.rename(columns={'Aircraft type ICAO': 'Aircraft', 'Distance_km': 'Flight_distance'})

    return schedule_data