from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class MyUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)


    def __str__(self):
        return self.username


class Admin(MyUser):
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"


class TA(MyUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    office = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    officeHours = models.CharField(max_length=20)
    class Meta:
        verbose_name = "TA"
        verbose_name_plural = "TAs"


class Instructor(MyUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    office = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    officeHours = models.CharField(max_length=20)
    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"


# class Syllabus(models.Model):
#     pass
#
#
# class Course(models.Model):
#     name = models.CharField(max_length=20)
#     number = models.IntegerField()
#     # not sure on the instructor and TA
#     instructors = models.ForeignKey(Instructor)
#     tas = models.ForeignKey(TA)
#     syllabus = models.ForeignKey(Syllabus)
#
#
# class Section(models.Model):
#     TypeOf = models.CharField(max_length=20)
#     number = models.IntegerField()
#     course = models.ForeignKey(Course)
