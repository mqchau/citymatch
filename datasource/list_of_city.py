import json
import re
import pickle
import pprint
import requests
from bs4 import BeautifulSoup
import argparse
import copy
import time


# GLOBAL VAR
spark_flag = False



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

def get_city_in_one_page(page_idx):
    page_idx = int(page_idx)

    url = "http://www.topix.com/city/list/"
    if page_idx > 1:
        url = url+'p'+str(page_idx)
    print(url)
    handle = requests.get(url)
    data = handle.text
    soup = BeautifulSoup(data, 'html.parser')
    d = soup.find_all('ul', class_='dir_col')
    out = []
    for i in range(len(d)-1):
        out.extend(clean_data(d[i].get_text()))
    if spark_flag:
        return (" ", out)
    else:
        return out

def get_zip_code_from_name(city_string):
    # print(city_string)
    name, state = extract_city_name_state(city_string)
    zipcode = get_zip_code(name, state)
    if spark_flag:
        return (city_string, zipcode)
    else:
        return zipcode

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--spark", action='store_true', help="run in spark mode")
    parser.add_argument("-n", type=int, help="number of iterations to run on single thread, 0 for maximum", default=1)
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)

    if args.spark:
        spark_flag = True
        from pyspark import SparkContext, SparkConf
        from operator import add

        # collect all city names
        # sc = SparkContext(appName="get_city_name")
        # lines = sc.textFile("pages_to_read.txt", 8)
        # city_names = lines.map(get_city_in_one_page).reduceByKey(add)
        
        # output = city_names.collect()

        # with open("spark_output.pickle", "wb") as f:
        #     pickle.dump(output, f)
        # with open("city_list.pickle", "wb") as f:
        #     pickle.dump(output[0][1], f)
        # with open("city_list.txt", "w") as f:
        #     for onecity in output[0][1]:
        #         f.write(onecity + "\n")

        # sc.stop()

        # collect city name and its zip code
        start = time.time()
        conf = SparkConf().setAppName("get_zip_code").setMaster("local")
        sc = SparkContext(conf=conf)
        # sc = SparkContext(appName="get_zip_code")
        lines = sc.textFile("city_list_short.txt", 1)
        city_names = lines.map(get_zip_code_from_name)
        
        output = city_names.collect()
        end = time.time()
        print("job finished in %f seconds" % (end-start))

        with open("spark_output.pickle", "wb") as f:
            pickle.dump(output, f)
        # with open("city_list.pickle", "wb") as f:
        #     pickle.dump(output[0][1], f)
        with open("city_list_with_zipcode.txt", "w") as f:
            for (cityname, zipcodes) in output:
                f.write("%s-%s\n" % (cityname, ','.join(map(lambda x: str(x), zipcodes))))

        sc.stop()

    else:
        if args.n == 0:
            list_of_city = get_list_of_city()
            list_of_city_and_zipcode = get_zipcode_per_city(list_of_city)
            with open("cities_with_zip.pickle", "wb") as f:
                pickle.dump(list_of_city_and_zipcode, f)
        else:
            page_idx = 1
            city_in_one_page = get_city_in_one_page(page_idx)
            name, state = extract_city_name_state(city_in_one_page[0])
            city_and_zip = get_zip_code(name, state)
            pp.pprint(city_and_zip)
