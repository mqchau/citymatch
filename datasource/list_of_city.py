
# coding: utf-8

# In[1]:

import pprint
import requests
from bs4 import BeautifulSoup

# remove extra \n and sub-cities
def filter_paren(s):
    if '(' in s:
        return False
    if ')' in s:
        return False
    if '' == s:
        return False
    return True

def clean_data(cities):
    c = cities.split('\n\n')
    for ind, city_state in enumerate(c):
        c[ind] = c[ind].strip() #takes out \n in front and behind '\ncity, state\n'
    
    return list(filter(filter_paren, c))
    

def get_list_of_city():
    out = []
    url = "http://www.topix.com/city/list/"
    for i in range(1,26):
        print('Processing page %d \n' %i)
        handle = requests.get(url+'p'+str(i))
        data = handle.text
        soup = BeautifulSoup(data, 'html.parser')
        d = soup.find_all('ul', class_='dir_col')
        for i in range(len(d)-1):
            out.extend(clean_data(d[i].get_text()))
    return out


if __name__ == "__main__":
    list_of_city = get_list_of_city()
    f = open('cities.txt', 'w')
    for s in list_of_city:
        f.writelines(s+'\n')
    f.close()
    print('Done')


# In[ ]:



