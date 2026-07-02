from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list_ajax, name='student_list_ajax'),
    path('list/', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('create/', views.student_create, name='student_create'),
    path('<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('<int:pk>/documents/upload/', views.document_upload, name='document_upload'),
]
