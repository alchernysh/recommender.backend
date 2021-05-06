# -*- coding: utf-8 -*-
from rest_framework import serializers

from src.apps.settings.models import Topic


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    checked = serializers.BooleanField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'checked']
