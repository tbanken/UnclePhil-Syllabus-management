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
            return redirect('home')
        else:
            return render(request, "login.html", {})


# class Home(View):
#     def get(self):
#         pass
