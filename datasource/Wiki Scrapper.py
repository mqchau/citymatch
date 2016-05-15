
# coding: utf-8

# In[ ]:

import json
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import html5lib
import numpy as np
import pandas as pd

def pop_type(dens):
    if dens < 300:
        return 'rural'
    elif dens > 1000:
        return 'urban'
    else:
        return 'suburban'
    
def parse_density_table(s):
    table = s.find('table', attrs={'class':'infobox geography vcard'})
    rows = table.find_all('tr')
    for row in rows:
        th_row = row.find_all('th')
        for ele in th_row:
            if re.search("Density", ele.text):
                density = ele.next_sibling.next_sibling.text
                density = density.replace(",", "")
                find = re.compile(r"^(.*?)\/")
                return float(re.search(find, density).group(1))
    return None     

def check_city(city, state, file):
    for f in range(len(file[0])):
        if file[0][f]==city and file[1][f]==state:
            return True
    return False

def parse_climate_table(s):
    tables = s.find_all('table')
    climate_table = ''
    for table in tables:
        try:
            if table.find('tr').find('th'):
                if table.find('tr').find('th').text.lower().find('climate data') == 0:
                    climate_table = table
        except:
            print("No Climate Data")
            continue
    rows = climate_table.find_all('tr')
    for row in rows:
        if re.search("Average high", row.find('th').text):
            temp_high = row.find_all('td')[12].text.split()[0]
        if re.search("Average low", row.find('th').text):
            temp_low = row.find_all('td')[12].text.split()[0]
            break
    return float(temp_high), float(temp_low)
    
with open('C:/Users/David/Downloads/all_cities_data.json', 'r') as data_file:  
    all_cities = map(lambda x: json.loads(x), data_file.readlines())
#check for cost > 0, job == true, zipcode == true

file = pd.read_csv('densityTable.csv', header=None)
# count = 0
for entry in all_cities:
#     if count >= 20:
#         break
    if check_city(entry['name'], entry['state'], file):
        print('Skipping: ' + entry['name'] + ', ' + entry['state'])
        continue
    if "job" in entry and entry["cost"] > 0 and len(entry["zipcode"]) != 0:
        try:
            city = entry['name']
            city.replace(' ','_')
            state = entry['state']
            url = "https://en.wikipedia.org/w/index.php?title=" + city + ",_" + state + "&printable=yes"
#             entry = 'Big Bar'
#             entry.replace(' ','_')
#             name = 'CA'
#             url = "https://en.wikipedia.org/w/index.php?title=Irvine,_CA&printable=yes"
        except:
            print('No Result:', city + ',', state)
            continue
        # HTML parsing
        handle = requests.get(url)
        data = handle.text
        soup = BeautifulSoup(data, 'html.parser')
        # Parse table for DENSITY
        try:
            DENSITY_OUT = 0
            DENSITY_OUT = parse_density_table(soup)
        except:
            print('No Density:', city + ',', state)
#         TEMP_HIGH_OUT, TEMP_LOW_OUT = parse_climate_table(soup)
#         POPULATION_TYPE_OUT = pop_type(DENSITY_OUT)
        # output to file
        output = city + ',' + state + ',' + str(DENSITY_OUT) + '\n'
        print(output)
        fd = open('densityTable.csv', 'a')
        fd.write(output)
        fd.close()
#     count = count + 1


# In[ ]:




# In[ ]:



