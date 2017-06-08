from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import CreateView

from student.forms import StudentRegistrationForm
from student.models import StudentApplication


class ApplicationView(CreateView):
    model = StudentApplication
    form_class = StudentRegistrationForm
    template_name = 'student/application.html'

    def get_success_url(self):
        messages.success(self.request, 'Student registered successfully')
        return reverse('account:dashboard')
