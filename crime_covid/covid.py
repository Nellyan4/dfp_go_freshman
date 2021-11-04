"""

@author: 

Tianyi Wang: tianyiwa@andrew.cmu.edu
Wan-Ju Yu: wyu2@andrew.cmu.edu
Xi Yan: xiyan@andrew.cmu.edu,
Florence Pan: qinghep@andrew.cmu.edu

"""

from tableauscraper import TableauScraper as TS
import numpy as np
import pandas as pd

"""Clean data"""


def clean_data(input_list, current_index, previous_index, change_index, name):
    list2 = np.ndarray.tolist(input_list)[0]
    current = round(list2[current_index], 1)
    previous = round(list2[previous_index], 1)
    change = round(list2[change_index], 1)
    list3 = [name, current, previous, change]
    return list3


def clean_positivity(input_list, current_index, previous_index, change_index, name):
    list_positivity = np.ndarray.tolist(input_list)[0]
    current = "{:.1%}".format(list_positivity[current_index])
    previous = "{:.1%}".format(list_positivity[previous_index])
    change = "{:.1%}".format(list_positivity[change_index])
    list3 = [name, current, previous, change]
    return list3


"""Output dashboard"""


def output_covid_dashboard():
    # Read Tableau dashboard
    url = "https://tableau.alleghenycounty.us/t/PublicSite/views/COVID-19Summary_16222279737570/COVID-19Summary?:showAppBanner=false&:display_count=n&:showVizHome=n&:origin=viz_share_link&:isGuestRedirectFromVizportal=y&:embed=y"
    ts = TS()
    ts.loads(url)
    workbook = ts.getWorkbook()
    # Extract values in Tableau dashboard
    cases = workbook.worksheets[2].data.values
    death = workbook.worksheets[5].data.values
    hospitalization = workbook.worksheets[9].data.values
    positivity = workbook.worksheets[15].data.values
    individual = workbook.worksheets[12].data.values
    # Clean data using previous funcitons
    cases_list = clean_data(cases, 5, 11, 4, 'Cases')
    death_list = clean_data(death, 4, 7, 5, 'Deaths')
    hospitalization_list = clean_data(hospitalization, 6, 5, 4, 'Hospitalizations')
    positivity_list = clean_positivity(positivity, 5, 6, 4, 'Positivity (PCR)')
    individual_list = clean_data(individual, 5, 6, 4, 'Individuals Tested')
    # Create covid dashboard
    L = [cases_list, death_list, hospitalization_list, positivity_list, individual_list]
    field = ['Type', 'Current 7 Average', 'Previous 7 Average', 'Change from 7 Period']
    df = pd.DataFrame(L, columns=field)
    print(df)

