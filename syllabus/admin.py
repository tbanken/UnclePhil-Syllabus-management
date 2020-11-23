from django.contrib import admin
from syllabus.models import TA, Instructor

# Register your models here.


# class RegTA(admin.ModelAdmin):
#     fields = ['username']


admin.site.register(TA)
admin.site.register(Instructor)
