import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import rona_db

results = rona_db.window()
results.window.mainloop()

countries_of_interest = results.country_list
countries_of_interest = [i.strip("''") for i in countries_of_interest]

countries = {}
country_sel = 0

dates = results.data['dateRep'].unique()
dates.sort()

for i, country in enumerate(countries_of_interest):
    temp = results.data.loc[results.data['countriesAndTerritories'] == country].copy()
    temp['cumulative'] = temp['cases'].cumsum()
    temp['cum_deaths'] = temp['deaths'].cumsum()
    print(country)
    temp['per_capita_cases'] = rona_db.find_per_capita(temp, pop_col='popData2018', vals_col='cumulative')
    temp['per_capita_deaths'] = rona_db.find_per_capita(temp, pop_col='popData2018', vals_col='cum_deaths')
    temp.reset_index(drop=True, inplace=True)
    countries[country] = temp
  
full_data = []
for j, date in enumerate(dates):
    date_countries = []
    for i, country in enumerate(countries):
        country_list = [str(i)[:10] for i in countries[country]['dateRep'].values]
        if str(date)[:10] in country_list:
            index = np.searchsorted(countries[country]['dateRep'], date)
            y = countries[country]['cumulative'].iloc[:index+1]
            x = countries[country]['dateRep'].iloc[:index+1]
            x = [str(i)[:10] for i in x]
            temp = {'country': country, 'x': x, 'y': y}
            
            date_countries.append(temp)
    full_data.append(date_countries)
    
# for i, country in enumerate(countries):
#     full_data.append({'country': country, 'x': [], 'y' : []})
#     country_list = [str(i)[:10] for i in countries[country]['dateRep'].values]
#     for j, date in enumerate(dates):
#         if str(date)[:10] in country_list:
#             index = np.searchsorted(countries[country]['dateRep'], date)
#             y = countries[country]['cumulative'].iloc[index]
#             x = str(countries[country]['dateRep'].iloc[index])[:10]
#             full_data[i]['x'].append(x)
#             full_data[i]['y'].append(y)
    
for idx, val in enumerate(full_data):
    fig, ax = plt.subplots(figsize=[14,10])
    max_vals = []
    [max_vals.append(i['y'].max()) for i in val]
    if np.max(max_vals) == 0:
        continue
    
    for i in val:    
        plt.semilogy(i['x'], i['y'], linewidth=2, label=i['country'])
        plt.scatter(i['x'][-1], i['y'].values[-1], s=8, marker='o')
        if i['country'] == 'United_States_of_America':
            i['country'] = 'USA'
        if i['country'] == 'United_Kingdom':
            i['country'] = 'UK'
        flags = rona_db.flag_images()
        image = plt.imread(flags[i['country']])
        im = OffsetImage(image, zoom=0.25)
        ab = AnnotationBbox(im, (i['x'][-1], np.max(i['y'])), xycoords='data', frameon=False)
        ax.add_artist(ab)
    #plt.annotate(i['country'], (i['x'][-1], i['y'].max()), xytext=(-30, 10), textcoords='offset pixels', fontsize=14)
    plt.annotate(f'{val[-1]["x"][-1]}', xy=(0.3, 0.95), xycoords='axes fraction', fontsize=14)
    plt.ylim([100, 1500000])
    plt.xlabel(f'Date')
    plt.ylabel(f'Cases of COVID-19')
    plt.xticks([], [])
    plt.legend(loc='upper left')
    plt.savefig(f'./animation/{i["x"][-1]}_covid19_case_rates.png', dpi=300)
    plt.show()