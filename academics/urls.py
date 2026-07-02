from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('years/', views.academic_year_list, name='academic_year_list'),
    path('years/create/', views.academic_year_create, name='academic_year_create'),
    path('years/<int:pk>/edit/', views.academic_year_edit, name='academic_year_edit'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:pk>/edit/', views.class_edit, name='class_edit'),
    path('sections/', views.section_list, name='section_list'),
    path('sections/create/', views.section_create, name='section_create'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
]
