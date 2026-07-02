from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('create/', views.exam_create, name='exam_create'),
    path('<int:pk>/', views.exam_detail, name='exam_detail'),
    path('<int:pk>/edit/', views.exam_edit, name='exam_edit'),
    path('<int:pk>/delete/', views.exam_delete, name='exam_delete'),
    path('<int:pk>/add-subject/', views.exam_subject_add, name='exam_subject_add'),
    path('class-results/<int:class_id>/<int:exam_id>/', views.class_results, name='class_results'),
    path('marks/<int:exam_subject_id>/', views.marks_entry, name='marks_entry'),
    path('marks/<int:exam_subject_id>/results/', views.marks_list, name='marks_list'),
    path('marks/<int:exam_subject_id>/export/', views.marks_export, name='marks_export'),
    path('marks/<int:exam_subject_id>/import/', views.marks_import, name='marks_import'),
    path('marks/edit/<int:pk>/', views.mark_edit, name='mark_edit'),
    path('marks/delete/<int:pk>/', views.mark_delete, name='mark_delete'),
    path('report-card/<int:student_id>/<int:exam_id>/', views.report_card, name='report_card'),
    path('report-card/<int:student_id>/<int:exam_id>/pdf/', views.report_card_pdf, name='report_card_pdf'),
]
