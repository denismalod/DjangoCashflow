from django.urls import path
from . import views

urlpatterns = [
    path('', views.records_list, name='records_list'),
    path('add/', views.record_add, name='record_add'),
    path('edit/<int:pk>/', views.record_edit, name='record_edit'),
    path('api/subcategories/', views.get_subcategories, name='get_subcategories'),
]
