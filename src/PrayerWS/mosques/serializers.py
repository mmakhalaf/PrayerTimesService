from rest_framework import serializers
from mosques.models import Mosque


##### #########################################################
class MosqueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mosque;
        fields = "__all__";

##### ###############################################################
class MosqueSearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mosque;
        fields = ('id', 'name', 'address', 'postcode');
