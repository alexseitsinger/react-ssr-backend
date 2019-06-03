from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^default_state/?$", views.DefaultStateView.as_view(), name="default_state"),
    url(r"^auth_state/?$", views.AuthStateView.as_view(), name="auth_state"),
    url(r"^secret_key/?$", views.SecretKeyView.as_view(), name="secret_key"),
    url(r"^user_agent/?$", views.UserAgentView.as_view(), name="user_agent"),
]
