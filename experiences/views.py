from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from experiences.models import Perk
from experiences.serializers import PerkSerializer
# Create your views here.


class PerkView(APIView):

    def get(self, request):
        all_perk = Perk.objects.all()
        serializer = PerkSerializer(all_perk, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerkDetailView(APIView):

    def get(self, request, perk_id):
        perk = Perk.objects.get(pk=perk_id)
        serializer = PerkSerializer(perk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, perk_id):
        perk = Perk.objects.get(pk=perk_id)
        serializer = PerkSerializer(perk, data=request.data, partial=True,)
        if serializer.is_valid():
            update_perk = serializer.save()
            return Response(PerkSerializer(update_perk).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, perk_id):
        perk = Perk.objects.get(pk=perk_id)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
