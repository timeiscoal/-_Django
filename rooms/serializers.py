from rest_framework import serializers
from rooms.models import Amenity, Room
from user.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer()
    amenities = AmenitiesSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1


class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
        )
