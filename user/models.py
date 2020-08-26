from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email: models.EmailField = models.EmailField(_("email address"), unique=True)
    first_name: models.EmailField = models.CharField(
        _("first name"), max_length=30, blank=True
    )
    last_name: models.EmailField = models.CharField(
        _("last name"), max_length=30, blank=True
    )
    date_joined: models.EmailField = models.DateTimeField(
        _("date joined"), auto_now_add=True
    )
    is_active: models.EmailField = models.BooleanField(_("active"), default=True)
    is_staff: models.BooleanField = models.BooleanField(_("staff"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
