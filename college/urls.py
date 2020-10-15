from django.urls import path
from . import views

app_name = "college"

urlpatterns = [
    path('', views.collegeHome, name="CollegeHome"),
    path("collectAlumni", views.addAlumni, name="AddAlumni"),
    path("editAlumni", views.editAlumni, name="EditAlumni"),
    path("deleteAlumni", views.deleteAlumni, name="DeleteAlumni"),
]