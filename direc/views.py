from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
import json
from app1.models import alumniDatabase
from alumni.models import college

def directorate(request):
    if request.is_ajax() and request.method == "POST":
        collegeName = request.POST.get("college")
        dept = request.POST.get("dept")
        batch = request.POST.get("batch")
        if alumniDatabase.objects.filter(College=collegeName, Dept=dept, Batch=batch):
            a = alumniDatabase.objects.filter(College=collegeName, Dept=dept, Batch=batch)
            data = []
            for i in a:
                l = [i.Name, i.Regno, i.Email, i.PhoneNo]
                data.append(l)
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponse(json.dumps("no data"), content_type="application/json")
    else:
        alumni = alumniDatabase.objects.all()
        colleges = college.objects.all()
        return render(request, 'direc/directorate.html', {'Alumni': enumerate(alumni, 1), 'college': colleges})

def directorateEditCollege(request):
    colleges = college.objects.all()
    return render(request, 'direc/ManageCollegeByDirectorate.html', {'college': enumerate(colleges, 1)})

def directorateemailsend(request):
    if request.is_ajax() and request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        send_mail(subject=subject, message=message, from_email="<noreply@gmail.com>", recipient_list=[email, ], fail_silently=True)
        return HttpResponse(json.dumps("message sent"), content_type="application/json")
    else:
        return HttpResponse(json.dumps("Illegal email sent"), content_type="application/json")

def directoratecollegeEditAjax(request):
    if request.is_ajax() and request.method == "POST":
        college_name = request.POST.get("college_name")
        college_code = request.POST.get("college_code")
        college_departments = request.POST.get("college_departments")
        college_address = request.POST.get("college_address")
        college_contact_no = request.POST.get("college_contact_no")
        college_email = request.POST.get("college_email")
        if college.objects.filter(college_name=college_name, college_code=college_code):
            c = college.objects.get(college_name=college_name, college_code=college_code)
            c.college_departments = college_departments
            c.college_address = college_address
            c.college_contact_no = college_contact_no
            c.college_email = college_email
            c.save()
        else:
            return HttpResponse(json.dumps("edit not possible, try again later..."), content_type="application/json")
        print(college_name, college_code, college_departments, college_address, college_contact_no, college_email)
        return HttpResponse(json.dumps("data you edited are stored"), content_type="application/json")
    else:
        return HttpResponse(json.dumps("edit not possible, try again later..."), content_type="application/json")