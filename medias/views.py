from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.room:
            if photo.room.owner != request.user:
                raise PermissionDenied

        elif photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied
        photo.delete()
        return Response(status=status.HTTP_200_OK)
