from rest_framework import serializers
from prayer_times.models import PrayerTimes


##### #########################################################
class PrayerTimesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PrayerTimes;
        fields = "__all__";
