from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "alumni"

urlpatterns = [
    path('alumni', views.AlumniHome, name="AlumniHome"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)