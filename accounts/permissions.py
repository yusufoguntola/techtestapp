from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from accounts.models import PermissionTable
from student.models import Student


def add_permissions():
    c_type = ContentType.objects.get_for_model(PermissionTable)
    try:
        Permission.objects.get(codename='c_staff')
    except:
        Permission.objects.create(codename='c_staff', name='Staff', content_type=c_type)
    try:
        Permission.objects.get(codename='c_student')
    except:
        Permission.objects.create(codename='c_student', name='Student', content_type=c_type)


try:
    content_type = ContentType.objects.get_for_model(PermissionTable)
    add_permissions()
except:
    pass


def get_user_type(user):
    if user.is_superuser:
        return "Admin"
    if user.has_perm('accounts.c_staff'):
        return "Staff"
    if user.has_perm('accounts.c_student'):
        return "Student"
    return "Admin"


def is_staff(user):
    return get_user_type(user) == 'Staff'


def is_student(user):
    return get_user_type(user) == 'Student'


def is_approved_student(user):
    return Student.objects.filter(user=user).exists()


def is_admin(user):
    return get_user_type(user) == 'Admin'
