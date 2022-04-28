from django.contrib import admin
from .models import Course,Section,Enrollment, User

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Section)

admin.site.register(Enrollment)

