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
from django.conf import settings
from django.conf.urls.static import static

from syllabus.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('tahome/', TAHome.as_view()),
    path('taedit<str:username>/', TAEdit.as_view()),
    path('instructorhome/', InstructorHome.as_view()),
    path('instructoredit<str:username>/', InstructorEditInfo.as_view()),
    path('adminhome/', AdminHome.as_view()),
    path('user/', AdminViewUsers.as_view()),
    path('edituser<str:username>-<str:utype>/', EditUser.as_view()),
    path('deleteuser<str:username>/', DeleteUser.as_view()),
    path('createuser/', CreateUser.as_view()),
    path('course/', AdminViewCourses.as_view()),
    path('createcourse/', CreateCourse.as_view()),
    path('editcourse<str:name>/', EditCourse.as_view()),
    path('deletecourse<str:name>/', DeleteCourse.as_view()),
    path('viewsections<str:name>/', ViewSections.as_view()),
    path('createsection<str:name>/', CreateSection.as_view()),
    path('editsection<str:number>-<str:name>/', EditSection.as_view()),
    path('deletesection<str:number>-<str:name>/', DeleteSection.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Uniform Syllabus Admin"
admin.site.site_title = "Uniform Syllabus Admin Portal"
admin.site.index_title = "Welcome to Uniform Syllabus Admin Portal"
