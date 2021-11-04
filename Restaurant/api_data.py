"""

@author: 

Tianyi Wang: tianyiwa@andrew.cmu.edu
Wan-Ju Yu: wyu2@andrew.cmu.edu
Xi Yan: xiyan@andrew.cmu.edu,
Florence Pan: qinghep@andrew.cmu.edu

"""

#Business Search    URL: 'https://api.yelp.com/v3/businesses/search'
import requests
import json
import time
import pandas as pd

import os


# Define the API Key, Endpoint and Header
def pull_data():
    API_KEY = "3c3UTWB8aykiNe9IAN7TLBRCjLE9UaNBFugv1NuRfo4dMl0oydSsHxAOp0Ho34t8hxTJxxcTw0nKdKetqT02otaIGiEwKgswlCn12hGswn08g24IL9MaEi6K8AdAYXYx"
    ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
    HEADER = {'Authorization': 'bearer %s' % API_KEY}

    # Define the parameters
    # other parameters: latitude, longtitude, categories, locale, offset, sort_by, price, open_now, attributes

    data = []
    for i in range(0, 200, 50):
        print(f"Pulling data from {i} to {i + 50}")
        PARAMETERS = {'term': 'restaurant',
                        'latitude':40.4431,
                        'longitude':-79.9442,
                        'limit': 50, 
                        'offset': i,
                        'radius': 10000,
                        'location': 'Pittsburgh'}

        # Make a request to the yelp API
        response  = requests.get(url = ENDPOINT, params = PARAMETERS, headers= HEADER, timeout= 5)
        time.sleep(10)
        # Convert the json str to a dictionary
        data.append(response.json())

        # if ('error' in data):
        #     print(f'Error response from server: {data}')
        #     import sys
        #     sys.exit()

    # Export json file
    with open("data/yelp_raw", "w") as f:
        json.dump(data, f)


def load_data():
    if os.path.exists("data/yelp_raw"):
        return

    print("No data found, pulling restaurant data")
    if not os.path.exists("data"):
        os.mkdir('data')

    pull_data()
    with open("data/yelp_raw", "r") as f:
        data = json.load(f)

    # Use pandas dataframe to filter the data we need
    new_data = []
    for dat in data:
        try:
            new_data.extend(dat['businesses'])
        except KeyError:
            pass
            # print(dat)

    print(f'Data count: {len(new_data)}, pull data complete')
    df = pd.json_normalize(new_data)
    clean_data = df.drop(columns = ["image_url", "url", "phone","location.address2", "location.address3", "location.city", "location.country", "location.state", "location.display_address"])

    # Export data
    clean_data.to_csv("data/yelp_restaurant.csv", index = None)

    df.to_pickle("data/yelp_restaurant.pickle")
    df = pd.read_pickle("data/yelp_restaurant.pickle")
