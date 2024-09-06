from django.test import TestCase
from django.urls import reverse
from users.models import User

# Create your tests here.


class TestUserLogin(TestCase):
    def setUp(self) -> None:
        self.login_url = reverse("users:login")
        User.objects.create_user(email="email1", password="pass")  # type: ignore

    def test_user_login_happy_path(self):
        # given
        # when
        resp = self.client.post(
            self.login_url, {"username": "email1", "password": "pass"}
        )
        # then
        self.assertTrue(resp.wsgi_request.user.is_authenticated)

    def test_user_login_fails_on_incorrect_pass(self):
        # given
        # when
        resp = self.client.post(
            self.login_url, {"username": "email1", "password": "wrong"}
        )
        # then
        self.assertFalse(resp.wsgi_request.user.is_authenticated)


class TestUserRegister(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse("users:register")

    def test_user_register_happy_path(self):
        # given
        # when
        resp = self.client.post(
            self.register_url,
            {
                "email": "user1@user.com",
                "password1": "ComplexPassword!23",
                "password2": "ComplexPassword!23",
            },
        )
        # then
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_fails_on_username_taken(self):
        # given
        User.objects.create_user(email="user1@user.com", password="pass")
        # when
        resp = self.client.post(
            self.register_url,
            {
                "email": "user1@user.com",
                "password1": "ComplexPassword!23",
                "password2": "ComplexPassword!23",
            },
        )
        # then
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.count(), 1)


class TestUserLogout(TestCase):
    def setUp(self) -> None:
        self.logout_url = reverse("users:logout")
        user1 = User.objects.create(email="user1@user.com")
        self.client.force_login(user1)

    def test_user_logout_happy_path(self):
        # given
        # when
        resp = self.client.post(self.logout_url)
        # then
        self.assertFalse(resp.wsgi_request.user.is_authenticated)
        self.assertEqual(resp.status_code, 302)
