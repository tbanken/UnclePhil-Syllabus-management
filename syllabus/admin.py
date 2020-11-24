from django.contrib import admin
from .models import TA, Admin, Instructor

admin.site.register(Instructor)
admin.site.register(TA)
admin.site.register(Admin)
