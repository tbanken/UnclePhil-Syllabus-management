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
        return render(request, "Admin/AdminHome.html", {"username": request.session["user"]})


class AdminViewUsers(View):
    def get(self, request):
        tas = list(TA.objects.all())
        instructors = list(Instructor.objects.all())
        return render(request, "Admin/AdminViewUsers.html",
                      {"username": request.session["user"], "instructors": instructors,
                       "tas": tas})


class CreateUser(View):
    def get(self, request):
        return render(request, "Admin/CreateUser.html", {"pf": ''})

    def post(self, request):
        utype = request.POST['utype']

        if request.POST['name'] == '' or request.POST['password'] == '' or request.POST['email'] == '':
            return render(request, "Admin/CreateUser.html",
                          {"pf": 'Please enter a username, password, and email to create '
                                 'a user'})

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
        return render(request, "Admin/CreateUser.html", {"pf": 'Success! User created'})


class EditUser(View):
    def get(self, request, username, utype):
        if utype == 'ta':
            user = TA.objects.get(username=username)
        else:
            user = Instructor.objects.get(username=username)
        return render(request, "Admin/EditUser.html", {"user": user, "utype": utype})

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
        return render(request, "Admin/EditUser.html", {"user": user, "utype": utype})


# assumes that usernames are unique across all users
class DeleteUser(View):
    def post(self, request, username):
        MyUser.objects.get(username=username).delete()
        return redirect("/user/")


class AdminViewCourses(View):
    def get(self, request):
        user = request.session["user"]
        courses = list(Course.objects.all())
        return render(request, "Admin/AdminViewCourses.html", {"username": user, "courses": courses})


class CreateCourse(View):
    def get(self, request):
        instructors = list(Instructor.objects.all())
        tas = list(TA.objects.all())
        return render(request, "Admin/CreateCourse.html", {"tas": tas, "instructors": instructors})

    def post(self, request):
        if request.POST['name'] == '' or request.POST['dep_number'] == '' or \
                request.POST['term'] == '':
            return render(request, "Admin/CreateCourse.html", {"pf": 'Please enter all fields excluding description'})
        if request.POST['instruct'] != '':
            instructor = Instructor.objects.get(username=request.POST['instruct'])
        else:
            instructor = None

        Course.objects.create(name=request.POST['name'], dep_number=request.POST['dep_number'],
                              term=request.POST['term'], instructor=instructor, description=request.POST['desc'])
        return render(request, "Admin/CreateCourse.html",
                      {"name": request.POST['name'], "pf": 'Success! Course created'})


class EditCourse(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        instructors = list(Instructor.objects.all())
        return render(request, "Admin/EditCourse.html", {"course": course, "instructors": instructors})

    def post(self, request, name):
        course = Course.objects.get(name=name)
        instructors = list(Instructor.objects.all())
        if request.POST['name'] != '':
            course.name = request.POST['name']
        if request.POST['dep_number'] != '':
            course.dep_number = request.POST['dep_number']
        if request.POST['term'] != '':
            course.term = request.POST['term']
        if request.POST['desc'] != '':
            course.desc = request.POST['desc']
        if request.POST['instruct'] != '':
            course.instructor = Instructor.objects.get(username=request.POST['instruct'])
        course.save()
        return render(request, "Admin/EditCourse.html", {"course": course, "instructors": instructors})


class CourseAddTA(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        tas = list(TA.objects.all())
        return render(request, "Admin/CourseAddTA.html", {"course": course, "tas": tas})

    def post(self, request, name):
        course = Course.objects.get(name=name)
        ta = TA.objects.get(username=request.POST['ta'])
        tas = list(TA.objects.all())
        course.ta_set.add(ta)
        return render(request, "Admin/CourseAddTA.html", {"course": course, "tas": tas})


# assumes that names are unique across all courses
class DeleteCourse(View):
    def post(self, request, name):
        Course.objects.get(name=name).delete()
        return redirect("/course/")


class ViewTAs(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        tas = list(TA.objects.filter(course=course))
        return render(request, "Admin/ViewTAs.html", {"tas": tas, "course": course})


class ViewSections(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        sections = list(Section.objects.filter(course=course))
        return render(request, "Admin/AdminViewSections.html", {"name": name, "sections": sections})


# assumes that only an instructor can be assigned to a lecture
class CreateSection(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        users = list()
        users.append(course.instructor)
        for t in list(course.ta_set.all()):
            users.append(t)
        return render(request, "Admin/CreateSection.html", {"name": name, "users": users})

    def post(self, request, name):
        if request.POST['number'] == '' or request.POST['stype'] == '' or request.POST['days'] == '' or \
                request.POST['time'] == '':
            return render(request, "Admin/CreateCourse.html", {"pf": 'Please enter all fields excluding instructor'})
        course = Course.objects.get(name=name)
        if request.POST['user'] == '':
            instructor = None
            ta = None
        elif request.POST['stype'] == "LEC":
            instructor = Instructor.objects.get(username=request.POST['user'])
            ta = None
        else:
            ta = TA.objects.get(username=request.POST['user'])
            instructor = None
        Section.objects.create(number=request.POST['number'], type_of=request.POST['stype'], ta=ta,
                               instructor=instructor, course=course, days=request.POST['days'],
                               time=request.POST['time'])
        return redirect("/viewsections" + name + "/")


class EditSection(View):
    def get(self, request, number, name):
        course = Course.objects.get(name=name)
        users = list()
        users.append(course.instructor)
        sec = Section.objects.get(number=number)
        for t in TA.objects.filter(course__in=Course.objects.filter(name=course.name)):
            users.append(t)
        return render(request, "Admin/EditSection.html",
                      {"number": number, "name": name, "users": users, "sec": sec})

    def post(self, request, number, name):
        section = Section.objects.get(number=number, course=Course.objects.get(name=name))
        if request.POST['stype'] != '':
            section.name = request.POST['stype']
        if request.POST['number'] != '':
            section.number = request.POST['number']
        if request.POST['days'] != '':
            section.days = request.POST['days']
        if request.POST['time'] != '':
            section.time = request.POST['time']

        if request.POST['user'] != '':
            if section.type_of == 'LEC':
                section.instructor = Instructor.objects.get(username=request.POST['user'])
                section.ta = None
            else:
                section.ta = TA.objects.get(username=request.POST['user'])
                section.instructor = None
        section.save()
        users = list()
        users.append(Course.objects.get(name=name).instructor)
        number = section.number
        for t in TA.objects.filter(course__in=Course.objects.filter(name=Course.objects.get(name=name).name)):
            users.append(t)
        return render(request, "Admin/EditSection.html", {"number": number, "name": name, "sec": section, "users": users})


class DeleteSection(View):
    def post(self, request, number, name):
        Section.objects.get(number=number, course=Course.objects.get(name=name)).delete()
        return redirect("/viewsections" + name + "/")


class TAHome(View):
    def get(self, request):
        username = request.session["user"]
        ta = TA.objects.get(username=username)
        return render(request, "TA/TAHome.html", {"ta": ta})


class TAEdit(View):
    def get(self, request):
        ta = TA.objects.get(username=request.session["user"])
        return render(request, "TA/TAEdit.html", {"ta": ta})

    def post(self, request):
        ta = TA.objects.get(username=request.session["user"])
        edit_info(ta, request.POST['email'], request.POST['first_name'], request.POST['last_name'],
                  request.POST['office'], request.POST['phone'], request.POST['office_hours'])
        return render(request, "TA/TAEdit.html", {"ta": ta})


class TAViewCourses(View):
    def get(self, request):
        courses = Course.objects.filter(ta__username=request.session["user"])
        return render(request, "Courses.html", {"courses": courses})


class InstructorHome(View):
    def get(self, request):
        username = request.session["user"]
        instructor = Instructor.objects.get(username=username)
        return render(request, "Instructor/InstructorHome.html", {"username": username, "instructor": instructor})


class InstructorEditInfo(View):
    def get(self, request):
        username = request.session["user"]
        instructor = Instructor.objects.get(username=username)
        return render(request, "Instructor/InstructorEdit.html", {"instructor": instructor})

    def post(self, request):
        username = request.session["user"]
        instructor = Instructor.objects.get(username=username)
        edit_info(instructor, request.POST['email'], request.POST['first_name'], request.POST['last_name'],
                  request.POST['office'], request.POST['phone'], request.POST['office_hours'])

        return render(request, "Instructor/InstructorEdit.html", {"instructor": instructor})


class InstructorViewCourses(View):
    def get(self, request):
        username = request.session["user"]
        instructor = Instructor.objects.get(username=username)
        courses = list(Course.objects.filter(instructor=instructor))
        return render(request, "Instructor/InstructorViewCourses.html", {"courses": courses})


class InstructorViewTAs(View):
    def get(self, request, name):
        course = Course.objects.get(name=name)
        tas = list(TA.objects.filter(course=course))
        return render(request, "Instructor/InstructorViewTAs.html", {"tas": tas, "course": course})


class InstructorViewPolicies(View):
    def get(self, request):
        username = request.session["user"]
        instructor = Instructor.objects.get(username=username)
        policies = SyllabusPolicy.objects.filter(instructor=instructor)
        return render(request, "Instructor/InstructorViewPolicies.html", {
            "instructor": instructor,
            "policies": policies})

    def post(self, request):
        new_policy_text = request.POST['new_policy_text']
        SyllabusPolicy.objects.create(
            policy_text=new_policy_text,
            instructor=Instructor.objects.get(username=request.session["user"])
        )
        return redirect("/instructorviewpolicies/")


class Courses(View):
    def get(self, request):
        courses = list(Course.objects.all())
        return render(request, "Courses.html", {"courses": courses})


class ViewCourse(View):
    def get(self, request, term, dep_number):
        course = Course.objects.get(dep_number=dep_number)
        sections = list(Section.objects.filter(course=course))
        instructor = course.instructor
        tas = list(course.ta_set.all())
        policies = list(course.policies.all())
        return render(request, "ViewCourse.html", {"course": course, "sections": sections, "instructor": instructor,
                                                   "tas": tas, "policies": policies})



class InstructorAssignPolicy(View):
    def get(self, request, policy_primary_key):
        policy = SyllabusPolicy.objects.get(pk=policy_primary_key)
        assignable_courses = Course.objects\
            .filter(instructor=Instructor.objects.get(username=request.session["user"]))\
            .exclude(policies__in=[policy])
        return render(request, "InstructorAssignPolicy.html", {
            "policy": policy,
            "assignable_courses": assignable_courses
        })

    def post(self, request, policy_primary_key):
        course = Course.objects.get(pk=request.POST['course_pk'])
        policy = SyllabusPolicy.objects.get(pk=policy_primary_key)
        course.policies.add(policy)
        return redirect("/instructorviewpolicies/")


class InstructorRemovePolicy(View):
    def get(self, request, policy_primary_key):
        policy = SyllabusPolicy.objects.get(pk=policy_primary_key)
        removable_courses = Course.objects\
            .filter(instructor=Instructor.objects.get(username=request.session["user"])) \
            .filter(policies__in=[policy])
        print(removable_courses)
        return render(request, "InstructorRemovePolicy.html", {
            "policy": policy,
            "removable_courses": removable_courses
        })

    def post(self, request, policy_primary_key):
        course = Course.objects.get(pk=request.POST['course_pk'])
        policy = SyllabusPolicy.objects.get(pk=policy_primary_key)
        course.policies.remove(policy)
        return redirect("/instructorviewpolicies/")