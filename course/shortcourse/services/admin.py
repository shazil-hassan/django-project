from django.contrib import admin
from .models import Course,Section,Enrollment, User,Review, Service, User, FAQ, Category, Project, Assignment

# Register your models here.
admin.site.register(User)

admin.site.register(Category)
admin.site.register(Assignment)
admin.site.register(Service)
admin.site.register(Enrollment)
admin.site.register(Review)

admin.site.register(Section)
admin.site.register(FAQ)

class CourseAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):  # have to wrk on it
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["instructors"].queryset = User.objects.filter(is_staff = True)
        return form

admin.site.register(Course, CourseAdmin)
admin.site.register(Project)


admin.site.site_header = "HiveSol Technologies"
admin.site.site_title = "HiveSol Technologies"
admin.site.index_title = "Welcome to HiveSol Technologies Portal"
