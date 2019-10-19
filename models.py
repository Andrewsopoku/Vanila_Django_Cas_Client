from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.

class VanilaCasUser(models.Model):
    cas_user_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    group = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=255,null=True,blank=True)



class SessionTicket(models.Model):
    session_key = models.CharField(max_length=255, null=True,blank=True)
    ticket = models.CharField(max_length=255)
