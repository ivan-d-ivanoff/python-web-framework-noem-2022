from django.contrib import admin

from demo_project.rest_app.models import Department, Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'salary', 'department')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display= ('name',)