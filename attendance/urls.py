from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('take/', views.attendance_take, name='attendance_take'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('export/', views.attendance_export, name='attendance_export'),
]
