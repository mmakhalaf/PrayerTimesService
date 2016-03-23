from rest_framework import serializers
from app.models.mosque import Mosque


class MosqueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mosque
        fields = ('id', 'name', 'address', 'postcode', 'capacity', 'gender', 'location')
