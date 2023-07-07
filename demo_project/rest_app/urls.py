from django.urls import path, include
from . import views
urlpatterns = (
    path('employees/', views.EmployeesListApiView.as_view(), name='api_list_employees'),
)