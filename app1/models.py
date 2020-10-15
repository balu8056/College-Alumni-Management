from django.db import models
from django.contrib.auth.models import User
import datetime
from alumni.models import college
#from django.dispatch import receiver
#from django.db.models.signals import post_delete

def college_list():
    col = [(str(i.college_name), str(i.college_name)) for i in college.objects.all()]
    return col

def user_profile_path(instance, filename):
    return f"profile/user_{instance.user.username}/{filename}"

class additionalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    regno = models.CharField(max_length=256)
    dob = models.CharField(max_length=15)
    listOFCollege = college_list()
    college = models.CharField(max_length=256, choices=listOFCollege)
    listOFDepts = [('Civil Engineering', 'Civil Engineering'), ('Mechanical Engineering', 'Mechanical Engineering'), ('Electronics and Communication Engineering', 'Electronics and Communication Engineering'), ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Metallurgical Engineering', 'Metallurgical Engineering')]
    dept = models.CharField(max_length=256, choices=listOFDepts)
    year = ((str(i) + "-" + str(i + 4), str(i) + "-" + str(i + 4)) for i in range(1970, datetime.datetime.now().year - 3))
    yoc = models.CharField(choices=year, max_length=10)
    profile = models.ImageField(default="Anonymous.png", upload_to=user_profile_path)
    isStudent = models.BooleanField(default=True)
    phone = models.CharField(max_length=10, default="None", blank=True)

    def __str__(self):
        return str(self.user) + "--" + str(self.regno)
"""
@receiver(post_delete, sender=additionalUser)
def submission_delete(sender, instance, **kwargs):
    instance.profile.delete(False)
"""
class alumniDatabase(models.Model):
    Name = models.CharField(max_length=256)
    Regno = models.CharField(max_length=256)
    Email = models.EmailField(max_length=256, blank=True, null=True)
    DOB = models.DateField(max_length=200, help_text="YYYY-MM-DD")

    listOfCollege = college_list()
    College = models.CharField(max_length=256, choices=listOfCollege)
    listOfDepts = [('Civil Engineering', 'Civil Engineering'), ('Mechanical Engineering', 'Mechanical Engineering'), ('Electronics and Communication Engineering', 'Electronics and Communication Engineering'), ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Metallurgical Engineering', 'Metallurgical Engineering')]
    Dept = models.CharField(max_length=200, choices=listOfDepts)
    year = ((str(i) + "-" + str(i + 4), str(i) + "-" + str(i + 4)) for i in range(1970, datetime.datetime.now().year - 3))
    Batch = models.CharField(choices=year, max_length=10)
    PhoneNo = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.Name) + "--" + str(self.College)