from django.contrib import admin
from django.urls import path,include
from services import views
from .views import *

urlpatterns = [

  path('',views.index,name='index'),
  path('base',views.base,name='base'),
  path('about',views.about,name='about'),
  path('description/<aid>',views.description, name='description'),
  path('applyform/<aid>',views.applyform),
  path('list', StudentList.as_view(),name='list'),
  path('<id>',StudentList.as_view(),name='list_id'),
  
]
