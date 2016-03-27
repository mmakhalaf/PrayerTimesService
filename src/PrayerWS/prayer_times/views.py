
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
        pass;

##### ########################################
class PrayerTimeTableRetrieveHandler(APIView):
    def get(self, request):
    ### ###################
        """
        Handle request to retrieve the timetable
        Requires,
          mosque id
          month | date_range
          day
        """
        pass;