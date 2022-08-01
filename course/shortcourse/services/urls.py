from django.contrib import admin
from django.urls import path, include
from services import views
from .views import *

urlpatterns = [

    path('', views.index, name='index'),
    # path('about', views.about, name='about'),
    path('course/<slug>', views.description, name='description'),
    path('login-success', views.loginSuccess, name='login-success'),
    path('like', views.like, name='like'),
    path('course/apply/<sid>', views.apply, name="course-apply"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup", views.signup, name="signup")

]
