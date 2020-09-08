
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.db.models.query import QuerySet
from django.test import Client
from selenium import webdriver
from user.models import User
import time
import re

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("window-size=1920x1080")


class ChromeUserPasswordChangeFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser: webdriver = webdriver.Chrome(
            "tests/chromedriver.exe", options=options
        )
        self.user: User = User.objects.create_user(
            email="test@mail.com",
            password="password8chars",
            first_name="firstname",
            last_name="lastname",
        )

    def test_reset_password_user_dont_exist(self):
        #Reset Password for a given email
        self.browser.get(f"{self.live_server_url}/password_reset")    
        self.browser.find_element_by_name("email").send_keys(
            "unknown-user@mail.com"
        )
        self.browser.find_element_by_name("change_password").click()

        self.assertEqual(
            self.browser.find_element_by_name("alert").text,
            "×\nUne adresse email non valide a été saisie.",
        )

    def test_reset_password(self):
        """Functional test for a User reset password.
        Using Selenium, go to the password_reset page,enter a the user email we need the password to be reset.
            then take the link in the email received and enter a new password.
        Finally check new password in database.
        """
        
        #Reset Password for a given email
        self.browser.get(f"{self.live_server_url}/password_reset")    
        self.browser.find_element_by_name("email").send_keys(
            "test@mail.com"
        )
        self.browser.find_element_by_name("change_password").click()
        
        #Check if mail is correctly sent and we are on the homepage with an alert div.
        self.assertEqual(
            self.browser.find_element_by_name("alert").text,
            "×\nUn message contenant des instructions pour réinitialiser le mot de passe a été envoyé dans votre boîte de réception.",
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, 'Réinitialisation du mot de passe demandée'
        )

        #Get the reset url link in the mail body and go to the reset page.
        urls = re.search('https?:(.+)', mail.outbox[0].body)
        self.browser.get(urls[0])

        #Enter new password, 
        #Check if we are correctly redirected on the right template 
        #Check the new password in database.
        self.assertIn("Réinitialiser mot de passe", self.browser.title)
        self.browser.find_element_by_name("new_password1").send_keys(
            "newpassword8chars"
        )
        self.browser.find_element_by_name("new_password2").send_keys(
            "newpassword8chars"
        )
        self.browser.find_element_by_name("change_password").click()

        self.assertIn("Réinitialiser mot de passe OK", self.browser.title)
        login_link = self.browser.find_element_by_name("login")
        self.assertEqual(login_link.text, "Vous connecter")

        user: QuerySet = User.objects.first()
        self.assertTrue(user.check_password("newpassword8chars"))