import json
import re
import pickle
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

def get_zipcode_per_city(citylist):
    all_cities_with_zip = []
    for idx, onecity in enumerate(citylist):
        name, state = extract_city_name_state(onecity)
        all_cities_with_zip.append({
            "name": name,
            "state": state,
            "zipcode": get_zip_code(name, state)
        })
        if idx % 500 == 0:
            print("got %d/%d" % (idx, len(citylist)))

    return all_cities_with_zip 
        
def extract_city_name_state(city_string):
    m = re.search("(\w+), (\w{2})", city_string)
    if not m:
        raise Exception("Can't extract city name and state from %s" % city_string)
    return m.group(1), m.group(2)

def get_zip_code(name, state):
    state = re.sub(" ", "%20", state)
    url = "http://api.zippopotam.us/us/%s/%s" % (state,name)
    handle = requests.get(url)
    data = handle.text
    json_data = json.loads(data)

    # print(data)
    if "places" in json_data:
        zipcodes = list(map(lambda x: x["post code"], json_data["places"]))
        return zipcodes
    else:
        return []


if __name__ == "__main__":
    # list_of_city = get_list_of_city()
    # list_of_city_and_zipcode = get_zipcode_per_city(list_of_city)

    # f = open('cities.txt', 'w')
    # for s in list_of_city:
    #     f.writelines(s+'\n')
    # f.close()
    # print('Done')

    with open("cities.txt", "r") as f:
        lines = f.readlines()
    city_string_list = list(map(lambda x: x.rstrip(), lines))
    city_string_list = list(filter(lambda x: len(x) > 0, city_string_list))
    list_of_city_and_zipcode = get_zipcode_per_city(city_string_list)
    with open("cities_with_zip.pickle", "wb") as f:
        pickle.dump(list_of_city_and_zipcode, f)




