from django.urls import path, include
from services import views

urlpatterns = [

    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('course/<slug>', views.description, name='description'),
    path('login-success', views.loginSuccess, name='login-success'),
    path('like', views.like, name='like'),
    path('course/apply/<sid>', views.apply, name="course-apply"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup", views.signup, name="signup"),
    path('enrollments', views.show_enrollment_detail, name='enrollments'),
    path('profile', views.profile, name='profile'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/<section_slug>',  
        views.activate, name='activate'),  

]
