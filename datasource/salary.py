import locale
import pprint
import requests
from bs4 import BeautifulSoup
import re
import ipdb

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

class HttpRequestError(Exception):
    pass

#--------------------------------------------------
# Look up expected salary of an occupation in a city
# Input:
#   - occupation: string
#   - zipcode: string
# Output:
#   - expected salary of that occupation in that city: integer, round to thousands
#--------------------------------------------------
def lookup_salary_by_occup_city(occupation, zipcode):

    try:
        r = requests.get('http://www.indeed.com/salary?q1=%s&l1=%s' % (urlify(occupation), str(zipcode)), timeout=10)
    except:
        raise HttpRequestError("Can't get indeed response")

    if r.status_code != 200:
        raise Exception("Error looking up occupation %s in %s" % (occupation, zipcode))

    soup = BeautifulSoup(r.text, "html.parser")
    salary_div = soup.find_all("span", {"class": "salary"})
    if len(salary_div) == 0:
        raise Exception("Error looking up occupation %s in %s" % (occupation, zipcode))

    average_salary_str = salary_div[0].text
    average_salary_str = average_salary_str.rstrip()
    average_salary_str = re.sub("\$", "", average_salary_str)

    # extract number 
    average_salary = locale.atof(average_salary_str)
    return average_salary

# convert all space to +
# so we can put it in url to request indeed salary
def urlify(normal_string):
    return re.sub(" ", "+", normal_string)

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lookup_salary_by_occup_city("Analyst", "92683"))
