
from geocoder import google
import re

from django.contrib.gis.geos import Point

class MosqueSearch:
    parLon = "lon";
    parLat = "lat";
    parDist = "distance";
    parAddress = "address";
    parGender = "gender";

    def __init__(self):
    ### ###############
        self.origin = None;
        self.distance = 0;
        self.gender = None;

    def Process(self, req_params):
    ### ##########################
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
        res = self.getLocation(req_params);
        if not res:
            # Must provide a location
            return False, "Must provide a location & distance.";

        self.__processGender(req_params);

        return True, None;

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
                self.distance = dist;
                if unit is not None:
                    unit = str.lower(unit);
                    if unit == 'm':
                        self.distance *= 1609.34;
                    elif unit == 'km':
                        self.distance *= 1000;
            else:
                return False;
        except Exception as e:
            return False;

        # See if we were given lon/lat coordinates
        try:
            lat = float(qparams[self.parLat]);
            lon = float(qparams[self.parLon]);

            # Return a lat/lon point
            self.origin = Point(lat, lon, srid=4326);
            return True;
        except Exception as e:
            pass;

        # We didn't get lon/lat, check for address
        try:
            # Convert city and postcodes to lon/lat
            addr = qparams[self.parAddress];
            # TODO : Use a Google Geocoding API Key to avoid hitting the maximum request limit
            gc = google(addr);
            if gc.json['status']:
                self.origin = Point(gc.json['lat'], gc.json['lng'], srid=4326);
                return True;
        except Exception as e:
            pass;

        return False;

    def __processGender(self, qparams):
    ### ###############################
        """Add a gender filter to the queryset if provided"""
        try:
            self.gender = qparams[self.parGender];
        except Exception as e:
            pass;