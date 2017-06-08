from django.conf.urls import url

from student import views

urlpatterns = [
    url(r'^apply$', views.ApplicationView.as_view(), name='apply')
]