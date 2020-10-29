#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:33:50 2020

@author: benjaminfeciura
"""

import pandas as pd
import matplotlib.pyplot as plt

### (0) Ask user before exporting results of query to CSV
def ExportCSV(dataframe):
    export = input("Do you want to export to CSV? [Y/N] ")
    if export.upper() == 'Y':
        filename = input("Provide filename: ")
        dataframe.pd.to_csv(filename)
    else:
        return 

### (1) Subset for range of year
def subset_by_year(dataFrame, start_year, stop_year = None):
    if stop_year == None:
        stop_year = start_year
    subset = dataFrame[(dataFrame['Year'] >= start_year) & (dataFrame['Year'] <= stop_year)]
    subset.reset_index(inplace = True, drop = True)
    return subset

### (2) Subset for given country
def subset_by_entity(dataFrame, entities):
    if type(entities) == str:
        entities = [entities]
    subset = dataFrame[(dataFrame['Entity'].isin(entities))]
    subset.reset_index(inplace = True, drop = True)
    return subset

### (3) Line plot of data over time

def line_plot(data, country_filter, start_year = 1751, stop_year = 2017, max_emissions = 7e9, fn = None):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    for country in country_filter:
        frame = data[data['Entity'] == country]
        plt.plot(frame['Year'], frame['Emissions'], label = frame['Entity'].iloc[0])
    
    plt.xlim(start_year, stop_year)
    plt.ylim(0, max_emissions)
    plt.xlabel('Year')
    plt.ylabel('Emissions')
    plt.title('Emissions over Time')
    ax.set_xticks(range(start_year, stop_year, 3))
    ax.set_xticklabels(range(start_year, stop_year, 3))
    plt.legend(loc=2, prop={'size': 7})
    
    if fn != None:
        plt.savefig(fn)
        print("Exported line plot to {}".format(fn))
    
    plt.show()
    return # a visual

def pie_chart(dataFrame, year, size_limit = 25, countries = None, fn = None):
    
    subset = subset_by_year(dataFrame, year)
    subset.sort_values(by = ['Emissions'], ascending = False, inplace = True)
    subset.reset_index(inplace = True, drop = True)
    labels = []
    slices = []
    other = 0
    if countries == None:
        for i in range(size_limit):
            labels.append(subset['Entity'][i])
            slices.append(subset['Emissions'][i])
        for i in range(size_limit, len(subset['Entity'])):
            other += subset['Emissions'][i]
    else:
        for i in range(len(subset['Entity'])):
            if subset["Entity"][i] in countries:
                labels.append(subset['Entity'][i])
                slices.append(subset['Emissions'][i])
            else:
                other += subset['Emissions'][i]
                
    slices.append(other)
    labels.append('Other')

    fig, ax = plt.subplots()
    ax.pie(slices, labels=labels, autopct='%.4f', startangle=90, radius = 3)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig = plt.gcf()
    fig.set_size_inches(12,12)
    fig.suptitle("Percentage of Global Emissions by Country in {}".format(year))
   
    if fn != None:
        plt.savefig(fn)
        print("Exported pie chart to {}".format(fn))
   
    plt.show()
    

    
    
    
    
    