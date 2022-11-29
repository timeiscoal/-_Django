from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rooms.models import Amenity
from rooms.serializers import AmenitiesSerializer
# Create your views here.

# 모든 view function은 request를 받는다.
# request는 장고로 인해서 자동적으로 받게 되는 것이다.
# class안의 메소드들은 self은 자기 자신을 먼저 넣어주어야 한다.


class Amenities(APIView):
    def get(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitiesSerializer(amenities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AmenitiesSerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitiesSerializer(amenity).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AmenitiesDetail(APIView):

    def get(self, request, amenities_pk):
        amenities = Amenity.objects.get(pk=amenities_pk)
        serializer = AmenitiesSerializer(amenities)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, amenities_pk):
        amenitiy = Amenity.objects.get(pk=amenities_pk)
        serializer = AmenitiesSerializer(
            amenitiy, data=request.data, partial=True,)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitiesSerializer(amenity).data, status=status.HTTP_200_OK)

    def delete(self, request, amenities_pk):
        amenities = Amenity.objects.get(pk=amenities_pk)
        amenities.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
