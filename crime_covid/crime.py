"""

@author: 

Tianyi Wang: tianyiwa@andrew.cmu.edu
Wan-Ju Yu: wyu2@andrew.cmu.edu
Xi Yan: xiyan@andrew.cmu.edu,
Florence Pan: qinghep@andrew.cmu.edu

"""

import matplotlib.pyplot as plt
import pandas as pd
import gmplot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import ssl


def get_df():
    """Collect data, output csv, clean data"""
    # disable certificate verification temporarily so that computer is able to access the website
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://data.wprdc.org/datastore/dump/1797ead8-8262-41cc-9099-cbc8a161924b'
    df = pd.read_csv(url)
    # If want to generate csv file uncomment the below line
    #df.to_csv('out.csv')
    df.head()
    df = df[df.X != 0]
    df = df[df['X'].notna()]
    df = df[df.Y != 0]
    df = df[df['Y'].notna()]
    return df


def lowest_crime_neighborhood(df):
    df['INCIDENTNEIGHBORHOOD'].value_counts().tail(10).plot(kind='bar')
    plt.xlabel("Incident Neighborhood", labelpad=14)
    plt.ylabel("Number of crime incidents in 90 days", labelpad=14)
    plt.title("10 lowest crime incidents neighborhood", y=1.02);
    plt.show()


def highest_crime_neighborhood(df):
    df['INCIDENTNEIGHBORHOOD'].value_counts().head(10).plot(kind='bar')
    plt.xlabel("Incident Neighborhood", labelpad=14)
    plt.ylabel("Number of crime incidents in 90 days", labelpad=14)
    plt.title("10 highest crime incidents neighborhood", y=1.02);
    plt.show()


def selected_neighborhood_crime(df):
    ans = input('What neighborhood do you want to search?').lower()
    out = (df['INCIDENTNEIGHBORHOOD'].str.lower() == ans).sum()
    while out == 0:
        sel = input('You input a non-existing Pittsburgh neighborhood, type 1 to try again, type any other to exit.')
        if sel == str(1):
            ans = input('What neighborhood do you want to search?').lower()
            out = (df['INCIDENTNEIGHBORHOOD'].str.lower() == ans).sum()
            return print('The total crime incidents of ' + ans + ' neighborhood is ' + str(out))
        else:
            break
    else:
        return print('The total crime incidents of ' + ans + ' neighborhood is ' + str(out))


def crime_heatmap(df):
    # Draw the heatmap and store as 'map.html'
    gmap = gmplot.GoogleMapPlotter(40.4406, -79.99, 13)
    gmap.heatmap(df['Y'], df['X'])
    gmap.apikey = "AIzaSyB9eUCbdQHA-d9neNixpaEdsDWOEUP4m30"
    gmap.draw('map.html')
    # Automatically direct to the url
    driver = webdriver.Chrome(ChromeDriverManager().install())
    file = '/map.html'
    path = 'file://' + os.getcwd() + file
    url = path
    driver.get(url)
    # sleep(2)
    # If user want to store this as picture they can implement the following code
    # driver.save_screenshot('./picture.png')
    # screenshot = Image.open('./picture.png')
    # screenshot.show()