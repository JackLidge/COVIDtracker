import pandas
import matplotlib.pyplot as plt

import COVID_db

results = COVID_db.window()
results.window.mainloop()

countries_of_interest = results.country_list
countries_of_interest = [i.strip("''") for i in countries_of_interest]

x_vals = []
y_vals = []

for country in countries_of_interest:
    temp = results.data.loc[results.data['countriesAndTerritories'] == country].copy()
    temp = temp.sort_values('dateRep')
    x_vals.append(temp['dateRep'].values)
    y_vals.append(temp['14_day_per_100k'].values)
    
COVID_db.plot_graphs(countries_of_interest, x_vals, y_vals, log_plot=False, search_bounds=(1,1), 
                    plot_type='Cases per 100k people', plot_date='2020-08-14', flag=True)
