#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:33:28 2020

@author: benjaminfeciura
"""

from cs_proj_functions import *
import pandas as pd

print("|| Global Warning Visualization Tool ||")
print("CS 5010 Semester Project | Fall 2020")
print("Authors:")
print("Nima Beheshti (nb9pp)")
print("Jess Cheu (jc4vg)")
print("Ben Feciura (bmf3bw)")
print("Gary Mitchell (gm3gq)")
print()

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
    print("\n[1] Filter by Country")
    print("[2] Filter by Year")
    print("[3] Clear Filters")
    print("[4] Produce Visualization")
    print("[5] Export Data\n")
    print("[0] Quit")    


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
        country = input("Enter another country (or if finished, enter DONE): ")
        if country == "DONE":
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
    print("[1] Single Year")
    print("[2] Range of Years")
    selection = int(input("Please make a selection: "))
    if selection == 1:
        start_year = int(input("Enter year: "))
        stop_year = start_year
    elif selection == 2:
        start_year = int(input("Enter first year: "))
        stop_year = int(input("Enter last year: "))
    else:
        print("Invalid Selection.")
        return
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
    elif selection == 3:
        country_filter = ["All"]
        start_year = -1
        stop_year = -1
        data = full_data
    else:
        print("Invalid selection.")

def produce_visualization(data, country_filter, start_year, stop_year):
    print("Which type of visualization?")
    print("[1] Pie Chart (Compare contributions of selected countries to")
    print("    total global emissions for selected year)")
    print("[2] Line Graph (Compare selected countries' emissions over")
    print("    selected range of years)")
    print()
    selection = int(input("Please make a selection: "))
    if selection == 1:
        size_limit = 0
        if country_filter == ["All"]:
            countries = None
            size_limit = int(input("Show __ largest contributors: "))
        else:
            countries = country_filter
        if start_year == -1:
            year = int(input("Please specify a year: "))
        elif start_year != stop_year:
            print("Multiple years selected.")
            year = int(input("Please choose a year between {0} and {1}: ".format(start_year, stop_year)))
        else:
            year = start_year
        save = input("Export visualization? [Y/N] ")
        if save == "Y" or "y":
            fn = input("Provide filename: ")
        else:
            fn = None
        pie_chart(full_data, year, size_limit, countries, fn)
    if selection == 2:
        if country_filter == ["All"]:
            print("Please filter by a subset of countries first.")
            return
        save = input("Export visualization? [Y/N] ")
        if save.upper() == "Y":
            fn = input("Provide filename: ")
        else:
            fn = None
        line_plot(data, country_filter, data['Year'].min(), data['Year'].max(), data['Emissions'].max(), fn)
    return
    
def export_subset(data):
    fn = input("Name of output file: ")
    data.to_csv(fn, index = False)
    print("Exported {0}".format(fn))
  
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
        produce_visualization(data, country_filter, start_year, stop_year)
    elif selection == 5:
        export_subset(data)
    elif selection == 0:
        break
    else:
        print("Invalid selection.")

print("Thank you for using our visualization utility!")
        