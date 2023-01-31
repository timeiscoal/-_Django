from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
     path("me/", views.Me.as_view(),),
     path("", views.Users.as_view(),),
     path("change-password/",views.ChangePassword.as_view()),
     path("log-in/", views.LogIn.as_view()),
     path("log-out/", views.LogOut.as_view()),
     path("token-login/", obtain_auth_token),
     path("jwt-login/", views.JWTLogIn.as_view(),),
     path("@<str:username>/", views.PublicUser.as_view(),),

    #  path("@<str:username>/reviews/", views.UserReviews.as_view(),),
]


# url 네이밍을 하는 과정에서 <str:username>같이 사용할 경우 다른 url과 이름이 겹치지 않게 잘 확인해야한다. 인식을 잘못할 수 있음. 그래서 @를 넣거나 하는 등의 방법이 필요함.