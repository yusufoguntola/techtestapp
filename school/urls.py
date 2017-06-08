from django.conf.urls import url

from school import views

urlpatterns = [
    url(r'^course/create$', views.CourseRegView.as_view(), name='course-reg'),
    url(r'^course/assign-course$', views.CourseAssignmentView.as_view(), name='assign-course'),
]
