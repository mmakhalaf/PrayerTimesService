# This script will populate the mosques table with data gathered

from PrayerWS.PrayerTimesAPI.models.mosque import Mosque
from PrayerWS.PrayerTimesAPI.serializers.mosque import MosqueSerializer
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.utils import layermapping
from django.db.utils import DataError
from django.db import connection
import json

# p1 = GEOSGeometry('SRID=3857;POINT(52.45 -1.9)');
# p2 = GEOSGeometry('SRID=3857;POINT(52.35 -1.8)');
# print("dist ", p1.distance(p2));
# exit(0);

print("Deleting..");
for m in Mosque.objects.all():
    m.delete();

print("Adding..");
uid = 0;
f = open("../MosqueDirParser/MD_Site.JSON");
data = json.load(f);
for m in data:
    m["id"] = uid;
    uid += 1;

    print(m["name"]);
    if "gender" in m.keys():
        g = str.lower(m["gender"]);
        if g.find("woman") != -1 or g.find("women") != -1 or g.find("female") != -1:
            m["gender"] = "both";
        elif g.find("men") != -1 or g.find("man") != -1 or g.find("male") != -1:
            m["gender"] = "men";
        else:
            m["gender"] = "unknown";
    #p = GEOSGeometry('SRID=4326;POINT({} {})'.format(m["latitude"], m["longitude"]));
    p = Point(float(m["latitude"]), float(m["longitude"]), srid=4326);
    m["location"] = p;

    serializer = MosqueSerializer(data=m);
    if serializer.is_valid():
        #try:
        serializer.save();
        #except DataError:
        #    print(connection.queries[-1]);

    else:
        print(" => Failed");
        print(" " + str(serializer.errors));

f.close();

# exec(open('Scripts/populate_mosque_table.py').read())