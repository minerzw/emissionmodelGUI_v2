# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 19:27:16 2022

@author: SYSTEM
"""



import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
from ctypes import windll
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo



from lib.f_GUIconnect_v2 import *


windll.shcore.SetProcessDpiAwareness(1)

image = True


class emissionmodelGUI_App(tk.Tk):
    def __init__(self):
        super().__init__()

        ## Window Geometry
        self.window_width = 1000
        self.window_height = 575

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - self.window_width / 2)
        center_y = int(screen_height/2 - self.window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.resizable(width=False, height=False)
        self.columnconfigure(0, minsize=250)

      
        ## Window Title
        self.title('Flight Emissions Tool')
        self.create_variables()
        self.create_notebooks()
        self.create_frames()
        self.create_widgets()



    def create_variables(self):
        self.UserGroup_var = tk.StringVar(self)

        self.AnalysisType = tk.StringVar(self)
        self.FuelType = tk.StringVar(self)
        self.ConversionType = tk.StringVar(self)
        self.ReferenceType = tk.StringVar(self)

        self.emi_type_1 = tk.IntVar(self)
        self.emi_type_2 = tk.IntVar(self)
        self.emi_type_3 = tk.IntVar(self)
        self.emi_type_4 = tk.IntVar(self)

        self.fc_type_1 = tk.IntVar(self)
        self.fc_type_2 = tk.IntVar(self)
        self.fc_type_3 = tk.IntVar(self)
        self.fc_type_4 = tk.IntVar(self)
        self.fc_type_5 = tk.IntVar(self)

        self.Scenario_var_1 = tk.StringVar(self)
        self.Scenario_var_2 = tk.StringVar(self)
        self.Scenario_var_3 = tk.StringVar(self)

        self.file_schedule = tk.StringVar(self)
        self.schedule_data = {}

        # TODO: these variables can be set in GUI per flight
        self.aircraft_var = tk.StringVar(self)
        self.distance = tk.StringVar(self)
        self.seat_config_var = tk.StringVar(self)
        self.np = tk.StringVar(self)
        self.total_m_pax = tk.StringVar(self)


    
    def create_notebooks(self):
        style = ttk.Style()
        style.layout("Tab",
        [('Notebook.tab', {'sticky': 'nswe', 'children':
            [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                #[('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                    [('Notebook.label', {'side': 'top', 'sticky': ''})],
                #})],
            })],
        })]
        )
        style.configure('TNotebook.Tab', width=15)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(pady=5)

        style.configure('Frame1.TFrame', background='green')



    def create_frames(self):

        s = ttk.Style()
        s.configure('Black.TLabelframe.Label', font=('courier', 12, 'bold'))
        s.configure('Black.TLabelframe.Label', foreground='green')
        s.configure('Black.TLabelframe.Label', background='white')

        s2 = ttk.Style()
        s2.configure('Blue.TLabelframe.Label', font=('courier', 12, 'bold'))
        s2.configure('Blue.TLabelframe.Label', foreground='blue')
        s2.configure('Blue.TLabelframe.Label', background='white')

        self.padding_outcomeframes = {'pady':(5,0)}


        self.nb_1 = ttk.Frame(
            self.notebook,
            width = self.window_width,
            height = self.window_height)
        self.nb_2 = ttk.Frame(
            self.notebook,
            width = self.window_width,
            height = self.window_height)
        self.nb_3 = ttk.Frame(
            self.notebook,
            width = self.window_width,
            height = self.window_height)
        self.nb_4 = ttk.Frame(
            self.notebook,
            width = self.window_width,
            height = self.window_height)
        self.nb_5 = ttk.Frame(
            self.notebook,
            width = self.window_width,
            height = self.window_height)





        self.first_frame_main = ttk.Frame(
            self.nb_1,
            height = self.window_height,
            width=self.window_width * 0.7)

        self.first_frame_logo = ttk.Frame(
            self.nb_1,
            height = self.window_height,
            width=self.window_width * 0.3)

        self.first_frame_1 = ttk.LabelFrame(
            self.first_frame_main,
            text='Upload flight schedule',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.2,
            width=self.window_width * 0.7)

        self.first_frame_2 = ttk.LabelFrame(
            self.first_frame_main,
            text='Select service package',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.4,
            width=self.window_width * 0.7)

        self.first_frame_3 = ttk.LabelFrame(
            self.first_frame_main,
            text='Saved and submit',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.15,
            width=self.window_width * 0.7)

        self.first_frame_4 = ttk.LabelFrame(
            self.first_frame_main,
            text='Help',
            labelanchor='nw',
            style="Blue.TLabelframe",
            height=self.window_height * 0.25,
            width=self.window_width * 0.7)






        self.second_frame_main = ttk.Frame(
            self.nb_2,
            height = self.window_height,
            width=self.window_width * 0.7)


        self.second_frame_2 = ttk.LabelFrame(
            self.second_frame_main,
            text='Flight Properties',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.4,
            width=self.window_width * 0.7)

        self.second_frame_3 = ttk.LabelFrame(
            self.second_frame_main,
            text='PAX Properties',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.2,
            width=self.window_width * 0.7)

        self.second_frame_4 = ttk.LabelFrame(
            self.second_frame_main,
            text='submit changes',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.15,
            width=self.window_width * 0.7)

        self.second_frame_5 = ttk.LabelFrame(
            self.second_frame_main,
            text='Help',
            labelanchor='nw',
            style="Blue.TLabelframe",
            height=self.window_height * 0.25,
            width=self.window_width * 0.7)


        self.second_frame_logo = ttk.Frame(
            self.nb_2,
            height = self.window_height,
            width=self.window_width * 0.3)


        self.third_frame_main = ttk.Frame(
            self.nb_3,
            height = self.window_height,
            width=self.window_width * 0.7)

        self.third_frame_1 = ttk.LabelFrame(
            self.third_frame_main,
            text='Select result components -- Emission',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.3,
            width=self.window_width * 0.7)

        self.third_frame_3 = ttk.LabelFrame(
            self.third_frame_main,
            text='Select result components -- Energy Consumption',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.4,
            width=self.window_width * 0.7)

        self.third_frame_2 = ttk.LabelFrame(
            self.third_frame_main,
            text='Help',
            labelanchor='nw',
            style="Blue.TLabelframe",
            height=self.window_height * 0.3,
            width=self.window_width * 0.7)

        self.third_frame_logo = ttk.Frame(
            self.nb_3,
            height = self.window_height,
            width=self.window_width * 0.3)


        self.fourth_frame_main = ttk.Frame(
            self.nb_4,
            height = self.window_height,
            width=self.window_width * 0.7)

        self.fourth_frame_1 = ttk.LabelFrame(
            self.fourth_frame_main,
            text='Select analysis scenarios',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.6,
            width=self.window_width * 0.7)

        self.fourth_frame_2 = ttk.LabelFrame(
            self.fourth_frame_main,
            text='Help',
            labelanchor='nw',
            style="Blue.TLabelframe",
            height=self.window_height * 0.4,
            width=self.window_width * 0.7)

        self.fourth_frame_logo = ttk.Frame(
            self.nb_4,
            height = self.window_height,
            width=self.window_width * 0.3)



        self.fifth_frame_main = ttk.Frame(
            self.nb_5,
            height=self.window_height,
            width=self.window_width * 0.7)

        self.fifth_frame_1 = ttk.LabelFrame(
            self.fifth_frame_main,
            text='Output Manager',
            labelanchor='nw',
            style="Black.TLabelframe",
            height=self.window_height * 0.3,
            width=self.window_width * 0.7)

        self.fifth_frame_2 = ttk.LabelFrame(
            self.fifth_frame_main,
            text='Help',
            labelanchor='nw',
            style="Blue.TLabelframe",
            height=self.window_height * 0.7,
            width=self.window_width * 0.7)

        self.fifth_frame_logo = ttk.Frame(
            self.nb_5,
            height = self.window_height,
            width=self.window_width * 0.3)


        # # # layout main containers
        self.nb_1.grid()
        self.nb_2.grid()
        self.nb_3.grid()
        self.nb_4.grid()
        self.nb_5.grid()

        self.first_frame_main.grid(row=0, column=0, sticky="nsew")
        self.first_frame_main.rowconfigure(5, weight=1)
        self.first_frame_main.grid_propagate(False)

        self.first_frame_logo.grid(row=0, column=1, sticky="nsew")
        self.first_frame_logo.rowconfigure(1, weight=1)
        self.first_frame_logo.grid_propagate(False)

        self.first_frame_1.grid(row=0, column=0, sticky="ew")
        self.first_frame_1.columnconfigure(5, weight=1)
        self.first_frame_1.grid_propagate(False)

        self.first_frame_2.grid(row=1, column=0, sticky="ew")
        self.first_frame_2.columnconfigure(5, weight=1)
        self.first_frame_2.grid_propagate(False)

        self.first_frame_3.grid(row=2, column=0, sticky="ew")
        self.first_frame_3.columnconfigure(5, weight=1)
        self.first_frame_3.grid_propagate(False)

        self.first_frame_4.grid(row=3, column=0, sticky="ew")
        self.first_frame_4.columnconfigure(5, weight=1)
        self.first_frame_4.grid_propagate(False)


        self.second_frame_main.grid(row=0, column=0, sticky="nsew")
        self.second_frame_main.rowconfigure(5, weight=1)
        self.second_frame_main.grid_propagate(False)


        self.second_frame_2.grid(row=1, column=0, sticky="ew")
        self.second_frame_2.columnconfigure(3, weight=1)
        self.second_frame_2.grid_propagate(False)

        self.second_frame_3.grid(row=2, column=0, sticky="ew")
        self.second_frame_3.columnconfigure(5, weight=1)
        self.second_frame_3.grid_propagate(False)

        self.second_frame_4.grid(row=3, column=0, sticky="ew")
        self.second_frame_4.columnconfigure(6, weight=1)
        self.second_frame_4.grid_propagate(False)

        self.second_frame_5.grid(row=4, column=0, sticky="ew")
        self.second_frame_5.columnconfigure(0, weight=1)
        self.second_frame_5.grid_propagate(False)

        self.second_frame_logo.grid(row=0, column=1, sticky="nsew")
        self.second_frame_logo.rowconfigure(1, weight=1)
        self.second_frame_logo.grid_propagate(False)



        self.third_frame_main.grid(row=0, column=0, sticky="nsew")
        self.third_frame_main.rowconfigure(3, weight=1)
        self.third_frame_main.grid_propagate(False)

        self.third_frame_1.grid(row=0, column=0, sticky="new")
        self.third_frame_1.columnconfigure(1, weight=1)
        self.third_frame_1.grid_propagate(False)

        self.third_frame_3.grid(row=1, column=0, sticky="new")
        self.third_frame_3.columnconfigure(2, weight=1)
        self.third_frame_3.grid_propagate(False)

        self.third_frame_2.grid(row=2, column=0, sticky="new")
        self.third_frame_2.columnconfigure(1, weight=1)
        self.third_frame_2.grid_propagate(False)

        self.third_frame_logo.grid(row=0, column=1, sticky="nsew")
        self.third_frame_logo.rowconfigure(1, weight=1)
        self.third_frame_logo.grid_propagate(False)



        self.fourth_frame_main.grid(row=0, column=0, sticky="nsew")
        self.fourth_frame_main.rowconfigure(5, weight=1)
        self.fourth_frame_main.grid_propagate(False)

        self.fourth_frame_1.grid(row=0, column=0, sticky="new")
        self.fourth_frame_1.rowconfigure(10, weight=1)
        self.fourth_frame_1.columnconfigure(5, weight=1)
        self.fourth_frame_1.grid_propagate(False)

        self.fourth_frame_2.grid(row=1, column=0, sticky="new")
        self.fourth_frame_2.columnconfigure(1, weight=1)
        self.fourth_frame_2.grid_propagate(False)

        self.fourth_frame_logo.grid(row=0, column=1, sticky="nsew")
        self.fourth_frame_logo.rowconfigure(1, weight=1)
        self.fourth_frame_logo.grid_propagate(False)



        self.fifth_frame_main.grid(row=0, column=0, sticky="nsew")
        self.fifth_frame_main.rowconfigure(2, weight=1)
        self.fifth_frame_main.grid_propagate(False)

        self.fifth_frame_1.grid(row=0, column=0, sticky="new")
        self.fifth_frame_1.columnconfigure(6, weight=1)
        self.fifth_frame_1.grid_propagate(False)

        self.fifth_frame_2.grid(row=1, column=0, sticky="new")
        self.fifth_frame_2.columnconfigure(1, weight=1)
        self.fifth_frame_2.grid_propagate(False)

        self.fifth_frame_logo.grid(row=0, column=1, sticky="nsew")
        self.fifth_frame_logo.rowconfigure(1, weight=1)
        self.fifth_frame_logo.grid_propagate(False)

        self.notebook.add(self.nb_1, text='Step-1')
        self.notebook.add(self.nb_2, text='Step-2')
        self.notebook.add(self.nb_3, text='Step-3')
        self.notebook.add(self.nb_4, text='Step-4')
        self.notebook.add(self.nb_5, text='Step-5')



    def focus_out_entry_box(self, widget, widget_text):
        if widget.cget('style') == 'Black.TEntry' and len(widget.get()) == 0:
            widget.delete(0, tk.END)
            widget.configure(style='Grey.TEntry')
            widget.insert(0, widget_text)

    def focus_in_entry_box(self, widget):
        if widget.cget('style') == 'Grey.TEntry':
            widget.configure(style='Black.TEntry')
            widget.delete(0, tk.END)


    def default_entry_box(self, default, column, row, frame):
        grey_entry_style = ttk.Style()
        grey_entry_style.configure('Grey.TEntry', foreground='grey')
        black_entry_style = ttk.Style()
        black_entry_style.configure('Black.TEntry', foreground='black')

        box_entry = ttk.Entry(frame, style='Grey.TEntry')
        box_entry.insert(0, default)
        box_entry.bind("<FocusIn>", lambda args: self.focus_in_entry_box(box_entry))
        box_entry.bind("<FocusOut>", lambda args: self.focus_out_entry_box(box_entry, default))
        box_entry.grid(column=column, row=row, sticky=tk.W, **self.padding_right)
        return box_entry




    def create_widgets(self):
        self.padding_left = {'padx': (15,15), 'pady': (0,3)}
        self.padding_left_title = {'padx': (15,15), 'pady': (0,1)}
        self.padding_right = {'padx': (5,5), 'pady': (0,3)}
        self.padding_right_unit = {'padx': (0,5), 'pady': (0,3)}
        self.padding_checkbox = {'padx': (3,3), 'pady': (0,3)}

        self.UserGroup_type = ('Airline Group (1)', 'Airline Group (2)', 'no selection')
        self.Scenario_selection = ('Yes', 'no selection')





        self.Analysis_types = ('minimal data requirement', 'detailed data requirement')
        self.Fuel_types = ('', 'Jet-A1', 'Low-cost biofuels', 'High-cost biofuels', 'Power-to-liquids', 'Low-cost SLNG',
                           'High-cost SLNG', 'Liquid Hydrogen', 'Electricity')
        self.Conversion_types = ('', 'GWP_100', 'GWP_100_star')
        self.Reference_types_1 = ('(Dray, 2022)', '(Lee, 2021)')
        self.Reference_types_2 = ('', '     default')






        choice_1 = ttk.Label(self.first_frame_2,  text='Analysis type:')
        choice_1.grid(column=0, row=0, sticky=tk.W, **self.padding_left)
        choice_1_menu = ttk.OptionMenu(
            self.first_frame_2,
            self.AnalysisType,
            self.Analysis_types[0],
            *self.Analysis_types)
        choice_1_menu.config(width=len(max(self.Analysis_types, key=len))+0)
        choice_1_menu.grid(column=1,row=0,columnspan=3,sticky=tk.W, padx=(9,3), pady=(0,3))


        choice_2 = ttk.Label(self.first_frame_2,  text='Fuel type:')
        choice_2.grid(column=0, row=1, sticky=tk.W, **self.padding_left)
        choice_2_menu = ttk.OptionMenu(
            self.first_frame_2,
            self.FuelType,
            self.Fuel_types[0],
            *self.Fuel_types)
        choice_2_menu.config(width=len(max(self.Fuel_types, key=len))+0)
        choice_2_menu.grid(column=1,row=1,columnspan=3,sticky=tk.W, padx=(9,3), pady=(0,3))


        choice_3 = ttk.Label(self.first_frame_2,  text='Conversion type:')
        choice_3.grid(column=0, row=2, sticky=tk.W, **self.padding_left)
        choice_3_menu = ttk.OptionMenu(
            self.first_frame_2,
            self.ConversionType,
            self.Conversion_types[0],
            *self.Conversion_types,
            command=self.Define_ChooseReference)
        choice_3_menu.config(width=len(max(self.Conversion_types, key=len))+0)
        choice_3_menu.grid(column=1,row=2,columnspan=3,sticky=tk.W, padx=(9,3), pady=(0,3))


        choice_4 = ttk.Label(self.first_frame_2,  text='Reference type:')
        choice_4.grid(column=0, row=3, sticky=tk.W, **self.padding_left)




        sce_1 = ttk.Label(self.fourth_frame_1,  text='Module-1: Evaluate benchmark footprint:')
        sce_1.grid(column=0, row=0, sticky=tk.W, **self.padding_left)
        sce_1_menu = ttk.OptionMenu(
            self.fourth_frame_1,
            self.Scenario_var_1,
            self.Scenario_selection[1],
            *self.Scenario_selection)
        sce_1_menu.config(width=len(max(self.Scenario_selection, key=len))+0)
        sce_1_menu.grid(column=1,row=0,columnspan=3,sticky=tk.W, padx=(9,3), pady=(0,3))

        sce_2 = ttk.Label(self.fourth_frame_1,  text='Module-2: Evaluate change in average PAX mass:')
        sce_2.grid(column=0, row=2, sticky=tk.W, **self.padding_left)
        sce_2_menu = ttk.OptionMenu(
            self.fourth_frame_1,
            self.Scenario_var_2,
            self.Scenario_selection[1],
            *self.Scenario_selection,
            command=self.Define_Scenario_2)
        sce_2_menu.config(width=len(max(self.Scenario_selection, key=len))+0)
        sce_2_menu.grid(column=1,row=2,columnspan=3,sticky=tk.W, padx=(9,3), pady=(0,3))

        sce_3 = ttk.Label(self.fourth_frame_1,  text='Module-3: Evaluate change in total PAX mass:')
        sce_3.grid(column=0, row=6, sticky=tk.W, **self.padding_left)
        sce_3_menu = ttk.OptionMenu(
            self.fourth_frame_1,
            self.Scenario_var_3,
            self.Scenario_selection[1],
            *self.Scenario_selection,
            command=self.Define_Scenario_3)
        sce_3_menu.config(width=len(max(self.Scenario_selection, key=len))+0)
        sce_3_menu.grid(column=1,row=6,columnspan=3,sticky=tk.W, padx=(9,3), pady=(0,3))



        ## Checkbuttons
        emi_t1 = ttk.Checkbutton(
            self.third_frame_1,
            text='Option-1: CO2 Emissions upstream',
            variable=self.emi_type_1,
            onvalue=1,
            offvalue=0)
        emi_t1.grid(column=0,row=1,sticky=tk.W, **self.padding_checkbox)
        emi_t2 = ttk.Checkbutton(
            self.third_frame_1,
            text='Option-2: Non-CO2 Emissions upstream',
            variable=self.emi_type_2,
            onvalue=1,
            offvalue=0)
        emi_t2.grid(column=0,row=2,sticky=tk.W, **self.padding_checkbox)
        emi_t3 = ttk.Checkbutton(
            self.third_frame_1,
            text='Option-3: CO2 Emissions on-flight',
            variable=self.emi_type_3,
            onvalue=1,
            offvalue=0)
        emi_t3.grid(column=0,row=3,sticky=tk.W, **self.padding_checkbox)
        emi_t4 = ttk.Checkbutton(
            self.third_frame_1,
            text='Option-4: Non-CO2 Emissions on-flight',
            variable=self.emi_type_4,
            onvalue=1,
            offvalue=0)
        emi_t4.grid(column=0,row=4,sticky=tk.W, **self.padding_checkbox)





        fc_t1 = ttk.Checkbutton(
            self.third_frame_3,
            text='Option-1: taxi',
            variable=self.fc_type_1,
            onvalue=1,
            offvalue=0)
        fc_t1.grid(column=0,row=0,sticky=tk.W, **self.padding_checkbox)

        fc_t2 = ttk.Checkbutton(
            self.third_frame_3,
            text='Option-2: take-off',
            variable=self.fc_type_2,
            onvalue=1,
            offvalue=0)
        fc_t2.grid(column=0, row=1, sticky=tk.W, **self.padding_checkbox)

        fc_t3 = ttk.Checkbutton(
            self.third_frame_3,
            text='Option-3: climb',
            variable=self.fc_type_3,
            onvalue=1,
            offvalue=0)
        fc_t3.grid(column=0,row=2,sticky=tk.W, **self.padding_checkbox)

        fc_t4 = ttk.Checkbutton(
            self.third_frame_3,
            text='Option-4: cruise',
            variable=self.fc_type_4,
            onvalue=1,
            offvalue=0)
        fc_t4.grid(column=0,row=3,sticky=tk.W, **self.padding_checkbox)

        fc_t5 = ttk.Checkbutton(
            self.third_frame_3,
            text='Option-5: descent',
            variable=self.fc_type_5,
            onvalue=1,
            offvalue=0)
        fc_t5.grid(column=0, row=4, sticky=tk.W, **self.padding_checkbox)









        ## Button
        open_button = ttk.Button(self.first_frame_1, text='Upload flight schedule', command=self.openfile)
        open_button.grid(column=0, row=3, columnspan=1, padx=(15,40), pady=(5,5))

        read_button = ttk.Button(self.first_frame_3, text='Save service package', command=self.readfile)
        read_button.grid(column=0, row=4, columnspan=1, padx=(15,40), pady=(5,5))

        change_button = ttk.Button(self.second_frame_4, text='save changes', command=self.save_change_schedule)
        change_button.grid(column=0, row=1, columnspan=6, padx=(5,40), pady=(5,5))

        submit_button = ttk.Button(self.fifth_frame_1, text='Submit', command=self.submit)
        submit_button.grid(column=0, row=1, columnspan=6, padx=(10,40), pady=(5,5))



        ## Taxi in time
        taxi_in_time_label = ttk.Label(self.second_frame_2, text='Taxi in time:')
        taxi_in_time_label.grid(column=0, row=1, sticky=tk.W, **self.padding_left)
        taxi_in_time_default = 5.3
        self.taxi_in_time = self.default_entry_box(taxi_in_time_default, 1, 1, self.second_frame_2)
        taxi_in_time_unit = ttk.Label(self.second_frame_2, text='min', width=3)
        taxi_in_time_unit.grid(column=2, row=1, sticky=tk.W, **self.padding_right_unit)

        ## Taxi out time
        taxi_out_time_label = ttk.Label(self.second_frame_2, text='Taxi out time:')
        taxi_out_time_label.grid(column=0, row=2, sticky=tk.W, **self.padding_left)
        taxi_out_time_default = 10.5
        self.taxi_out_time = self.default_entry_box(taxi_out_time_default, 1, 2, self.second_frame_2)
        taxi_out_time_unit = ttk.Label(self.second_frame_2, text='min', width=3)
        taxi_out_time_unit.grid(column=2, row=2, sticky=tk.W, **self.padding_right_unit)

        ## Arrival holding time
        holding_time_label = ttk.Label(self.second_frame_2, text='Arrival holding time:')
        holding_time_label.grid(column=0, row=3, sticky=tk.W, **self.padding_left)
        holding_time_default = 0
        self.holding_time = self.default_entry_box(holding_time_default, 1, 3, self.second_frame_2)
        holding_time_unit = ttk.Label(self.second_frame_2, text='min', width=3)
        holding_time_unit.grid(column=2, row=3, sticky=tk.W, **self.padding_right_unit)

        ## Alternate airport flight time
        alternate_time_label = ttk.Label(self.second_frame_2, text='Alternate airport flight time:')
        alternate_time_label.grid(column=0, row=4, sticky=tk.W, **self.padding_left)
        alternate_time_default = 45
        self.alternate_time = self.default_entry_box(alternate_time_default, 1, 4, self.second_frame_2)
        alternate_time_unit = ttk.Label(self.second_frame_2, text='min', width=3)
        alternate_time_unit.grid(column=2, row=4, sticky=tk.W, **self.padding_right_unit)

        ## Final reserve flight time
        reserve_time_label = ttk.Label(self.second_frame_2, text='Final reserve flight time:')
        reserve_time_label.grid(column=0, row=5, sticky=tk.W, **self.padding_left)
        reserve_time_default = 30
        self.reserve_time = self.default_entry_box(reserve_time_default, 1, 5, self.second_frame_2)
        reserve_time_unit = ttk.Label(self.second_frame_2, text='min', width=3)
        reserve_time_unit.grid(column=2, row=5, sticky=tk.W, **self.padding_right_unit)


        ## average passenger mass
        p_mass_label = ttk.Label(self.second_frame_3, text='average passenger mass:')
        p_mass_label.grid(column=0, row=1, sticky=tk.W, **self.padding_left)
        p_mass_default = 77.4
        self.mass_pas = self.default_entry_box(p_mass_default, 1, 1, self.second_frame_3)
        p_mass_unit = ttk.Label(self.second_frame_3, text='kg', width=3)
        p_mass_unit.grid(column=2, row=1, sticky=tk.W, **self.padding_right_unit)

        ## average baggage mass
        b_mass_label = ttk.Label(self.second_frame_3, text='average baggage mass:')
        b_mass_label.grid(column=0, row=2, sticky=tk.W, **self.padding_left)
        b_mass_default = 22.8
        self.mass_bag = self.default_entry_box(b_mass_default, 1, 2, self.second_frame_3)
        b_mass_unit = ttk.Label(self.second_frame_3, text='kg', width=3)
        b_mass_unit.grid(column=2, row=2, sticky=tk.W, **self.padding_right_unit)





        ## help message
        message = 'First, select the flight schedule file' + '\n' + \
                  'Then, select analysis type, fuel type, conversion type and reference' + '\n' + \
                  'Lastly, save your selection'
        text1 = ttk.Label(self.first_frame_4, text=message, font=("Courier", 8), foreground='blue')
        text1.grid(column=0,row=0,sticky=tk.W, **self.padding_right_unit)


        message = 'This step is optional!' + '\n' + \
                  'Set calculation pararmeters, default values are now displayed'
        text1 = ttk.Label(self.second_frame_5, text=message, font=("Courier", 8), foreground='blue')
        text1.grid(column=0,row=0,sticky=tk.W, **self.padding_right_unit)

        message = 'Select desired results, including:' + '\n' + \
                  '- emission results' + '\n' + \
                  '- energy consumption results'
        text1 = ttk.Label(self.third_frame_2, text=message, font=("Courier", 8), foreground='blue')
        text1.grid(column=0,row=0,sticky=tk.W, **self.padding_right_unit)

        message = 'Select desired analysis scenarios' + '\n' + \
                  'Module-1 is benchmark scenario where: ' + '\n' + \
                  '     emission results are calculated with default values ' + '\n' + \
                  'Module-2 create scenarios where:  ' + '\n' + \
                  '     emission results are calculated with different average PAX mass' + '\n' + \
                  'Module-3 create scenarios where:  ' + '\n' + \
                  '     emission results are calculated with different total PAX mass'
        text1 = ttk.Label(self.fourth_frame_2, text=message, font=("Courier", 8), foreground='blue')
        text1.grid(column=0,row=0,sticky=tk.W, **self.padding_right_unit)

        message = 'Submit all data and start calculation' + '\n' + \
                  'When calculation is finished, result files will be generated into ./result folder ' + '\n' + \
                  'under the same source folder as the previously submitted flight schedule data' + '\n\n' + \
                  'In order to view results on our dashboard, please:' + '\n' + \
                  '(1) Open the Greenbaggage_Dashboard_Airline.xlsm file in the result folder' + '\n' + \
                  '(2) Click "Refresh" button on the top right corner'
        text1 = ttk.Label(self.fifth_frame_2, text=message, font=("Courier", 8), foreground='blue')
        text1.grid(column=0,row=0,sticky=tk.W, **self.padding_right_unit)



        ## Logo Image
        if image == True:

            img = Image.open("./data/GUI_background.png")

            img_width = int(self.window_width * 0.3)
            hsize = int(self.window_height)

            img = img.resize((img_width,hsize), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            img_label = ttk.Label(self.first_frame_logo, image=img)
            img_label.image = img
            img_label.grid(pady=(10,10))

            img_label = ttk.Label(self.second_frame_logo, image=img)
            img_label.image = img
            img_label.grid(pady=(10,10))

            img_label = ttk.Label(self.third_frame_logo, image=img)
            img_label.image = img
            img_label.grid(pady=(10,10))

            img_label = ttk.Label(self.fourth_frame_logo, image=img)
            img_label.image = img
            img_label.grid(pady=(10,10))

            img_label = ttk.Label(self.fifth_frame_logo, image=img)
            img_label.image = img
            img_label.grid(pady=(10,10))

    
        ## Initialize values
        self.Define_Scenario_2()
        self.Define_Scenario_3()



    def Define_ChooseReference(self, *args):
        if (str(self.FuelType.get()) == 'Jet-A1' and str(self.ConversionType.get()) == 'GWP_100'):
            choice_4_menu = ttk.OptionMenu(
                self.first_frame_2,
                self.ReferenceType,
                self.Reference_types_1[0],
                *self.Reference_types_1)
            choice_4_menu.config(width=len(max(self.Reference_types_1, key=len)) + 0)
            choice_4_menu.grid(column=1, row=3, columnspan=3, sticky=tk.W, padx=(9, 3), pady=(0, 3))
        else:
            choice_4_menu = ttk.OptionMenu(
                self.first_frame_2,
                self.ReferenceType,
                self.Reference_types_2[1],
                *self.Reference_types_2)
            choice_4_menu.config(width=len(max(self.Reference_types_2, key=len)) + 0, state='disabled')
            choice_4_menu.grid(column=1, row=3, columnspan=3, sticky=tk.W, padx=(9, 3), pady=(0, 3))




    def Define_Scenario_2(self, *args):
        if (self.Scenario_var_2.get() == self.Scenario_selection[1]):
            A_type_style = ttk.Style()
            A_type_style.configure('A_type.TLabel',foreground='grey')

            self.sce_2_stepsize = ttk.Entry(self.fourth_frame_1, state='disabled', width=10)
            self.sce_2_stepsize.insert(0,'0')
            self.sce_2_stepsize.grid(column=3,row=3,sticky=tk.W, **self.padding_right)

            self.sce_2_min = ttk.Entry(self.fourth_frame_1, state='disabled', width=10)
            self.sce_2_min.insert(0,'0')
            self.sce_2_min.grid(column=3,row=4,sticky=tk.W, **self.padding_right)

            self.sce_2_max = ttk.Entry(self.fourth_frame_1, state='disabled', width=10)
            self.sce_2_max.insert(0,'0')
            self.sce_2_max.grid(column=3,row=5,sticky=tk.W, **self.padding_right)
        else:
            A_type_style = ttk.Style()
            A_type_style.configure('A_type.TLabel',foreground='black')

            self.sce_2_stepsize = ttk.Entry(self.fourth_frame_1, style='Grey.TEntry', width=10)
            self.sce_2_stepsize.insert(0,'0')
            self.sce_2_stepsize.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.sce_2_stepsize))
            self.sce_2_stepsize.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.sce_2_stepsize,'0'))
            self.sce_2_stepsize.grid(column=3,row=3,sticky=tk.W, **self.padding_right)

            self.sce_2_min = ttk.Entry(self.fourth_frame_1, style='Grey.TEntry', width=10)
            self.sce_2_min.insert(0,'0')
            self.sce_2_min.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.sce_2_min))
            self.sce_2_min.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.sce_2_min,'0'))
            self.sce_2_min.grid(column=3,row=4,sticky=tk.W, **self.padding_right)


            self.sce_2_max = ttk.Entry(self.fourth_frame_1, style='Grey.TEntry', width=10)
            self.sce_2_max.insert(0,'0')
            self.sce_2_max.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.sce_2_max))
            self.sce_2_max.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.sce_2_max,'0'))
            self.sce_2_max.grid(column=3,row=5,sticky=tk.W, **self.padding_right)

        ss_label = ttk.Label(self.fourth_frame_1, text='Change stepsize:', style='A_type.TLabel')
        ss_label.grid(column=2, row=3, sticky=tk.W, **self.padding_left)

        mass_change_unit = ttk.Label(self.fourth_frame_1, text='kg ', style='A_type.TLabel')
        mass_change_unit.grid(column=4,row=3,sticky=tk.W, **self.padding_right_unit)

        min_label = ttk.Label(self.fourth_frame_1, text='Minimum change:', style='A_type.TLabel')
        min_label.grid(column=2, row=4, sticky=tk.W, **self.padding_left)

        mass_change_unit = ttk.Label(self.fourth_frame_1, text='kg ', style='A_type.TLabel')
        mass_change_unit.grid(column=4,row=4,sticky=tk.W, **self.padding_right_unit)

        max_label = ttk.Label(self.fourth_frame_1, text='Maximum change:', style='A_type.TLabel')
        max_label.grid(column=2, row=5, sticky=tk.W, **self.padding_left)

        mass_change_unit = ttk.Label(self.fourth_frame_1, text='kg ', style='A_type.TLabel')
        mass_change_unit.grid(column=4,row=5,sticky=tk.W, **self.padding_right_unit)





    def Define_Scenario_3(self, *args):
        if (self.Scenario_var_3.get() == self.Scenario_selection[1]):
            A_type_style = ttk.Style()
            A_type_style.configure('A_type.TLabel',foreground='grey')

            self.sce_3_stepsize = ttk.Entry(self.fourth_frame_1, state='disabled', width=10)
            self.sce_3_stepsize.insert(0,'0')
            self.sce_3_stepsize.grid(column=3,row=7,sticky=tk.W, **self.padding_right)

            self.sce_3_min = ttk.Entry(self.fourth_frame_1, state='disabled', width=10)
            self.sce_3_min.insert(0,'0')
            self.sce_3_min.grid(column=3,row=8,sticky=tk.W, **self.padding_right)

            self.sce_3_max = ttk.Entry(self.fourth_frame_1, state='disabled', width=10)
            self.sce_3_max.insert(0,'0')
            self.sce_3_max.grid(column=3,row=9,sticky=tk.W, **self.padding_right)
        else:
            A_type_style = ttk.Style()
            A_type_style.configure('A_type.TLabel',foreground='black')
            self.sce_3_stepsize = ttk.Entry(self.fourth_frame_1, style='Grey.TEntry', width=10)
            self.sce_3_stepsize.insert(0,'0')
            self.sce_3_stepsize.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.sce_3_stepsize))
            self.sce_3_stepsize.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.sce_3_stepsize,'0'))
            self.sce_3_stepsize.grid(column=3,row=7,sticky=tk.W, **self.padding_right)

            self.sce_3_min = ttk.Entry(self.fourth_frame_1, style='Grey.TEntry', width=10)
            self.sce_3_min.insert(0,'0')
            self.sce_3_min.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.sce_3_min))
            self.sce_3_min.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.sce_3_min,'0'))
            self.sce_3_min.grid(column=3,row=8,sticky=tk.W, **self.padding_right)

            self.sce_3_max = ttk.Entry(self.fourth_frame_1, style='Grey.TEntry', width=10)
            self.sce_3_max.insert(0,'0')
            self.sce_3_max.bind("<FocusIn>", lambda args: self.focus_in_entry_box(self.sce_3_max))
            self.sce_3_max.bind("<FocusOut>", lambda args: self.focus_out_entry_box(self.sce_3_max,'0'))
            self.sce_3_max.grid(column=3,row=9,sticky=tk.W, **self.padding_right)


        ss_label = ttk.Label(self.fourth_frame_1, text='Change stepsize:', style='A_type.TLabel')
        ss_label.grid(column=2, row=7, sticky=tk.W, **self.padding_left)

        mass_change_unit = ttk.Label(self.fourth_frame_1, text='kg ', style='A_type.TLabel')
        mass_change_unit.grid(column=4,row=7,sticky=tk.W, **self.padding_right_unit)

        min_label = ttk.Label(self.fourth_frame_1, text='Minimum change:', style='A_type.TLabel')
        min_label.grid(column=2, row=8, sticky=tk.W, **self.padding_left)

        mass_change_unit = ttk.Label(self.fourth_frame_1, text='kg ', style='A_type.TLabel')
        mass_change_unit.grid(column=4,row=8,sticky=tk.W, **self.padding_right_unit)

        max_label = ttk.Label(self.fourth_frame_1, text='Maximum change:', style='A_type.TLabel')
        max_label.grid(column=2, row=9, sticky=tk.W, **self.padding_left)

        mass_change_unit = ttk.Label(self.fourth_frame_1, text='kg ', style='A_type.TLabel')
        mass_change_unit.grid(column=4,row=9,sticky=tk.W, **self.padding_right_unit)


    def UserCheck(self):
        showinfo(
            title='Log-in',
            message= 'Log in sucessefully'
        )



    def openfile(self):
        filetypes = (
            ("csv file", "*.csv"),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Select input file',
            initialdir='/',
            filetypes=filetypes)

        self.file_schedule = filename

        showinfo(
            title='Selected File',
            message=filename
        )


    def read(self):
        self.schedule_data = f_readFlightSchedule(self)
        showinfo(
            title='status',
            message='finish reading data'
        )




    def readfile(self):
        showinfo(
            title='status',
            message='start reading data'
        )
        self.read()







    def save_change_schedule(self):

        f_correctFlightSchedule(self)
        showinfo(
            title='parameter settings',
            message='changes saved sucessfully'
        )



    def Run(self):
        self.d_ver = 0
        f_GUIconnect(self)
        showinfo(
            title='status',
            message='result written into the input folder'
        )


    def submit(self):
        showinfo(
            title='status',
            message='start calculating emissions'
        )
        self.Run()



        




if __name__ == "__main__":
    root = emissionmodelGUI_App()
    root.mainloop()
