from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('structure/', views.fee_structure_list, name='fee_structure_list'),
    path('structure/create/', views.fee_structure_create, name='fee_structure_create'),
    path('structure/<int:pk>/edit/', views.fee_structure_edit, name='fee_structure_edit'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
    path('payments/<int:pk>/receipt/', views.payment_receipt, name='payment_receipt'),
    path('summary/', views.fee_summary, name='fee_summary'),
]
