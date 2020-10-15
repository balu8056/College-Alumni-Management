from django.urls import path
from . import views

app_name = "direc"

urlpatterns = [
    path('', views.directorate, name="directorateDashboard"),

    path('sendemail', views.directorateemailsend, name="DirectoratesendmailtoAlumni"),

    path('college/edit', views.directorateEditCollege, name="DirectorateEditCollege"),

    path('college/edit/save', views.directoratecollegeEditAjax, name="DirectorateEditCollegeSave"),
]