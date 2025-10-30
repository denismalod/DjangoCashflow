from django.urls import path
from . import views

urlpatterns = [
    path("", views.records_list, name="records_list"),
    path("add/", views.record_add, name="record_add"),
    path("edit/<int:pk>/", views.record_edit, name="record_edit"),
    path("delete/<int:pk>/", views.record_delete, name="record_delete"),
    path("api/subcategories/", views.get_subcategories, name="get_subcategories"),
    path("reference/", views.reference_manage, name="reference_manage"),
    path("delete/status/<int:pk>/", views.delete_status, name="delete_status"),
    path("delete/type/<int:pk>/", views.delete_type, name="delete_type"),
    path("delete/category/<int:pk>/", views.delete_category, name="delete_category"),
    path(
        "delete/subcategory/<int:pk>/",
        views.delete_subcategory,
        name="delete_subcategory",
    ),
]
