from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from school.models import Course


class Staff(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='staff/photo/')
    designation = models.CharField(max_length=20)
    date_employed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class StaffCourses(models.Model):
    staff = models.OneToOneField(Staff)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return str(self.staff)
