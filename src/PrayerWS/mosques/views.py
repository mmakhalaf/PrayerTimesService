from rest_framework import viewsets

from mosques.http_utils.json_response import JSONResponse
from mosques.serializers import *
from mosques.models import Mosque

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from geocoder import google
import re;

from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.measure import D
from django.db import connection
from django.utils.datastructures import MultiValueDictKeyError


###### ########################################################################
class ListMosquesHandler(APIView):
    """
    Handle request for listing all mosques
    This is a GET request which takes no arguments
    """

    def get(self, request):
    ### ###################
        mosques = Mosque.objects.all();
        serializer = MosqueSerializer(mosques, many=True);
        return Response(serializer.data);


##### #########################################################################
class SearchMosquesHandler(APIView):
    """Search for mosques given some criteria"""
    def __init__(self):
    ### ###############
        self.parLon = "lon";
        self.parLat = "lat";
        self.parDist = "distance";
        self.parAddress = "address";
        self.parGender = "gender";


    def get(self, request):
    ### ###################
        """
        Extract parameters for the search
         origin
         location   - origin point
         postcode   - origin postcode
         city       - origin city/town name
         Need to convert postcode / city to lon/lat coordinates
        
         distance <  - distance to location
          Need to convert distance to be between lon/lat coordinates
         unit        - unit that the distance was provided in
        
         gender      - male only or male/female
        """

        origin, distance = self.getLocation(request.query_params);
        if origin is None:
            # Must provide a location
            return Response(status=status.HTTP_417_EXPECTATION_FAILED);

        m = Mosque.objects.filter(location__distance_lt=(origin, D(m=distance)));
        m = self.filterByGender(request.query_params, m);

        print(m.query);
        serializer = MosqueSearchSerializer(m, many=True);
        return Response(serializer.data);

    def getLocation(self, qparams):
    ### ###########################
        """
        Return the origin, distance (in meters)
        Parse the search radius. It could be,
         10   - meters
         10m  - miles
         10km - km
        """
        try:
            dist = qparams[self.parDist];
            m = re.match(r'^([0-9]+\.?[0-9]*)\s*([A-Za-z]+)?$', str(dist));
            if m is not None:
                dist = float(m.group(1));
                unit = m.group(2);
                distance = dist;
                if unit is not None:
                    unit = str.lower(unit);
                    if unit == 'm':
                        distance *= 1609.34;
                    elif unit == 'km':
                        distance *= 1000;
            else:
                return None, None;
        except MultiValueDictKeyError:
            return None, None;

        # See if we were given lon/lat coordinates
        try:
            lat = float(qparams[self.parLat]);
            lon = float(qparams[self.parLon]);

            # Return a lat/lon point
            origin = Point(lat, lon, srid=4326);
            return origin, distance;
        except MultiValueDictKeyError:
            print("No Lat/Lon");

        # We didn't get lon/lat, check for address
        try:
            # Convert city and postcodes to lon/lat
            addr = qparams[self.parAddress];
            # TODO : Use a Google Geocoding API Key to avoid hitting the maximum request limit
            gc = google(addr);
            if gc.json['status']:
                origin = Point(gc.json['lat'], gc.json['lng'], srid=4326);
                return origin, distance;
        except MultiValueDictKeyError:
            print("No address");

        return None, None;

    def filterByGender(self, qparams, queryset):
    ### ########################################
        """Add a gender filter to the queryset if provided"""
        try:
            gender = qparams[self.parGender];
            queryset = queryset.filter(gender=gender);
        except:
            return queryset;
        return queryset;

##### #########################################################################
class MosqueDetailsHandler(APIView):
    """Get a single mosque details given an ID"""
    def get(self, request, id):
    ### #######################
        try:
            m = Mosque.objects.get(id=id);
            serializer = MosqueSerializer(m);
            return Response(serializer.data);
        except:
            return Response(status=status.HTTP_404_NOT_FOUND);
