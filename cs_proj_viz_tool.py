#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:33:28 2020

@author: benjaminfeciura
"""

from cs_proj_functions import *
import pandas as pd

# Ask until the user provides a valid filename
while True:
    try:
        fn = input("Please provide a filename for the dataset: ")
        full_data = pd.read_csv(fn, )
        break
    except:
        print("File not found!")
# Notify the user
print("Loaded {0}\n".format(fn))

# Global variables
data = full_data # Copy of full dataset
country_filter = ["All"] # List of countries (default value ["All"])
start_year = -1 # First year of range in filter (default value -1)
stop_year = -1 # Last year of range in filter (default value -1)
entries = len(data) # Number of entries in subset (initialize on full dataset)

# Print out the current state of the subset and the menu options.
def print_menu():
    print("\n{0} observations found.\n".format(entries))
    print("--Filters--")
    print("Countries:")
    print(*country_filter, sep = ", ")
    print("Years:")
    if start_year == -1:
        print("All")
    elif start_year == stop_year:
        print(start_year)
    else:
        print("{0} to {1}".format(start_year, stop_year))
    print("\n[1] Filter by Country\n[2] Filter by Year\n[3] Clear Filters\n[X] Produce Visualization\n[5] Export Data\n\n[0] Quit")    


def filter_country():
    global data
    global country_filter
    if country_filter == ["All"]:
        country_filter = []
        country = input("Enter first country: ")
        country_filter.append(country)
    while True:
        print("\nIncluded Countries:")
        print(*country_filter, sep = ", ")
        country = input("Enter another country (or if finished, enter Done): ")
        if country == "Done":
            break
        else:
            country_filter.append(country)
    data = subset_by_entity(full_data, country_filter)
    if start_year != -1:
        data = subset_by_year(data, start_year, stop_year)
        
def filter_year():
    global data
    global start_year
    global stop_year
    print("[1] Single Year\n[2] Range of Years")
    selection = int(input("Please make a selection: "))
    if selection == 1:
        start_year = int(input("Enter year: "))
        stop_year = start_year
    else:
        start_year = int(input("Enter first year: "))
        stop_year = int(input("Enter last year: "))
    data = subset_by_year(full_data, start_year, stop_year)
    if country_filter != ["All"]:
        data = subset_by_entity(data, country_filter)

        
def clear_filters():
    global full_data
    global data
    global country_filter
    global year_filter
    global start_year
    global stop_year
    print("Reset which filters?")
    print("[1] Countries")
    print("[2] Years")
    print("[3] All")
    selection = int(input("Please make a selection: "))
    if selection == 1:
        country_filter = ["All"]
        if start_year == -1:
            data = full_data
        else:
            data = subset_by_year(full_data, start_year, stop_year)
    elif selection == 2:
        start_year = -1
        stop_year = -1
        if country_filter == ["All"]:
            data = full_data
        else:
            data = subset_by_entity(data, country_filter)
    else:
        country_filter = ["All"]
        start_year = -1
        stop_year = -1
        data = full_data
    return
    
def export_subset(data):
    fn = input("Name of output file: ")
    data.to_csv(fn, index = False)
    print("Exported {}".format(fn))
    return
  
end_program = False
while True:
    print_menu()
    selection = int(input("Please make a selection: "))
    if selection == 1:
        filter_country()
        entries = len(data)
        continue
    elif selection == 2:
        filter_year()
        entries = len(data)
    elif selection == 3:
        clear_filters()
        entries = len(data)
    elif selection == 4:
        continue
    elif selection == 5:
        export_subset(data)
    elif selection == 0:
        break
    else:
        print("Invalid selection.")

print("Thank you for using our visualization utility!")
        