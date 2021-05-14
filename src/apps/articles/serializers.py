# -*- coding: utf-8 -*-
from rest_framework import serializers

from src.apps.articles.models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Article
        fields = ['link', 'title', 'content']
