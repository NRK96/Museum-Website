from django.test import TestCase
from django.urls import resolve


class UserURLSTestCase(TestCase):

    def test_user_login_page_exists(self):
        response = resolve('accounts/login/')
        self.assertEqual(response.status_code, 200)