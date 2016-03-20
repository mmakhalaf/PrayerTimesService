#!/usr/bin/env python

import requests;
import json;


URL = "http://127.0.0.1:8000/{}";

def searchLatLon(lat, lon, dist, gender = None):
    search_str = "mosque/search?lat={}&lon={}&distance={}".format(lat, lon, dist);
    if gender is not None:
        search_str += "&gender={}".format(gender);

    r = requests.get(URL.format(search_str));
    if r.status_code != 200:
        print("Error. Status Code: {}".format(r.status_code));
        return 0;
    js = json.loads(r.text);
    print("Num: {}".format(len(js)));
    return len(js);

def searchAddress(addr, dist, gender = None):
    search_str = "mosque/search?address={}&distance={}".format(addr, dist);
    if gender is not None:
        search_str += "&gender={}".format(gender);

    r = requests.get(URL.format(search_str));
    if r.status_code != 200:
        print("Error. Status Code: {}".format(r.status_code));
        return 0;
    js = json.loads(r.text);
    print("Num: {}".format(len(js)));
    return len(js);


n = searchLatLon(52.465744, -1.937817, 10);

n = searchLatLon(52.465744, -1.937817, "3km");

n = searchLatLon(52.465744, -1.937817, "2m");

n = searchAddress("B153UE", "2m");

n = searchAddress("4 Balcaskie Close, Birmingham", "3km");

n = searchLatLon(52.465744, -1.937817, "2m", gender="both");

n = searchLatLon(52.465744, -1.937817, "2m", gender="men");

n = searchLatLon(52.465744, -1.937817, "2m", gender="unknown");