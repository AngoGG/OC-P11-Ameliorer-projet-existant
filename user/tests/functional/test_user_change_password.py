from django.db.models.query import QuerySet
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from selenium import webdriver
from user.models import User

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("window-size=1920x1080")


class ChromeUserPasswordChangeFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser: webdriver = webdriver.Chrome(
            "user/tests/functional/chromedriver.exe", options=options
        )
        self.user: User = User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )
        self.client: Client = Client()
        self.user = self.client.login(email="test@mail.com", password="password8chars")
        self.cookie = self.client.cookies["sessionid"]

    def test_change_password(self):
        """Functional test for a User changing his password.
        Using Selenium, go to the change_password page,enter a new password
            then check if the correct template is used and have the success-alert div.
        Finally check new password in database.
        """

        self.browser.get(f"{self.live_server_url}/user/change_password")
        self.browser.add_cookie(
            {
                "name": "sessionid",
                "value": self.cookie.value,
                "secure": False,
                "path": "/",
            }
        )
        self.browser.get(f"{self.live_server_url}/user/change_password")
        self.assertIn("Modifier mot de passe", self.browser.title)

        self.browser.find_element_by_name("old_password").send_keys("password8chars")
        self.browser.find_element_by_name("new_password1").send_keys(
            "newpassword8chars"
        )
        self.browser.find_element_by_name("new_password2").send_keys(
            "newpassword8chars"
        )
        self.browser.find_element_by_name("change_password").click()

        self.assertEqual(
            self.browser.find_element_by_name("change_password_success").text,
            "×\nSuccès! Vous avez modifié votre compte avec succès !",
        )

        self.assertIn("Mon Compte", self.browser.title)

        user: QuerySet = User.objects.first()
        self.assertTrue(user.check_password("newpassword8chars"))
