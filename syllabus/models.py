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
    office_hours = models.CharField(max_length=20)

    class Meta:
        verbose_name = "TA"
        verbose_name_plural = "TAs"


class Instructor(MyUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    office = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    office_hours = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"


class Course(models.Model):
    name = models.CharField(max_length=20)
    term = models.CharField(max_length=20)
    dep_number = models.CharField(max_length=20)
    instructor = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING)
    #TODO ta needs to be ManyToMany(need multiple TAs in one course)
    ta = models.ForeignKey(TA, on_delete=models.DO_NOTHING)


class Section(models.Model):
    type_of = models.CharField(max_length=20)
    number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta = models.OneToOneField(TA, on_delete=models.DO_NOTHING)
    instructor = models.OneToOneField(Instructor, on_delete=models.DO_NOTHING)
