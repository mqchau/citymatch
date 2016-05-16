
# coding: utf-8

# In[1]:

import json
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import html5lib

states = {
        'Illinois':'IL',
        'Kansas':'KS',
        'South Dakota':'SD',
        'Idaho':'ID',
        'South Carolina':'SC',
        'Ohio':'OH',
        'Wyoming':'WY',
        'District of Columbia':'DC',
        'Alaska':'AK',
        'Rhode Island':'RI',
        'Texas':'TX',
        'Maryland':'MD',
        'Minnesota':'MN',
        'New Mexico':'NM',
        'Nevada':'NV',
        'Iowa':'IA',
        'West Virginia':'WV',
        'North Dakota':'ND',
        'Arkansas':'AR',
        'Arizona':'AZ',
        'Louisiana':'LA',
        'Delaware':'DE',
        'Florida':'FL',
        'Montana':'MT',
        'Missouri':'MO',
        'North Carolina':'NC',
        'Oklahoma':'OK',
        'Nebraska':'NE',
        'California':'CA',
        'Mississippi':'MS',
        'Wisconsin':'WI',
        'Indiana':'IN',
        'Georgia':'GA',
        'Massachusetts':'MA',
        'Tennessee':'TN',
        'New Hampshire':'NH',
        'Washington':'WA',
        'New Jersey':'NJ',
        'Connecticut':'CT',
        'Maine':'ME',
        'Oregon':'OR',
        'Vermont':'VT',
        'New York':'NY',
        'Alabama':'AL',
        'Hawaii':'HI',
        'Michigan':'MI',
        'Pennsylvania':'PA',
        'Virginia':'VA',
        'Utah':'UT',
        'Kentucky':'KY',
        'Colorado':'CO'
}
def getURL(state):
    state_abbr = states[state]
    state = state.replace(" ","-")
    url = 'http://www.weatherbase.com/weather/city.php3?c=US&s='+state_abbr+'&statename='+state+'-United-States-of-America'
    return url
#     print(url)

def getCitiesURL(cities):
    cityURL = {}
    for city in cities:
        url = 'http://www.weatherbase.com'+city.a.get('href')
        cityname = city.text
        cityURL[cityname] = url
#         break
    return cityURL

def getClimate(cities, state):
    
    for city in cities:
        temp_high = ''
        temp_high_f = False
        temp_low = ''
        temp_low_f = False
        precip = ''
        precip_f = False
        
        url = cities[city]
        handle = requests.get(url)
        data = handle.text
        soup = BeautifulSoup(data, 'html.parser')
        div = soup.find(attrs={'class':'p402_premium'})
        tables = div.find_all('table')
        
        print('-'*5+city+', '+state+'-'*5)
        for table in tables:
#             print(table.find('td').text)
            if table.find('td').text == 'Average Precipitation' and precip_f == False:
                print('\tPrecipitation Found')
                precip_f = True
                continue
            if table.find('td').text == 'Average High Temperature' and temp_high_f == False:
                print('\tHigh Temperature Found')
                temp_high_f = True
                continue
            if table.find('td').text == 'Average Low Temperature' and temp_low_f == False:
                print('\tLow Temperature Found')
                temp_low_f = True
                continue
            if precip_f == False and temp_high_f == False and temp_low_f == False:
                continue
            else:
                val = table.find('tr', attrs={'bgcolor':'white'}).find('td', attrs={'class':'data'}).text
#                 print(data)
                if precip_f == True:
                    precip = val
#                     print('precip',precip)
                    precip_f = False
                if temp_high_f == True:
                    temp_high = val
#                     print('temphigh',temp_high)
                    temp_high_f = False
                if temp_low_f == True:
                    temp_low = val
#                     print('templow',temp_low)
                    temp_low_f = False
        
        city_output = city+','+state+','+temp_high+','+temp_low+','+precip
        print(city_output)
        fd = open('climateTable.csv', 'a')
        fd.write(city_output)
        fd.close()

for state in states.keys():
    url = getURL(state)
#     url = 'http://www.weatherbase.com/weather/city.php3?c=US&s='+'CA'+'&statename='+'California'+'-United-States-of-America'
    handle = requests.get(url)
    data = handle.text
    soup = BeautifulSoup(data, 'html.parser')
    city_list = soup.find(id="row-nohover").find_all('li')
    cities = getCitiesURL(city_list)
    getClimate(cities, state)


# In[ ]:



