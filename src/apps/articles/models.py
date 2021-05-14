from django.db import models

from django.contrib.postgres.fields import ArrayField


class Article(models.Model):
    link = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1000000)
    timestamp = models.DateTimeField()
    embedding = ArrayField(models.FloatField())
