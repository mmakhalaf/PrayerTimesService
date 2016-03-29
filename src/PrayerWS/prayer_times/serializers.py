from rest_framework import serializers
from prayer_times.models import PrayerTimes
from mosques.serializers import MosqueSerializer

##### #########################################################
class PrayerTimesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PrayerTimes;
        fields = ('id', 'date', 'fajr_jamaa', 'duhr_jamaa', 'asr_jamaa', 'maghrib_jamaa', 'ishaa_jamaa');
