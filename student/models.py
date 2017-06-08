from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from school.models import Course
from staff.models import Staff


class Student(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='student/photo/')
    date_approved = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(Staff)

    def __str__(self):
        return self.user.username


class StudentApplication(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='student/photo/')
    date_applied = models.DateTimeField(auto_now_add=True)
    application_status = models.CharField(max_length=30, choices=(
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('DECLINED', 'DECLINED'),
    ), default='PENDING')

    def __str__(self):
        return self.user.username


class CourseReg(models.Model):
    student = models.OneToOneField(Student)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return str(self.student)
