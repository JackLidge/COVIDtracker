import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import COVID_db

results = COVID_db.window()
results.window.mainloop()

countries_of_interest = results.country_list
countries_of_interest = [i.strip("''") for i in countries_of_interest]

countries = {}
country_sel = 0

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
print(bounds)

max_days = 45

fig, ax = plt.subplots(figsize=[14,10])
for country in countries:
    start_index = np.searchsorted(countries[country]['cumulative'], bounds[0])
    end_index = np.searchsorted(countries[country]['cumulative'], bounds[1])
    
    try:
        if end_index - start_index < max_days:
            y = countries[country]['cases'].iloc[start_index:end_index]
            x = countries[country]['cumulative'].iloc[start_index:end_index]
        else:
            y = countries[country]['cases'].iloc[start_index:start_index+max_days]
            x = countries[country]['cumulative'].iloc[start_index:start_index+max_days]
    except IndexError:
        y = countries[country]['cases'].iloc[start_index:]
        x = countries[country]['cumulative'].iloc[start_index:]
    plt.loglog(x, y, linewidth=2, label=country)

    plt.scatter(x.iloc[-1], y.iloc[-1], s=8, marker='o')
    plt.legend(loc='upper left')
    
    if country == 'United_States_of_America':
        country = 'USA'
    if country == 'United_Kingdom':
        country = 'UK'

    flags = COVID_db.flag_images()
    image = plt.imread(flags[country])
    im = OffsetImage(image, zoom=0.25)
    ab = AnnotationBbox(im, (x.iloc[-1], y.iloc[-1]), xycoords='data', frameon=False)
    ax.add_artist(ab)
    
plt.annotate(f'Data accurate up to {results.date}', xy=(0.3, 0.95), xycoords='axes fraction', fontsize=14)
plt.xlabel(f'Total cases')
plt.ylabel(f'New cases')
plt.savefig(f'./covid19/{results.date}_Europe.png', dpi=300)
plt.show()