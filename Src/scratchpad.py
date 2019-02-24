""" This file is for testing random ideas """

import json

test = {
    "apple": 0,
    "orange": 2
}


with open("test.json", "w") as write_file:
        json.dump(test, write_file)