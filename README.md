# Data Focused Python Final Project: Go Freshmen

### Brief Introduction:
Our product aims to help CMU freshmen settle down in Pittsburgh easily. This is an integrated information platform that provides three aspects of information: safety and health, restaurant recommendation, and apartments renting. In safety and health sector, covid-19 confirmed cases and crime statistics are provided and they are divided by neighborhood. In restaurant recommendation sector, we provide restaurant information categorized by distance to CMU campus, prices, and ratings. In apartments renting sector, we provide data of apartments for rent nearby CMU campus.

### Data Source and Implementation:
1. Restaurant Recommendation
We Acquired restaurant data from Yelp Business Search Endpoint using API. We define our source data as searching results including keyword “restaurant” which locate in a radius of 10000 miles around CMU campus.
2. Apartment Renting: Apartments.com
In this sector, we live scrape data from Apartments.com and parse html data by using beautiful soup. Only apartments nearby CMU campus are scraped. Here, we provide information of more than 450 apartments.
3. Crime and Covid statistics
- For the Crime data, we collect data from WPRDC police incidents blotter of Pittsburgh
using csv download link. We use the neighborhood data to create two box plots for the highest 10 and lowest 10 neighborhood; we combine longitude and latitude with Google Maps API to visualize heatmap.
- For the Covid data, we collect data from Allegany County Covid Dashboard and generate a dashboard of confirm cases, deaths, positivity rate, number of individual testing, and hospitalizations of current and previous 7 days moving average, and the
differences between the two.

### Group members:
- Tianyi Wang: tianyiwa@andrew.cmu.edu 
- Wan-Ju Yu: wyu2@andrew.cmu.edu
- Xi Yan: xiyan@andrew.cmu.edu
- Florence Pan: qinghep@andrew.cmu.edu
