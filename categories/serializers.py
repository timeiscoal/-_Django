from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
    created_at = serializers.DateTimeField()
