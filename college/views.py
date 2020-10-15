from django.shortcuts import render, redirect
from django.http import HttpResponse
from app1.models import alumniDatabase, college_list
from alumni.models import college
import openpyxl
import json
from django.contrib import messages
import datetime

# Create your views here.
def addAlumni(request):
    if request.is_ajax() and request.method == "POST":
        alumni = json.loads(request.POST.get("alumni"))
        try:
            alumniDatabase(Name=alumni['name'], Regno=alumni['regno'], Email=alumni['email'], DOB=alumni['date'], College=alumni['college'], Dept=alumni['dept'], Batch=alumni['batch-end'], PhoneNo=alumni['phone']).save()
        except Exception as e:
            print(str(e))
            return HttpResponse(json.dumps("error in upload"), content_type="application/json")
        return HttpResponse(json.dumps("success"), content_type="application/json")
    else:
        return HttpResponse(json.dumps("error in ajax"), content_type="application/json")
def collegeHome(request):
    if request.method == "POST" and request.FILES['excel']:
        excel = request.FILES['excel']
        w_s = openpyxl.load_workbook(excel)
        work = w_s["Sheet1"]
        test = []

        #validating
        college_name = []
        for i in college.objects.all():
            college_name.append(i.college_name)
        BATCH = []
        for i in range(1970, int(datetime.datetime.now().year) - 3):
            BATCH.append(str(i)+"-"+str(i+4))
        validate_or_not = False
        try:
            for index, rows in enumerate(work.iter_rows(), start=1):
                temp = []
                for cell in rows:
                    temp.append(str(cell.value))
                if index > 1:
                    if temp[4] not in college_name:
                        messages.warning(request, "college should be in "+ str(college_name))
                        return redirect('college:CollegeHome')
                    elif temp[5] not in ["Civil Engineering", "Mechanical Engineering", "Electronics and Communication Engineering", "Electrical and Electronics Engineering", "Computer Science and Engineering", "Metallurgical Engineering"]:
                        messages.warning(request, 'college should be in ["Civil Engineering", "Mechanical Engineering", "Electronics and Communication Engineering", "Electrical and Electronics Engineering", "Computer Science and Engineering", "Metallurgical Engineering"]')
                        return redirect('college:CollegeHome')
                    elif temp[6] not in BATCH:
                        messages.warning(request, f"Batch should be in {BATCH}")
                        return redirect('college:CollegeHome')
                    test.append(temp)
        except Exception as e:
            print(str(e))
        finally:
            validate_or_not = True
        print("valid", validate_or_not)

        # upload alumni data using excel
        if validate_or_not:
            for temp in test:
                try:
                    DOB = temp[3].replace('00:00:00', '').strip()
                    if alumniDatabase.objects.filter(Name=temp[0], Regno=temp[1], Email=temp[2], DOB=DOB, College=temp[4], Dept=temp[5], Batch=temp[6], PhoneNo=temp[7]):
                        pass
                    else:
                        alumniDatabase(Name=temp[0], Regno=temp[1], Email=temp[2], DOB=DOB, College=temp[4], Dept=temp[5], Batch=temp[6], PhoneNo=temp[7]).save()
                except Exception as e:
                    messages.warning(request, f"failed to upload {e}")
                    return redirect('college:CollegeHome')
            messages.warning(request, "successfully uploaded")
            return redirect('college:CollegeHome')
        else:
            messages.warning(request, "try again to upload")
            return redirect('college:CollegeHome')
    else:
        alumni = alumniDatabase.objects.all()
        colleges = college.objects.all()
        return render(request, 'college/CollegeHome.html', {"colleges": college.objects.all(), 'Alumni': enumerate(alumni, 1), 'college': colleges})

def editAlumni(request):
    if request.is_ajax() and request.method == "POST":
        needEdit = json.loads(request.POST.get("edit"))
        print(type(needEdit))
        print(needEdit)
        try:
            edit = alumniDatabase.objects.get(pk=needEdit['primary_key'])
            edit.Name = needEdit['name']
            edit.Regno = needEdit['regno']
            edit.Email = needEdit['email']
            edit.DOB = needEdit['date']
            edit.College = needEdit['college']
            edit.Dept = needEdit['dept']
            edit.Batch = needEdit['batch-end']
            edit.PhoneNo = needEdit['phone']
            edit.save()
            return HttpResponse(json.dumps("successfully uploaded"), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps('error'+str(e)), content_type="application/json")
    return HttpResponse(json.dumps("error in ajax"), content_type="application/json")

def deleteAlumni(request):
    if request.is_ajax() and request.method == "POST":
        deleteAlumniPk = request.POST.get("primary_key")
        try:
            alumniDatabase.objects.get(pk=int(deleteAlumniPk)).delete()
            return HttpResponse(json.dumps("alumni deleted"), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps("error in deleting alumni"), content_type="application/json")