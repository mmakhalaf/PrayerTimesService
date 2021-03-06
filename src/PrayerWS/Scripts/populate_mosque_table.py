#!/usr/bin/env python
#
# This script will populate the mosques table with data gathered from
# the mosques website.
#
# The script needs to be run from a django shell
#  exec(open('Scripts/populate_mosque_table.py').read());

from mosques.models import Mosque
from mosques.serializers import MosqueSerializer
from django.contrib.gis.geos import Point
from geocoder import google
import pyproj;
import json

print("Deleting..");
for m in Mosque.objects.all():
    m.delete();

print("Adding..");
uid = 0;
f = open("../../data/MD_Site.JSON");
data = json.load(f);

for m in data:

    m["id"] = uid;

    #print(m["name"]);
    if "gender" in m.keys():
        g = str.lower(m["gender"]);
        if g.find("woman") != -1 or g.find("women") != -1 or g.find("female") != -1:
            m["gender"] = "both";
        elif g.find("men") != -1 or g.find("man") != -1 or g.find("male") != -1:
            m["gender"] = "men";
        else:
            m["gender"] = "unknown";
    else:
        m["gender"] = "unknown";

    try:
        if m["accuracy"] > "C":
            print("Ignored {}".format(m['name']));
            continue;
    except KeyError:
        print("");

    # gc = google("{}, {}, {}, United Kingdom".format(m['name'], m['address'], m['postcode']));
    # if gc.json['status'] == False:
    #     print(" ===> Failed");
    #     continue;
    # p = Point(gc.json['lat'], gc.json['lng'], srid=4326);
    #
    # geod = pyproj.Geod(ellps='WGS84')
    # d1, d2, p_dist = geod.inv(gc.json['lng'], gc.json['lat'], float(m['longitude']), float(m['latitude']), False);

    p = Point(float(m['latitude']), float(m['longitude']), srid=4326);
    m["location"] = p;
    del m['latitude'];
    del m['longitude'];
    try:
        del m['accuracy'];
    except KeyError:
        print("");

    serializer = MosqueSerializer(data=m);
    if serializer.is_valid():
        uid = uid + 1;
        serializer.save();
    else:
        print(" => Failed");
        print(" " + m["name"]);
        print(" " + str(serializer.errors));



f.close();

# exec(open('Scripts/populate_mosque_table.py').read())