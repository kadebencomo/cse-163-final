import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

crimes = pd.read_csv('ucr_by_state.csv')
race = pd.read_csv('populations_states.csv')
data = pd.read_csv('incarceration_rates_merged.csv')


# joining dataframes
race['Date'] = pd.to_datetime(race['date'])
race = race.set_index(['Date'])
race_yr = race.resample('Y').mean()
y = race_yr.index.year
race_yr['Year'] = y
i = crimes.merge(race_yr, left_on='year', right_on='Year')
incarceration_rates = i[ ['jurisdiction'] + list(i.iloc[:,4:14]) + list(i.iloc[:,21:]) ]
incarceration_rates.to_csv('incarceration_rates_merged.csv')


# research question 1
crimes_columns = ['murder_manslaughter', 'rape_legacy', 'robbery', 'agg_assault', 
                  'property_crime_total', 'burglary', 'larceny']
data[crimes_columns] = data[crimes_columns].replace(',', '', regex=True).astype(float)
grouped_data = data.groupby('Year')[crimes_columns].sum().reset_index()
years_in_range = grouped_data[(grouped_data['Year'] >= 2015) & (grouped_data['Year'] <= 2018)]
crime_names = ['Murder', 'Rape', 'Robbery', 'Assault', 'Property Crime', 'Burglary', 'Larceny']
colors = ['red', 'skyblue', 'lightpink', 'purple', 'yellow', 'lightgreen', 'orange']
for index, row in years_in_range.iterrows():
    year = int(row['Year'])
    data = row[crimes_columns]
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data.values, color=colors)
    plt.title(f'Crimes for Year {year}')
    plt.xlabel('Crime Type')
    plt.ylabel('Number of Crimes (in millions)')
    plt.xticks(data.index, crime_names)


# research question 2
data['violent_crime_total'] = pd.to_numeric(data['violent_crime_total'], errors='coerce')
data.dropna(subset=['violent_crime_total'], inplace=True)
fig, axs = plt.subplots(1, 3, figsize=(18, 6))
years = range(2015, 2018)
for i, year in enumerate(years):
    df_year = data[data['Year'] == year]
    df_year_grouped = df_year.groupby('jurisdiction')['violent_crime_total'].sum().reset_index()
    ax = axs[i]
    df_year_grouped.plot(kind='bar', x='jurisdiction', y='violent_crime_total', ax=ax)
    ax.set_xticklabels(df_year_grouped['jurisdiction'], rotation=45)
    ax.set_title(f'Year {year}')
    ax.set_xlabel('State')
    ax.set_ylabel('Incarcerations')
    ax.set_title(f'Year {year}')
    plt.savefig('violentcrime_peryear')


# research question 3
murder = incarceration_rates[['murder_manslaughter', 'Year', 'jurisdiction']]
murder.murder_manslaughter = murder.murder_manslaughter.apply(lambda x : x.replace(',',''))
murder['murder_manslaughter'] = murder['murder_manslaughter'].astype(float)
grouped_murder = murder.groupby('Year')['murder_manslaughter'].sum().reset_index(name ='murder')

white = incarceration_rates.groupby('Year')['incarcerated_white'].mean().reset_index(name ='White')
black = incarceration_rates.groupby('Year')['incarcerated_black'].mean().reset_index(name ='Black')
hispanic = incarceration_rates.groupby('Year')['incarcerated_hispanic'].mean().reset_index(name ='Hispanic')
amerind = incarceration_rates.groupby('Year')['incarcerated_amerind'].mean().reset_index(name ='Amerind')
asian = incarceration_rates.groupby('Year')['incarcerated_asian'].mean().reset_index(name ='Asian')

fig, axs = plt.subplots(5, 1, figsize=(8, 15))
axs[0].plot(white['Year'], white['White'], label='white')
axs[0].plot(grouped_murder['Year'], grouped_murder['murder'], label='murders in US')
axs[0].set_title('US White Prison Population versus Murder Rates Over Time')

axs[1].plot(black['Year'], black['Black'], label='black')
axs[1].plot(grouped_murder['Year'], grouped_murder['murder'], label='murders in US')
axs[1].set_title('US Black Prison Population versus Murder Rates Over Time')

axs[2].plot(hispanic['Year'], hispanic['Hispanic'], label='hispanic')
axs[2].plot(grouped_murder['Year'], grouped_murder['murder'], label='murders in US')
axs[2].set_title('US Hispanic Prison Population versus Murder Rates Over Time')

axs[3].plot(amerind['Year'], amerind['Amerind'], label='amerind')
axs[3].plot(grouped_murder['Year'], grouped_murder['murder'], label='murders in US')
axs[3].set_title('US Amerind Prison Population versus Murder Rates Over Time')

axs[4].plot(asian['Year'], asian['Asian'], label='asian')
axs[4].plot(grouped_murder['Year'], grouped_murder['murder'], label='murders in US')
axs[4].set_title('US Asian Prison Population versus Murder Rates Over Time')

for ax in axs:
    ax.legend()

plt.tight_layout()
plt.savefig('line_plot.png')


# for testing
grouped_murder.to_csv('murders.csv')
white.to_csv('white.csv')
black.to_csv('black.csv')
hispanic.to_csv('hispanic.csv')
amerind.to_csv('amerind.csv')
asian.to_csv('asian.csv')
