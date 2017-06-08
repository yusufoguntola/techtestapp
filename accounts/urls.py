from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^logout$', views.logout_user, name='logout'),
]
