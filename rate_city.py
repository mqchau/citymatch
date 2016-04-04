import pprint

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
    pass



if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(rate_city("Analyst", {
        "temp_low" : 40,
        "temp_high" : 120,
        "precip_low" : 0,
        "precip_high" : 20,
        "humid_low": 50,
        "humid_high": 80,
        "settle_type": "urban"
    }))

