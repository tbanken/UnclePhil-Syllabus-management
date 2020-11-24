from django.shortcuts import render, redirect
from django.views import View
from syllabus.models import *


# Create your views here.


class Login(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        try:
            m = MyUser.objects.get(username=request.POST['name'])
            isValid = (m.password == request.POST['password'])
        except:
            pass
        if isValid:
            request.session["user"] = m.username
            request.session["pswd"] = m.password
            return redirect("/home/")
        else:
            return render(request, "login.html", {})


class Home(View):
    def get(self, request):
        user = MyUser.objects.filter(username=request.session["user"], password=request.session["pswd"])
        if isinstance(user, TA):
            return render(request, "TAHome.html", {})
        elif isinstance(user, Instructor):
            return render(request, "InstructorHome.html", {})
        else:
            return render(request, "AdminHome.html", {})

