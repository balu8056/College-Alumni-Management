import json
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import additionalUser, alumniDatabase
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .form import PasswordSet, UserPasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm
from alumni.models import college

class TokenForAlumniReg(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return user.pk + timestamp + user.is_active
generateTokenReg = TokenForAlumniReg()

class TokenForAlumniForgetpassword(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return user.pk + timestamp + user.is_active
generateTokenForgetpassword = TokenForAlumniForgetpassword()

directorateOfGce = User.objects.get(username="directorate@gce.salem")
gceSalem = User.objects.get(username="gcesalem")

def Home(request):
    c = college.objects.all()
    return render(request, 'app1/Home.html', {'colleges': c, 'directorateOfGce': directorateOfGce, 'gceSalem': gceSalem})

def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("userpassword")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            u1 = User.objects.get(username=user)
            a1 = None
            try:
                a1 = additionalUser.objects.get(user=u1)
            except:
                pass
            login(request, user=user)
            if a1 is not None:
                if a1.isStudent:
                    return redirect('alumni:AlumniHome')
            elif u1.is_superuser and u1.is_staff:
                return redirect('admin:index')
            elif u1 is not None and a1 is None:
                if u1 == directorateOfGce:
                    return redirect('direc:directorateDashboard')
                elif u1 == gceSalem:
                    return redirect('college:CollegeHome')
        else:
            messages.warning(request, "User not Found")
            return redirect("app1:HomePage")
    return redirect("app1:HomePage")

def StudentRegister(request):
    if request.method == "POST" and request.FILES['regpro']:
        name = request.POST.get("regname")
        regno = request.POST.get("regregno")
        email = request.POST.get("regemail")
        dob = request.POST.get("regdob")
        dept = request.POST.get("regdept")
        col = request.POST.get("regcol")
        yoc = request.POST.get("regyoc")
        profile = request.FILES["regpro"]
        phone = request.POST.get('regphone')
        if User.objects.filter(email=email):
            if User.objects.filter(username=email, email=email, first_name=name) and additionalUser.objects.filter(regno=regno, dob=dob, dept=dept, college=col, yoc=yoc):
                user = User.objects.get(username=email)
                if not user.is_active:
                    token = generateTokenReg.make_token(user=user)
                    link = get_current_site(request).domain + '/' + 'student' + '/' + "activate" + '/' + urlsafe_base64_encode(force_bytes(user.pk)) + '/' + token
                    linked = render_to_string('app1/EmailSending.html', context={'user': user, 'link': link, })
                    send_mail(subject="projectx", message="link to activate your account", html_message=linked, from_email="<noreply@gmail.com>", recipient_list=[email, ], fail_silently=True)
                    messages.warning(request, "you didn't set your password check your email")
                    return redirect("app1:HomePage")
                else:
                    messages.warning(request, "Already registered!!!")
                    return redirect("app1:HomePage")
            else:
                messages.warning(request, "Email already registered")
                return redirect("app1:HomePage")
        elif additionalUser.objects.filter(regno=regno):
            if User.objects.filter(username=email, email=email, first_name=name) and additionalUser.objects.filter(regno=regno, dob=dob, dept=dept, college=col, yoc=yoc):
                user = User.objects.get(username=email)
                if not user.is_active:
                    token = generateTokenReg.make_token(user=user)
                    link = get_current_site(request).domain + '/' + 'student' + '/' + "activate" + '/' + urlsafe_base64_encode(force_bytes(user.pk)) + '/' + token
                    linked = render_to_string('app1/EmailSending.html', context={'user': user, 'link': link, })
                    send_mail(subject="projectx", message="link to activate your account", html_message=linked, from_email="<noreply@gmail.com>", recipient_list=[email, ], fail_silently=True)
                    messages.warning(request, "you didn't set password check your email")
                    return redirect("app1:HomePage")
                else:
                    messages.warning(request, "Already registered!!!")
                    return redirect("app1:HomePage")
            else:
                messages.warning(request, "Register number already registered")
                return redirect("app1:HomePage")
        elif alumniDatabase.objects.filter(Regno=regno, DOB=dob, Dept=dept, Batch=yoc):
            student_register = User.objects.create_user(username=email, email=email, first_name=name)
            student_register.is_active = False
            student_register.save()
            additional_info = additionalUser(user=student_register, regno=regno, dob=dob, dept=dept, yoc=yoc, college=col, profile=profile, phone=phone)
            additional_info.save()
            alumni = alumniDatabase.objects.get(Regno__iexact=regno, College=col)
            alumni.Email = email
            alumni.PhoneNo = phone
            alumni.save()
            token = generateTokenReg.make_token(user=student_register)
            link = get_current_site(request).domain + '/' + 'student' + '/' + "activate" + '/' + urlsafe_base64_encode(force_bytes(student_register.pk)) + '/' + token
            linked = render_to_string('app1/EmailSending.html', context={'user': student_register, 'link': link, })
            send_mail(subject="projectx", message="link to activate your account", html_message=linked, from_email="<noreply@gmail.com>", recipient_list=[email, ], fail_silently=True)
            messages.warning(request, "check your email and confirm your account")
            return redirect("app1:HomePage")
        else:
            messages.warning(request, "your authentication with college database is rejected")
            return redirect("app1:HomePage")
    else:
        return render(request, 'app1/HomePage.html')

def activatingStudentAccount(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if request.method == "POST":
        passs = request.POST.get('new_password2')
        user.set_password(passs)
        user.is_active = True
        user.save()
        update_session_auth_hash(request, user=user)
        messages.warning(request, "successfully registered")
        return redirect("app1:HomePage")
    else:
        if user is not None and generateTokenReg.check_token(user, token):
            form = PasswordSet(user=user)
            return render(request, 'app1/PasswordSetAfterConfirmEmail.html', {'form': form, 'user': user, 'heading': 'Confirm Password', 'title': 'confirm password | Alumni Tracking System'})
        else:
            messages.warning(request, 'link is not valid')
            return redirect('app1:HomePage')

def UserLogout(request):
    logout(request)
    return redirect("app1:HomePage")

def UserForgetPassword(request):
    if request.method == "POST":
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email__iexact=email):
                user = User.objects.get(email__iexact=email)
                link = get_current_site(request).domain + '/' + 'user' + '/' + 'forgetpassword' + '/' + urlsafe_base64_encode(force_bytes(user.pk)) + '/' + generateTokenForgetpassword.make_token(user=user)
                mes = render_to_string('app1/EmailSending.html', context={'link': link, })
                send_mail(subject="New", message="link to change password", html_message=mes, from_email='<noreply@gmail.com>', recipient_list=[email, ], fail_silently=True)
                messages.info(request, 'Check your email and click the link to activate your account')
                return redirect("app1:HomePage")
            else:
                messages.warning(request, 'email not found')
                return redirect("app1:UserForgetPassword")
    else:
        form = UserPasswordResetForm()
        return render(request, 'app1/PasswordSetAfterConfirmEmail.html', {'form': form, 'heading': 'Password reset form', 'title': 'Password reset form | Alumni Tracking System'})

def SetPasswordAfterUserForgetPassword(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(user)
    if request.method == "POST":
            passs = request.POST.get("new_password2")
            user.set_password(passs)
            user.save()
            update_session_auth_hash(request, user=user)
            messages.warning(request, "successfully registered")
            return redirect("app1:HomePage")
    else:
        if user is not None and generateTokenReg.check_token(user, token):
            return render(request, 'app1/SetPassword.html', {'user': user, 'heading': 'Confirm Password', 'title': 'confirm password | Alumni Tracking System'})
        else:
            messages.warning(request, 'link is not valid')
            return redirect('app1:HomePage')

def onCollegeChangeInRegisterForm(request):
    if request.is_ajax() and request.method == "POST":
        collegeFromRegister = request.POST['college']
        depts = ""
        try:
            if college.objects.filter(college_name=collegeFromRegister):
                depts = college.objects.get(college_name=collegeFromRegister).college_departments
        except Exception as e:
            return HttpResponse(json.dumps(str(e)), content_type="application/json")
        return HttpResponse(json.dumps(depts), content_type="application/json")
    else:
        print("no")
        return HttpResponse(json.dumps("no"), content_type="application/json")