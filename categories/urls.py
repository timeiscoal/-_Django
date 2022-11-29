from django.urls import path
from categories import views

urlpatterns = [
    path('', views.categories, name="categories"),
    path('<int:pk>/', views.categoriesdetail, name="categoriesdetail"),
]
