from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import CustomUser

User = get_user_model()


class DashboardViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('dashboard')
        self.user = User.objects.create_user(
            username='author', password='password123', role='AUTHOR'
        )
        self.redactor = User.objects.create_user(
            username='red', password='password123', role=CustomUser.REDACTOR
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/users/login/?next=' + self.url)

    def test_redirect_for_redactor(self):
        self.client.login(username='red', password='password123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('my_bids'))

    def test_dashboard_loads_for_author(self):
        self.client.login(username='author', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_post_invalid_forms_returns_form(self):
        self.client.login(username='author', password='password123')
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This field is required.')
