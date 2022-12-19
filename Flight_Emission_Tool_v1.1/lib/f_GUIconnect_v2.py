# -*- coding: utf-8 -*-


from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
import pandas as pd


from lib.getscheduledata_v2 import get_schedule_data_v2
from lib.f_main import f_main





car_TtW = 0.1223
car_WtT = 0.0318
tree_factor = 25

t_hold_time_default = 0
taxi_out_time_default = 10.5
taxi_in_time_default = 5.3
t_alt_default = 45
t_fr_default = 30
lf_default = 1
avg_pas_mass_default = 77.4
avg_bag_mass_default = 22.8
m_freight_default = 0
seat_configs = ('Single class','Two or three class')
seat_configs_default = seat_configs[0]
full_economy_default = True

ReferenceDefault = {'Jet-A1_GWP_100_star':'(Lee, 2021)',
                    'Low-cost biofuels_GWP_100':'(Dray, 2022)',
                    'High-cost biofuels_GWP_100':'(Dray, 2022)',
                    'Power-to-liquids_GWP_100':'(Dray, 2022)',
                    'Low-cost SLNG_GWP_100':'(Dray, 2022)',
                    'High-cost SLNG_GWP_100':'(Dray, 2022)',
                    'Liquid Hydrogen_GWP_100':'(Dray, 2022)',
                    'Electricity_GWP_100':'(Dray, 2022)',
                    'Low-cost biofuels_GWP_100_star':'(Lee, 2021 and Dray, 2022)',
                    'High-cost biofuels_GWP_100_star':'(Lee, 2021 and Dray, 2022)',
                    'Power-to-liquids_GWP_100_star':'(Lee, 2021 and Dray, 2022)',
                    'Low-cost SLNG_GWP_100_star':'(Lee, 2021 and Dray, 2022)',
                    'High-cost SLNG_GWP_100_star':'(Lee, 2021 and Dray, 2022)',
                    'Liquid Hydrogen_GWP_100_star':'(Lee, 2021 and Dray, 2022)',
                    'Electricity_GWP_100_star':'(Lee, 2021 and Dray, 2022)'}


def f_readFlightSchedule(self):
    schedule_info = {}

    if(self.AnalysisType.get() == 'minimal data requirement'):
        Ls_flights = get_schedule_data_v2(self.file_schedule, data_type = 1)
        for index, row in Ls_flights.iterrows():
            flightid = str(row['FlightNumber'])
            TravelDate = str(row['TravelDate'])
            AirlineCode = str(row['AirlineCode'])
            Origin = str(row['OriginCode'])
            Destination = str(row['DestinationCode'])
            aircraft = str(row['Aircraft'])


            @dataclass
            class param:
                fuel_type:          str = self.FuelType.get()
                conversion_metric:  str = self.ConversionType.get()
                reference:          str = self.ReferenceType.get()

                distance:           float = float(row['Flight_distance']) * 1000
                n_seats:            int = int(row['Seats'])
                n_passengers:       int = int(row['Seats']) * float(lf_default)

                overwrite_m_freight:int = -1
                ns_type:            str = seat_configs_default
                full_economy:       bool = full_economy_default
                load_factor:        float = float(lf_default)
                avg_pas_mass:       float = float(avg_pas_mass_default)
                t_hold:             float = float(t_hold_time_default) * 60
                t_taxi_out:         float = float(taxi_out_time_default) * 60
                t_taxi_in:          float = float(taxi_in_time_default) * 60
                t_alt:              float = float(t_alt_default)
                t_fr:               float = float(t_fr_default)
                avg_bag_mass:       float = float(avg_bag_mass_default)

                m_pax_benchmark:    float = 0
                m_pax:              float = 0
                dm_payload:         float = 0
                dm_pax:             float = 0
                p_f_factor:         float = 0.7996

            param.m_pax_benchmark = float(param.avg_pas_mass) + float(param.avg_bag_mass)
            param.m_pax = float(param.avg_pas_mass) + float(param.avg_bag_mass)

            if(param.reference == self.Reference_types_2[1]):
                param.reference = ReferenceDefault[str(self.FuelType.get()) + '_' + str(self.ConversionType.get())]

            schedule_info[str(flightid)] = {'flightid': flightid,
                                            'aircraft': aircraft,
                                            'TravelDate': TravelDate,
                                            'AirlineCode': AirlineCode,
                                            'route': [Origin, Destination],
                                            'param': param}

    else:
        if(self.AnalysisType.get() == 'detailed data requirement'):
            Ls_flights = get_schedule_data_v2(self.file_schedule, data_type = 2)

            for index, row in Ls_flights.iterrows():
                flightid = str(row['FlightNumber'])
                TravelDate = str(row['TravelDate'])
                AirlineCode = str(row['AirlineCode'])
                Origin = str(row['OriginCode'])
                Destination = str(row['DestinationCode'])
                aircraft = str(row['Aircraft'])

                @dataclass
                class param:
                    fuel_type:          str = self.FuelType.get()
                    conversion_metric:  str = self.ConversionType.get()
                    reference:          str = self.ReferenceType.get()

                    distance:           float = float(row['Flight_distance']) * 1000
                    overwrite_m_freight:int = int(row['m_freight'])
                    n_seats:            int = int(row['Seats'])
                    n_passengers:       int = int(row['n_p'])
                    avg_bag_mass:       float = round(float(row['m_checked_baggage']) / int(row['n_p']), 1)

                    ns_type:            str = seat_configs_default
                    full_economy:       bool = full_economy_default
                    load_factor:        float = float(lf_default)
                    t_hold:             float = float(t_hold_time_default)*60
                    t_taxi_out:         float = float(taxi_out_time_default)*60
                    t_taxi_in:          float = float(taxi_in_time_default)*60
                    t_alt:              float = float(t_alt_default)
                    t_fr:               float = float(t_fr_default)
                    avg_pas_mass:       float = float(avg_pas_mass_default)

                    m_pax_benchmark:    float = 0
                    m_pax:              float = 0
                    dm_payload:         float = 0
                    dm_pax:             float = 0
                    p_f_factor:         float = 0.7996

                param.m_pax_benchmark = float(param.avg_pas_mass) + float(param.avg_bag_mass)
                param.m_pax = float(param.avg_pas_mass) + float(param.avg_bag_mass)

                if (param.reference == self.Reference_types_2[1]):
                    param.reference = ReferenceDefault[str(self.FuelType.get()) + '_' + str(self.ConversionType.get())]

                schedule_info[str(flightid)] = {'flightid':flightid,
                                                'aircraft':aircraft,
                                                'TravelDate': TravelDate,
                                                'AirlineCode': AirlineCode,
                                                'route': [Origin, Destination],
                                                'param':param}

    return schedule_info






def f_correctFlightSchedule(self):
    for k in self.schedule_data.keys():
        self.schedule_data[k]['param'].t_taxi_in = float(self.taxi_in_time.get())
        self.schedule_data[k]['param'].t_taxi_out = float(self.taxi_out_time.get())
        self.schedule_data[k]['param'].t_hold = float(self.holding_time.get())
        self.schedule_data[k]['param'].t_alt = float(self.alternate_time.get())
        self.schedule_data[k]['param'].t_fr = float(self.reserve_time.get())

        self.schedule_data[k]['param'].avg_bag_mass = float(self.mass_pas.get())
        self.schedule_data[k]['param'].avg_pas_mass = float(self.mass_bag.get())
        self.schedule_data[k]['param'].m_pax_benchmark = float(self.mass_pas.get()) + float(self.mass_bag.get())
        self.schedule_data[k]['param'].m_pax= float(self.mass_pas.get()) + float(self.mass_bag.get())




def f_GUIconnect(self):

    @dataclass
    class numerical_parameters:
        t_step_climb: int = 1
        t_step_descent: int = 1
        t_step_cruise: int = 10

    df = pd.DataFrame(columns=["flight_index", "aircraft", "TravelDate", "AirlineCode", "route",
                               'Scenario_type', 'Scenario_MassChange_avg','Scenario_MassChange_total',
                               'emi_1', 'emi_2', 'emi_3', 'emi_4',
                               'fc_1', 'fc_2', 'fc_3', 'fc_4', 'fc_5'])

    for k in self.schedule_data.keys():
        index = k
        aircraft = self.schedule_data[k]['aircraft']
        input_parameters = self.schedule_data[k]['param']
        dist = float(input_parameters.distance)

        if (self.Scenario_var_1.get() == self.Scenario_selection[0]):
            (results, emissions, fuel_consumption) = f_main(input_parameters, numerical_parameters, aircraft, dist)
            entry = pd.DataFrame.from_dict({
                "flight_index":[index],
                "aircraft": [aircraft],
                "TravelDate": [self.schedule_data[k]['TravelDate']],
                "AirlineCode": [self.schedule_data[k]['AirlineCode']],
                "route": [self.schedule_data[k]['route']],
                "Scenario_type": ["benchmark"],
                "Scenario_MassChange_avg": [0],
                "Scenario_MassChange_total": [0],
                "emi_1": [int(self.emi_type_1.get()) * emissions.CO2_WtT],               # if not selected, then emi_1 = 0, 0 is filtered later on
                "emi_2": [int(self.emi_type_2.get()) * emissions.non_CO2_WtT],
                "emi_3": [int(self.emi_type_3.get()) * emissions.CO2_TtW],
                "emi_4": [int(self.emi_type_4.get()) * emissions.non_CO2_TtW],
                "fc_1": [int(self.fc_type_1.get()) * fuel_consumption['total_fuel_taxi']],
                "fc_2": [int(self.fc_type_2.get()) * fuel_consumption['total_fuel_TO']],
                "fc_3": [int(self.fc_type_3.get()) * fuel_consumption['total_fuel_climb']],
                "fc_4": [int(self.fc_type_4.get()) * fuel_consumption['total_fuel_cruise']],
                "fc_5": [int(self.fc_type_5.get()) * fuel_consumption['total_fuel_descent']],
            })
            df = pd.concat([df, entry], ignore_index=True)



        if (self.Scenario_var_2.get() == self.Scenario_selection[0]):
            change = float(self.sce_2_min.get())
            while(change <= float(self.sce_2_max.get())):
                input_parameters.m_pax = input_parameters.m_pax_benchmark + change

                # print(str(change) + '--------' + str(input_parameters.m_pax))

                (results, emissions, fuel_consumption) = f_main(input_parameters, numerical_parameters, aircraft, dist)
                input_parameters.m_pax = input_parameters.m_pax_benchmark

                entry = pd.DataFrame.from_dict({
                    "flight_index": [index],
                    "aircraft": [aircraft],
                    "TravelDate": [self.schedule_data[k]['TravelDate']],
                    "AirlineCode": [self.schedule_data[k]['AirlineCode']],
                    "route": [self.schedule_data[k]['route']],
                    "Scenario_type": ["change_in_avg_mass"],
                    "Scenario_MassChange_avg": [change],
                    "Scenario_MassChange_total": [0],
                    "emi_1": [int(self.emi_type_1.get()) * emissions.CO2_WtT],
                    "emi_2": [int(self.emi_type_2.get()) * emissions.non_CO2_WtT],
                    "emi_3": [int(self.emi_type_3.get()) * emissions.CO2_TtW],
                    "emi_4": [int(self.emi_type_4.get()) * emissions.non_CO2_TtW],
                    "fc_1": [int(self.fc_type_1.get()) * fuel_consumption['total_fuel_taxi']],
                    "fc_2": [int(self.fc_type_2.get()) * fuel_consumption['total_fuel_TO']],
                    "fc_3": [int(self.fc_type_3.get()) * fuel_consumption['total_fuel_climb']],
                    "fc_4": [int(self.fc_type_4.get()) * fuel_consumption['total_fuel_cruise']],
                    "fc_5": [int(self.fc_type_5.get()) * fuel_consumption['total_fuel_descent']],
                })
                df = pd.concat([df, entry], ignore_index=True)

                change += float(self.sce_2_stepsize.get())



        if (self.Scenario_var_3.get() == self.Scenario_selection[0]):
            change = float(self.sce_3_min.get())
            while(change <= float(self.sce_3_max.get())):
                input_parameters.m_pax = input_parameters.m_pax_benchmark + change / input_parameters.m_pax

                # print(str(change) + '--------' + str(input_parameters.m_pax))

                (results, emissions, fuel_consumption) = f_main(input_parameters, numerical_parameters, aircraft, dist)
                input_parameters.m_pax = input_parameters.m_pax_benchmark

                entry = pd.DataFrame.from_dict({
                    "flight_index": [index],
                    "aircraft": [aircraft],
                    "TravelDate": [self.schedule_data[k]['TravelDate']],
                    "AirlineCode": [self.schedule_data[k]['AirlineCode']],
                    "route": [self.schedule_data[k]['route']],
                    "Scenario_type": ["change_in_total_mass"],
                    "Scenario_MassChange_avg": [0],
                    "Scenario_MassChange_total": [change],
                    "emi_1": [int(self.emi_type_1.get()) * emissions.CO2_WtT],
                    "emi_2": [int(self.emi_type_2.get()) * emissions.non_CO2_WtT],
                    "emi_3": [int(self.emi_type_3.get()) * emissions.CO2_TtW],
                    "emi_4": [int(self.emi_type_4.get()) * emissions.non_CO2_TtW],
                    "fc_1": [int(self.fc_type_1.get()) * fuel_consumption['total_fuel_taxi']],
                    "fc_2": [int(self.fc_type_2.get()) * fuel_consumption['total_fuel_TO']],
                    "fc_3": [int(self.fc_type_3.get()) * fuel_consumption['total_fuel_climb']],
                    "fc_4": [int(self.fc_type_4.get()) * fuel_consumption['total_fuel_cruise']],
                    "fc_5": [int(self.fc_type_5.get()) * fuel_consumption['total_fuel_descent']],
                })
                df = pd.concat([df, entry], ignore_index=True)

                change += float(self.sce_3_stepsize.get())







#############################################################################################################



    df['emi_2_car'] = [0] * len(df)
    df['emi_2_tree'] = [0] * len(df)
    df['emi_4_car'] = [0] * len(df)
    df['emi_4_tree'] = [0] * len(df)

    df['emi_24_total'] = [0] * len(df)
    df['emi_24_total_tree'] = [0] * len(df)
    df['emi_24_total_car'] = [0] * len(df)


    df_benchmark = df.copy()
    for index, row in df_benchmark.iterrows():
        if not (row['Scenario_type'] == 'benchmark'):
            df_benchmark = df_benchmark.drop(index)

    for index, row in df.iterrows():
        if not (row['Scenario_type'] == 'benchmark'):
            emi_benchmark_2 = 0
            emi_benchmark_4 = 0
            for index2, row2 in df_benchmark.iterrows():
                if(row["flight_index"] == row2["flight_index"] and row["aircraft"] == row2["aircraft"]):
                    emi_benchmark_2 = row2["emi_2"]
                    emi_benchmark_4 = row2["emi_4"]

            if not (str(row["emi_2"]) == 'nan'):
                df.at[index, 'emi_2_car'] = (row["emi_2"] - emi_benchmark_2) / car_WtT
                df.at[index, 'emi_2_tree'] = (row["emi_2"] - emi_benchmark_2) / tree_factor

            if not (str(row["emi_4"]) == 'nan'):
                df.at[index, 'emi_4_car'] = (row["emi_4"] - emi_benchmark_4) / car_TtW
                df.at[index, 'emi_4_tree'] = (row["emi_4"] - emi_benchmark_4) / tree_factor

    for index, row in df.iterrows():
        df.at[index, 'emi_24_total'] = (row["emi_2"] + row["emi_4"]) / 1000
        df.at[index, 'emi_24_total_tree'] = row['emi_2_tree'] + row['emi_4_tree']
        df.at[index, 'emi_24_total_car'] = row['emi_2_car'] + row['emi_4_car']


#############################################################################################################
    ls = self.file_schedule.split('/')[:-1]
    folder = ''
    for i in ls:
        folder += i
        folder += '/'
    output_file = folder + 'results/AirlineEmission_result.xlsx'
    df.to_excel(output_file, index=False, sheet_name= 'results', header = False,
                columns = ["flight_index", "aircraft", "TravelDate", "AirlineCode", "route",
                           'Scenario_type', 'Scenario_MassChange_avg','Scenario_MassChange_total',
                           'emi_1', 'emi_2', 'emi_3', 'emi_4',
                           'fc_1', 'fc_2', 'fc_3', 'fc_4', 'fc_5',
                           'emi_2_car', 'emi_2_tree', 'emi_4_car', 'emi_4_tree',
                           'emi_24_total', 'emi_24_total_tree', 'emi_24_total_car'])


    print('finish writing results into table')



#############################################################################################################

    def plot_routemap(schedule, output):
        plt.style.use("default")
        dpi = 2400
        plt.style.use("dark_background")

        fs = pd.read_csv(schedule)
        fig = plt.figure(dpi=dpi)
        m = Basemap(projection='robin', lon_0=0, resolution='c')
        m.drawcoastlines(linewidth=0.01)
        m.fillcontinents(color='#072B2C', lake_color='#04191A')

        for O_Lon, O_Lat, D_Lon, D_Lat in zip(fs.O_Lon, fs.O_Lat, fs.D_Lon, fs.D_Lat):
            m.drawgreatcircle(O_Lon, O_Lat, D_Lon, D_Lat, linewidth=0.1, color='#B4CD0D')

        m.drawparallels(np.arange(-90., 120., 30.), linewidth=0.1)
        m.drawmeridians(np.arange(0., 360., 60.), linewidth=0.1)
        m.drawmapboundary(fill_color='#04191A', linewidth=0.1)
        plt.savefig(output, dpi=dpi, transparent=True)

    ls = self.file_schedule.split('/')[:-1]
    folder = ''
    for i in ls:
        folder += i
        folder += '/'
    output = folder + 'results/AirlineEmission_map.png'
    plot_routemap(schedule=self.file_schedule,output=output)

    print('finish printing route map')









