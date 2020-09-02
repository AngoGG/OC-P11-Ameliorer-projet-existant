from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView, View
from .forms import ConnectionForm, RegisterForm
from .models import User


class RegistrationView(FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "user/register.html", {"form": RegisterForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Manages the user registration.
        """
        email: str = request.POST.get("email")
        password: str = request.POST.get("password1")
        extra_fields: dict = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
        }
        user: User = User.objects.create_user(
            email=email, password=password, **extra_fields
        )
        login(self.request, user)
        return redirect("/")


class LoginView(FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "user/connection.html", {"form": ConnectionForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Manages the user connection.
        """
        error: bool = False

        form: ConnectionForm = ConnectionForm(request.POST)
        if form.is_valid():
            username: str = form.cleaned_data["username"]
            password: str = form.cleaned_data["password"]
            user: User = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
            else:
                error: bool = True
        return render(request, "user/connection.html", locals())


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect("/")


class UserPasswordChangeView(LoginRequiredMixin, FormView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "user/change_password.html",
            {"form": PasswordChangeForm(user=request.user)},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form: PasswordChangeForm = PasswordChangeForm(
            data=request.POST, user=request.user
        )
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, "user/profile.html", {"change": "success",})
        return render(request, "user/change_password.html", locals())


class ProfileView(View):
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return render(request, "user/profile.html", **kwargs)
