from random import randint
from django.contrib import messages
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.db.models import Q

from accounts.permissions import get_user_type, is_approved_student
from school.models import Course
from staff.models import Staff, StaffCourses
from student.models import Student, StudentApplication


def login_user(request):
    if request.get_full_path().__contains__('?next='):
        messages.warning(request,
                         'Authorization required to view the requested page. Please login with an authorized account.')
    elif request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account:dashboard'))
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        redirect_field_name = REDIRECT_FIELD_NAME
        redirect_to = request.POST.get(redirect_field_name,
                                       request.GET.get(redirect_field_name, ''))
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if str(redirect_to) != '':
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect(reverse('account:dashboard'))
            else:
                return HttpResponseRedirect(reverse('account:login'))
        else:
            messages.error(request, "Invalid username/password")
            return HttpResponseRedirect(reverse('account:login'))
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))


@login_required
def dashboard(request):
    user_type = get_user_type(request.user)
    if user_type == 'Admin':
        return render(request, 'school/index.html', admin_context())
    if user_type == 'Staff':
        return render(request, 'staff/dashboard.html', staff_context(request))
    if user_type == 'Student':
        if is_approved_student(request.user):
            return render(request, 'student/dashboard.html',
                          {'staffs': Staff.objects.all(), 'courses': Course.objects.all()})
        status = StudentApplication.objects.get(user=request.user).application_status
        return render(request, 'student/pending_students.html', {'status': status})
    return HttpResponseRedirect(reverse('account:login'))


def admin_context():
    context = {
        'staffs': Staff.objects.all(),
        'students': Student.objects.all(),
        'courses': Course.objects.all()
    }
    return context


def staff_context(request):
    context = {
        'staffs': Staff.objects.all(),
        'courses': Course.objects.all(),
        'students': Student.objects.all(),
        'pending_students': StudentApplication.objects.filter(application_status='PENDING'),
        'my_courses': request.user.staff.staffcourses.courses.all()
    }
    return context
