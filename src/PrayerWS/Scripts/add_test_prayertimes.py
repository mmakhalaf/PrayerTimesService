#!/usr/bin/env python
#
# Add some initial prayer times
#
# The script needs to be run from a django shell
#  exec(open('Scripts/add_test_prayertimes.py').read());
#   

from prayer_times.parser.ptt_excel import PrayerTimeExcelParser
from prayer_times.parser.ptt_prayer_names import *

from prayer_times.models import PrayerTimes
from prayer_times.serializers import PrayerTimesSerializer
from mosques.models import Mosque

import datetime;


imp = PrayerTimeExcelParser();
imp.month = 3; imp.year = 2016;
prayer_times = imp.ImportFromFile("../../data/Excel/test.xlsx");
'''
for pt in prayer_times:
    print(pt);
'''

mosque = Mosque.objects.get(id=2);
if mosque is None:
    print("Could not find mosque with ID=2");

print("N Days: {}".format(str(len(prayer_times))));

for idx, pt in enumerate(prayer_times):
    
    #print(idx);
    pt_model = PrayerTimes(mosque=mosque,
                           date=datetime.date(1990, 3, idx+1),
                           fajr_jamaa=pt[FajrPrayerName.name],
                           duhr_jamaa=pt[DuhrPrayerName.name],
                           asr_jamaa=pt[AsrPrayerName.name],
                           maghrib_jamaa=pt[MaghribPrayerName.name],
                           ishaa_jamaa=pt[IshaPrayerName.name]);
    pt_model.save();

    #ser = PrayerTimesSerializer(data=pt);
    #if ser.is_valid():
    #    ser.save();
    #else:
    #    print(" => Failed");
    #    print(" " + str(idx));
    #    print(" " + str(ser.errors));

