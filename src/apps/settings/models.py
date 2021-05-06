from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=100)
    embedding = ArrayField(models.FloatField())
    users = models.ManyToManyField(User, related_name='users')
