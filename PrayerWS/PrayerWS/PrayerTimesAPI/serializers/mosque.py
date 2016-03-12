from rest_framework import serializers
from PrayerWS.PrayerTimesAPI.models.mosque import Mosque


class MosqueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mosque
        fields = ('id', 'name', 'address', 'postcode', 'capacity', 'gender', 'latitude', 'longitude' )
