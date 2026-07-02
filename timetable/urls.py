from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.timetable_list, name='timetable_list'),
    path('slot/create/', views.slot_create, name='slot_create'),
    path('slot/<int:pk>/edit/', views.slot_edit, name='slot_edit'),
    path('slot/<int:pk>/delete/', views.slot_delete, name='slot_delete'),
    path('teacher/', views.teacher_timetable, name='teacher_timetable'),
]
