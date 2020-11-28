from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from syllabus.models import *


class Login(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        isValid = False
        m = None
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

        if m is None:
            isValid = False
        else:
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
        utype = request.POST['utype']

        if utype == 'ta':
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
    def get(self, request, username, utype):
        return render(request, "EditUser.html", {"username": username, "utype": utype})

    def post(self, request, username, utype):
        if utype == 'ta':
            user = TA.objects.get(username=username)
        else:
            user = Instructor.objects.get(username=username)
        #TODO display the user information next to the text input
        user.username = request.POST['name']
        user.password = request.POST['password']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.office = request.POST['office']
        user.phone = request.POST['phone']
        user.officeHours = request.POST['office_hours']
        user.save()
        # TODO: check to see if fields are blank, if so don't update those fields
        return render(request, "EditUser.html", {})


class DeleteUser(View):
    def post(self, request, username):
        MyUser.objects.get(username=username).delete()
        return redirect("/user/")


class AdminCourse(View):
    pass


class TAHome(View):
    def get(self, request):
        username = request.session["user"]
        ta = TA.objects.get(username=username)
        print(ta.email)
        return render(request, "TAHome.html", {"ta": ta})



class TAEdit(View):
    def get(self, request, username):
        ta = TA.objects.get(username=username)
        return render(request, "TAEdit.html", {"ta": ta})

    def post(self, request, username):
        ta = TA.objects.get(username=username)
        ta.email = request.POST['email']
        ta.first_name = request.POST['first_name']
        ta.last_name = request.POST['last_name']
        ta.office = request.POST['office']
        ta.phone = request.POST['phone']
        ta.officeHours = request.POST['office_hours']
        ta.save()
        return redirect("/tahome/")



class InstructorHome(View):
    def get(self, request):
        pass
