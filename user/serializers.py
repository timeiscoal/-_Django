from rest_framework import serializers
from user.models import User
from reviews.serializers import ReviewSerializer

class PrivateUserSerializer(serializers.ModelSerializer):

    # 패스워드맨 제외해서 보여주기.
    class Meta:
        model = User
        exclude = ("password","is_superuser","id","is_staff","is_active","first_name","last_name",)

class UserReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer()

    class Meta:
        model = User
        fields = "__all__"

