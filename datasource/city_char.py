import pprint

#--------------------------------------------------
# Look up list of top 50 cities that best match this char object
# Input:
#   - char object:
#       + temp_low: int in F
#       + temp_high: int in F
#       + precip_low: int in inches/year
#       + precip_high: int in inches/year
#       + humid_low: int in percent
#       + humid_high: int in percent
#       + settle_type: array of string "urban", "suburban", "rural", "outerspace"
# Output:
#   - list of cities, which has
#        + city name
#        + state
#        + zip code
#        + match score
#        + temperature
#        + precipitation
#        + humidity
#        + settle type
#--------------------------------------------------
def lookup_by_char(char):
    pass

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    result = lookup_by_char({
        "temp_low" : 40,
        "temp_high" : 120,
        "precip_low" : 0,
        "precip_high" : 20,
        "humid_low": 50,
        "humid_high": 80,
        "settle_type": "urban"
    })

    pp.pprint(result)

    # check if LA is in here

    for one in result
