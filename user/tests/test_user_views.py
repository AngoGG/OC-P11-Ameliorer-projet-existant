from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.test import Client, TestCase
from user.models import User


class TestRegistrationView(TestCase):
    def test_register_post(self) -> None:
        """Test if the url returns a correct 302 http status code
        and test if a user is correctly created.
        """
        client: Client = Client()
        response: HttpResponse = client.post(
            "/user/register",
            {
                "email": "user-name@gmail.com",
                "first_name": "user",
                "last_name": "name",
                "password1": "password8chars",
                "password2": "password8chars",
                "submit": "Register",
            },
        )
        assert response.status_code == 302  # Testing redirection
        user_created: QuerySet = User.objects.first()  # type: ignore
        self.assertEqual("user-name@gmail.com", user_created.email)
        self.assertTrue(user_created.check_password("password8chars"))
        self.assertEqual("user", user_created.first_name)
        self.assertEqual("name", user_created.last_name)

    def test_register_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        client: Client = Client()
        response: HttpResponse = client.get("/user/register")
        assert response.status_code == 200  # Testing redirection


class TestLoginView(TestCase):
    def test_login_success(self) -> None:
        """Test if the url returns a correct 302 http status code 
        when a user success to connect.
        """
        User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        client: Client = Client()
        response: HttpResponse = client.post(
            "/user/login",
            {"username": ["test@mail.com"], "password": ["password8chars"],},
        )
        assert response.status_code == 302  # Testing redirection

    def test_login_fail(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        client: Client = Client()
        response: HttpResponse = client.post(
            "/user/login",
            {"username": ["test@mail.com"], "password": ["wrongpassword"],},
        )
        assert response.status_code == 200  # Testing redirection

    def test_login_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """
        client: Client = Client()
        response: HttpResponse = client.get("/user/login")
        assert response.status_code == 200  # Testing redirection


class TestLogoutView(TestCase):
    def test_logout(self):
        User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        client: Client = Client()
        client.post(
            "/user/login",
            {"username": ["test@mail.com"], "password": ["password8chars"],},
        )
        response: HttpResponse = client.get("/user/logout",)
        assert response.status_code == 302  # Testing redirection


class TestProfileView(TestCase):
    def test_profile_get(self):
        User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        client: Client = Client()
        client.post(
            "/user/login",
            {"username": ["test@mail.com"], "password": ["password8chars"],},
        )
        response: HttpResponse = client.get("/user/profile",)
        assert response.status_code == 200  # Testing redirection
