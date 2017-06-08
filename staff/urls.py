from django.conf.urls import url

from staff import views

urlpatterns = [
    url(r'^register$', views.StaffRegView.as_view(), name='register'),
    url(r'^pending-students$', views.pending_students_view, name='pending-students'),
]