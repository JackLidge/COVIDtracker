import COVID_db

results = COVID_db.window()
results.window.mainloop()

countries_of_interest = results.country_list
countries_of_interest = [i.strip("''") for i in countries_of_interest]

# ['China', 'Italy', 'Iran', 'South_Korea', 'Japan', 'France', 'Germany', 'Spain', 
#  'United_Kingdom', 'United_States_of_America']
# ['Norway', 'Portugal', 'Canada', 'Australia', 'Malaysia', 'Brazil', 'Israel']

countries = {}
country_sel = 0

no_infected_countries = len(results.data['countriesAndTerritories'].unique())

for i, country in enumerate(countries_of_interest):
    temp = results.data.loc[results.data['countriesAndTerritories'] == country].copy()
    temp['cumulative'] = temp['cases'].cumsum()
    temp['cum_deaths'] = temp['deaths'].cumsum()
    print(country)
    temp['per_capita_cases'] = COVID_db.find_per_capita(temp, pop_col='popData2018', vals_col='cumulative')
    temp['per_capita_deaths'] = COVID_db.find_per_capita(temp, pop_col='popData2018', vals_col='cum_deaths')
    temp.reset_index(drop=True, inplace=True)
    countries[country] = temp
    
bounds = [100, 100000]
start_cases = input("Select initial number of cases to plot (default is 100): ")
end_cases = input("Select final number of case to plot (default is 100,000): ")
try:
    bounds[0] = int(start_cases)
except ValueError:
    pass
try:
    bounds[1] = int(end_cases)
except ValueError:
    pass

'''
Invocation of plot_graphs needs redoing
'''

COVID_db.plot_graphs(countries, col_to_search='cumulative', search_bounds=bounds, plot_date=results.date,
            plot_type='cases', constants=True)

COVID_db.plot_graphs(countries, col_to_search='cumulative', search_bounds=bounds, log_plot=False,
            plot_date=results.date, plot_type='cases per capita', data_column='per_capita_cases')

bounds = [10, 5000]
start_deaths = input("Select initial number of deaths to plot (default is 10): ")
end_deaths = input("Select final number of deaths to plot (default is 5,000): ")
try:
    bounds[0] = int(start_deaths)
except ValueError:
    pass
try:
    bounds[1] = int(end_deaths)
except ValueError:
    pass

COVID_db.plot_graphs(countries, col_to_search='cum_deaths', search_bounds=bounds, plot_date=results.date,
            plot_type='deaths', constants=True)

COVID_db.plot_graphs(countries, col_to_search='cum_deaths', search_bounds=bounds, log_plot=False,
            plot_date=results.date, plot_type='deaths per capita', data_column='per_capita_deaths')
