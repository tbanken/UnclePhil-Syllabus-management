"""UnclePhilSyllabus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from syllabus.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', Login.as_view(), name='login'),
    path('adminhome/', AdminHome.as_view(), name='ahome'),
    path('tahome/', TAHome.as_view(), name='thome'),
    path('instructorhome/', InstructorHome.as_view(), name='ihome')
]

admin.site.site_header = "Uniform Syllabus Admin"
admin.site.site_title = "Uniform Syllabus Admin Portal"
admin.site.index_title = "Welcome to Uniform Syllabus Admin Portal"
