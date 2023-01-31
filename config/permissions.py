import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import User

class TrustMeBroAutentication(BaseAuthentication):
    
    def authenticate(self,request):
        username = request.headers.get('Trust-me')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user,None) # 튜플안에 user와 none 이건 규칙임;
        except User.DoesNotExist:
            raise AuthenticationFailed(f"no user {username}")

class JWTAuthentication(BaseAuthentication):

    def authenticate(self,request):
        token = request.headers.get("Jwt")
        # 토큰 안보내면 none
        if not token:
            return None
        decoded= jwt.decode(
            token,
            settings.SECRET_KEY, 
            algorithms=["HS256"],
        )
        pk =decoded.get("pk")
        # 토큰을 디코딩했는데 유효하지 않은 토큰이면 에러
        if not pk:
            return AuthenticationFailed("invalid token")
        try:
            user = User.objects.get(pk=pk)
            return (user,None)
        except User.DoesNotExist:
            raise AuthenticationFailed("user not found")
