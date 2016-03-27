#!/usr/bin/env python

import requests;
import json;
import urllib

URL = "http://127.0.0.1:8000/{}";
r = requests.post(URL.format("timetable/upload"), files={'file': open('../data/Excel/test.xlsx', 'rb')});
js = json.loads(r.text);
if js['result'] == False:
    print("Error. {}".format(js['reason']));
else:
    print("Number of mosques: {}".format(js['data']));
