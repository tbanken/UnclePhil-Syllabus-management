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
        pass


class TAHome(View):
    def get(self, request):
        pass



class InstructorHome(View):
    def get(self, request):
        pass





