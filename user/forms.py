#!/usr/bin/env python3
"""
@desc    description
@author  ANGO <ango@afnor.org>
@version 0.0.1
@date    2020-06-02
@note    0.0.1 (2020-06-02) : Init file
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class ConnectionForm(forms.Form):
    """Class description.
    Description details here (if needed).
    
    Attributes:
        name (type): Description. Default to False.
    """

    username = forms.CharField(label="Adresse email", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email: forms.EmailField = forms.EmailField(
        max_length=254,
        required=True,
        help_text="Obligatoire. Renseignez une addresse mail valide.",
    )
    first_name: forms.CharField = forms.CharField(
        label="Prénom", max_length=30, required=False, help_text="Optionnel."
    )
    last_name: forms.CharField = forms.CharField(
        label="Nom", max_length=30, required=False, help_text="Optionnel."
    )

    class Meta:
        model = User
        fields: tuple = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

