from django.urls import path
from . import views

urlpatterns = [
    path('', views.records_list, name='records_list'),
    path('record/add/', views.record_form, name='record_add'),
    path('record/<int:pk>/edit/', views.record_form, name='record_edit'),
]
