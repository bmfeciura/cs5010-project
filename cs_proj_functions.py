#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:33:50 2020

@author: benjaminfeciura
"""

import pandas as pd

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
def LinePlot(entity, start_year, end_year):
    return # a visual