from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestClientLoginRegisterLogout(TestCase):
    """Test client login, register, logout."""

    valid_password = ']=_az&4qVDY2h9y'

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='test_user',
            password=cls.valid_password
        )

        # Define urls map
        cls.urls_reverse = {
            'home': reverse('home'),
            'register': reverse('register'),
            'login': reverse('login'),
            'logout': reverse('logout'),
            'upload_json': reverse('upload_json'),
            'profiles': reverse('profiles'),
            'visualize': reverse('visualize', args=[1]),
            'delete_profile': reverse('delete_profile', args=[1]),
        }

    def test_user_must_be_logged_in(self):
        """Test user must be logged in to access:
        - upload_json
        - profiles
        - visualize
        - delete_profile
        """

        # Urls that must be accessed only by logged-in user
        urls_login_required = [
            self.urls_reverse['upload_json'],
            self.urls_reverse['profiles'],
            self.urls_reverse['visualize'],
            self.urls_reverse['delete_profile'],
        ]

        for url in urls_login_required:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'{self.urls_reverse["login"]}?next={url}')

    def test_user_logged_in_after_registration(self):
        """Test user logged in after registration."""
        response = self.client.post(self.urls_reverse['register'], {
            'username': 'new_user',
            'password1': self.valid_password,
            'password2': self.valid_password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls_reverse['home'])

        # Check if user is logged in
        response = self.client.get(self.urls_reverse['home'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'new_user')

    def test_user_logged_in_after_login(self):
        """Test user logged in after login."""
        response = self.client.post(self.urls_reverse['login'], {
            'username': self.user.username,
            'password': self.valid_password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls_reverse['upload_json'])

        # Check if user is logged in
        response = self.client.get(self.urls_reverse['home'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_user_logged_out_after_logout(self):
        """Test user logged out after logout."""
        self.client.login(username=self.user.username, password=self.valid_password)
        response = self.client.get(self.urls_reverse['logout'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls_reverse['login'])

        # Check if user is logged out
        response = self.client.get(self.urls_reverse['home'])
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user.username)
