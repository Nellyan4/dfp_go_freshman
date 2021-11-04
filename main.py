# -*- coding: utf-8 -*-
"""

@author: 

Tianyi Wang: tianyiwa@andrew.cmu.edu
Wan-Ju Yu: wyu2@andrew.cmu.edu
Xi Yan: xiyan@andrew.cmu.edu,
Florence Pan: qinghep@andrew.cmu.edu

"""

import pandas as pd

# import individual modules

from crime_covid.covid import output_covid_dashboard
from crime_covid.crime import get_df
from crime_covid.crime import lowest_crime_neighborhood
from crime_covid.crime import highest_crime_neighborhood
from crime_covid.crime import selected_neighborhood_crime
from crime_covid.crime import crime_heatmap
from Restaurant import Restaurant_search
from Apartments import web_scrape_apartments


print('Welcome to Go Freshmen!')
print('--------------------------------------------------------------------')
print('Option menu: ')
print('    1. Introduction: Health & Safety in Pittsburgh')
print('    2. Where to dine in Pittsburgh')
print('    3. Where to live in Pittsburgh')
print('    4. Exit')
choice = eval(input('Please enter your choice: '))
while choice != 4:
    if choice ==1:
        print('--------------------------------------------------------------------')
        print('    1. Show me COVID statistics')
        print('    2. Show me Crime Statistics')
        print('    3. Exit')
        choice1 = eval(input('Please enter your choice: '))
        while choice1 !=3:
            if choice1 ==1:
                output_covid_dashboard()
            elif choice1 ==2:
                print('--------------------------------------------------------------------')
                print('    1. Show me the 10 lowest crime incidents neighborhood')
                print('    2. Show me the 10 highest crime incidents neighborhood')
                print('    3. Show me the crime statistics in my own neighbourhood')
                print('    4. Show me the crime heatmap in Pittsburgh')
                print('    5. Exit')
                choice2 = eval(input('Please enter your choice: '))
                while choice2 !=5:
                    if choice2 ==1:	
			# run lowest_crime_neighborhood(df)
                        lowest_crime_neighborhood(get_df())
                    elif choice2 ==2:
			# run highest_crime_neighborhood(df)
                        highest_crime_neighborhood(get_df())
                    elif choice2==3:
			# run selected_crime_neighborhood(df)
                        selected_neighborhood_crime(get_df())
                    elif choice2==4:
			# run crime_heatmap(df)
                        crime_heatmap(get_df())
                    else:
                        pass
                    print('--------------------------------------------------------------------')
                    print('    1. Show me the 10 lowest crime incidents neighborhood')
                    print('    2. Show me the 10 highest crime incidents neighborhood')
                    print('    3. Show me the crime statistics in your own neighbourhood')
                    print('    4. Show me the crime heatmap in Pittsburgh')
                    print('    5. Exit')
                    choice2 = eval(input('Please enter your choice: '))
            else:
                pass
            print('--------------------------------------------------------------------')
            print('    1. Show me COVID statistics')
            print('    2. Show me Crime Statistics')
            print('    3. Exit')
            choice1 = eval(input('Please enter your choice: '))
        print('--------------------------------------------------------------------')
        print('Thank you for browsing the introduction!')
    
    
    if choice ==2:
        print('--------------------------------------------------------------------')
        # run the restaurant search main
        Restaurant_search.main()
        print('--------------------------------------------------------------------')
        print('Thank you for using the restaurants recommendation!')

    
    if choice ==3:
        print('--------------------------------------------------------------------')
        y_or_n = input('Do you want to try live scraping? (Y/N) It takes about 10 seconds')
        if y_or_n in ['Y', 'y']:
            apmt_data = web_scrape_apartments.liveScraping()
        else:
            # read from a file generated on October 5th
            apmt_data = pd.read_csv('Apartments/apmt_data.csv', index_col=0)
        print('--------------------------------------------------------------------')
        print('    1. Show me the location distribution of apartments')
        print('    2. Show me the type distribution of apartments')
        print('    3. Show me the price distribution of apartments')
        print('    4. I want to customize my own zipcode and budget')
        print('    5. Exit')
        choice3 = eval(input('Please enter your choice: '))
        while choice3 !=5:
            if choice3 ==1:
                web_scrape_apartments.address(apmt_data['Apartment_Add'])
            elif choice3 ==2:
                web_scrape_apartments.type(apmt_data['Apartment_Type'])
            elif choice3==3:
                web_scrape_apartments.price_dist(apmt_data['Apartment_Price'])
            elif choice3==4:
                zipcode = input('What is the zip code that you are interested in? ')
                price = input('What is the price that you can afford? ')
                result = web_scrape_apartments.search(apmt_data, zipcode, int(price))
                pd.set_option('display.max_columns', None)
                pd.set_option('display.max_rows', None)
                pd.set_option('display.width', 2000)
                pd.set_option('max_colwidth', 1500)
                print(result)
                # save the results to a local file
                result.to_csv('apmt_search_result.csv')
            else:
                pass
            print('--------------------------------------------------------------------')
            print('    1. Show me the location distribution of apartments')
            print('    2. Show me the type distribution of apartments')
            print('    3. Show me the price distribution of apartments')
            print('    4. I want to customize my own zipcode and budget')
            print('    5. Exit')
            choice3 = eval(input('Please enter your choice: '))

        print('--------------------------------------------------------------------')
        print('Thank you for using apartments recommendation!')
    print('--------------------------------------------------------------------')
    print('Option menu: ')
    print('    1. Introduction: Health & Safety in Pittsburgh')
    print('    2. Where to dine in Pittsburgh')
    print('    3. Where to live in Pittsburgh')
    print('    4. Exit')
    choice = eval(input('Please enter your choice: '))
    
print('--------------------------------------------------------------------')
print('Thank you for using Go Freshmen!')