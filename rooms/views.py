from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rooms.models import Amenity, Room
from rooms.serializers import AmenitiesSerializer, RoomListSerializer, RoomDetailSerializer
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
        amenities = Amenity.objects.get(pk=amenities_pk)
        serializer = AmenitiesSerializer(
            amenities, data=request.data, partial=True,)
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(AmenitiesSerializer(update_amenity).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, amenities_pk):
        amenities = Amenity.objects.get(pk=amenities_pk)
        amenities.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomView(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomListSerializer(data=request.data)
        if serializer.is_valid():
            create_room = serializer.save()
            return Response(RoomListSerializer(create_room).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        serializer = RoomDetailSerializer(room, data=request.data)
        if serializer.is_valid():
            update_room = serializer.save()

    def delete(self, request, room_id):
        pass
