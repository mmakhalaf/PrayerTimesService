# This script will populate the mosques table with data gathered

from PrayerWS.PrayerTimesAPI.models.mosque import Mosque
from PrayerWS.PrayerTimesAPI.serializers.mosque import MosqueSerializer

import json

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

    serializer = MosqueSerializer(data=m);
    if serializer.is_valid():
        serializer.save();
    else:
        print(" => Failed");
        print(" " + str(serializer.errors));

f.close();

# exec(open('Scripts/populate_mosque_table.py').read())