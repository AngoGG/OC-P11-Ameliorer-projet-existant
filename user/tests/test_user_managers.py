import pytest
from django.db.models.query import QuerySet
from django.test import TestCase
from user.models import User


class TestUserManager(TestCase):
    def test__create_user(self) -> None:
        """Test the correct user creation.
        """
        user: User = User.objects._create_user(
            email="mail@mail.com",
            password="password",
            first_name="firstname",
            last_name="lastname",
        )
        user_created: QuerySet = User.objects.first()  # type: ignore
        self.assertEqual(user, user_created)
        self.assertEqual("mail@mail.com", user_created.email)
        self.assertTrue(user_created.check_password("password"))
        self.assertEqual("firstname", user_created.first_name)
        self.assertEqual("lastname", user_created.last_name)

    def test_create_user(self) -> None:
        """Test the correct user creation.
        """
        user: User = User.objects.create_user(
            email="mail@mail.com",
            password="password",
            first_name="firstname",
            last_name="lastname",
        )
        user_created: QuerySet = User.objects.first()
        self.assertEqual(user, user_created)
        self.assertEqual("mail@mail.com", user_created.email)
        self.assertTrue(user_created.check_password("password"))
        self.assertEqual("firstname", user_created.first_name)
        self.assertEqual("lastname", user_created.last_name)
        self.assertFalse(user_created.is_superuser)

        with pytest.raises(ValueError) as ExceptionInfo:
            user: User = User.objects.create_user(
                email="",
                password="password",
                first_name="firstname",
                last_name="lastname",
            )
        ExceptionInfo.match(r"The given email must be set.")

    def test_create_superuser(self) -> None:
        """Test the correct user creation.
        """
        user: User = User.objects.create_superuser(
            email="mail@mail.com",
            password="password",
            first_name="firstname",
            last_name="lastname",
        )
        user_created: QuerySet = User.objects.first()
        self.assertEqual(user, user_created)
        self.assertEqual("mail@mail.com", user_created.email)
        self.assertTrue(user_created.check_password("password"))
        self.assertEqual("firstname", user_created.first_name)
        self.assertEqual("lastname", user_created.last_name)
        self.assertTrue(user_created.is_superuser)
        self.assertTrue(user_created.is_staff)

        with pytest.raises(ValueError) as ExceptionInfo:
            user: User = User.objects.create_superuser(
                email="",
                password="password",
                first_name="firstname",
                last_name="lastname",
            )
        ExceptionInfo.match(r"The given email must be set.")

        with pytest.raises(ValueError) as ExceptionInfo:
            user: User = User.objects.create_superuser(
                email="mail@mail.com",
                password="password",
                first_name="firstname",
                last_name="lastname",
                is_staff=False,
            )
        ExceptionInfo.match(r"Superuser must have is_staff=True.")

        with pytest.raises(ValueError) as ExceptionInfo:
            user: User = User.objects.create_superuser(
                email="mail@mail.com",
                password="password",
                first_name="firstname",
                last_name="lastname",
                is_superuser=False,
            )
        ExceptionInfo.match(r"Superuser must have is_superuser=True.")
