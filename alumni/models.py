from django.db import models
from django.contrib.auth.models import User

class college(models.Model):
    college_name = models.CharField(max_length=256)
    college_code = models.CharField(max_length=100)
    college_departments = models.TextField(max_length=1000000, help_text="dept's must be separated by commas.")
    college_address = models.TextField(max_length=10000)
    college_contact_no = models.CharField(max_length=256)
    college_email = models.CharField(max_length=256)
    chat_room_name = models.CharField(max_length=256)

    def __str__(self):
        return str(self.college_name)

class chat_room_messages(models.Model):
    chat_room_name = models.OneToOneField(college, on_delete=models.CASCADE)
    M1 = models.TextField(null=True, blank=True)
    M2 = models.TextField(null=True, blank=True)
    M3 = models.TextField(null=True, blank=True)
    M4 = models.TextField(null=True, blank=True)
    M5 = models.TextField(null=True, blank=True)
    M6 = models.TextField(null=True, blank=True)
    M7 = models.TextField(null=True, blank=True)
    M8 = models.TextField(null=True, blank=True)
    M9 = models.TextField(null=True, blank=True)
    M10 = models.TextField(null=True, blank=True)


    def __str__(self):
        return "Messages == " + str(self.chat_room_name)