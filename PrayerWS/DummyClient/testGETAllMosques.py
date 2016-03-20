#!/usr/bin/env python

import requests;
import json;

URL = "http://127.0.0.1:8000/{}";
r = requests.get(URL.format("mosque"));
if r.status_code != 200:
    print("Error. Status Code: {}".format(r.status_code));
else:
    js = json.loads(r.text);
    print("Number of mosques: {}".format(len(js)));
