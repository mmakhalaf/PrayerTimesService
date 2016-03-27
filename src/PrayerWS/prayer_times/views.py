from prayer_times.http_utils.prayer_tt_get import PTTGetRequest
from prayer_times.models import PrayerTimes
from prayer_times.serializers import PrayerTimesSerializer

from mosques.http_utils.json_response import JSONResponse

from rest_framework.views import APIView

class PrayerTimeTableUploadHandler(APIView):
    def post(self, request):
    ### ####################
        """
        Handle a file uplaod request.
        Requires,
          file to read
          month
          multiple months???
        """
        return JSONResponse.CreateDataResponse("In Upload POST");

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
        req_parser.Process(request.query_params);
        res, err = req_parser.IsValid();
        if res == False:
            return JSONResponse.CreateErrorResponse(err);

        qs = PrayerTimes.objects.\
                filter(mosque_id=req_parser.mosque_id).\
                filter(date__gte=req_parser.start_date).\
                filter(date__lte=req_parser.end_date);

        ser = PrayerTimesSerializer(qs, many=True);
        return JSONResponse.CreateDataResponse(ser.data);


