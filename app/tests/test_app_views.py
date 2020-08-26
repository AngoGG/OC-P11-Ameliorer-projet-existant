import pytest
from django.test import Client, TestCase
from app.views import HomeView


class TestHomeView(TestCase):
    def test_home_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """

        client: Client = Client()
        response = client.get("/",)
        assert response.status_code == 200  # Testing redirection

    def test_legal_get(self) -> None:
        """Test if the url returns a correct 200 http status code.
        """

        client: Client = Client()
        response = client.get("/legal",)
        assert response.status_code == 200  # Testing redirection
