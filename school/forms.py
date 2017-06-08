from django import forms

from school.models import Course
from staff.models import StaffCourses


class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CourseAssignmentForm(forms.ModelForm):
    class Meta:
        model = StaffCourses
        fields = ('staff', 'courses')
        widgets = {
            'staff': forms.Select(attrs={'class': 'bs-select', 'data-live-search': 'true'}),
            'courses': forms.SelectMultiple(attrs={'class': 's2-select-search form-control'})
        }
