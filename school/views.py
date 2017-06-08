from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import CreateView

from school.forms import CourseRegistrationForm, CourseAssignmentForm
from school.models import Course
from staff.models import StaffCourses, Staff


class CourseRegView(CreateView):
    model = Course
    form_class = CourseRegistrationForm
    template_name = 'school/course-reg.html'

    def get_context_data(self, **kwargs):
        context = super(CourseRegView, self).get_context_data()
        context['courses'] = Course.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, 'Course registered successfully')
        return reverse('school:course-reg')


class CourseAssignmentView(CreateView):
    model = StaffCourses
    form_class = CourseAssignmentForm
    template_name = 'school/assign-course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseAssignmentView, self).get_context_data()
        context['assignments'] = StaffCourses.objects.all()
        return context

    def get_success_url(self):
        messages.success(self.request, 'Courses successfully assigned to the selected staff')
        return reverse('school:assign-course')
