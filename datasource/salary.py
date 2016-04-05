import pprint
import requests
from bs4 import BeautifulSoup
import re

#--------------------------------------------------
# Look up list of top 50 cities that best match this char object
# Input:
#   - occupation: string
#   - city: string
#   - state: string
# Output:
#   - expected salary of that occupation in that city: integer, round to thousands
#--------------------------------------------------
def lookup_salary_by_occup_city(occupation, city, state):
    pass

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lookup_salary_by_occup_city("Analyst", "Los Angeles", "CA"))
