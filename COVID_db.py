import tkinter
import pandas
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tkinter.filedialog import askopenfilename
from tkinter import ttk

class window():
    def __init__(self):
        self.create_window()
        
        self.read_file(self.filename)
        self.country_list()
       
    def create_window(self):
        self.window = tkinter.Tk()
        
        def OpenFile(self):
            name = askopenfilename()
            self.filename = name
            
        self.title = self.window.title( "COVID-19 Country Plotter")
        
        self.menu = tkinter.Menu(self.window)
        self.window.config(menu=self.menu)
        
        self.file = tkinter.Menu(self.menu)
        
        self.file.add_command(label = 'Open', command = OpenFile(self))
        self.file.add_command(label = 'Exit', command = lambda:exit())
        self.menu.add_cascade(label = 'File', menu = self.file)
        
    def read_file(self,filename):
        splitname = filename.split('-')
        self.date = f'{splitname[-3]}-{splitname[-2]}-{splitname[-1][:2]}'
        
        self.data = pandas.read_excel(filename)
        self.data = self.data.reindex(index=self.data.index[::-1])
        return self.data
    
    def country_list(self):

        def onselect(event):
            w = event.widget

            self.curselections = w.curselection()
            idx = [i for i in self.curselections if i not in self.country_idx]
            value = w.get(idx)
            self.country_list.append(value)
            self.country_idx.extend(idx)
                
        self.frame = ttk.Frame(self.window, padding=(3, 3, 12, 12))
        self.frame.grid(column=0, row=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
       
        self.values = tkinter.StringVar()
        countries = self.data['countriesAndTerritories'].unique()
        self.values.set(countries)
        self.scrollbar = tkinter.Scrollbar(self.window, orient="vertical")
        self.listbox = tkinter.Listbox(self.frame, listvariable=self.values, selectmode=tkinter.MULTIPLE, 
                                       width=40, height=20, yscrollcommand=self.scrollbar.set)
        self.listbox.grid(column=0, row=0, columnspan=2, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
        self.country_list = []
        self.country_idx = []
        self.listbox.bind('<<ListboxSelect>>', onselect)
        
def find_per_capita(init_data, pop_col=None, vals_col=None):
    '''
    Function which finds out cases/deaths per capita.
    '''
    
    per_cap = (init_data.loc[:, vals_col] / init_data.loc[:, pop_col]) * 100
    return per_cap

def plot_graphs(countries, x_vals, y_vals, max_days=100, search_bounds=None, log_plot=True, 
                plot_date=None, plot_type=None, data_column=None, flag=None, constants=None):
    '''
    A function to produce nice plots of COVID-19 data.
    '''
    fig, ax = plt.subplots(figsize=[14,10])
    for country, x, y in zip(countries, x_vals, y_vals):
        if log_plot is True:
            plt.semilogy(x, y, linewidth=2, label=country)
        else:
            plt.plot(x, y, linewidth=2, label=country)
            
        plt.scatter(x[-1], y[-1], s=8, marker='o')
        plt.legend(loc='upper left')
        
        if country == 'United_States_of_America':
            flag_v = 'USA'
        elif country == 'United_Kingdom':
            flag_v = 'UK'
        else:
            flag_v = country
        print(flag_v, country)
        if flag:
            flags = flag_images()
            image = plt.imread(flags[flag_v])
            im = OffsetImage(image, zoom=0.25)
            ab = AnnotationBbox(im, (x[-1], y[-1]), xycoords='data', frameon=False)
            ax.add_artist(ab)
        else:
            plt.annotate(flag_v, (x[-1], y[-1]), 
                         xytext=(-30, 10), textcoords='offset pixels', fontsize=14)
            
        if constants:
            add_constant_curves(search_bounds, max_days)

    plt.annotate(f'Data accurate up to {plot_date}', xy=(0.3, 0.95), xycoords='axes fraction', fontsize=14)
    plt.xlabel(f'Days since {search_bounds[0]}th {plot_type.split(" ")[0]}')
    plt.ylabel(f'{plot_type} from COVID-19')
    plt.savefig(f'./{plot_date}_covid19_{plot_type}_rates.png', dpi=300)
    plt.show()
    
        
def flag_images():    
    flags = {'China': './flags/Flag_of_china.png',
             'Italy': './flags/Flag_of_italy.png',
             'Iran': './flags/Flag_of_iran.png',
             'South_Korea': './flags/Flag_of_south_korea.png',
             'France': './flags/Flag_of_France.png',
             'Germany': './flags/Flag_of_germany.png',
             'Spain': './flags/Flag_of_spain.png',
             'USA': './flags/Flag_of_USA.png',
             'UK': './flags/Flag_of_UK.png',
             'Netherlands': './flags/Flag_of_netherlands.png',
             'Japan': './flags/Flag_of_japan.png',
             'Turkey': './flags/Flag_of_turkey.png',
             'Brazil': './flags/Flag_of_brazil.png',
             'Austria': './flags/Flag_of_austria.png',
             'Denmark': './flags/flag_of_denmark.png',
             'Finland': './flags/Flag_of_finland.png',
             'Norway': './flags/Flag_of_norway.png',
             'South_Africa': './flags/Flag_of_south_africa.png',
             'Sweden': './flags/Flag_of_sweden.png',
             'Iceland': './flags/Flag_of_iceland.png',
             'India': './flags/Flag_of_india.png',
             'Russia': './flags/Flag_of_russia.png'
             }
    return flags

def add_constant_curves(bounds, max_days):
    '''
    Function to add cases of constant exponential increase to a graph.
    '''
    def exp_growth(init, d, g):
        return init + 2 ** (d / g)
    
    growth_rates = [2, 3, 5, 10]
    
    for i in growth_rates:
        x = np.linspace(0, 220, 221)
        y = exp_growth(0, x, i)
        totals = np.cumsum(y)
        start_idx = [i for i, val in enumerate(totals) if val < bounds[0]]
        stop_idx = [i for i, val in enumerate(totals) if val > bounds[1]]
        try:
            x = x[:stop_idx[0]-start_idx[-1]]
            totals = totals[start_idx[-1]:stop_idx[0]]
            if len(totals) > max_days:
                x = x[:max_days]
                totals = totals[:max_days]
        except IndexError:
            x = x[:max_days]
            totals = totals[start_idx[-1]:start_idx[-1]+max_days]
        plt.semilogy(x, totals, '--', color='grey', alpha=0.3)
        plt.annotate(f'{i} days', (x[-1], totals[-1]), 
                     xytext=(-30, 3), textcoords='offset pixels', color='grey', alpha=0.3)