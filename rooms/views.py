from django.shortcuts import render
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework import status
from rest_framework.views import APIView
from rooms.models import Amenity, Room
from categories.models import Category
from rooms.serializers import AmenitiesSerializer, RoomListSerializer, RoomDetailSerializer, ReviewSerializer
from medias.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookings.models import Booking
from bookings.serializers import PubilcBookingSerializer , CreateRoomBookingSerializer
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
            serializer = AmenitiesSerializer(amenity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AmenitiesDetail(APIView):

    def get_object(self,amenities_pk):
        try:
            return Amenity.objects.get(pk=amenities_pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, amenities_pk):
        amenities = self.get_object(amenities_pk)
        serializer = AmenitiesSerializer(amenities)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, amenities_pk):
        amenities = self.get_object(amenities_pk)
        serializer = AmenitiesSerializer(
            amenities, data=request.data, partial=True,)
        if serializer.is_valid():
            update_amenity = serializer.save()
            serializer = AmenitiesSerializer(update_amenity)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, amenities_pk):
        amenities = self.get_object(amenities_pk)
        amenities.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomView(APIView):

    # 읽기 전용 메소드 / 하지만 생성은 인증된 사용자에게만.
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, many=True, context={"request": request})
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# owner가 여기 request.user라고 serializer에게 말해주면됨.
# 유저를 신뢰하기 어렵기 때문에 유저로부터 owner의 정보를 얻지 않고(request.data) , serializer에게 onwer는 이 url를 호출한 사람이 될 것이라고 말해주고 싶다.
# owner의 데이터를 request.data에서 받아오는 것이 아니라 request.user에서 받아온다.

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    # 유저가 잘못된 정보를 보냈을 때. request가 잘못된 데이터를 가지고 있을 때 발생한다.
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                        raise ParseError("The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("category not found")
                try:
                    with transaction.atomic():
                        create_room = serializer.save(
                            owner=request.user, category=category)
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            create_room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(create_room)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception:
                    return ParseError("Amenity not found")
            else:
                raise ParseError("")
        else:
            raise NotAuthenticated


class RoomDetailView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        # if request.user.is_authenticated:
        #     raise NotAuthenticated permistionclass추가.하면서 주석
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room, data=request.data, partial=True)
        if serializer.is_valid():
            update_room = serializer.save()
            serializer = RoomDetailSerializer(update_room)
            return Response(serializer.data, status=status.HTTP_206_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, room_id):

        try:
            page = request.query_params.get("page", 1)
            page = int("page")

        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = Room.objects.get(pk=room_id)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end], many=True,)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id):

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user, room=self.get_object(room_id)
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            # 왜 room을 넣어주는 걸까...음... 사진을 어디 방에 넣어줄지가 필요해서 넣는 것이겠지?
            upload_photo = serializer.save(
                room=room
            )
            serializer = PhotoSerializer(upload_photo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 예약 방
class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self,room_id):
        try:
            return Room.objects.get(pk=room_id)
        except:
            raise NotFound

    def get(self, request, room_id):
        room = self.get_object(room_id)
        now = timezone.localtime(timezone.now()).date()
        booking = Booking.objects.filter(room=room, kind=Booking.BookingKindChoice.ROOM, check_in__gt=now,)
        serializer = PubilcBookingSerializer(booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id):
        room = self.get_object(room_id)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoice.ROOM,
            )
            serializer = PubilcBookingSerializer(booking)
            # check_in = request.data.get("check_in")
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    # def delete(self,request,room_id):
    #     room = self.get_object(room_id)
    #     room.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)