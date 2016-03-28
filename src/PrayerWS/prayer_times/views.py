
from prayer_times.http_utils.prayer_tt_upload import PTTUploadRequest
from prayer_times.http_utils.prayer_tt_get import PTTGetRequest
from prayer_times.models import PrayerTimes
from prayer_times.serializers import PrayerTimesSerializer

from mosques.http_utils.json_response import JSONResponse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

import os

class PrayerTimeTableUploadHandler(APIView):
    parser_classes = (MultiPartParser, FormParser, )
    def post(self, request):
    ### ####################
        """
        Handle a file uplaod request.
        Requires,
          file to read
          month
          multiple months???
        """

        try:
            file_data = request.data['files'];
        except Exception:
            return JSONResponse.CreateErrorResponse("No file was uploaded");

        req_parser = PTTUploadRequest();

        res, err = req_parser.StoreFile(file_data);
        if not res:
            return JSONResponse.CreateErrorResponse(err);

        res, err = req_parser.ProcessData(request.data);
        if not res:
            return JSONResponse.CreateErrorResponse(err);

        res, st = req_parser.ParseFile();
        if not res:
            return JSONResponse.CreateErrorResponse(st);

        return JSONResponse.CreateDataResponse(st);

##### ########################################
class PrayerTimeTableRetrieveHandler(APIView):
    def get(self, request):
    ### ###################
        """
        Handle request to retrieve the timetable
        Requires,
          mosque id
          month | number of days
        """

        req_parser = PTTGetRequest();
        res, err = req_parser.Process(request.query_params);
        if res == False:
            return JSONResponse.CreateErrorResponse(err);

        qs = PrayerTimes.objects.\
                filter(mosque_id=req_parser.mosque_id).\
                filter(date__gte=req_parser.start_date).\
                filter(date__lte=req_parser.end_date);

        ser = PrayerTimesSerializer(qs, many=True);
        return JSONResponse.CreateDataResponse(ser.data);


