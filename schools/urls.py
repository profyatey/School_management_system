from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("students/", views.students_list, name="students_list"),
    path("teachers/", views.teachers_list, name="teachers_list"), 
    path("teachers/add/", views.add_teacher, name="add_teacher"), 
    path("teachers/<int:pk>/edit/", views.edit_teacher, name="edit_teacher"), 
    path("teachers/<int:pk>/delete/", views.delete_teacher, name="delete_teacher"),
    path("import-students/", views.import_students, name="import_students"),
]
