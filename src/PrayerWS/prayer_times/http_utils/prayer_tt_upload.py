from prayer_times.parser.ptt_excel import PrayerTimeExcelParser
from prayer_times.parser.ptt_parser import ParsingError
from prayer_times.parser.ptt_prayer_names import *

from prayer_times.models import PrayerTimes
from mosques.models import Mosque

from django.conf import settings
import json
import datetime
import os

##### #########################################################################
class PTTUploadRequest:
    """Parse the upload request"""
    
    def __init__(self):
    ### ###############
        self.file_path = None;
        self.month = None;
        self.mosque_id = None;

    def StoreFile(self, file_data):
    ### ###########################
        """Process the given file data and store it onto the file system."""

        now = datetime.datetime.now();
        root_dir = os.path.join(settings.MEDIA_ROOT, now.strftime("%Y-%m-%d"));
        fname = os.path.join(root_dir, now.strftime("%H%M%S_{}".format(file_data.name)));

        try:
            os.makedirs(root_dir, exist_ok=True);
            dest = open(fname, 'wb+');
            for c in file_data.chunks():
                dest.write(c);
            dest.close();
        except Exception as e:
            os.remove(fname);
            return False, "Failed to write uploaded file.";

        if not os.path.exists(fname):
            return False, "Failed to write upload file.";

        self.file_path = fname;

        return True, None;

    def ProcessData(self, data):
    ### ########################
        """Process the rest of the request data"""
        try:
            self.month = int(float(data['month']));
        except Exception as e:
            return False, "A month must be provided.";

        try:
            self.mosque_id = int(float(data['mosqueid']));
        except Exception as e:
            return False, "A mosque ID must be provided.";

        return True, None;

    def ParseFile(self):
    ### ################
        """Parse the timetable file, and input into the database"""
        imp = PrayerTimeExcelParser();

        # Import the timetable in the correct year
        # We can't import into the past
        now = datetime.datetime.now();
        curr_month = now.month;
        curr_year = now.year;
        if self.month < curr_month:
            imp.year = curr_year + 1;

        imp.month = self.month;
        imp.year = curr_year;

        try:
            mosque = Mosque.objects.get(id=self.mosque_id);
        except Exception as e:
            return False, "No mosque was found with the given ID {}".format(self.mosque_id);

        try:
            prayer_times = imp.ImportFromFile(self.file_path);
        except ParsingError as e:
            return False, "Parsing Error: {}".format(str(e));

        for idx, pt in enumerate(prayer_times):
            pt_model = PrayerTimes(mosque=mosque,
                                   date=datetime.date(imp.year, imp.month, idx+1),
                                   fajr_jamaa=pt[FajrPrayerName.name],
                                   duhr_jamaa=pt[DuhrPrayerName.name],
                                   asr_jamaa=pt[AsrPrayerName.name],
                                   maghrib_jamaa=pt[MaghribPrayerName.name],
                                   ishaa_jamaa=pt[IshaPrayerName.name]);
            pt_model.save();

        return True, "Added {} days from the timetable".format(len(prayer_times));