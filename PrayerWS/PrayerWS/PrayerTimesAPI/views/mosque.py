from rest_framework import viewsets

from PrayerWS.PrayerTimesAPI.http_utils.json_response import JSONResponse
from PrayerWS.PrayerTimesAPI.serializers.mosque import MosqueSerializer
from PrayerWS.PrayerTimesAPI.models.mosque import Mosque

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.measure import D
from django.db import connection


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

    def __init__(self):
        self.pLon = "lon";
        self.pLat = "lat";
        self.pDist = "distance";


    def get(self, request):
        # https://developers.google.com/maps/articles/phpsqlsearch_v3#populating-the-table
        #
        #
        # Extract parameters for the search
        # origin
        #  location   - origin point
        #  postcode   - origin postcode
        #  city       - origin city/town name
        #  Need to convert postcode / city to lon/lat coordinates
        #
        # distance <  - distance to location
        #  Need to convert distance to be between lon/lat coordinates
        # unit        - unit that the distance was provided in
        #
        # capacity <> -
        #
        # gender      - male only or male/female
        #

        origin = self.getLocation(request.query_params);
        if origin is None:
            # Must provide a location
            return Response(status=status.HTTP_417_EXPECTATION_FAILED);

        distance = request.query_params[self.pDist];
        if distance is None:
            distance = 1;

        m = Mosque.objects.filter(location__distance_lt=(origin, D(km=distance)));
        print(m.query);
        serializer = MosqueSerializer(m, many=True);
        return Response(serializer.data);

    def getLocation(self, qparams):
        if qparams[self.pLon] is None or qparams[self.pLat] is None:
            return None;

        origin = Point(float(qparams[self.pLon]), float(qparams[self.pLat]), srid=4326);
        # TODO Convert city and postcodes to lon/lat
        #      use Google geocoders

        return origin;



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
