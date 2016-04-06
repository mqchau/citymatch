import pprint
import requests
from bs4 import BeautifulSoup
import re
import argparse
import time

#--------------------------------------------------
# Look up list of top 50 cities that best match this char object
# Input:
#   - zipcode: int 
# Output:
#   - cost of living: integer, round to thousands
#--------------------------------------------------
def lookup_cost_by_zip(zipcode):
    r = requests.get('http://www.city-data.com/zips/%d.html' % zipcode)

    if r.status_code != 200:
        raise Exception("Error looking up cost of living in %d" % zipcode)

    soup = BeautifulSoup(r.text, "html.parser")
    all_b = soup.find_all("b")
    b_cost_living = list(filter(lambda x: re.search("cost of living index", x.get_text()), all_b))
    if len(b_cost_living) == 0:
        raise Exception("Can't find cost of living in %d" % zipcode)
    cost_living_string = b_cost_living[0].next_sibling.strip()
    try:
        cost_living = float(cost_living_string)
        return cost_living
    except:
        raise Exception("Can't find cost of living in %d" % zipcode)

def get_cost_by_city(city_string):
    splitted = city_string.split("\t")
    zip_string = splitted[1]
    zips = map(lambda x: int(x), filter(lambda x: len(x) > 0, zip_string.split(",")))
    cost = None
    for z in zips:
        try:
            cost = lookup_cost_by_zip(z)
            print("%s=%f" % (city_string, cost))
            break
        except Exception as e:
            pass
    if cost is None:
        return (city_string, "")
    else:
        return (city_string, cost)

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

        # collect cost of living from one of the zip code of the city
        start = time.time()
        conf = SparkConf().setAppName("get_zip_code").setMaster("local")
        sc = SparkContext(conf=conf)
        # sc = SparkContext(appName="get_zip_code")
        lines = sc.textFile("city_list_with_zipcode.txt", 8)
        city_with_cost = lines.map(get_cost_by_city).collect()
        end = time.time()
        print("job finished in %f seconds" % (end-start))

        with open("city_list_with_zip_cost.txt", "w") as f:
            for (cityname, cost) in city_with_cost:
                f.write("%s\t%s\n" % (cityname, str(cost)))

        sc.stop()

