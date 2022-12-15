from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from rooms.models import Room


class WishlistView(APIView):

    # 나만 볼 수 있음
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(all_wishlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = serializer(wishlist)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class WishListDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serilaizer = WishlistSerializer(
            wishlist, data=request.data, partial=True)
        if serilaizer.is_valid():
            wishlist = serilaizer.save()
            serilaizer = WishlistSerializer(wishlist)
            return Response(serilaizer.data, status=status.HTTP_200_OK)
        else:
            return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=status.HTTP_200_OK)


class WishlistToggleView(APIView):

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        Wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        # 만약 위시리스트에 있다면 삭제되고 없으면 추가됨
        if Wishlist.rooms.filter(pk=room.pk).exists():
            Wishlist.rooms.remove(room)
        else:
            Wishlist.rooms.add(room)

        return Response(status=status.HTTP_200_OK)
