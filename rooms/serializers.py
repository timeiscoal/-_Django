from rest_framework import serializers
from rooms.models import Amenity


class AmenitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = "__all__"
