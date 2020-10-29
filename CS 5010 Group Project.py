#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS 5010 Project

"Global Warning"

Gary Mitchell ()
Jess Cheu ()
Nima Beheshti ()
Ben Feciura (bmf3bw)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as m

#-----------------------------------------------------------------------------

'''
FUNCTIONS
'''

### (0) Ask user before exporting results of query to CSV
def ExportCSV(dataframe):
    export = input("Do you want to export to CSV? [Y/N] ")
    if export.upper() == 'Y':
        filename = input("Provide filename: ")
        dataframe.to_csv(filename)
    else:
        return 

### (1) Subset for range of year
def subset_by_year(dataFrame, start_year, stop_year = None):
    if stop_year == None:
        stop_year = start_year
    subset = dataFrame[(dataFrame['Year'] >= start_year) & (dataFrame['Year'] <= stop_year)]
    return subset

### (2) Subset for given country
def subset_by_entity(dataFrame, entity):
    subset = dataFrame[(dataFrame['Entity'] == entity)]
    return subset

### (3) Line plot of data over time
def LinePlot(entity, start_year, end_year):
    return # a visual

#-----------------------------------------------------------------------------
'''
DATA CLEANING
'''
data = pd.read_csv("co2_emission.csv")

# Rename the terribly named C02 Emissions Column.
data.rename(columns = {"Annual CO₂ emissions (tonnes )": "Emissions"}, inplace = True)
print(data.head())

# Get summary statistics for our dataset
print("\nSummary Statistics:\n")
print(data.describe())


# We see that there are negative values for emission... find out why
print("\nNegative Emissions Values:\n")
print(data[data["Emissions"] < 0].head())

# Get and print a list of all the Entities in the dataset
country_names = []

for countries in data["Entity"]:
    if countries not in country_names:
        country_names.append(countries)

print("\nAll Entities:\n")        
print(country_names)
        
# List entities from that list which we want to exclude (continents, special
# categories, negative emission value, etc.)
countries_to_exclude = ['Africa', 'Americas (other)', 'Antarctic Fisheries', 'Asia and Pacific (other)', 'Christmas Island', 'Czechoslovakia', 'EU-28', 'Europe (other)', 'Gibraltar', 'Greenland', 'International transport', 'Kyrgyzstan', 'Lesotho', 'Middle East', 'New Caledonia', 'Reunion', 'Sint Maarteen', 'Statistical Differences','Statistical differences', 'World', 'Wallis and Futuna Islands']

# And subset the dataset so as to exclude those
exclude = []

for entity in data["Entity"]:
    if entity in countries_to_exclude:
        exclude.append(True)
    else:
        exclude.append(False)
    

data["Exclude"] = pd.Series(exclude)

data_countries = data[(data["Exclude"]) == False]

# And remove the exclude column
data_countries.drop(columns = ['Exclude'], inplace = True)
data_countries.reset_index(inplace = True, drop = True)



### Subset the data to showonly global data
world = data[data['Entity'] == 'World'].reset_index(drop = True)

### Emissions from international transport
trans = data[data['Entity'] == 'International transport'].reset_index(drop = True)

#-----------------------------------------------------------------------------

'''
FEATURE ENGINEERING
'''
### Emission statistic per capita for example - possible difficulties with population dataset


### Emission change year over year.
yearly_change = [0]

for i in range(1, len(data_countries['Entity'])):
    # If we find the country name changes, it's the first entry for that 
    # country so the percent change should be 0.
    if data_countries['Entity'][i] != data_countries['Entity'][i-1]:
        yearly_change.append(0)
        continue
    # Otherwise, find percent change.
    else:
        difference = data_countries['Emissions'][i] - data_countries['Emissions'][i-1]
        # If the previous value was 0, avoid divide by 0 error
        if data_countries['Emissions'][i-1] == 0:
            # If the current value is nonzero, make sure the percentage change
            # ends up being 100 by setting denominator = numerator
            if data_countries['Emissions'][i] != 0:
                denominator = data_countries['Emissions'][i]
            # Otherwise ensure percentage change is 0 by calculating 0/1
            else:
                denominator = 1
        else:
            denominator = data_countries['Emissions'][i-1]
            
        pct_change = (difference*100) / denominator
    
        yearly_change.append(pct_change)

# Create a column to add to our cleaned data
data_countries['YoY_Pct_Change'] = pd.Series(yearly_change)

data_countries.to_csv("pctchange.csv")

### Examine streaks of consecutive years of similar change.
streak_double = [0]
streak = 0
for i in range(1, len(data_countries['Entity'])):
    if data_countries['YoY_Pct_Change'][i] >= 100:
        streak += 1
    else:
        streak = 0
    streak_double.append(streak)
    
data_countries['Streak_Double'] = pd.Series(streak_double)
print("\nSummary including new columns:\n")
print(data_countries.describe())


### Global emission per year compared to individual countries
# Country's percent of global emissions for any given year
percent_of_global = [] #empty list for percent of global emissions for the year by every country

for i in range(len(data_countries['Year'])):
    year = data_countries['Year'][i]
    global_amt = world[world['Year'] == year]['Emissions'].iloc[0]
    pctCountry = data_countries['Emissions'][i]/global_amt*100   #I don't think I have the original dataset - global emissions already removed 
    percent_of_global.append(pctCountry)
    
data_countries['Pct_Global'] = pd.Series(percent_of_global)


data_countries.to_csv("data_cleaned.csv", index = False)

#-----------------------------------------------------------------------------

'''
SUBSETTING
'''


### Subset the data to only show years greater than or equal to the mean year for all countries
data_modern = subset_by_year(data_countries, m.ceil(data_countries['Year'].mean()), data_countries['Year'].max())
data_modern.reset_index(inplace = True, drop = True)
print("\nSummary for {0} onward:\n".format(m.ceil(data_countries['Year'].mean())))
print(data_modern.describe())


#-----------------------------------------------------------------------------

'''
QUERIES
'''

### All entries where a country's output at least doubled from the previous 
### year:

doubles = data_countries[data_countries['YoY_Pct_Change'] >= 100]
print("\nInstances of >2x Year-over-year increase in emissions:\n")
print(doubles.head())


###Output decreases from previous year:

reduced = data_countries[data_countries['YoY_Pct_Change'] < 0]
print("\nInstances where countries cut their emissions:\n")
print(reduced.head())


### Any carbon-zero years?
no_carbon = data_modern[(data_modern['Emissions'] == 0)]
print("\nModern isntances of carbon-zero years?:\n")
print(no_carbon.head())
print("{0} instances of carbon-zero years.".format(len(no_carbon['Entity'])))

no_carbon = data_modern[(data_modern['Emissions'] == 0) & (data_modern['Year'] >= 2000)]
print("\nInstances in the 21st century of carbon-zero years?:\n")
print(no_carbon.head())
print("{0} instances of carbon-zero years.".format(len(no_carbon['Entity'])))
# RIP


### Check percentage of global emission contributed by International Transport
transport = []
for i in trans['Emissions']:
    transport.append(i)
world_total = []
for i in world['Emissions']:
    world_total.append(i)
#print(transport)
#print(world_total)
t = np.array(transport, dtype=np.float)
wt = np.array(world_total, dtype=np.float)

Percentage_of_total_emissions_from_international_transport = 100*(t/wt)
#print(Percentage_of_total_emissions_from_international_transport)
trans['% of world emissions'] = Percentage_of_total_emissions_from_international_transport
print(trans)


### Emission statistics by continent
continents_filter = data.Entity.isin(['Africa', 'Americas (other)','Asia and Pacific (other)','Europe (other)','Australia','Antarctic Fisheries'])
print(data[continents_filter])



#-----------------------------------------------------------------------------

'''
VISUALIZATION
'''

### Make sure to specify what subset of data is used for the visualization

### Heatmap or pie chart based on 2017 emission quantities
### Ben
def pie_chart(dataframe, year, top_contributors = 25):
    subset = subset_by_year(dataframe, year)
    subset.sort_values(by = ['Emissions'], ascending = False, inplace = True)
    subset.reset_index(inplace = True, drop = True)
    labels = []
    slices = []
    other = 0
    for i in range(top_contributors):
        labels.append(subset['Entity'][i])
        slices.append(subset['Emissions'][i])
    for i in range(top_contributors, len(subset['Entity'])):
        other += subset['Emissions'][i]
    slices.append(other)
    labels.append('Other')

    fig, ax = plt.subplots()
    ax.pie(slices, labels=labels, autopct='%.4f', startangle=90, radius = 3)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig = plt.gcf()
    fig.set_size_inches(12,12)
    fig.suptitle("Percentage of Global Emissions by Country in 2017 ({0} largest)".format(str(top_contributors)))
    plt.show()
    
pie_chart(data_countries, 2017, 25)

### Line plot of global emission over time
### Gary

world = data[(data['Entity'] == 'World')]
world.plot(x = 'Year',y='Emissions')


### Look at countries with decreasing emissions/rate of decrease
### Jess
### Look at countries with decreasing emissions/rate of decrease
### Find a section of time where emissions generally decreased and look at the
### top 5 emission countries over range of years
### Decrease in the late 20s into the early 30s until beginning of WWII
### Upspike until 1945 at the end it WWII

### Find decreasing emissions for countries
streak_decrease = [0]
streak = 0
for i in range(1, len(data_countries['Entity'])):
    if data_countries['YoY_Pct_Change'][i] < 0:
        streak += 1 
    else:
        streak = 0
    streak_decrease.append(streak)
    
data_countries['Streak_Decrease'] = pd.Series(streak_decrease)
#print("\nSummary including new Streak_Decrease column:\n")
#print(data_countries.describe())

### Find years where global emissions fell over 20% to determine year range for graph 
years_decrease = []
for i in range(1,len(data_countries['Year'])):
    year = data_countries['Year'][i]
    year_last = data_countries['Year'][i-1]
    if world[world['Year'] == year]['Emissions'].iloc[0] < 0.8*world[world['Year'] == year_last]['Emissions'].iloc[0]:
        years_decrease.append(year)

years_decrease.sort()
years_decrease = list(dict.fromkeys(years_decrease))
#print(years_decrease)

### global emissions from 1927 to 1948
### search highest emissions for 1927
highemission_1927 = data_countries[data_countries['Year'] == 1927]
highemission_1927 = highemission_1927.sort_values(by=['Pct_Global'])
#print(highemission_1927.head())
#print(highemission_1927.tail())

### create data frame for top 5 energy producers during time frame and global emissions
### United States, Germany, UK, France, Canada, and global emissions
def countrydf(countryName):
    countrydf = data_countries.loc[data_countries['Entity'] == countryName]
    return countrydf

UnitedStatesdf = countrydf('United States')
UnitedKingdomdf = countrydf('United Kingdom')
Germanydf = countrydf('Germany')
Francedf = countrydf('France')
Canadadf = countrydf('Canada')

### dataframe of all countries and world from 1927-1947
def countrydfyr(dataframe):
    new_data = []
    for year in range(1927,1948):
        data = dataframe.loc[dataframe['Year'] == year]
        new_data.append(data)
        final = pd.concat(new_data)
    return final
    
US = countrydfyr(UnitedStatesdf)
UK = countrydfyr(UnitedKingdomdf)
Germany = countrydfyr(Germanydf)
France = countrydfyr(Francedf)
Canada = countrydfyr(Canadadf)
World = countrydfyr(world)
dflst = [US, UK, Germany, France, Canada, World]
years_decrease_df = pd.concat(dflst)
#print(years_decrease_df)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
for frame in [US, UK, Germany, France, Canada, World]:
    plt.plot(frame['Year'], frame['Emissions'], label = frame['Entity'].iloc[0])
    
plt.xlim(1927,1947)
plt.ylim(0,6e9)
plt.xlabel('Year')
plt.ylabel('Emissions')
plt.title('Emissions over the Years')
ax.set_xticks(range(1927,1948,3))
ax.set_xticklabels(range(1927,1948,3))
plt.legend(loc=2, prop={'size': 7})
plt.show()


### Significant Events
### Nima
# Syria during Civil War 2011-2017
# Significant decrease in emissions
syria_df = subset_by_year(subset_by_entity(data, 'Syria'), 2000,2017)
print(syria_df)
syria_df.plot.line(x = 'Year', y = 'Emissions')

# Lebanon during civil war 1975-1990
# No noticable changes to slope
lebanon_df = subset_by_year(subset_by_entity(data, 'Lebanon'), 1970,2017)
print(lebanon_df)
lebanon_df.plot.line(x = 'Year', y = 'Emissions')

# Global internet age 2000-2017
# No significant changes to slope
transport_df = subset_by_year(subset_by_entity(data, 'International transport'), 1980,2017)
print(transport_df)
transport_df.plot.line(x = 'Year', y = 'Emissions')

# North Korea
# Decrease in emissios during the past 30 years
nkorea_df = subset_by_year(subset_by_entity(data, 'North Korea'), 1980, 2017)
print(nkorea_df)
nkorea_df.plot.line(x = 'Year', y = 'Emissions')

#-----------------------------------------------------------------------------

'''
UNIT TESTING
'''
# I/O Functions

# Visualization functions (not testable?)

# Subsetting functions
# By year
# By entity




#-----------------------------------------------------------------------------
'''
HOUSEKEEPING
'''

# Make sure to take notes along the way to make unit tests easy and manageable

#-----------------------------------------------------------------------------
'''
FOR NEXT WEEK
'''
### Presentation November 18

# Come up with ideas for more functions to reuse and modularize
# Convert existing work to use functions

# Come up with a program flow

# Think of a time and questions for meeting with Dr. Basit
## Friday October 30, 6:00PM?
## Preference for presentation of code/number of files etc.
## Use of pandas/numpy utilities in unit testing

# Ideas for "putting emissions in context" portion of presentation
