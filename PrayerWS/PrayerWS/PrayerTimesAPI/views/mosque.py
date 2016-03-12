from rest_framework import viewsets

from PrayerWS.PrayerTimesAPI.http_utils.json_response import JSONResponse
from PrayerWS.PrayerTimesAPI.serializers.mosque import MosqueSerializer
from PrayerWS.PrayerTimesAPI.models.mosque import Mosque

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


###
# Handle request for listing all mosques
# This is a GET request which takes no arguments
class ListMosquesHandler(APIView):
    def get(self, request):
        mosques = Mosque.objects.all();
        serializer = MosqueSerializer(mosques, many=True);
        return Response(serializer.data);


###
# Search for mosques given some criteria
class SearchMosquesHandler(APIView):
    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT);


###
# Get a single mosque details given an ID
class MosqueDetailsHandler(APIView):
    def get(self, request, id):
        try:
            m = Mosque.objects.get(id=id);
            serializer = MosqueSerializer(m);
            return Response(serializer.data);
        except:
            return Response(status=status.HTTP_404_NOT_FOUND);
