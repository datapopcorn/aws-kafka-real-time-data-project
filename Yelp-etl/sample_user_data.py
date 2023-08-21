import json
import yaml


# read /yelp_raw_data/yelp_academic_dataset_user.json and dump first 1000 lines to /yelp_raw_data_sample/user_data_sample.json

user_list = []

# read the first 1000 lines of the file
with open(f"yelp_raw_data/yelp_academic_dataset_user.json", 'r', encoding="utf-8") as f:
    for line_number, line in enumerate(f):
        if line_number == 1000:
            break
        obj = json.loads(line)
        user_list.append(obj)

# erase the file if it exists
open(f"yelp_raw_data_sample/user_data_sample.json", 'w').close()

# write the first 1000 lines to the file
with open(f"yelp_raw_data_sample/user_data_sample.json", 'a', encoding="utf-8") as f:
    for obj in user_list:
        json.dump(obj, f)
        f.write('\n')