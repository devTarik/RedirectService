import uuid

import shortuuid
from django.contrib.auth.models import User
from django.db import models


class RedirectRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    redirect_url = models.URLField()
    is_private = models.BooleanField(default=False)
    redirect_identifier = models.CharField(unique=True, max_length=16, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.redirect_identifier:
            self.redirect_identifier = shortuuid.uuid()[:16]
        super().save(*args, **kwargs)
