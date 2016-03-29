#!/usr/bin/env python

import requests;
import json;

URL = "http://127.0.0.1:8000/{}";
r = requests.get(URL.format("mosque"));
js = json.loads(r.text);
if js['result'] == False:
    print("Error. {}".format(js['reason']));
else:
    print("Number of mosques: {}".format(len(js['data'])));
