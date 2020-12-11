from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from .models import *


def edit_info(user, email, first_name, last_name, office, phone, office_hours):
    if email != '':
        user.email = email
    if first_name != '':
        user.first_name = first_name
    if last_name != '':
        user.last_name = last_name
    if office != '':
        user.office = office
    if phone != '':
        user.phone = phone
    if office_hours != '':
        user.office_hours = office_hours
    user.save()


class Login(View):
    # TODO add session expiry??
    def get(self, request):
        return render(request, "Login.html", {})

    def post(self, request):
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
            return render(request, "Login.html", {})


class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect("/")


class AdminHome(View):
    def get(self, request):
        return render(request, "AdminHome.html", {"username": request.session["user"]})


class AdminViewUsers(View):
    def get(self, request):
        tas = list(TA.objects.all())
        instructors = list(Instructor.objects.all())
        return render(request, "AdminViewUsers.html", {"username": request.session["user"], "instructors": instructors,
                                                       "tas": tas})


class CreateUser(View):
    def get(self, request):
        return render(request, "CreateUser.html", {})

    def post(self, request):
        utype = request.POST['utype']

        if request.POST['name'] == '' or request.POST['password'] == '' or request.POST['email'] == '':
            return redirect("/createuser/")

        if utype == 'ta':
            TA.objects.create(username=request.POST['name'], password=request.POST['password'],
                              email=request.POST['email'], first_name=request.POST['first_name'],
                              last_name=request.POST['last_name'], office=request.POST['office'],
                              phone=request.POST['phone'], office_hours=request.POST['office_hours'])
        else:
            Instructor.objects.create(username=request.POST['name'], password=request.POST['password'],
                                      email=request.POST['email'], first_name=request.POST['first_name'],
                                      last_name=request.POST['last_name'], office=request.POST['office'],
                                      phone=request.POST['phone'], office_hours=request.POST['office_hours'])
        return render(request, "CreateUser.html", {})


class EditUser(View):
    def get(self, request, username, utype):
        user = MyUser.objects.get(username=username)
        return render(request, "EditUser.html", {"user": user, "utype": utype})

    def post(self, request, username, utype):
        if utype == 'ta':
            user = TA.objects.get(username=username)
        else:
            user = Instructor.objects.get(username=username)
            if request.POST['name'] != '':
                user.username = request.POST['name']
            if request.POST['password'] != '':
                user.password = request.POST['password']
        edit_info(user, request.POST['email'], request.POST['first_name'], request.POST['last_name'],
                  request.POST['office'], request.POST['phone'], request.POST['office_hours'])
        return render(request, "EditUser.html", {})


# assumes that usernames are unique across all users
class DeleteUser(View):
    def post(self, request, username):
        MyUser.objects.get(username=username).delete()
        return redirect("/user/")


class AdminViewCourses(View):
    def get(self, request):
        user = request.session["user"]
        courses = list(Course.objects.all())
        # tas = {}
        # for c in courses:
        #     tas[c] = frozenset((TA.objects.filter(course__in=Course.objects.filter(name=c.name))))
        # print(tas)

        return render(request, "AdminViewCourses.html", {"username": user, "courses": courses})


class CreateCourse(View):
    def get(self, request):
        instructors = list(Instructor.objects.all())
        tas = list(TA.objects.all())
        return render(request, "CreateCourse.html", {"tas": tas, "instructors": instructors})

    def post(self, request):
        instructor = Instructor.objects.get(username=request.POST['instruct'])
        c = Course.objects.create(name=request.POST['name'], dep_number=request.POST['number'],
                                  term=request.POST['term'], instructor=instructor)
        # c.ta_set.add(TA.objects.get(username=request.POST['ta']))
        return render(request, "CreateCourse.html", {"name": request.POST['name']})


class EditCourse(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        instructors = list(Instructor.objects.all())
        tas = list(TA.objects.all())
        return render(request, "EditCourse.html", {"course": course, "tas": tas, "instructors": instructors})

    def post(self, request, name):

        course = Course.objects.get(name=name)
        if request.POST['name'] != '':
            course.name = request.POST['name']
        if request.POST['dep_number'] != '':
            course.dep_number = request.POST['dep_number']
        if request.POST['term'] != '':
            course.term = request.POST['term']
        course.save()
        return render(request, "EditCourse.html", {"name": name})


class CourseAddTA(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        tas = list(TA.objects.all())
        return render(request, "CourseAddTA.html", {"course": course, "tas": tas})

    def post(self, request, name):
        course = Course.objects.get(name=name)
        ta = TA.objects.get(username=request.POST['ta'])
        tas = list(TA.objects.all())
        course.ta_set.add(ta)
        return render(request, "CourseAddTA.html", {"course": course, "tas": tas})


# assumes that names are unique across all courses
class DeleteCourse(View):
    def post(self, request, name):
        Course.objects.get(name=name).delete()
        return redirect("/course/")


class ViewSections(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        sections = list(Section.objects.filter(course=course))
        return render(request, "AdminViewSections.html", {"name": name, "sections": sections})


class CreateSection(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        users = list()
        users.append(course.instructor)
        for t in TA.objects.filter(course__in=Course.objects.filter(name=course.name)):
            users.append(t)
        return render(request, "CreateSection.html", {"name": name, "users": users})

    def post(self, request, name):
        course = Course.objects.get(name=name)
        user = MyUser.objects.get(username=request.POST['user'])
        Section.objects.create(number=request.POST['number'], type_of=request.POST['stype'], user=user, course=course)
        return redirect("/viewsections" + name + "/")


class EditSection(View):
    def get(self, request, number, name):
        course = Course.objects.get(name=name)
        users = list()
        users.append(course.instructor)
        for t in TA.objects.filter(course__in=Course.objects.filter(name=course.name)):
            users.append(t)
        return render(request, "EditSection.html", {"number": number, "name": name, "users": users})

    def post(self, request, number, name):
        # TODO display the section information next to the text input
        section = Section.objects.get(number=number)
        if request.POST['stype'] != '':
            section.name = request.POST['stype']
        if request.POST['number'] != '':
            section.dep_number = request.POST['number']
        if request.POST['user'] != '':
            section.user = MyUser.objects.get(username=request.POST['user'])
        section.save()
        return render(request, "EditSection.html", {"number": number, "name": name})


class DeleteSection(View):
    def post(self, request, number, name):
        Section.objects.get(number=number).delete()
        return redirect("/viewsections" + name + "/")


class TAHome(View):
    def get(self, request):
        username = request.session["user"]
        ta = TA.objects.get(username=username)
        return render(request, "TAHome.html", {"ta": ta})


class TAEdit(View):
    def get(self, request, username):
        ta = TA.objects.get(username=username)
        return render(request, "TAEdit.html", {"ta": ta})

    def post(self, request, username):
        ta = TA.objects.get(username=username)
        edit_info(ta, request.POST['email'], request.POST['first_name'], request.POST['last_name'],
                  request.POST['office'], request.POST['phone'], request.POST['office_hours'])
        return redirect("/tahome/")


class InstructorHome(View):
    def get(self, request):
        username = request.session["user"]
        instructor = Instructor.objects.get(username=username)
        return render(request, "InstructorHome.html", {"instructor": instructor})


class InstructorEditInfo(View):
    def get(self, request, username):
        instructor = Instructor.objects.get(username=username)
        courses = list(Course.objects.filter(instructor=instructor))
        return render(request, "InstructorEdit.html", {"instructor": instructor, "courses": courses})

    def post(self, request, username):
        instructor = Instructor.objects.get(username=username)
        edit_info(instructor, request.POST['email'], request.POST['first_name'], request.POST['last_name'],
                  request.POST['office'], request.POST['phone'], request.POST['office_hours'])
        return redirect("/instructorhome/")


class Courses(View):
    def get(self, request):
        courses = list(Course.objects.all())
        return render(request, "Courses.html", {"courses": courses})


