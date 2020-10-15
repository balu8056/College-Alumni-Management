from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'app1'

urlpatterns = [
    path('', views.Home, name="HomePage"),

    path('user/login', views.UserLogin, name="UserLogin"),

    path('student/register', views.StudentRegister, name="StudentRegister"),
    path('student/activate/<uidb64>/<token>', views.activatingStudentAccount, name="ActivatingStudentAccount"),

    path('userlogout', views.UserLogout, name="StudentLogout"),

    path('user/forgetpassword', views.UserForgetPassword, name="UserForgetPassword"),
    path('user/forgetpassword/<uidb64>/<token>', views.SetPasswordAfterUserForgetPassword, name="SetPasswordAfterUserForgetPassword"),

    path('oncollegechange', views.onCollegeChangeInRegisterForm, name="OnCollegeChange")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
