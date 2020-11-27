from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from syllabus.models import *


# Create your views here.


class Login(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        isValid = False
        try:
            m = Admin.objects.get(username=request.POST['name'])
        except ObjectDoesNotExist:
            pass

        try:
            m = TA.objects.get(username=request.POST['name'])
        except ObjectDoesNotExist:
            pass

        try:
            m = Instructor.objects.get(username=request.POST['name'])
        except ObjectDoesNotExist:
            pass

        isValid = (m.password == request.POST['password'])

        if isValid:
            request.session["user"] = m.username
            if isinstance(m, TA):
                return redirect("/tahome/")
            elif isinstance(m, Instructor):
                return redirect("/instructorhome/")
            else:
                return redirect("/adminhome/")
        else:
            return render(request, "login.html", {})


class AdminHome(View):
    def get(self, request):
        user = request.session["user"]
        return render(request, "AdminHome.html", {"username": user})

    def post(self, request):
        user = request.session["user"]
        return render(request, "AdminHome.html", {"username": user})


class AdminViewUsers(View):
    def get(self, request):
        user = request.session["user"]
        tas = list(TA.objects.all())
        instructors = list(Instructor.objects.all())
        return render(request, "AdminViewUsers.html", {"username": user, "instructors": instructors, "tas": tas})


class CreateUser(View):
    def get(self, request):
        return render(request, "CreateUser.html", {})

    def post(self, request):
        uType = request.POST['uType']

        if uType.__eq__('ta'):
            TA.objects.create(username=request.POST['name'], password=request.POST['password'],
                              email=request.POST['email'], first_name=request.POST['first_name'],
                              last_name=request.POST['last_name'], office=request.POST['office'],
                              phone=request.POST['phone'], officeHours=request.POST['office_hours'])
        else:
            Instructor.objects.create(username=request.POST['name'], password=request.POST['password'],
                                      email=request.POST['email'], first_name=request.POST['first_name'],
                                      last_name=request.POST['last_name'], office=request.POST['office'],
                                      phone=request.POST['phone'], officeHours=request.POST['office_hours'])
        return render(request, "CreateUser.html", {})


class EditUser(View):
    def get(self, request, username):
        request.session['user'] = username
        return render(request, "EditUser.html", {})

    def post(self, request):
        # set user data from EditUser.html
        # render EditUser.html again
        pass


class DeleteUser(View):
    def post(self, request, username):
        MyUser.objects.get(username=username).delete()
        return redirect("/user/")


class AdminCourse(View):
    pass


class TAHome(View):
    def get(self, request):
        pass


class InstructorHome(View):
    def get(self, request):
        pass
