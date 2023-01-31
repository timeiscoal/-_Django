from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate, login ,logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError ,NotFound
from rest_framework.permissions import IsAuthenticated
from .serializers import PrivateUserSerializer , UserReviewSerializer
from .models import User
import jwt
from django.conf import settings

# Create your views here.

class Me(APIView):

    # 개인정보는 자기 자신만 보는 것이 안전.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)
    
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user=serializer.save()
            serializer =PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class Users(APIView):
    
    def post(self,request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    def get(self, request, username):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

        serializer = PrivateUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self,request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError

# 리뷰만 가져오기 
# class UserReviews(APIView):

#     def get(self,request,username):
#         user = User.objects.get(username=username)
#         serializer = UserReviewSerializer(user, many=True)
#         return Response(serializer.data , status=status.HTTP_200_OK)


class LogIn(APIView):

    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username,password=password)
        if user:
            login(request, user)
            return Response({"ok":"welcome"})
        else:
            return Response({"error":"wrong password"})

class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        logout(request)
        return Response({"ok":"bye"})



class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token =jwt.encode({"pk":user.pk}, settings.SECRET_KEY,algorithm="HS256")
            return Response({"token":token})
        else:
            return Response({"error":"wrong password!"})