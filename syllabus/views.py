from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
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


class AdminUser(View):
    def get(self, request):
        user = request.session["user"]
        tas = list(TA.objects.all())
        instructors = list(Instructor.objects.all())
        return render(request, "AdminUser.html", {"username": user, "instructors": instructors, "tas": tas,
                                                  "request": request.session})

    def post(self, request):
        # toDelete = request.session["toModify"]
        # print(toDelete)
        # #toDelete.delete()
        # user = request.session["user"]
        # tas = list(TA.objects.all())
        # instructors = list(Instructor.objects.all())
        # return render(request, "AdminUser.html", {"username": user, "instructors": instructors, "tas": tas})
        pass


class EditUser(View):
    # get username from session then change fields based on HTML input
    def get(self):
        pass


class AdminCourse(View):
    pass


class TAHome(View):
    def get(self, request):
        pass


class InstructorHome(View):
    def get(self, request):
        pass
