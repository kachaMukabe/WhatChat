from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.FileField()
    conversation_id = models.CharField(max_length=255)
    job_id = models.CharField(max_length=255)
    topics = models.JSONField(null=True, blank=True)
    actions = models.JSONField(null=True, blank=True)
