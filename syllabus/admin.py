from django.contrib import admin
from .models import *

admin.site.register(Instructor)
admin.site.register(TA)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(SyllabusPolicy)
