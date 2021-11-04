"""

@author: 

Tianyi Wang: tianyiwa@andrew.cmu.edu
Wan-Ju Yu: wyu2@andrew.cmu.edu
Xi Yan: xiyan@andrew.cmu.edu,
Florence Pan: qinghep@andrew.cmu.edu

"""

import geopy
import pandas as pd
import numpy as np
import math
import folium
import webbrowser
from Restaurant import api_data as ad
import os

def CalDistance(lat_1: float, long_1: float, lat_2: float, long_2: float) -> int:
    """Convert coordinates to distance

    Args:
        lat_1 (float): latitude of first coord
        long_1 (float): longitude of first coord
        lat_2 (float): latitude of second coord
        long_2 (float): longitude of second coord

    Returns:
        int: Calculated distance in meters as integer
    """
    # Transfer to radius
    lat_1 *= math.pi / 180
    lat_2 *= math.pi / 180
    long_1 *= math.pi / 180
    long_2 *= math.pi / 180

    # Calculate distance (in meters)
    delta_lat = abs(lat_1 - lat_2)
    delta_long = abs(long_1 - long_2)
    a = math.sin(delta_lat /2) ** 2 + math.cos(lat_1) * math.cos(lat_2) * (math.sin(delta_long/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = c * 6_371_000
    return int(d)

def PrintTopN(df, n):
    """Print the top n of the desired columns of our table
    
    Args:
        df (pd.DataFrame): Data of the restaurant
        n (int): Top N columns to print
    """

    if (df.shape[0] == 0):
        print("No results found, please remove filters")
        return

    topn_df = df[['name', 'rating', 'price', 'display_phone', 'distance', 'coordinates.latitude', 'coordinates.longitude']].head(n)
    print(topn_df[['name', 'rating', 'price', 'display_phone', 'distance']])
    print()

    if "y" == input("Do you want to show a map?: (y/n)"):
        DrawMap(topn_df)

def FilterByDistance(df):
    """Filter table according to distance input (meter)

    Args:
        df (pd.DataFrame): Restaurant data

    Returns:
        pd.DataFrame: Filtered data
    """
    distance_filter = int(input("Please enter distance (m): "))
    df = df[df['distance'] <= distance_filter]
    return df
    
def FilterByRating(df):
    """Filter table according to rating input from 0.0 to 5.0

    Args:
        df (pd.DataFrame): Restaurant data

    Returns:
        pd.DataFrame: Restaurant data
    """
    rating_filter = float(input("Input rating: (0.0-5.0)"))
    df = df[df['rating'] >= rating_filter]
    return df

def FilterByPrice(df):
    """Filter table according to price input from 1 to 4

    Args:
        df (pd.DataFrame): Restaurant data

    Returns:
        pd.DataFrame: Restaurant data
    """
    pricing_filter = int(input("Input price: (1-4)"))
    df = df[df['price'] != '']
    df = df[df['price'].str.count('\$') <= pricing_filter]
    return df

def SelectAddress():
    """Transfer address to coordinates and calculate distance between input location and desired restaurants
    """
    def GetDistance(row):
        return CalDistance(latitude, longitude, row['coordinates.latitude'], row['coordinates.longitude'])
    
    # Extract latitude and longitude of entered location
    global latitude, longitude, df, filtered_df
    address = input("Enter the street name: ")
    locator = geopy.Nominatim(user_agent = "Geocoder")
    location = locator.geocode(address + ", Pittsburgh, United States")
    latitude = location.latitude
    longitude = location.longitude
    
    # Append calculated distance to dataframe as new column 'distance'; Remove NA
    df['distance'] = df.apply(GetDistance, axis=1)
    df = df.sort_values('distance', axis=0, ascending=True).replace(np.NaN, "")
    filtered_df = df.copy()
    
def ChooseAction():
    """Create menu and allow user to choose actions

    Raises:
        ValueError: When input is not valid, raise error

    Returns:
        bool: Return true if user choose to exit
    """
    global address
    print("\n".join([
        "Select Action:",
        "1. Filter",
        "2. Change Address",
        "3. Display Results",
        "4. Remove Filters",
        "5. Exit",
    ]))

    try:
        user_input = int(input())

        global filtered_df 
        if user_input == 1:
            ChooseFilter()
        elif user_input == 2:
            SelectAddress()
        elif user_input == 3:
            PrintTopN(filtered_df, 5)
        elif user_input == 4:
            filtered_df = df.copy()
        elif user_input == 5:
            return True

    except:
        raise ValueError("User input was not a valid input")

def ChooseFilter():
    """Allow user to choose filter

    Raises:
        ValueError: When input is not valid, raise error
    """
    
    global filtered_df
    print("\n".join([
        "Select Filter:",
        "1. Filter by Distance(meter)",
        "2. Filter by Ratings",
        "3. Filter by Price",
    ]))
    try:
        user_input = int(input())

        results = [
            None,
            FilterByDistance,
            FilterByRating,
            FilterByPrice
        ]
        filtered_df = results[user_input](filtered_df)
        PrintTopN(filtered_df, 5)
    except:
        raise ValueError("User input was not a valid input")

def DrawMap(df):
    """Draw user location and searched results on html map

    Args:
        df (pd.DataFrame): Filtered data
    """

    # Create map canvas
    map = folium.Map(
        location=[latitude, longitude],
        tiles = 'cartodbpositron',
        zoom_start = 15
    )
    # Mark location and searched restaurants on map
    folium.CircleMarker(location = [latitude, longitude], radius = 30, tooltip='<b>Your Location</b>', color = 'crimson', fill_color = True).add_to(map)
    t_df = df.copy()
    t_df['display_phone'] = t_df['display_phone'].replace('', "Phone Number: N/A")
    t_df.apply(lambda row: folium.CircleMarker(location = [row["coordinates.latitude"], row["coordinates.longitude"]],
                                            fill_color = True,
                                            tooltip = f'<b>{row["name"]}</b><br/><b>{row["display_phone"]}</b>')
                                            .add_to(map), axis = 1)
    # Export and open map
    map.save("data/map.html")
    webbrowser.open("file://" + os.path.realpath("data/map.html"))
    print("Map Drawn\n")
    
df = None
filtered_df = None
address = None
latitude = None
longitude = None

def main():
    global df
    ad.load_data()

    file = "data/yelp_restaurant.pickle"
    df = pd.read_pickle(file)
    
    SelectAddress()

    # Before user select exit, ask user for next action
    exit = False
    while(not exit):
        exit = ChooseAction()

if __name__ == "__main__":
    main()