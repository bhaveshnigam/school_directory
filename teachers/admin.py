from django.contrib import admin

from teachers.models import Subject, Teacher


class TeacherModelAdmin(admin.ModelAdmin):
    filter_horizontal = ['subjects_taught']


admin.site.register(Subject)
admin.site.register(Teacher, TeacherModelAdmin)
