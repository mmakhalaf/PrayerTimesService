
from mosques.http_utils.json_response import JSONResponse
from mosques.serializers import *
from mosques.models import Mosque
from mosques.http_utils.mosque_search import MosqueSearch

from rest_framework.views import APIView

from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.measure import D

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
    
    def get(self, request):
    ### ###################

        req_parser = MosqueSearch();
        res, err = req_parser.Process(request.query_params);
        if not res:
            return JSONResponse.CreateErrorResponse(err);
        
        m = Mosque.objects.filter(location__distance_lt=(req_parser.origin, D(m=req_parser.distance)));
        if req_parser.gender is not None:
            m = m.filter(gender=req_parser.gender);

        #TODO when filtering by gender, display unknown mosques
        #TODO Sort result by distance

        serializer = MosqueSearchSerializer(m, many=True);
        return JSONResponse.CreateDataResponse(serializer.data);


##### #########################################################################
class MosqueDetailsHandler(APIView):
    """Get a single mosque details given an ID"""
    def get(self, request, id):
    ### #######################
        try:
            m = Mosque.objects.get(id=id);
            serializer = MosqueSerializer(m);
            return JSONResponse.CreateDataResponse(serializer.data);
        except:
            return JSONResponse.CreateErrorResponse("Could not find mosque with an ID of {}".format(id));
