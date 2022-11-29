from rest_framework import serializers
from user.models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "profile_photo", "username",)
