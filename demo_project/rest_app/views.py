from django.shortcuts import render
from django.views import generic as views
from rest_framework import generics as rest_views
from rest_framework import serializers
from demo_project.rest_app.models import Department, Employee

# Create your views here.

# Naming convention:
# When creating a serializer, start the name with Short if class is used
# to only extend the JSON
class ShortDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    # This will add the JSON info about the department data
    # The attribute should be called the same as the foreign key (without the _id)
    # many=True tells Django to expect a list of items
    department  = ShortDepartmentSerializer(""" many=True """)
    
    class Meta:
        model = Employee    
        fields = "__all__"
        
    def create(self, validated_data):
        # This will det the name of the department upon adding data to the JSON data
        department_name = validated_data.pop('department').get('name')
        
        # this tries to find the department by name
        # it the department does not exist, it will be created
        try:
            department = Department.objects.get(name=department_name).get()
        
        except Department.DoesNotExist:
            department = Department.objects.create(name=department_name,)
        
        return Employee.objects.create(**validated_data, department=department)

        
# Class view
# result is rendered HTML
class EmployeesListView(views.ListView):
    model = Employee
    template_name = ""


""" 
API Class Views
ListAPIViews       - lists the API data
ListCreateAPIView  - lists and can add to the API data
"""


# API class view
# parses model into JSON
class EmployeesListApiView(rest_views.ListCreateAPIView):
    queryset = Employee.objects.all()
    # This is what tells what and how to parse to JSON
    serializer_class = EmployeeSerializer
    
    # This method lets when you type http://127.0.0.1:8000/api/employees/?department_id=1 to get all objects that
    # contain only department_id 1
    def get_queryset(self):
        department_id = self.request.query_params.get('department_id')
        queryset = self.queryset
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        return queryset.all()
        


""" 
Generic API Class views
imported from rest_framework.generics
"""