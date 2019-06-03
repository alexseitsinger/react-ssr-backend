from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User, AnonymousUser

from .backend import views


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test", email="test@example.org", password="test")

    def test_default_state_view(self):
        request = self.factory.get("/default_state/")
        view = views.DefaultStateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_auth_state_view(self):
        request = self.factory.get("/auth_state/")
        request.user = self.user
        view = views.AuthStateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_secret_key_view(self):
        request = self.factory.get("/secret_key/")
        view = views.SecretKeyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_agent_view(self):
        request = self.factory.get("/user_agent/")
        view = views.UserAgentView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)



