from django.conf.urls import url

from . import views

urlpatterns = [url("^$", views.IndexPageView.as_view(), name="index")]
