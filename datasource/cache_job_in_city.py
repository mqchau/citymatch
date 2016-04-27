import json
import salary

def read_current_city_data():
    with open("all_cities_data_working.json", "r") as f:
        all_lines = f.readlines()

    return list(map(lambda x: json.loads(x), all_lines))

def save_city_data(new_city_data):
    with open("all_cities_data_working.json", "w") as f:
        for one_city in new_city_data:
            f.write("%s\n" % json.dumps(one_city))

if __name__ == "__main__":
    with open("most_popular_jobs.txt", "r") as f: 
        all_lines = f.readlines()

    job_title_array = list(map(lambda x: x.rstrip(), all_lines))
    city_array = read_current_city_data()

    for one_city in city_array[:1000]:
        if "job" in one_city or len(one_city["zipcode"]) == 0:
            continue

        try:
            this_city_salary = []
            for one_job in job_title_array:
                job_salary = salary.lookup_salary_by_occup_city(one_job, one_city["zipcode"][0])
                this_city_salary.append({
                    "name": one_job,
                    "salary": job_salary
                })
                print("%s in %s,%s" % (one_job, one_city["name"], one_city["state"]))
            one_city["job"] = this_city_salary
        except:
            break

        save_city_data(city_array)

