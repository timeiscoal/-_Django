from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@api_view(["GET", "POST"])
def categories(request):
    if request == "GET":
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    if request == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELTE"])
def categoriesdetail(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)

    return Response(serializer.data)
