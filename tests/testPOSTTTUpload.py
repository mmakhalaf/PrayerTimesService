#!/usr/bin/env python
#
# http://stackoverflow.com/questions/33721905/django-rest-framework-and-file-upload
# http://stackoverflow.com/questions/20473572/django-rest-framework-file-upload/27305713#27305713
#
import requests
import json
import urllib
import sys


multiple_files = [('files', ('test.xlsx', open('../data/Excel/test.xlsx', 'rb'), '*/*'))];
data = { 'month': 3, 'mosqueid': 3 };

URL = "http://127.0.0.1:8000/{}";
r = requests.post(\
        URL.format("timetable/upload"),\
        #"http://www.httpbin.org/post",\
        files=multiple_files,\
        data=data);
js = json.loads(r.text);

if js['result'] == False:
    print("Error: {}".format(js['reason']));
else:
    print(js);
