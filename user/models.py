# user/models.py
import uuid as uuid_lib
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        unique=True)

    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"uuid": self.uuid})
