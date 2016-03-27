from rest_framework import serializers
from mosques.models import Mosque


##### #########################################################
class MosqueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mosque;
        fields = ('id', 'name', 'address', 'postcode', 'gender', 'capacity', 'location');

##### ###############################################################
class MosqueSearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mosque;
        fields = ('id', 'name', 'address', 'postcode');
