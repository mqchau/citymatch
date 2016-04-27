import pprint
import os.path
import json
import time
from pyspark import SparkContext, SparkConf

all_cities = None

def load_data_to_memory():
    global all_cities
    with open(os.path.join("datasource", "all_cities_data.json"), "r") as f:
        all_cities = map(lambda x: json.loads(x), f.readlines())

# --------------------------------------------------
# Find cities with best matches to the char and highest ratio of salaray / cost
# Input:
#   - occupation: string
#   - city_char: object structure as defined in datasource/city_char.py
# output:
#   - List of top 10 matches, with details as indicated in datasource/city_char.py
#        And expected salary and cost
# --------------------------------------------------
def rate_city(occupation, city_char):
    start_time = time.time()
    # all_cities_with_char_rate = map(lambda x: rate_one_city(x, city_char), all_cities)
    top_cities_with_char_rate = sorted(all_cities, key=(lambda x: rate_one_city(x, city_char)), reverse=True)
    print("--- finished in %s seconds ---" % (time.time() - start_time))
    return top_cities_with_char_rate

def rate_one_city(city_obj, city_char):
    return (city_obj["name"] + ", " + city_obj["state"], city_obj["cost"])

if __name__ == "__main__":
    # load_data_to_memory()

    city_char = {
        "temp_low" : 40,
        "temp_high" : 120,
        "precip_low" : 0,
        "precip_high" : 20,
        "settle_type": "urban"
    }


    pp = pprint.PrettyPrinter(indent=4)
    # a = rate_city("Sales Associate", {
    #     "temp_low" : 40,
    #     "temp_high" : 120,
    #     "precip_low" : 0,
    #     "precip_high" : 20,
    #     "settle_type": "urban"
    # })

    conf = SparkConf().setAppName("rate_city").setMaster("local[4]")
    sc = SparkContext(conf=conf)
    lines = sc.textFile(os.path.join("datasource", "all_cities_data.json"), 4)

    start_time = time.time()
    all_cities = lines.map(lambda x: rate_one_city(json.loads(x), city_char)).top(2, lambda x: x[1])
    print("--- finished in %s seconds ---" % (time.time() - start_time))

    all_cities_result = all_cities

    pp.pprint(all_cities_result)

