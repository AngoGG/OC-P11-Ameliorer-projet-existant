from django.contrib import messages  # import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import View
from user.models import User
import purbeurre.settings as Settings


# Create your views here.


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "app/home.html")


class LegalNoticeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "app/legal_notice.html")


class PasswordResetView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        password_reset_form: PasswordResetForm = PasswordResetForm()
        return render(
            request=request,
            template_name="app/password_reset.html",
            context={"password_reset_form": password_reset_form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        password_reset_form: PasswordResetForm = PasswordResetForm(self.request.POST)
        if password_reset_form.is_valid():
            data: str = password_reset_form.cleaned_data["email"]
            associated_users: QuerySet = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject: str = "Réinitialisation du mot de passe demandée"
                    email_template_name: str = "app/password_reset_email.txt"
                    c: dict = {
                        "email": user.email,
                        "domain": request.META["HTTP_HOST"],
                        "site_name": "Pur Beurre",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email: str = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            Settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Paramètres invalides.")
                    messages.success(
                        request,
                        "Un message contenant des instructions pour réinitialiser le mot de passe a été envoyé dans votre boîte de réception.",
                    )
                    return redirect("/")
            else:
                messages.error(request, "Une adresse email non valide a été saisie.")
                return render(
                    request=request,
                    template_name="app/password_reset.html",
                    context={"password_reset_form": password_reset_form},
                )

