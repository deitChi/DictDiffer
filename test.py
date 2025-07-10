from module import DictDiffer

dict1 = {
    "host_name": "abc_123",
    "address": "123.123.123.0",
    "attributes": {
        "max_check_attempts": 5,
        "time_period": "24x7"
    },
    "list_of_data": [
        {
            "name": "harry"
        },
        {
            "name": "barry",
            "age": 21
        }
    ]
}

dict2 = {
    "host_name": "abc_126",
    "address": "123.123.123.0",
    "attributes": {
        "max_check_attempts": 6,
        "max_load_attempts": 7
    },
    "list_of_data": [
        {
            "name": "barry",
            "age": 22
        },
        {
            "name": "garry",
            "age": 19,
            "type": "employee"
        }
    ]
}

dict1["meta"] = {
    "coordinates": (10, 20),
    "tags": {"x", "y", "z"}
}

dict2["meta"] = {
    "coordinates": (10, 30),
    "tags": {"y", "z", "a"}
}

# Running the comparison
# Text Output (default)
print(DictDiffer(dict1, dict2).compare())

# JSON Output
import json
json_diff = DictDiffer(dict1, dict2, mode='json').compare()
print(json.dumps(json_diff, indent=2))

# Flat Change Log
flat = DictDiffer(dict1, dict2, mode='flat').compare()
for entry in flat:
    print(" -> ".join(map(str, entry['path'])), ":", entry['from'], "->", entry['to'])