"""

@author: 

Tianyi Wang: tianyiwa@andrew.cmu.edu
Wan-Ju Yu: wyu2@andrew.cmu.edu
Xi Yan: xiyan@andrew.cmu.edu,
Florence Pan: qinghep@andrew.cmu.edu

"""

from bs4 import BeautifulSoup
import urllib.request
import ssl
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#a method gets web url as a input and return html it scrapes
def askURL(url):
    head = {
        "User-Agent":  "Mozilla / 5.0(Macintosh; 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 92.0.4515.159 Safari/537.36"
        }

    context = ssl._create_unverified_context()
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response =urllib.request.urlopen(request, context= context)
        html = response.read().decode('utf-8')
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html

#a method do live scraping and parse html
#returns a pandas dataframe as data source
def liveScraping():

    apmt_data =pd.DataFrame(np.zeros((500,6)),
                            columns = ['Apartment_Name', 'Apartment_Add', 'Apartment_Price', 'Apartment_Tel',
                                       'Apartment_Type', 'Apartment_Link'])

    base_url = 'https://www.apartments.com/off-campus-housing/pa/pittsburgh/carnegie-mellon-university/'
    j = 0
    for i in range(1, 20):
        if i ==1:
            url = base_url
        else:
            url = base_url + str(i) + '/'
        bs_apmts = askURL(url)
        soup = BeautifulSoup(bs_apmts, "html.parser")


        for li in soup.find_all('li', class_ = "mortar-wrapper"):
            link = li.article.get("data-url")
            apmt_data.loc[j, 'Apartment_Link'] = link

            if li.find('a', class_ = "phone-link js-phone") is not None:
                tel_phone = str(li.find('a', class_="phone-link js-phone").span.text).strip()
            elif li.find('a', class_="phone-link tablet js-phone") is not None:

                tel_phone = str(li.find('a', class_="phone-link tablet js-phone").span.text).strip()
            else:
                tel_phone = None


            apmt_data.loc[j, 'Apartment_Tel'] = tel_phone
            if li.find('div', class_ = "property-address js-url") is not None:
                address = li.find('div', class_ = "property-address js-url").get("title")
            elif li.find('a', class_ = "property-address js-url") is not None:
                address = li.find('a', class_ = "property-address js-url") .get("title")
            elif li.find('p', class_ = "property-address js-url") is not None:
                address = li.find('p', class_ = "property-address js-url") .get("title")
            else:
                address = None

            apmt_data.loc[j, 'Apartment_Add'] = address

            name = str(li.find('span', class_="js-placardTitle title").text).strip()
            apmt_data.loc[j, 'Apartment_Name'] = name

            if li.find('div', class_ = "bed-range") is not None:
                type = str(li.find('div', class_="bed-range").text).strip()
            elif li.find('p', class_="property-beds") is not None:
                type = str(li.find('p', class_="property-beds").text).strip()
            elif li.find('span', class_="property-beds") is not None:
                type = str(li.find('span', class_="property-beds").text).strip()
            else:
                type = None


            apmt_data.loc[j, 'Apartment_Type'] = type
            if li.find('div', class_="price-range") is not None:
                price = str(li.find('div', class_="price-range").text).strip()
            elif li.find('p', class_="property-pricing") is not None:
                price = str(li.find('p', class_="property-pricing").text).strip()
            elif li.find('span', class_="property-rents") is not None:
                price = str(li.find('span', class_="property-rents").text).strip()
            else:
                price = 0


            apmt_data.loc[j, 'Apartment_Price'] = price
            j += 1
    return apmt_data

#a method to draw rent price distribution plot
def price_dist(apmt_price):
    apmt_price = apmt_price[apmt_price!='0']
    apmt_price = apmt_price[apmt_price != '0.0']
    apmt_price = apmt_price[pd.notna(apmt_price)]
    pat = r'[1-9],[0-9]{3}|[1-9][0-9]{2}'
    price_list = np.zeros((len(apmt_price), 2))
    i=0
    for price in apmt_price:
        if isinstance(price, str):

            price_temp = re.findall(pat, price)
            if len(price_temp) == 1:
                price_list[i, 0] = price_temp[0].replace(',', '')
            elif len(price_temp) == 2:
                price_list[i, 0] = price_temp[0].replace(',', '')
                price_list[i, 1] = price_temp[1].replace(',', '')

        i += 1
    price = []
    for row in price_list:
        if row[0] == 0:
            continue
        elif row[1] == 0:
            price.append(row[0])
        else:
            price.append((row[0]+row[1])/2)
    plt.hist(x=price, bins='auto', color='navy',
             alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title('Renting Price Distribution')
    plt.show()




def address(apmt_address):
    zipcode = []
    for addr in apmt_address:
        if addr =='0.0' or not isinstance(addr, str):
            continue

        zip = addr[-5:]
        zipcode.append(zip)
    zipdict = {zip: zipcode.count(zip) for zip in zipcode}
    zip_set = []
    zip_count = []
    for zipitems in zipdict.items():
        zip_set.append(zipitems[0])
        zip_count.append(zipitems[1])

    plt.figure(figsize=(20, 20))
    colors = ['slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'plum', 'mediumorchid',
              'thistle', 'plum', 'purple', 'darkmagenta', 'm',
              'orchid', 'palevioletred', 'pink', 'lightpink', 'lavenderblush']

    plt.pie(zip_count, labels=zip_set, textprops={'fontsize': 20}, colors = colors)
    plt.title("Apartment Distribution based on Zipcode", fontsize = 50)

    plt.show()

def type(apmt_type):
    apmt_type = apmt_type[pd.notna(apmt_type)]
    type_list =[]
    for i in apmt_type:
        if i == '0.0' or i == 'nan':
            continue
        type_list.append(i)
    beds = []
    count = []


    type_data = {bed: type_list.count(bed) for bed in type_list}

    for type_count in type_data.items():
        beds.append(type_count[0])
        count.append(type_count[1])

    plt.figure(figsize=(20, 20))
    colors = ['bisque', 'sandybrown', 'peachpuff', 'peru',
              'darkorange', 'burlywood', 'antiquewhite', 'tan', 'navajowhite', 'blanchedalmond',
              'papayawhip', 'moccasin', 'orange', 'wheat', 'oldlace', 'goldenrod', 'cornsilk', 'khaki']
    plt.pie(count, labels=beds,   labeldistance=1.2, textprops={'fontsize': 16}, colors = colors)
    plt.title("Apartment Type Distribution", fontsize = 50)

    plt.show()


#Apartment Search()
def search(apmt_data, zipcode, input_price):
    apmt_price = apmt_data['Apartment_Price']
    revised_apmt_data = apmt_data.copy()
    pat = r'[1-9],[0-9]{3}|[1-9][0-9]{2}'


    price_list_lower = np.zeros(len(apmt_price), dtype = int)
    price_list_higher =np.zeros(len(apmt_price),  dtype = int)

    i = 0
    for price in apmt_price:
        if isinstance(price, str):
            price_temp = re.findall(pat, price)
            if len(price_temp) == 0:
                price_list_lower[i] = 0
                price_list_higher[i] = 0
            elif len(price_temp) == 1:
                price_list_lower[i] = int(price_temp[0].replace(',', ''))
                price_list_higher[i] = 0
            elif len(price_temp) == 2:
                price_list_lower[i] = int(price_temp[0].replace(',', ''))
                price_list_higher[i] = int(price_temp[1].replace(',', ''))
        else:
            price_list_lower[i] = 0
            price_list_higher[i] = 0

        i += 1
    revised_apmt_data['lower_price'] = price_list_lower
    revised_apmt_data['higher_price'] = price_list_higher
    zipcodes = []
    for addr in apmt_data['Apartment_Add']:
        if isinstance(addr, str):
            zipcodes.append(addr[-5:])
        else:
            zipcodes.append('0')
    revised_apmt_data['zipcodes'] = zipcodes



    result = apmt_data.loc[(revised_apmt_data['zipcodes'] == zipcode) & (revised_apmt_data['lower_price'] != 0) & (revised_apmt_data['lower_price'] <= input_price)]

    return result





if __name__=="__main__":
    livescrape = True
    if livescrape:
        # call live scraping method to get data
        apmt_data = liveScraping()
    else:
        apmt_data = pd.read_csv('apmt_data.csv', index_col=0)

    address(apmt_data['Apartment_Add'])
    #call type() method, show type distribution
    type(apmt_data['Apartment_Type'])
    price_dist(apmt_data['Apartment_Price'])
    #receive user input : zipcode andexpected renting price: return apartment info
    #example:
    result = search(apmt_data, '15213', 1500)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 2000)
    pd.set_option('max_colwidth', 150)

    print(result)























