import pprint
import os.path
import json
import time
from pyspark import SparkContext, SparkConf

all_cities = None

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
    conf = SparkConf().setAppName("rate_city").setMaster("local[4]")
    sc = SparkContext(conf=conf)
    lines = sc.textFile(os.path.join("datasource", "all_cities_data_dummy.json"), 4)
    # top 50 cities by characteristics
    print("debug 1")
    best_cities_char = lines.map(lambda x: rate_city_char(json.loads(x), city_char)).top(500, lambda x: x[1])
    print("debug 2")
    best_cities_cost = sc.parallelize(best_cities_char).map(lambda x: (x[0], rate_city_job(x[0], occupation) + x[1])).sortBy(lambda x: x[1], ascending=False)
    print("debug 3")
    # best_cities_cost = sc.parallelize(best_cities_char).map(lambda x: (x[0], rate_city_job(x[0], occupation))).sortBy(lambda x: x[1], ascending=False)
    return best_cities_cost.collect()

def rampf(x):
    return x if x > 0 else 0

def rate_city_char(city_obj, city_char):
    # calculate climate score 
    temp_score = rampf(12.5 - rampf(city_char["temp_low"] - city_obj["temp_low"]) -  rampf(city_obj["temp_high"] - city_char["temp_high"]))
    precip_score = rampf(12.5 - rampf(city_char["precip_low"] - city_obj["precip_low"]) -  rampf(city_obj["precip_high"] - city_char["precip_high"]))
    climate_score = temp_score + precip_score 

    # calculate city type and score it
    if city_obj["density"] < 300:
        city_type = 0 
    elif city_obj["density"] < 1000:
        city_type = 1
    else:
        city_type = 2

    settle_type = map(lambda x: get_settle_type(x), city_char["settle_type"])
    urban_score = 25 - min(map(lambda x: abs(x - city_type), settle_type)) * 12.5

    char_score = climate_score + urban_score
    return (city_obj, char_score)

def rate_city_job(city_obj, occupation):
    if "job" not in city_obj or city_obj["cost"] == 0:
        return 0

    salary = 0
    for cached_occ in city_obj["job"]:
        if cached_occ["name"] == occupation:
            salary = cached_occ["salary"]
            break
    if salary == 0:
        # will call indeed api here
        # for now just hard code value
        salary = 30000

    average_household_income = 55000
    raw_salary_score = salary / (city_obj["cost"] / 100.0 * average_household_income)
    
    if raw_salary_score > 2:
        return 50
    elif raw_salary_score < 0.5:
        return 0
    else:
        return (raw_salary_score - 0.5) / 1.5 * 50

def get_settle_type(type_str):
    if type_str == "rural":
        return 0
    elif type_str == "suburban":
        return 1
    else:
        return 2

if __name__ == "__main__":
    # load_data_to_memory()

    city_char = {
        "temp_low" : 40,
        "temp_high" : 120,
        "precip_low" : 0,
        "precip_high" : 20,
        "settle_type": ["urban"]
    }
    occupation = "Physical Therapist"


    pp = pprint.PrettyPrinter(indent=4)
    rate_city(occupation, city_char)

    start_time = time.time()
    all_cities = rate_city(occupation, city_char)
    print("--- finished in %s seconds ---" % (time.time() - start_time))

    all_cities_result = all_cities
    
    with open(".tmp.txt", "w") as f:
        pprint.pprint(all_cities_result, stream=f, indent=4)

