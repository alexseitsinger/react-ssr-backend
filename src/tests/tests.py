from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User, AnonymousUser

from .backend import views


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test", email="test@example.org", password="test"
        )

    def test_index_page_view(self):
        request = self.factory.get("/")
        request.user = self.user
        view = views.IndexPageView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
