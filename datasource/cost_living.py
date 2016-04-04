import pprint
import requests
from bs4 import BeautifulSoup
import re

#--------------------------------------------------
# Look up list of top 50 cities that best match this char object
# Input:
#   - zipcode: int 
# Output:
#   - cost of living: integer, round to thousands
#--------------------------------------------------
def lookup_cost_by_city(zipcode):
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

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(lookup_cost_by_city(90024))
    r = lookup_cost_by_city(92620)
    print(r)
    # print(r[0].prettify())
