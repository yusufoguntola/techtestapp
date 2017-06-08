from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from accounts import permissions
from staff.forms import RegistrationForm
from staff.models import Staff
from student.models import StudentApplication, Student


@method_decorator(login_required, name='dispatch')
class StaffRegView(CreateView):
    model = Staff
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'

    def get_success_url(self):
        messages.success(self.request, 'Staff registered successfully')
        return reverse('account:dashboard')


@login_required
@user_passes_test(permissions.is_staff)
def pending_students_view(request):
    pending_students = StudentApplication.objects.filter(application_status='PENDING')
    if request.method == 'POST':
        student_id = request.POST.get('student')
        action = request.POST.get('action')
        if student_id and action:
            student = StudentApplication.objects.get(pk=int(student_id))
            student.application_status = action
            student.save()
            if action == 'APPROVED':
                Student.objects.create(user=student.user, mobile=student.mobile, pic=student.pic,
                                       approved_by=request.user.staff)
            messages.success(request, "%s's application has been %s" % (student.user.get_full_name(), action))
            return HttpResponseRedirect(reverse('staff:pending-students'))
        messages.error(request, 'Something went wrong')
    return render(request, 'staff/pending-students.html', {'pending_students': pending_students})
